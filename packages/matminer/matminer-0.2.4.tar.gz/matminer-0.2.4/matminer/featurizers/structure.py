from __future__ import division, unicode_literals, print_function

import itertools
from math import pi, fabs
from operator import itemgetter
import warnings

import numpy as np
import pandas as pd
import scipy.constants as const

from pymatgen import Structure
from pymatgen.analysis.defects.point_defects import \
    ValenceIonicRadiusEvaluator
from pymatgen.analysis.ewald import EwaldSummation
from pymatgen.core.periodic_table import Specie, Element
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
import pymatgen.analysis.local_env as pmg_le
from matminer.featurizers.base import BaseFeaturizer
from matminer.featurizers.site import OPSiteFingerprint, CrystalSiteFingerprint, \
    CoordinationNumber
from matminer.featurizers.stats import PropertyStats

__authors__ = 'Anubhav Jain <ajain@lbl.gov>, Saurabh Bajaj <sbajaj@lbl.gov>, ' \
              'Nils E.R. Zimmerman <nils.e.r.zimmermann@gmail.com>'
# ("@article{label, title={}, volume={}, DOI={}, number={}, pages={}, journal={}, author={}, year={}}")

ANG_TO_BOHR = const.value('Angstrom star') / const.value('Bohr radius')


# To do:
# - Use local_env-based neighbor finding
#   once this is part of the stable Pymatgen version.
# - Use more than 1 method for MinimumRelativeDistance

class DensityFeatures(BaseFeaturizer):

    def __init__(self, desired_features=None):
        self.features = ["density", "vpa", "packing fraction"] if not \
            desired_features else desired_features

    def featurize(self, s):
        output = []

        if "density" in self.features:
            output.append(s.density)

        if "vpa" in self.features:
            if not s.is_ordered:
                raise ValueError("Disordered structure support not built yet.")
            output.append(s.volume / len(s))

        if "packing fraction" in self.features:
            if not s.is_ordered:
                raise ValueError("Disordered structure support not built yet.")
            total_rad = 0
            for site in s:
                total_rad += site.specie.atomic_radius ** 3
            output.append(4 * pi * total_rad / (3 * s.volume))

        return output

    def feature_labels(self):
        all_features = ["density", "vpa", "packing fraction"]  # enforce order
        return [x for x in all_features if x in self.features]

    def citations(self):
        return []

    def implementors(self):
        return ["Saurabh Bajaj", "Anubhav Jain"]


class GlobalSymmetryFeatures(BaseFeaturizer):
    crystal_idx = {"triclinic": 7,
                   "monoclinic": 6,
                   "orthorhombic": 5,
                   "tetragonal": 4,
                   "trigonal": 3,
                   "hexagonal": 2,
                   "cubic": 1
                   }

    def __init__(self, desired_features=None):
        self.features = ["spacegroup_num", "crystal_system",
                         "crystal_system_int", "is_centrosymmetric"] if not \
            desired_features else desired_features

    def featurize(self, s):
        sga = SpacegroupAnalyzer(s)
        output = []

        if "spacegroup_num" in self.features:
            output.append(sga.get_space_group_number())

        if "crystal_system" in self.features:
            output.append(sga.get_crystal_system())

        if "crystal_system_int" in self.features:
            output.append(GlobalSymmetryFeatures.crystal_idx[
                              sga.get_crystal_system()])

        if "is_centrosymmetric" in self.features:
            output.append(sga.is_laue())

        return output

    def feature_labels(self):
        all_features = ["spacegroup_num", "crystal_system",
                        "crystal_system_int",
                        "is_centrosymmetric"]  # enforce order
        return [x for x in all_features if x in self.features]

    def citations(self):
        return []

    def implementors(self):
        return ["Anubhav Jain"]


class RadialDistributionFunction(BaseFeaturizer):
    """
    Calculate the radial distribution function (RDF) of a crystal
    structure.
    Args:
        cutoff: (float) distance up to which to calculate the RDF.
        bin_size: (float) size of each bin of the (discrete) RDF.
    """

    def __init__(self, cutoff=20.0, bin_size=0.1):
        self.cutoff = cutoff
        self.bin_size = bin_size

    def featurize(self, s):
        """
        Get RDF of the input structure.
        Args:
            s: Pymatgen Structure object.

        Returns:
            rdf, dist: (tuple of arrays) the first element is the
                    normalized RDF, whereas the second element is
                    the inner radius of the RDF bin.
        """
        if not s.is_ordered:
            raise ValueError("Disordered structure support not built yet")

        # Get the distances between all atoms
        neighbors_lst = s.get_all_neighbors(self.cutoff)
        all_distances = np.concatenate(
            tuple(map(lambda x: [itemgetter(1)(e) for e in x], neighbors_lst)))

        # Compute a histogram
        rdf_dict = {}
        dist_hist, dist_bins = np.histogram(
            all_distances, bins=np.arange(
                0, self.cutoff + self.bin_size, self.bin_size), density=False)

        # Normalize counts
        shell_vol = 4.0 / 3.0 * pi * (np.power(
            dist_bins[1:], 3) - np.power(dist_bins[:-1], 3))
        number_density = s.num_sites / s.volume
        rdf = dist_hist / shell_vol / number_density
        return [{'distances': dist_bins[:-1], 'distribution': rdf}]

    def feature_labels(self):
        return ["radial distribution function"]

    def citations(self):
        return []

    def implementors(self):
        return ["Saurabh Bajaj"]


class PartialRadialDistributionFunction(BaseFeaturizer):
    """
    Compute the partial radial distribution function (PRDF) of a crystal
    structure, which is the radial distibution function
    broken down for each pair of atom types.  The PRDF was proposed as a
    structural descriptor by [Schutt *et al.*]
    (https://journals.aps.org/prb/abstract/10.1103/PhysRevB.89.205118)
    Args:
        cutoff: (float) distance up to which to calculate the RDF.
        bin_size: (float) size of each bin of the (discrete) RDF.
    """

    def __init__(self, cutoff=20.0, bin_size=0.1):
        self.cutoff = cutoff
        self.bin_size = bin_size

    def featurize(self, s):
        """
        Get PRDF of the input structure.
        Args:
            s: Pymatgen Structure object.

        Returns:
            prdf, dist: (tuple of arrays) the first element is a
                    dictionary where keys are tuples of element
                    names and values are PRDFs.
        """

        if not s.is_ordered:
            raise ValueError("Disordered structure support not built yet")

        # Get the composition of the array
        composition = s.composition.fractional_composition.to_reduced_dict

        # Get the distances between all atoms
        neighbors_lst = s.get_all_neighbors(self.cutoff)

        # Sort neighbors by type
        distances_by_type = {}
        for p in itertools.product(composition.keys(), composition.keys()):
            distances_by_type[p] = []

        def get_symbol(site):
            return site.specie.symbol if isinstance(site.specie,
                                                    Element) else site.specie.element.symbol

        for site, nlst in zip(s.sites,
                              neighbors_lst):  # Each list is a list for each site
            my_elem = get_symbol(site)

            for neighbor in nlst:
                rij = neighbor[1]
                n_elem = get_symbol(neighbor[0])
                # LW 3May17: Any better ideas than appending each element at a time?
                distances_by_type[(my_elem, n_elem)].append(rij)

        # Compute and normalize the prdfs
        prdf = {}
        dist_bins = np.arange(0, self.cutoff + self.bin_size, self.bin_size)
        shell_volume = 4.0 / 3.0 * pi * (
                np.power(dist_bins[1:], 3) - np.power(dist_bins[:-1], 3))
        for key, distances in distances_by_type.items():
            # Compute histogram of distances
            dist_hist, dist_bins = np.histogram(distances,
                                                bins=dist_bins, density=False)
            # Normalize
            n_alpha = composition[key[0]] * s.num_sites
            rdf = dist_hist / shell_volume / n_alpha

            prdf[key] = {'distances': dist_bins, 'distribution': rdf}

        return [prdf]

    def feature_labels(self):
        return ["partial radial distribution functions"]

    def citations(self):
        return []

    def implementors(self):
        return ["Saurabh Bajaj"]


class RadialDistributionFunctionPeaks(BaseFeaturizer):
    """
    Determine the location of the highest peaks in the radial distribution
    function (RDF) of a structure.
    Args:
        n_peaks: (int) number of the top peaks to return .
    """

    def __init__(self, n_peaks=2):
        self.n_peaks = n_peaks

    def featurize(self, rdf):
        """
        Get location of highest peaks in RDF.

        Args:
            rdf: (ndarray) RDF as obtained from the
                    RadialDistributionFunction class.

        Returns: (ndarray) distances of highest peaks in descending order
                of the peak height
        """

        return [[rdf[0]['distances'][i] for i in np.argsort(
            rdf[0]['distribution'])[-self.n_peaks:]][::-1]]

    def feature_labels(self):
        return ["radial distribution function peaks"]

    def citations(self):
        return []

    def implementors(self):
        return ["Saurabh Bajaj"]


class ElectronicRadialDistributionFunction(BaseFeaturizer):
    """
    Calculate the crystal structure-inherent
    electronic radial distribution function (ReDF) according to
    Willighagen et al., Acta Cryst., 2005, B61, 29-36.
    The ReDF is a structure-integral RDF (i.e., summed over
    all sites) in which the positions of neighboring sites
    are weighted by electrostatic interactions inferred
    from atomic partial charges. Atomic charges are obtained
    from the ValenceIonicRadiusEvaluator class.
    Args:
        cutoff: (float) distance up to which the ReDF is to be
                calculated (default: longest diagaonal in
                primitive cell).
        dr: (float) width of bins ("x"-axis) of ReDF (default: 0.05 A).
    """

    def __init__(self, cutoff=None, dr=0.05):
        self.cutoff = cutoff
        self.dr = dr

    def featurize(self, s):
        """
        Get ReDF of input structure.

        Args:
            s: input Structure object.

        Returns: (dict) a copy of the electronic radial distribution
                functions (ReDF) as a dictionary. The distance list
                ("x"-axis values of ReDF) can be accessed via key
                'distances'; the ReDF itself is accessible via key
                'redf'.
        """
        if self.dr <= 0:
            raise ValueError("width of bins for ReDF must be >0")

        # Make structure primitive.
        struct = SpacegroupAnalyzer(s).find_primitive() or s

        # Add oxidation states.
        struct = ValenceIonicRadiusEvaluator(struct).structure

        if self.cutoff is None:
            # Set cutoff to longest diagonal.
            a = struct.lattice.matrix[0]
            b = struct.lattice.matrix[1]
            c = struct.lattice.matrix[2]
            self.cutoff = max(
                [np.linalg.norm(a + b + c), np.linalg.norm(-a + b + c),
                 np.linalg.norm(a - b + c), np.linalg.norm(a + b - c)])

        nbins = int(self.cutoff / self.dr) + 1
        redf_dict = {"distances": np.array(
            [(i + 0.5) * self.dr for i in range(nbins)]),
            "distribution": np.zeros(nbins, dtype=np.float)}

        for site in struct.sites:
            this_charge = float(site.specie.oxi_state)
            neighs_dists = struct.get_neighbors(site, self.cutoff)
            for neigh, dist in neighs_dists:
                neigh_charge = float(neigh.specie.oxi_state)
                bin_index = int(dist / self.dr)
                redf_dict["distribution"][bin_index] += (
                                                                this_charge * neigh_charge) / (
                                                                struct.num_sites * dist)

        return [redf_dict]

    def feature_labels(self):
        return ["electronic radial distribution function"]

    def citations(self):
        return ["@article{title={Method for the computational comparison"
                " of crystal structures}, volume={B61}, pages={29-36},"
                " DOI={10.1107/S0108768104028344},"
                " journal={Acta Crystallographica Section B},"
                " author={Willighagen, E. L. and Wehrens, R. and Verwer,"
                " P. and de Gelder R. and Buydens, L. M. C.}, year={2005}}"]

    def implementors(self):
        return ["Nils E. R. Zimmermann"]


class CoulombMatrix(BaseFeaturizer):
    """
    Generate the Coulomb matrix, M, of the input
    structure (or molecule).  The Coulomb matrix was put forward by
    Rupp et al. (Phys. Rev. Lett. 108, 058301, 2012) and is defined by
    off-diagonal elements M_ij = Z_i*Z_j/|R_i-R_j|
    and diagonal elements 0.5*Z_i^2.4, where Z_i and R_i denote
    the nuclear charge and the position of atom i, respectively.

    Args:
        diag_elems: (bool) flag indicating whether (True, default) to use
                    the original definition of the diagonal elements;
                    if set to False, the diagonal elements are set to zero.
    """

    def __init__(self, diag_elems=True):
        self.diag_elems = diag_elems

    def featurize(self, s):
        """
        Get Coulomb matrix of input structure.

        Args:
            s: input Structure (or Molecule) object.

        Returns:
            m: (Nsites x Nsites matrix) Coulomb matrix.
        """
        m = [[] for site in s.sites]
        z = []
        for site in s.sites:
            if isinstance(site, Specie):
                z.append(Element(site.element.symbol).Z)
            else:
                z.append(Element(site.species_string).Z)
        for i in range(s.num_sites):
            for j in range(s.num_sites):
                if i == j:
                    if self.diag_elems:
                        m[i].append(0.5 * z[i] ** 2.4)
                    else:
                        m[i].append(0)
                else:
                    d = s.get_distance(i, j) * ANG_TO_BOHR
                    m[i].append(z[i] * z[j] / d)
        return [np.array(m)]

    def feature_labels(self):
        return ["coulomb matrix"]

    def citations(self):
        return ["@article{rupp_tkatchenko_muller_vonlilienfeld_2012, title={"
                "Fast and accurate modeling of molecular atomization energies"
                " with machine learning}, volume={108},"
                " DOI={10.1103/PhysRevLett.108.058301}, number={5},"
                " pages={058301}, journal={Physical Review Letters}, author={"
                "Rupp, Matthias and Tkatchenko, Alexandre and M\"uller,"
                " Klaus-Robert and von Lilienfeld, O. Anatole}, year={2012}}"]

    def implementors(self):
        return ["Nils E. R. Zimmermann"]


class SineCoulombMatrix(BaseFeaturizer):
    """
    This function generates a variant of the Coulomb matrix developed
    for periodic crystals by Faber et al. (Inter. J. Quantum Chem.
    115, 16, 2015). It is identical to the Coulomb matrix, except
    that the inverse distance function is replaced by the inverse of a
    sin**2 function of the vector between the sites which is periodic
    in the dimensions of the structure lattice. See paper for details.

    Args:
        diag_elems (bool): flag indication whether (True, default) to use
                the original definition of the diagonal elements;
                if set to False, the diagonal elements are set to 0
    """

    def __init__(self, diag_elems=True):
        self.diag_elems = diag_elems

    def featurize(self, s):
        """
        Args:
            s (Structure or Molecule): input structure (or molecule)

        Returns:
            (Nsites x Nsites matrix) Sine matrix.
        """
        sites = s.sites
        Zs = np.array([site.specie.Z for site in sites])
        sin_mat = np.zeros((len(sites), len(sites)))
        coords = np.array([site.frac_coords for site in sites])
        lattice = s.lattice.matrix
        pi = np.pi

        for i in range(len(sin_mat)):
            for j in range(len(sin_mat)):
                if i == j:
                    if self.diag_elems:
                        sin_mat[i][i] = 0.5 * Zs[i] ** 2.4
                elif i < j:
                    vec = coords[i] - coords[j]
                    coord_vec = np.sin(pi * vec) ** 2
                    trig_dist = np.linalg.norm(
                        (np.matrix(coord_vec) * lattice).A1) * ANG_TO_BOHR
                    sin_mat[i][j] = Zs[i] * Zs[j] / trig_dist
                else:
                    sin_mat[i][j] = sin_mat[j][i]
        return [sin_mat]

    def feature_labels(self):
        return ["sine coulomb matrix"]

    def citations(self):
        return ["@article {QUA:QUA24917,"
                "author = {Faber, Felix and Lindmaa, Alexander and von Lilienfeld, O. Anatole and Armiento, Rickard},"
                "title = {Crystal structure representations for machine learning models of formation energies},"
                "journal = {International Journal of Quantum Chemistry},"
                "volume = {115},"
                "number = {16},"
                "issn = {1097-461X},"
                "url = {http://dx.doi.org/10.1002/qua.24917},"
                "doi = {10.1002/qua.24917},"
                "pages = {1094--1101},"
                "keywords = {machine learning, formation energies, representations, crystal structure, periodic systems},"
                "year = {2015},"
                "}"]

    def implementors(self):
        return ["Kyle Bystrom"]


class OrbitalFieldMatrix(BaseFeaturizer):
    """
    This function generates an orbital field matrix (OFM) as developed
    by Pham et al (arXiv, May 2017). Each atom is described by a 32-element
    vector (or 39-element vector, see period tag for details) uniquely
    representing the valence subshell. A 32x32 (39x39) matrix is formed
    by multiplying two atomic vectors. An OFM for an atomic environment is the
    sum of these matrices for each atom the center atom coordinates with
    multiplied by a distance function (In this case, 1/r times the weight of
    the coordinating atom in the Voronoi Polyhedra method). The OFM of a structure
    or molecule is the average of the OFMs for all the sites in the structure.

    Args:
        period_tag (bool): In the original OFM, an element is represented
                by a vector of length 32, where each element is 1 or 0,
                which represents the valence subshell of the element.
                With period_tag=True, the vector size is increased
                to 39, where the 7 extra elements represent the period
                of the element. Note lanthanides are treated as period 6,
                actinides as period 7. Default False as in the original paper.

    ...attribute:: size
        Either 32 or 39, the size of the vectors used to describe elements.
    """

    def __init__(self, period_tag=False):
        my_ohvs = {}
        if period_tag:
            self.size = 39
        else:
            self.size = 32
        for Z in range(1, 95):
            el = Element.from_Z(Z)
            my_ohvs[Z] = self.get_ohv(el, period_tag)
            my_ohvs[Z] = np.matrix(my_ohvs[Z])
        self.ohvs = my_ohvs

    def get_ohv(self, sp, period_tag):
        """
        Get the "one-hot-vector" for pymatgen Element sp. This 32 or 39-length
        vector represents the valence shell of the given element.
        Args:
            sp (Element): element whose ohv should be returned
            period_tag (bool): If true, the vector contains items
                    corresponding to the period of the element

        Returns:
            my_ohv (numpy array length 39 if period_tag, else 32): ohv for sp
        """
        el_struct = sp.full_electronic_structure
        ohd = {j: {i + 1: 0 for i in range(2 * (2 * j + 1))} for j in range(4)}
        nume = 0
        shell_num = 0
        max_n = el_struct[-1][0]
        while shell_num < len(el_struct):
            if el_struct[-1 - shell_num][0] < max_n - 2:
                shell_num += 1
                continue
            elif el_struct[-1 - shell_num][0] < max_n - 1 and \
                    el_struct[-1 - shell_num][1] != u'f':
                shell_num += 1
                continue
            elif el_struct[-1 - shell_num][0] < max_n and (
                    el_struct[-1 - shell_num][1] != u'd' and
                    el_struct[-1 - shell_num][1] != u'f'):
                shell_num += 1
                continue
            curr_shell = el_struct[-1 - shell_num]
            if curr_shell[1] == u's':
                l = 0
            elif curr_shell[1] == u'p':
                l = 1
            elif curr_shell[1] == u'd':
                l = 2
            elif curr_shell[1] == u'f':
                l = 3
            ohd[l][curr_shell[2]] = 1
            nume += curr_shell[2]
            shell_num += 1
        my_ohv = np.zeros(self.size, np.int)
        k = 0
        for j in range(4):
            for i in range(2 * (2 * j + 1)):
                my_ohv[k] = ohd[j][i + 1]
                k += 1
        if period_tag:
            row = sp.row
            if row > 7:
                row -= 2
            my_ohv[row + 31] = 1
        return my_ohv

    def get_single_ofm(self, site, site_dict):
        """
        Gets the orbital field matrix for a single chemical environment,
        where site is the center atom whose environment is characterized and
        site_dict is a dictionary of site : weight, where the weights are the
        Voronoi Polyhedra weights of the corresponding coordinating sites.

        Args:
            site (Site): center atom
            site_dict (dict of Site:float): chemical environment

        Returns:
            atom_ofm (size X size numpy matrix): ofm for site
        """
        ohvs = self.ohvs
        atom_ofm = np.matrix(np.zeros((self.size, self.size)))
        ref_atom = ohvs[site.specie.Z]
        for other_site in site_dict:
            scale = site_dict[other_site]
            other_atom = ohvs[other_site.specie.Z]
            atom_ofm += other_atom.T * ref_atom * scale / site.distance(
                other_site) / ANG_TO_BOHR
        return atom_ofm

    def get_atom_ofms(self, struct, symm=False):
        """
        Calls get_single_ofm for every site in struct. If symm=True,
        get_single_ofm is called for symmetrically distinct sites, and
        counts is constructed such that ofms[i] occurs counts[i] times
        in the structure

        Args:
            struct (Structure): structure for find ofms for
            symm (bool): whether to calculate ofm for only symmetrically
                    distinct sites

        Returns:
            ofms ([size X size matrix] X len(struct)): ofms for struct
            if symm:
                ofms ([size X size matrix] X number of symmetrically distinct sites):
                    ofms for struct
                counts: number of identical sites for each ofm
        """
        ofms = []
        vnn = pmg_le.VoronoiNN(allow_pathological=True)
        if symm:
            symm_struct = SpacegroupAnalyzer(struct).get_symmetrized_structure()
            indices = [lst[0] for lst in symm_struct.equivalent_indices]
            counts = [len(lst) for lst in symm_struct.equivalent_indices]
        else:
            indices = [i for i in range(len(struct.sites))]
        for index in indices:
            ofms.append(self.get_single_ofm(struct.sites[index], \
                                            vnn.get_voronoi_polyhedra(struct, index)))
        if symm:
            return ofms, counts
        return ofms

    def get_mean_ofm(self, ofms, counts):
        """
        Averages a list of ofms, weights by counts
        """
        ofms = [ofm * c for ofm, c in zip(ofms, counts)]
        return sum(ofms) / sum(counts)

    def get_structure_ofm(self, struct):
        """
        Calls get_mean_ofm on the results of get_atom_ofms
        to give a size X size matrix characterizing a structure
        """
        ofms, counts = self.get_atom_ofms(struct, True)
        return self.get_mean_ofm(ofms, counts)

    def featurize(self, s):
        """
        Makes a supercell for structure s (to protect sites
        from coordinating with themselves), and then finds the mean
        of the orbital field matrices of each site to characterize
        a structure

        Args:
            s (Structure): structure to characterize

        Returns:
            mean_ofm (size X size matrix): orbital field matrix
                    characterizing s
        """
        s *= [3, 3, 3]
        ofms, counts = self.get_atom_ofms(s, True)
        mean_ofm = self.get_mean_ofm(ofms, counts)
        return [mean_ofm.A]

    def feature_labels(self):
        return ["orbital field matrix"]

    def citations(self):
        return ["@article{LamPham2017,"
                "author = {{Lam Pham}, Tien and Kino, Hiori and Terakura, Kiyoyuki and "
                "Miyake, Takashi and Tsuda, Koji and Takigawa, Ichigaku and {Chi Dam}, Hieu},"
                "doi = {10.1080/14686996.2017.1378060},"
                "journal = {Science and Technology of Advanced Materials},"
                "month = {dec},"
                "number = {1},"
                "pages = {756--765},"
                "publisher = {Taylor {\&} Francis},"
                "title = {{Machine learning reveals orbital interaction in materials}},"
                "url = {https://www.tandfonline.com/doi/full/10.1080/14686996.2017.1378060},"
                "volume = {18},"
                "year = {2017}"
                "}"]

    def implementors(self):
        return ["Kyle Bystrom"]


class MinimumRelativeDistances(BaseFeaturizer):
    """
    Determines the relative distance of each site to its closest
    neighbor. We use the relative distance,
    f_ij = r_ij / (r^atom_i + r^atom_j), as a measure rather than the
    absolute distances, r_ij, to account for the fact that different
    atoms/species have different sizes.  The function uses the
    valence-ionic radius estimator implemented in Pymatgen.
    Args:
        cutoff: (float) (absolute) distance up to which tentative
                closest neighbors (on the basis of relative distances)
                are to be determined.
    """

    def __init__(self, cutoff=10.0):
        self.cutoff = cutoff

    def featurize(self, s, cutoff=10.0):
        """
        Get minimum relative distances of all sites of the input structure.

        Args:
            s: Pymatgen Structure object.

        Returns:
            min_rel_dists: (list of floats) list of all minimum relative
                    distances (i.e., for all sites).
        """
        vire = ValenceIonicRadiusEvaluator(s)
        min_rel_dists = []
        for site in vire.structure:
            min_rel_dists.append(min([dist / (
                    vire.radii[site.species_string] +
                    vire.radii[neigh.species_string]) for neigh, dist in \
                                      vire.structure.get_neighbors(site,
                                                                   self.cutoff)]))
        return [min_rel_dists[:]]

    def feature_labels(self):
        return ["minimum relative distance of each site"]

    def citations(self):
        return ["@article{Zimmermann2017,"
                "author = {Zimmermann, Nils E. R. and Horton, Matthew K."
                " and Jain, Anubhav and Haranczyk, Maciej},"
                "doi = {10.3389/fmats.2017.00034},"
                "journal = {Frontiers in Materials},"
                "pages = {34},"
                "title = {{Assessing Local Structure Motifs Using Order"
                " Parameters for Motif Recognition, Interstitial"
                " Identification, and Diffusion Path Characterization}},"
                "url = {https://www.frontiersin.org/articles/10.3389/fmats.2017.00034},"
                "volume = {4},"
                "year = {2017}"
                "}"]

    def implementors(self):
        return ["Nils E. R. Zimmermann"]


class SiteStatsFingerprint(BaseFeaturizer):
    """
    Calculates all order parameters (OPs) for all sites in a crystal
    structure.
    Args:
        site_featurizer (BaseFeaturizer): a site-based featurizer
        stats ([str]): list of weighted statistics to compute for each feature.
            If stats is None, for each order parameter, a list is returned that
            contains the calculated parameter for each site in the structure.
            *Note for nth mode, stat must be 'n*_mode'; e.g. stat='2nd_mode'
        min_oxi (int): minimum site oxidation state for inclusion (e.g.,
            zero means metals/cations only)
        max_oxi (int): maximum site oxidation state for inclusion
    """

    def __init__(self, site_featurizer, stats=('mean', 'std_dev', 'minimum',
                                               'maximum'), min_oxi=None,
                 max_oxi=None):

        self.site_featurizer = site_featurizer
        self._labels = self.site_featurizer.feature_labels()
        self.stats = tuple([stats]) if type(stats) == str else stats
        if self.stats and '_mode' in ''.join(self.stats):
            nmodes = 0
            for stat in self.stats:
                if '_mode' in stat and int(stat[0]) > nmodes:
                    nmodes = int(stat[0])
            self.nmodes = nmodes

        self.min_oxi = min_oxi
        self.max_oxi = max_oxi

    def featurize(self, s):
        """
        Calculate all sites' local structure order parameters (LSOPs).

        Args:
            s: Pymatgen Structure object.

            Returns:
                vals: (2D array of floats) LSOP values of all sites'
                (1st dimension) order parameters (2nd dimension). 46 order
                parameters are computed per site: q_cn (coordination
                number), q_lin, 35 x q_bent (starting with a target angle
                of 5 degrees and, increasing by 5 degrees, until 175 degrees),
                q_tet, q_oct, q_bcc, q_2, q_4, q_6, q_reg_tri, q_sq, q_sq_pyr.
        """
        vals = [[] for t in self._labels]
        for i, site in enumerate(s.sites):
            if (self.min_oxi is None or site.specie.oxi_state >= self.min_oxi) \
                    and (
                    self.max_oxi is None or site.specie.oxi_state >= self.max_oxi):
                opvalstmp = self.site_featurizer.featurize(s, i)
                for j, opval in enumerate(opvalstmp):
                    if opval is None:
                        vals[j].append(0.0)
                    else:
                        vals[j].append(opval)

        if self.stats:
            stats = []
            for op in vals:
                if '_mode' in ''.join(self.stats):
                    modes = self.n_numerical_modes(op, self.nmodes, 0.01)
                for stat in self.stats:
                    if '_mode' in stat:
                        stats.append(modes[int(stat[0]) - 1])
                    else:
                        stats.append(PropertyStats().calc_stat(op, stat))

            return stats
        else:
            return vals

    def feature_labels(self):
        if self.stats:
            labels = []
            for attr in self._labels:

                for stat in self.stats:
                    labels.append('%s %s' % (stat, attr))
            return labels
        else:
            return self._labels

    def citations(self):
        return ['@article{zimmermann_jain_2017, title={Applications of order'
                ' parameter feature vectors}, journal={in progress}, author={'
                'Zimmermann, N. E. R. and Jain, A.}, year={2017}}']

    def implementors(self):
        return ['Nils E. R. Zimmermann', 'Alireza Faghaninia', 'Anubhav Jain']

    @staticmethod
    def from_preset(preset, **kwargs):

        if preset == "OPSiteFingerprint":
            return SiteStatsFingerprint(OPSiteFingerprint(), **kwargs)

        elif preset == "CrystalSiteFingerprint_cn":
            return SiteStatsFingerprint(
                CrystalSiteFingerprint.from_preset("cn", cation_anion=False),
                **kwargs)

        elif preset == "CrystalSiteFingerprint_cn_cation_anion":
            return SiteStatsFingerprint(
                CrystalSiteFingerprint.from_preset("cn", cation_anion=True),
                **kwargs)

        elif preset == "CrystalSiteFingerprint_ops":
            return SiteStatsFingerprint(
                CrystalSiteFingerprint.from_preset("ops", cation_anion=False),
                **kwargs)

        elif preset == "CrystalSiteFingerprint_ops_cation_anion":
            return SiteStatsFingerprint(
                CrystalSiteFingerprint.from_preset("ops", cation_anion=True),
                **kwargs)

        else:
            # One of the various Coordination Number presets:
            # MinimumVIRENN, MinimumDistanceNN, JMolNN, VoronoiNN, etc.
            try:
                return SiteStatsFingerprint(
                    CoordinationNumber.from_preset(preset), **kwargs)
            except:
                pass

        raise ValueError("Unrecognized preset!")

    # TODO: @nisse3000, move this function elsewhere. Probably the PropertyStats
    # packages which is responsible for turning higher-dimensional data into
    # lower dimensional data
    @staticmethod
    def n_numerical_modes(data_lst, n=2, dl=0.1):
        """
        Returns the n first modes of a data set that are obtained with
            a finite bin size for the underlying frequency distribution.
        Args:
            data_lst ([float]): data values.
            n (integer): number of most frequent elements to be determined.
            dl (float): bin size of underlying (coarsened) distribution.
        Returns:
            ([float]): first n most frequent entries (or nan if not found).
        """
        if len(set(data_lst)) == 1:
            return [data_lst[0]] + [float('NaN') for _ in range(n - 1)]
        hist, bins = np.histogram(data_lst, bins=np.arange(
            min(data_lst), max(data_lst), dl), density=False)
        modes = list(bins[np.argsort(hist)[-n:]][::-1])
        return modes + [float('NaN') for _ in range(n - len(modes))]


# TODO: @nisse3000, move this function elsewhere
def get_op_stats_vector_diff(s1, s2, max_dr=0.2, ddr=0.01, ddist=0.01):
    """
    Determine the difference vector between two order parameter-statistics
    feature vector resulting from two input structures.

    Args:
        s1 (Structure): first input structure.
        s2 (Structure): second input structure.
        max_dr (float): maximum neighbor-finding parameter to be tested.
        ddr (float): step size for increasing neighbor-finding parameter.
        ddist (float): bin size for histogramming distances of varying dr.

    Returns: (float, [float]) optimal neighbor-finding parameter
        and difference vector between order
        parameter-statistics feature vectors obtained from the
        two input structures (s1 - s2).
    """
    # Compute OP stats vector distances for varying neigh-find paras.
    dr = []
    dist = []
    delta = []
    nbins = int(max_dr / ddr) + 1
    for i in range(nbins):
        dr.append(float(i + 1) * ddr)
        opsf = SiteStatsFingerprint(site_featurizer=OPSiteFingerprint(dr=dr[i]))
        delta.append(np.array(
            opsf.featurize(s1)) - np.array(opsf.featurize(s2)))
        dist.append(np.linalg.norm(delta[i]))

    # Compute distance histogram, determine peak, and location
    # of smallest dr with peak value.
    nbins = int(max(dist) / ddist) + 1
    hist, bin_edges = np.histogram(
        dist, bins=[float(i) * ddist for i in range(nbins)],
        normed=False, weights=None, density=False)
    idx = list(hist).index(max(hist))
    dist_peak = 0.5 * (bin_edges[idx] + bin_edges[idx + 1])
    idx = -1
    for i, d in enumerate(dist):
        if fabs(d - dist_peak) <= ddist:
            idx = i
            break

    return dr[idx], delta[idx]


class EwaldEnergy(BaseFeaturizer):
    """Compute the energy from Coulombic interactions

    Note: The energy is computed using _charges already defined for the structure_.

    Features:
        ewald_energy - Coulomb interaction energy of the structure"""

    def __init__(self, accuracy=None):
        """
        Args:
            accuracy (int): Accuracy of Ewald summation, number of decimal places
        """
        self.accuracy = accuracy

    def featurize(self, strc):
        """

        Args:
             (Structure) - Structure being analyzed
        Returns:
            ([float]) - Electrostatic energy of the structure
        """
        # Compute the total energy
        ewald = EwaldSummation(strc, acc_factor=self.accuracy)
        return [ewald.total_energy]

    def feature_labels(self):
        return ["ewald_energy"]

    def implementors(self):
        return ["Logan Ward"]

    def citations(self):
        return ["@Article{Ewald1921,"
                "author = {Ewald, P. P.},"
                "doi = {10.1002/andp.19213690304},"
                "issn = {00033804},"
                "journal = {Annalen der Physik},"
                "number = {3},"
                "pages = {253--287},"
                "title = {{Die Berechnung optischer und elektrostatischer Gitterpotentiale}},"
                "url = {http://doi.wiley.com/10.1002/andp.19213690304},"
                "volume = {369},"
                "year = {1921}"
                "}"]


class BagofBonds(BaseFeaturizer):
    """
    Compute the number of each kind of bond in a structure, as a fraction of
    the total number of bonds, based on NearestNeighbors.

    For example, in a structure with 2 Li-O bonds and 3 Li-P bonds:

    Li-0: 0.4
    Li-P: 0.6

    For dataframes containing structures with various compositions, a unified
    dataframe is returned which has the collection of bond types gathered
    from all structures as columns. Use allowed_bonds and approx_bonds to
    intelligently limit the possible bonds in the dataframe.

    Args:
        nn (NearestNeighbors): A Pymatgen nearest neighbors derived object. For
            example, pymatgen.analysis.local_env.VoronoiNN().
        bbv (float): The 'bad bond values', values substituted for
            structure-bond combinations which can not physically exist, but
            exist in the unified dataframe. For example, if a dataframe contains
            structures of BaLiP and BaTiO3, determines the value to place in
            the Li-P column for the BaTiO3 row; by default, is 0.
        allowed_bonds ([str]): A list of allowed bond types; limits the possible
            columns in the output dataframe. If a structure has a bond type not
            in allowed_bonds, the bond is skipped and all allowed bonds are
            returned as normal (including bad bond values). Behavior can be
            changed with approx_bonds. The output of .feature_labels() will
            return a list of allowed_bonds for that BagofBonds object.
        approx_bonds (bool): If True, approximates the fractions of bonds not
            in allowed_bonds (forbidden bonds) with similar allowed bonds.
            Chemical rules are used to determine which bonds are most 'similar';
            particularly, the Euclidean distance between the 2-tuples of the
            bonds in Mendeleev no. space is minimized for the approximate
            bond chosen.
    """

    def __init__(self, nn, bbv=0.0, allowed_bonds=None, approx_bonds=False):
        self.nn = nn
        self.bbv = bbv
        self.allowed_bonds = allowed_bonds
        self.approx_bonds = approx_bonds
        if self.approx_bonds and self.allowed_bonds is None:
            raise ValueError("allowed_bonds was not defined but approx_bonds "
                             "are enabled. Define a list of allowed bonds or "
                             "set approx_bonds=False.")

        self._token = ' - '
        self._dataframe_featurizing = False

    @staticmethod
    def from_preset(preset):
        """
        Use one of the standard instances of a given NearNeighbor class.

        Args:
            preset (str): preset type ("VoronoiNN", "JMolNN",
            "MiniumDistanceNN", "MinimumOKeeffeNN", or "MinimumVIRENN").

        Returns:
            CoordinationNumber from a preset.
        """
        nn = getattr(pmg_le, preset)
        return BagofBonds(nn())

    def featurize_dataframe(self, df, col_id, *args, **kwargs):
        """
        Compute features for all entries contained in input dataframe.
        Necessary for returning the correct unified dataframe.

        Args:
            df (Pandas dataframe): Dataframe containing input data
            col_id (str or [str]): The dataframe key corresponding to structures

        Returns:
            (DataFrame) BagofBonds-featurized dataframe
        """

        self._dataframe_featurizing = True
        if self.allowed_bonds is None:
            self.unified_bonds = self.enumerate_all_bonds(df[col_id])
        else:
            listlike = (tuple, list, np.ndarray, pd.Series)
            if not isinstance(self.allowed_bonds, listlike):
                raise TypeError("allowed_bonds must be a list of strings.")
            self.unified_bonds = self._sanitize_bonds(self.allowed_bonds)

        df = super(BagofBonds, self).featurize_dataframe(df, col_id, *args,
                                                         **kwargs)
        self._dataframe_featurizing = False
        return df

    def enumerate_bonds(self, s):
        """
        Lists out all the bond possibilities in a single structure.

        Args:
            s (Structure): A pymatgen structure

        Returns:
            A list of bond types in 'Li-O' form, where the order of the
            elements in each bond type is alphabetic.
        """
        if isinstance(s, dict):
            s = Structure.from_dict(s)
        els = s.composition.elements
        het_bonds = list(itertools.combinations(els, 2))
        het_bonds = [tuple(sorted([str(i) for i in j])) for j in het_bonds]
        hom_bonds = [(str(el), str(el)) for el in els]
        bond_types = [k[0] + self._token + k[1] for k in het_bonds + hom_bonds]
        return sorted(bond_types)

    def enumerate_all_bonds(self, structures):
        """
        Identify all the unique, possible bonds types of all structures present,
        and create the 'unified' bonds list.

        Args:
             structures (list/ndarray): List of pymatgen Structures

        Returns:
            A tuple of unique, possible bond types for an entire list of
            structures. This tuple is used to form the unified feature labels.
        """
        bond_types = []
        for s in structures:
            bts = self.enumerate_bonds(s)
            for bt in bts:
                if bt not in bond_types:
                    bond_types.append(bt)
        return tuple(sorted(bond_types))

    def _sanitize_bonds(self, bonds):
        """
        Prevent errors and/or bond duplicates from badly formatted allowed_bonds

        Args:
            bonds ([str]): A listlike object of bond types, specified as strings
                with the general format "El-Sp", where El or Sp can be a specie
                or an element with pymatgen's str representation of a bond. For
                example, a Cesium Chloride bond could be represented as either
                "Cs-Cl" or "Cs+-Cl-" or "Cl-Cs" or "Cl--Cs+". "bond frac." may
                be present at the end of each bond, as it will be sanitized.
        Returns:
            bonds ([str]): A listlike object containing alphabetized bond types.
                Note that ions and elements will still have distinct bonds if
                the bonds list originally contained them.
        """
        for i, bond in enumerate(bonds):
            if not isinstance(bond, str) or "-" not in bond:
                raise TypeError("Bonds must be specified as strings between"
                                "elements or species, for example Cl-Cs")
            bond = bond.replace(" bond frac.", "")
            species = sorted(bond.split(self._token))
            bonds[i] = self._token.join(species)
        return tuple(sorted(bonds))

    def _species_from_bondstr(self, bondstr):
        """
        Create a 2-tuple of species objects from a bond string.

        Args:
            bondstr (str): A string representing a bond between elements or
                species, or a combination of the two. For example, "Cl- - Cs+".

        Returns:
            ((Species)): A tuple of pymatgen Species objects in alphabetical
                order.
        """
        species = []
        for ss in bondstr.split(self._token):
            try:
                species.append(Specie.from_string(ss))
            except ValueError:
                d = {'element': ss, 'oxidation_state': 0}
                species.append(Specie.from_dict(d))
        return tuple(species)

    def _approximate_bonds(self, local_bonds):
        """
        Approximate a structure's bonds if the structure contains bonds not in
        allowed_bonds.

        Local bonds are approximated according to the "nearest" bonds present in
        allowed_bonds (the unified list). Nearness is measured by the euclidean
        distance (diff) in mendeleev number of each element. For example a Na-O
        bond could be approximated as a Li-O bond ( distance is sqrt(0^2 + 1^2)
         = 1).

        Args:
            local_bonds (dict): The bonds present in the structure with the bond
                types as keys ("Cl--Cs+") and the bond fraction as values (0.7).

        Returns:
            ubonds_data (dict): A dictionary of the unified (allowed) bonds
                with the bond names as keys and the corresponding bond fractions
                (whether approximated or true) as values.

        """

        # At this stage, local_bonds may contain unified bonds which
        # are nan.

        ubonds_data = {k: 0.0 for k in self.unified_bonds}
        ubonds_species = {k: None for k in self.unified_bonds}
        for ub in self.unified_bonds:
            species = self._species_from_bondstr(ub)
            ubonds_species[ub] = tuple(species)
        # keys are pairs of species, values are bond names in unified_bonds
        ubonds_species = {v: k for k, v in ubonds_species.items()}

        for lb in local_bonds.keys():
            local_bonds[lb] = 0.0 if np.isnan(local_bonds[lb]) else local_bonds[lb]

            if lb in self.unified_bonds:
                ubonds_data[lb] += local_bonds[lb]
            else:
                lbs = self._species_from_bondstr(lb)

                nearest = []
                d_min = None
                for ubs in ubonds_species.keys():

                    # The distance between bonds is euclidean. To get a good
                    # measure of the coordinate between mendeleev numbers for
                    # each specie, we use the minumum difference. ie, for
                    # finding the distance between Na-O and O-Li, we would
                    # not want the distance between (Na and O) and (O and Li),
                    # we want the distance between (Na and Li) and (O and O).

                    u_mends = sorted([j.element.mendeleev_no for j in ubs])
                    l_mends = sorted([j.element.mendeleev_no for j in lbs])

                    d0 = u_mends[0] - l_mends[0]
                    d1 = u_mends[1] - l_mends[1]

                    d = (d0**2.0 + d1**2.0)**0.5
                    if not d_min:
                        d_min = d
                        nearest = [ubs]
                    elif d < d_min:
                        # A new best approximation has been found
                        d_min = d
                        nearest = [ubs]
                    elif d == d_min:
                        # An equivalent approximation has been found
                        nearest += [ubs]
                    else:
                        pass

                # Divide bond fraction equally among all equiv. approximate bonds
                bond_frac = local_bonds[lb]/len(nearest)
                for n in nearest:
                    # Get the name of the approximate bond from the map
                    ub = ubonds_species[n]

                    # Add the bond frac to that/those nearest bond(s)
                    ubonds_data[ub] += bond_frac
        return ubonds_data

    def featurize(self, s):
        """
        Quantify the fractions of each bond type in a structure.

        For collections of structures, bonds types which are not found in a
        particular structure (e.g., Li-P in BaTiO3) are represented as NaN.

        Args:
            s (Structure): A pymatgen structure object

        Returns:
            (list) The feature list of bond fractions, in the order of the
                alphabetized corresponding bond names.
        """
        if isinstance(s, dict):
            s = Structure.from_dict(s)

        bond_types = tuple(self.enumerate_bonds(s))
        bonds = {k: 0.0 for k in bond_types}
        tot_bonds = 0.0

        # If featurize is being called from a dataframe or featurize_many,
        # a comprehensize 'unified' bond list is created. The following code
        # places nan in all bad bond values, where bonds are not physically
        # possible.
        if hasattr(self, 'unified_bonds'):

            # if we find a bond in unified_bonds not in bond_types, mark as nan
            for b in self.unified_bonds:
                if b not in bond_types:
                    if self.bbv is None:
                        bonds[b] = float("nan")
                    else:
                        bonds[b] = self.bbv

            # if we find a bond in bond_types not in unified_bonds, skip
            if not self.approx_bonds:
                for b in bond_types:
                    if b not in self.unified_bonds:
                        # return [float("nan")] * len(self.unified_bonds)
                        bonds.pop(b)
            ordered_bonds = self.unified_bonds
        else:
            self.local_bonds = bond_types
            ordered_bonds = self.local_bonds

        for i, _ in enumerate(s.sites):
            nearest = self.nn.get_nn(s, i)
            origin = s.sites[i].specie

            for neigh in nearest:
                btup = tuple(sorted([str(origin), str(neigh.specie)]))
                b = btup[0] + self._token + btup[1]
                # The bond will not be in bonds if it is a forbidden bond
                # (when a local bond is not in allowed_bonds)
                tot_bonds += 1.0
                if b in bonds:
                    bonds[b] += 1.0

        if self.approx_bonds:
            bonds = self._approximate_bonds(bonds)

        # tot_bonds = sum(v for v in bonds.values() if not np.isnan(v))

        # If allowed_bonds caused no bonds to be present, all bonds will be 0.
        # Prevent division by zero error.
        tot_bonds = tot_bonds or 1.0

        return [bonds[b] / tot_bonds for b in ordered_bonds]

    def feature_labels(self):
        """
        If an entire dataframe is featurized, returns all unique possible
        bonds gathered across all structures.

        If only .featurize called, returns all bond labels for the last structure
        featurized.
        """
        if self._dataframe_featurizing:
            labels = self.unified_bonds
        else:
            if hasattr(self, 'unified_bonds'):
                labels = self.unified_bonds
            else:
                labels = self.local_bonds
        return [b + " bond frac." for b in labels]

    def implementors(self):
        return ["Alex Dunn"]

    def citations(self):
        return ["@article{doi:10.1021/acs.jpclett.5b00831, "
                "author = {Hansen, Katja and Biegler, "
                "Franziska and Ramakrishnan, Raghunathan and Pronobis, Wiktor"
                "and von Lilienfeld, O. Anatole and Muller, Klaus-Robert and"
                "Tkatchenko, Alexandre},"
                "title = {Machine Learning Predictions of Molecular Properties: "
                "Accurate Many-Body Potentials and Nonlocality in Chemical Space},"
                "journal = {The Journal of Physical Chemistry Letters},"
                "volume = {6},"
                "number = {12},"
                "pages = {2326-2331},"
                "year = {2015},"
                "doi = {10.1021/acs.jpclett.5b00831}, "
                "note ={PMID: 26113956},"
                "URL = {http://dx.doi.org/10.1021/acs.jpclett.5b00831}"
                "}"]
