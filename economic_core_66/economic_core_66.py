# -*- coding: utf-8 -*-
"""
economic_core_66.py — Noyau complet Cl(6,6).

Ce module intègre tous les composants du modèle Cl(6,6) :
    - Fondations AHRN (β_k, seuils spectraux, formule spectrale)
    - Socle statique Cl(6,0) (20 attracteurs, 12 pentades)
    - Extension dynamique (144 pentades, 400 attracteurs, opérateur T)
    - Seuils spectraux et tension topologique

Usage :
    from economic_core_66 import EconomicCore66

    core = EconomicCore66(noise_level=0.0, seed=42)
    core.set_attractor_eco('S')
    core.set_attractor_geo('S')
    diag = core.diagnose()
"""

import numpy as np
from typing import Dict, List, Any, Optional, Set
from collections import deque
from itertools import combinations
import threading

# Imports des modules internes
from economic_core_66.foundations_ahrn import BETA_K, SEUILS_SPECTRAUX, spectral_energy
from economic_core_66.pentads_144 import (
    build_144_pentads, build_144_pentads_by_sector,
    FEUILLETS, PENTADES_BASE, ATTRACTEURS,
    CEINTURE_POSITIVE, CEINTURE_NEGATIVE, SEUILS_POLAIRES,
)
from economic_core_66.attractors_400 import (
    build_400_attractors, get_attractor_400,
    attractor_distance_400, ATTRACTOR_NAMES, ATTRACTOR_POLARITY,
)
from economic_core_66.operateur_T import OperateurT
from economic_core_66.seuils_spectraux import (
    GestionnaireSeuils, can_cross_threshold, get_polarity_from_tension,
)
from economic_core_66.tension_topologique import SuiviTension, compute_topological_tension

# ============================================================
# VERROU GLOBAL (thread-safety)
# ============================================================

_CORE_LOCK = threading.Lock()


def get_core_lock() -> threading.Lock:
    """Retourne le verrou global pour la thread-safety."""
    return _CORE_LOCK


# ============================================================
# RÉGIME
# ============================================================

class Regime:
    """Régime économique."""
    SHENG = "Sheng"
    KE = "Ke"
    EQUILIBRE = "Equilibre"


# ============================================================
# NOYAU PRINCIPAL Cl(6,6)
# ============================================================

class EconomicCore66:
    """
    Noyau endorégulé complet pour le modèle Cl(6,6).

    Intègre :
        - Le socle statique Cl(6,0) (20 attracteurs)
        - L'extension dynamique Cl(6,6) (144 pentades, 400 attracteurs)
        - L'opérateur de transition T
        - Les 7 seuils spectraux
        - La tension topologique
    """

    def __init__(self, noise_level: float = 0.0, seed: Optional[int] = None):
        """
        Initialise le noyau Cl(6,6).

        Args:
            noise_level: niveau de bruit stochastique (défaut 0.0)
            seed: graine aléatoire pour la reproductibilité
        """
        self._rng = np.random.default_rng(seed)

        # --------------------------------------------------------
        # Socle statique Cl(6,0)
        # --------------------------------------------------------
        self.attractors: Dict[str, Set[str]] = ATTRACTEURS
        self.current_attractor_eco: str = 'A'
        self.current_attractor_geo: str = 'A'

        # Graphe des pentades (12 nœuds)
        self.pentad_graph = self._build_pentad_graph()

        # --------------------------------------------------------
        # Extension dynamique Cl(6,6)
        # --------------------------------------------------------
        self.pentads_144: Dict[str, Dict[str, Any]] = build_144_pentads()
        self.pentads_144_by_sector = build_144_pentads_by_sector()
        self.attractors_400: Dict[str, Dict[str, Any]] = build_400_attractors()

        # Opérateur de transition T
        self.operateur_T = OperateurT(self)

        # --------------------------------------------------------
        # Seuils spectraux
        # --------------------------------------------------------
        self.gestionnaire_seuils = GestionnaireSeuils()

        # --------------------------------------------------------
        # Tension topologique
        # --------------------------------------------------------
        self.suivi_tension = SuiviTension(window=10)

        # Historiques pour la tension
        self.eta_history: deque = deque(maxlen=100)
        self.r_threshold_history: deque = deque(maxlen=100)

        # --------------------------------------------------------
        # État
        # --------------------------------------------------------
        self.noise_level = noise_level
        self.history: List[Dict[str, Any]] = []
        self.input_counter = 0

        # Cache pour les observables spectrales
        self._spectral_dim: Optional[float] = None
        self._spectral_gap: Optional[float] = None

        # Initialisation
        self._init_balanced()
        self._update_spectral_observables()

    # --------------------------------------------------------
    # Propriétés de compatibilité
    # --------------------------------------------------------

    @property
    def current_attractor(self) -> str:
        """Attracteur économique courant (compatibilité operateur_T)."""
        return self.current_attractor_eco

    @current_attractor.setter
    def current_attractor(self, value: str) -> None:
        """Définit l'attracteur économique courant."""
        if value not in self.attractors:
            raise ValueError(f"Attracteur inconnu : {value}")
        self.current_attractor_eco = value
        self._update_spectral_observables()

    # --------------------------------------------------------
    # Construction
    # --------------------------------------------------------

    def _build_pentad_graph(self):
        """Construit le graphe des pentades."""
        import networkx as nx
        G = nx.Graph()
        all_pentads = set()
        for triplet in self.attractors.values():
            all_pentads.update(triplet)
        G.add_nodes_from(sorted(all_pentads))
        for triplet in self.attractors.values():
            for p1, p2 in combinations(sorted(triplet), 2):
                G.add_edge(p1, p2)
        return G

    def _init_balanced(self) -> None:
        """Initialise avec un état équilibré."""
        self.current_attractor_eco = 'A'
        self.current_attractor_geo = 'A'

    # --------------------------------------------------------
    # Configuration
    # --------------------------------------------------------

    def set_attractor_eco(self, attractor: str) -> None:
        """Définit l'attracteur économique."""
        if attractor not in self.attractors:
            raise ValueError(f"Attracteur inconnu : {attractor}")
        self.current_attractor_eco = attractor
        self._update_spectral_observables()

    def set_attractor_geo(self, attractor: str) -> None:
        """Définit l'attracteur géographique."""
        if attractor not in self.attractors:
            raise ValueError(f"Attracteur inconnu : {attractor}")
        self.current_attractor_geo = attractor
        self._update_spectral_observables()

    def set_attractor_400(self, key: str) -> None:
        """Définit l'attracteur conjoint (éco et géo)."""
        a = get_attractor_400(key)
        self.current_attractor_eco = a['eco']
        self.current_attractor_geo = a['geo']
        self._update_spectral_observables()

    def set_from_config(self, config: Dict[str, int]) -> str:
        """Définit l'attracteur économique à partir d'une configuration."""
        active_pentads = {p for p, s in config.items() if s > 0}

        best_match = 'A'
        best_score = -float('inf')
        for name, triplet in self.attractors.items():
            n_active = len(triplet & active_pentads)
            n_inactive = len(triplet) - n_active
            score = n_active - 0.5 * n_inactive
            if score > best_score:
                best_score = score
                best_match = name

        self.current_attractor_eco = best_match
        self._update_spectral_observables()
        return best_match

    # --------------------------------------------------------
    # Observables Cl(6,0)
    # --------------------------------------------------------

    def _active_triplet(self) -> Set[str]:
        """Retourne le triplet de l'attracteur économique."""
        return self.attractors[self.current_attractor_eco]

    def eta_direct(self) -> float:
        """Asymétrie spectrale économique."""
        triplet = self._active_triplet()
        if not triplet:
            return 0.0

        total = 0.0
        for p in triplet:
            if p.startswith('P'):
                total += 1.0
            elif p.startswith('N'):
                total -= 1.0

        return total / len(triplet)

    def frustration(self) -> int:
        """Frustration : nombre d'arêtes entre pentades actives et inactives."""
        triplet = self._active_triplet()
        E = 0
        for p1, p2 in combinations(self.pentad_graph.nodes(), 2):
            if self.pentad_graph.has_edge(p1, p2):
                s1 = +1 if p1 in triplet else -1
                s2 = +1 if p2 in triplet else -1
                if s1 != s2:
                    E += 1
        return E

    def r_threshold(self) -> float:
        """Ratio de saturation des seuils polaires."""
        triplet = self._active_triplet()
        r_frustrated = 0
        r_total = 0

        for p in SEUILS_POLAIRES:
            s_p = +1 if p in triplet else -1
            for n in self.pentad_graph.neighbors(p):
                s_n = +1 if n in triplet else -1
                r_total += 1
                if s_p != s_n:
                    r_frustrated += 1

        if r_total == 0:
            return 0.0

        return r_frustrated / r_total

    def spectral_dimension(self) -> float:
        """Dimension spectrale effective d."""
        return self._spectral_dim if self._spectral_dim is not None else 0.0

    def spectral_gap(self) -> float:
        """Gap spectral."""
        return self._spectral_gap if self._spectral_gap is not None else 0.0

    def _update_spectral_observables(self) -> None:
        """Met à jour d et gap."""
        try:
            # d dépend de la frustration (diversité)
            frustr = self.frustration()
            # Plage étendue : 0.5 à 2.0
            self._spectral_dim = max(0.5, 2.0 - frustr / 40.0)

            # gap dépend de |R - 0.5| et de |η|
            eta = abs(self.eta_direct())
            r = self.r_threshold()
            # Formule discriminante avec minimum garanti
            self._spectral_gap = 0.5 * abs(r - 0.5) + 0.3 * eta + 0.1
        except Exception:
            self._spectral_dim = 0.0
            self._spectral_gap = 0.0

    # --------------------------------------------------------
    # Observables Cl(6,6)
    # --------------------------------------------------------

    def eta_66(self) -> float:
        """Asymétrie spectrale Cl(6,6)."""
        total_polarity = 0.0
        n_pentads = 0

        for key, p in self.pentads_144.items():
            base = p['base']
            if base in self._active_triplet():
                weight = 1.0
            else:
                weight = 0.1
            total_polarity += p['polarity'] * weight
            n_pentads += weight

        if n_pentads == 0:
            return 0.0

        return total_polarity / n_pentads

    def d_66(self) -> float:
        """Dimension spectrale Cl(6,6)."""
        return self.spectral_dimension()

    def gap_66(self) -> float:
        """Gap spectral Cl(6,6)."""
        return self.spectral_gap()

    def r_threshold_66(self) -> float:
        """Ratio de saturation Cl(6,6)."""
        return self.r_threshold()

    def topological_tension(self) -> float:
        """Tension topologique T = ∇η · ∇R_seuil."""
        if len(self.eta_history) < 2 or len(self.r_threshold_history) < 2:
            return 0.0

        return compute_topological_tension(
            list(self.eta_history),
            list(self.r_threshold_history),
            window=10,
        )

    # --------------------------------------------------------
    # Distance et stabilité
    # --------------------------------------------------------

    def attractor_distance(self, a1: str, a2: str) -> int:
        """Distance de Hamming entre deux attracteurs."""
        if a1 not in self.attractors or a2 not in self.attractors:
            raise ValueError(f"Attracteur inconnu : {a1} ou {a2}")
        return len(self.attractors[a1] ^ self.attractors[a2])

    def attractor_distance_400(self, key1: str, key2: str) -> int:
        """Distance entre deux attracteurs conjoints."""
        return attractor_distance_400(key1, key2)

    def attractor_stability(self, attractor: str) -> float:
        """Stabilité intrinsèque d'un attracteur."""
        triplet = self.attractors[attractor]
        n_pos = sum(1 for p in triplet if p.startswith('P'))
        n_neg = sum(1 for p in triplet if p.startswith('N'))

        if n_pos == 3 or n_neg == 3:
            return 1.0
        else:
            return 0.5

    # --------------------------------------------------------
    # Régulation Cl(6,0)
    # --------------------------------------------------------

    def _get_targets_60(self) -> List[str]:
        """Retourne les cibles depuis l'attracteur courant."""
        current = self.current_attractor_eco

        targets_map = {
            'S': ['E', 'F', 'D'],
            'T': ['I', 'J', 'K'],
            'R': ['D', 'F', 'E'],
            'A': ['D', 'E', 'F'],
            'C': ['D', 'E', 'F'],
            'N': ['E', 'F', 'D'],
        }

        if current in targets_map:
            return targets_map[current]

        return [a for a in self.attractors if a != current]

    def regulate_60(
        self,
        steps: int = 15,
        target: Optional[str] = None,
    ) -> None:
        """Régulation Cl(6,0) par distance minimale."""
        if target and target in self.attractors:
            candidates = [target]
        else:
            candidates = self._get_targets_60()

        best = None
        best_distance = float('inf')
        best_stability = -1.0

        for candidate in candidates:
            dist = self.attractor_distance(
                self.current_attractor_eco, candidate
            )
            stab = self.attractor_stability(candidate)

            if dist < best_distance or (
                dist == best_distance and stab > best_stability
            ):
                best = candidate
                best_distance = dist
                best_stability = stab

        if best and best != self.current_attractor_eco:
            from_attractor = self.current_attractor_eco
            self.current_attractor_eco = best
            self._update_spectral_observables()

            self.history.append({
                'type': 'regulation_60',
                'from': from_attractor,
                'to': best,
                'distance': best_distance,
                'stability': best_stability,
            })

    # --------------------------------------------------------
    # Transition Cl(6,6)
    # --------------------------------------------------------

    def apply_T(
        self,
        composante: str = 'mixed',
        intensity: float = 1.0,
    ) -> Dict[str, Any]:
        """Applique une composante de l'opérateur T."""
        self.eta_history.append(self.eta_direct())
        self.r_threshold_history.append(self.r_threshold())

        tension = self.topological_tension()
        self.suivi_tension.update(self.eta_direct(), self.r_threshold())

        result = self.operateur_T.apply(composante, intensity)

        seuils_franchis = self.gestionnaire_seuils.cross_all_possible(tension)
        result['seuils_franchis'] = self.gestionnaire_seuils.get_crossed()
        result['tension'] = tension
        result['polarity'] = self.gestionnaire_seuils.get_current_polarity()

        return result

    def try_cross_threshold(self, seuil: int) -> bool:
        """
        Tente de franchir un seuil.

        Franchit d'abord tous les seuils précédents si possible,
        puis tente de franchir le seuil cible.
        """
        tension = self.topological_tension()

        # Franchir les seuils précédents si possible
        for s in range(1, seuil):
            if not self.gestionnaire_seuils.crossed.get(s, False):
                self.gestionnaire_seuils.try_cross(tension, s)

        # Vérifier que tous les seuils précédents sont franchis
        for s in range(1, seuil):
            if not self.gestionnaire_seuils.crossed.get(s, False):
                return False

        return self.gestionnaire_seuils.try_cross(tension, seuil)

    # --------------------------------------------------------
    # Méthodes combinées
    # --------------------------------------------------------

    def regulate_and_apply_T(
        self,
        steps_60: int = 15,
        composante_T: str = 'mixed',
        intensity_T: float = 1.0,
    ) -> Dict[str, Any]:
        """Régulation complète : Cl(6,0) puis Cl(6,6)."""
        diag_before = self.diagnose()
        self.regulate_60(steps=steps_60)
        diag_after_60 = self.diagnose()
        result_T = self.apply_T(composante_T, intensity_T)
        diag_after_66 = self.diagnose()

        return {
            'diag_before': diag_before,
            'diag_after_60': diag_after_60,
            'diag_after_66': diag_after_66,
            'result_T': result_T,
        }

    # --------------------------------------------------------
    # Diagnostic
    # --------------------------------------------------------

    def get_regime(self) -> str:
        """Retourne le régime actuel."""
        eta = self.eta_direct()
        if eta > 0.1:
            return Regime.SHENG
        elif eta < -0.1:
            return Regime.KE
        else:
            return Regime.EQUILIBRE

    def diagnose(self) -> Dict[str, Any]:
        """Diagnostic complet."""
        eta = self.eta_direct()
        d = self.spectral_dimension()
        gap = self.spectral_gap()
        r = self.r_threshold()
        frustration = self.frustration()

        dominant_eco = self.current_attractor_eco
        dominant_geo = self.current_attractor_geo
        key_400 = f"{dominant_eco}_{dominant_geo}"

        seuils_franchis = self.gestionnaire_seuils.get_crossed()
        polarite = self.gestionnaire_seuils.get_current_polarity()
        tension = self.topological_tension()

        diagnostic = {
            'attractor_eco': dominant_eco,
            'attractor_geo': dominant_geo,
            'attractor_400': key_400,
            'attractor_name_eco': ATTRACTOR_NAMES.get(dominant_eco, '?'),
            'attractor_name_geo': ATTRACTOR_NAMES.get(dominant_geo, '?'),
            'polarity_eco': ATTRACTOR_POLARITY.get(dominant_eco, '?'),
            'polarity_geo': ATTRACTOR_POLARITY.get(dominant_geo, '?'),
            'eta': eta,
            'eta_66': self.eta_66(),
            'd': d,
            'd_66': self.d_66(),
            'gap': gap,
            'gap_66': self.gap_66(),
            'r_threshold': r,
            'r_threshold_66': self.r_threshold_66(),
            'frustration': frustration,
            'tension': tension,
            'regime': self.get_regime(),
            'seuils_franchis': seuils_franchis,
            'polarite_spectrale': polarite,
            'stability': self.attractor_stability(dominant_eco),
        }

        # Sévérité
        if abs(eta) > 0.6 and r > 0.7:
            diagnostic['severity'] = 'sévère'
            diagnostic['state'] = 'RETROPOLARITE'
        elif d < 1.0 and gap < 0.1:
            diagnostic['severity'] = 'critique'
            diagnostic['state'] = 'CRISE'
        elif d < 1.2 and gap < 0.15:
            diagnostic['severity'] = 'modéré'
            diagnostic['state'] = 'STASE'
        elif d > 1.5 and gap > 0.3:
            diagnostic['severity'] = 'léger'
            diagnostic['state'] = 'EQUILIBRE'
        else:
            diagnostic['severity'] = 'modéré'
            diagnostic['state'] = 'TRANSITION'

        return diagnostic

    # --------------------------------------------------------
    # Historique et résumé
    # --------------------------------------------------------

    def get_history(self) -> List[Dict[str, Any]]:
        """Retourne l'historique complet."""
        return self.history

    def get_full_history(self) -> Dict[str, List[Dict[str, Any]]]:
        """Retourne l'historique complet (régulation + T)."""
        return {
            'core': self.history,
            'T': self.operateur_T.history,
            'seuils': self.gestionnaire_seuils.crossing_history,
        }

    def reset(self) -> None:
        """Réinitialise le noyau."""
        self.current_attractor_eco = 'A'
        self.current_attractor_geo = 'A'
        self.history = []
        self.operateur_T.history = []
        self.gestionnaire_seuils.reset()
        self.suivi_tension.reset()
        self.eta_history.clear()
        self.r_threshold_history.clear()
        self._update_spectral_observables()

    # --------------------------------------------------------
    # Affichage
    # --------------------------------------------------------

    def print_diagnostic(self) -> None:
        """Affiche le diagnostic."""
        diag = self.diagnose()

        print("\n" + "=" * 60)
        print("  DIAGNOSTIC Cl(6,6)")
        print("=" * 60)

        print(f"\n  Attracteur conjoint : {diag['attractor_400']}")
        print(f"    Éco : {diag['attractor_eco']} — {diag['attractor_name_eco']}")
        print(f"          ({diag['polarity_eco']})")
        print(f"    Géo : {diag['attractor_geo']} — {diag['attractor_name_geo']}")
        print(f"          ({diag['polarity_geo']})")
        print(f"    Stabilité : {diag['stability']:.2f}")

        print(f"\n  Observables Cl(6,0) :")
        print(f"    η        = {diag['eta']:+.3f}")
        print(f"    d        = {diag['d']:.3f}")
        print(f"    gap      = {diag['gap']:.3f}")
        print(f"    R_seuil  = {diag['r_threshold']:.3f}")
        print(f"    Frustration = {diag['frustration']}")

        print(f"\n  Observables Cl(6,6) :")
        print(f"    η_66     = {diag['eta_66']:+.3f}")
        print(f"    d_66     = {diag['d_66']:.3f}")
        print(f"    gap_66   = {diag['gap_66']:.3f}")
        print(f"    R_66     = {diag['r_threshold_66']:.3f}")

        print(f"\n  Tension topologique : {diag['tension']:.6f}")
        print(f"\n  Seuils franchis : {diag['seuils_franchis']}")
        print(f"  Polarité spectrale : {diag['polarite_spectrale']}")
        print(f"  Régime : {diag['regime']}")
        print(f"  État : {diag['state']} ({diag['severity']})")

        print("=" * 60)


# ============================================================
# TEST
# ============================================================

def test_chine_2026():
    print("\n" + "=" * 60)
    print("  TEST CHINE 2026 — Noyau Cl(6,6)")
    print("=" * 60)

    core = EconomicCore66(noise_level=0.0, seed=42)

    config = {
        'P1': -1, 'P2': -1, 'P3': -1, 'P4': -1, 'P5': -1,
        'P6': +1,
        'N1': -1, 'N2': -1, 'N3': -1, 'N4': -1,
        'N5': +1, 'N6': +1,
    }
    attractor = core.set_from_config(config)
    core.set_attractor_geo(attractor)

    print(f"\n  Configuration : {config}")
    print(f"  Attracteur identifié : {attractor}")

    core.print_diagnostic()

    print("\n  >>> Régulation Cl(6,0) <<<\n")
    core.regulate_60(steps=15)
    core.print_diagnostic()

    # Simuler des historiques MODÉRÉS (correction 1)
    print("\n  >>> Simulation des historiques (modérés) <<<\n")
    for i in range(10):
        eta = core.eta_direct() + i * 0.02   # 0.02 au lieu de 0.05
        r = core.r_threshold() + i * 0.02    # 0.02 au lieu de 0.05
        core.eta_history.append(eta)
        core.r_threshold_history.append(r)
        tension = core.topological_tension()
        print(f"    Pas {i}: η = {eta:+.3f}, R = {r:.3f}, T = {tension:.6f}")

    print("\n  >>> Transition Cl(6,6) : T_mixed <<<\n")
    result = core.apply_T('mixed', intensity=1.0)
    print(f"  Transition : {result['attracteur_avant']} → {result['attracteur_apres']}")
    print(f"  Tension : {result['tension']:.6f}")
    print(f"  Seuils franchis : {result['seuils_franchis']}")

    core.print_diagnostic()

    return core


# ============================================================
# POINT D'ENTRÉE
# ============================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  VÉRIFICATION DES MODULES")
    print("=" * 60)

    print(f"  ✓ foundations_ahrn : {len(BETA_K)} β_k, {len(SEUILS_SPECTRAUX)} seuils")
    print(f"  ✓ pentads_144 : {len(build_144_pentads())} pentades")
    print(f"  ✓ attractors_400 : {len(build_400_attractors())} attracteurs")

    core = test_chine_2026()
