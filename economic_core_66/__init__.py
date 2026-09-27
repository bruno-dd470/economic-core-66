"""
economic_core_66 — Noyau endorégulé Cl(6,6) pour la modélisation économique.

Ce package implémente un modèle économique fondé sur l'algèbre de Clifford Cl(6,6),
intégrant :
- Les fondations AHRN (15 constantes β_k, 7 seuils spectraux)
- Le socle statique Cl(6,0) (20 attracteurs, 12 pentades)
- L'extension dynamique Cl(6,6) (144 pentades, 400 attracteurs conjoints)
- L'opérateur de transition T (4 composantes)
- La tension topologique T = ∇η · ∇R_seuil

Auteur : Bruno DE DOMINICIS
Licence : MIT
Version : 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Bruno DE DOMINICIS"
__license__ = "MIT"

# Exports principaux
from .economic_core_66 import EconomicCore66
from .foundations_ahrn import BETA_K, SEUILS_SPECTRAUX, spectral_energy
from .pentads_144 import build_144_pentads, ATTRACTEURS
from .attractors_400 import build_400_attractors, get_attractor_400
from .operateur_T import OperateurT
from .seuils_spectraux import GestionnaireSeuils
from .tension_topologique import SuiviTension, compute_topological_tension

__all__ = [
    'EconomicCore66',
    'BETA_K', 'SEUILS_SPECTRAUX', 'spectral_energy',
    'build_144_pentads', 'ATTRACTEURS',
    'build_400_attractors', 'get_attractor_400',
    'OperateurT', 'GestionnaireSeuils', 'SuiviTension',
    'compute_topological_tension',
]
