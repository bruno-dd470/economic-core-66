# -*- coding: utf-8 -*-
"""
economic_core_v6.py — Noyau endorégulé pour le modèle économique Cl(6,0)

Version 6 avec toutes les corrections :
  1. Convention binaire stricte (+1 actif, -1 inactif)
  2. Dimension spectrale par entropie de Shannon, NORMALISÉE par 12
  3. R_seuil normalisé par arêtes incidentes
  4. Régulation par distance entre attracteurs
  5. Score pondéré pour l'identification d'attracteur

Usage :
    python economic_core_v6.py                     # test Chine 2026
    python economic_core_v6.py --config trente     # Trente Glorieuses
    python economic_core_v6.py --config stagflation
    python economic_core_v6.py --target D          # cible explicite
    python economic_core_v6.py --json              # sortie JSON
"""

import argparse
import json
import threading
from enum import Enum
from itertools import combinations
from typing import Dict, Optional, Tuple, Set

import numpy as np
import networkx as nx
from scipy.linalg import eigh


# ============================================================
# TABLES DE CORRESPONDANCE
# ============================================================

PENTAD_NAMES = {
    'P1': 'Keynésianisme',
    'P2': 'Marché libéral',
    'P3': 'Endettement',
    'P4': 'Exportation',
    'P5': 'Phase nodale',
    'P6': 'Consommation',
    'N1': 'Austérité salariale',
    'N2': 'Rigidité',
    'N3': 'Désendettement',
    'N4': 'Protectionnisme',
    'N5': 'Stase',
    'N6': 'Austérité intérieure',
}

PENTAD_POLARITY = {
    'P1': +1, 'P2': +1, 'P3': +1, 'P4': +1, 'P5': +1, 'P6': +1,
    'N1': -1, 'N2': -1, 'N3': -1, 'N4': -1, 'N5': -1, 'N6': -1,
}

ATTRACTOR_NAMES = {
    'A': 'Croissance perverse extrême',
    'B': 'Croissance perverse exportatrice',
    'C': 'Croissance perverse avec dispersion',
    'D': 'Croissance tempérée',
    'E': 'Expansion urbaine',
    'F': 'Stagflation naissante',
    'G': 'Croissance appauvrie',
    'H': 'Économie de rente',
    'I': 'Récession déflationniste',
    'J': 'Crise de liquidité',
    'K': 'Dépression agricole',
    'L': 'Économie de guerre',
    'M': 'Phase nodale en front pionnier',
    'N': 'Phase nodale avec dispersion',
    'O': 'Front pionnier en déflation',
    'P': 'Dispersion en œkoumène',
    'Q': 'Récession avec pouvoir d\'achat bas',
    'R': 'Stagflation',
    'S': 'Stase',
    'T': 'Dépression terminale',
}

ATTRACTOR_POLARITY = {
    'A': '3P', 'B': '3P', 'C': '3P',
    'D': '2P+1N', 'E': '2P+1N', 'F': '2P+1N', 'G': '2P+1N', 'H': '2P+1N',
    'I': '1P+2N', 'J': '1P+2N', 'K': '1P+2N', 'L': '1P+2N', 'M': '1P+2N',
    'N': '1P+2N', 'O': '1P+2N', 'P': '1P+2N', 'Q': '1P+2N', 'R': '1P+2N',
    'S': '1P+2N',
    'T': '3N',
}

TARGET_ATTRACTORS = {
    'S': ['E', 'F', 'D'],
    'T': ['I', 'J', 'K'],
    'R': ['D', 'F', 'E'],
    'A': ['D', 'E', 'F'],
    'C': ['D', 'E', 'F'],
    'N': ['E', 'F', 'D'],
}

N_PENTADS = 12  # Nombre de pentades (pour normalisation de d)


# ============================================================
# STABILITÉ INTRINSÈQUE
# ============================================================

def attractor_stability(triplet: Set[str]) -> float:
    polarities = [PENTAD_POLARITY[p] for p in triplet]
    n_pos = sum(1 for p in polarities if p > 0)
    n_neg = sum(1 for p in polarities if p < 0)
    if n_pos == 3 or n_neg == 3:
        return 1.0
    else:
        return 0.5


# ============================================================
# OPÉRATEUR DE DIRAC DISCRET
# ============================================================

def build_discrete_dirac_operator(
    pentad_graph: nx.Graph,
    active_triplet: Set[str],
    beta: float = 1.0,
) -> np.ndarray:
    nodes = list(pentad_graph.nodes())
    n = len(nodes)

    sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
    sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)

    D = np.zeros((2 * n, 2 * n), dtype=complex)

    for i, node_i in enumerate(nodes):
        for j, node_j in enumerate(nodes):
            if pentad_graph.has_edge(node_i, node_j):
                s_i = PENTAD_POLARITY[node_i] * (+1 if node_i in active_triplet else -1)
                s_j = PENTAD_POLARITY[node_j] * (+1 if node_j in active_triplet else -1)

                frustration = 1 if s_i != s_j else 0
                weight = np.exp(-beta * frustration)

                if s_i == s_j:
                    coupling = sigma_x
                else:
                    coupling = sigma_y

                D[2*i:2*i+2, 2*j:2*j+2] = weight * coupling

    D = 0.5 * (D + D.conj().T)
    return D


def spectral_dimension(
    pentad_graph: nx.Graph,
    active_triplet: Set[str],
    beta: float = 1.0,
) -> float:
    """
    Dimension spectrale effective d.
    
    Calculée par entropie de Shannon puis NORMALISÉE par le nombre de pentades.
    
    d_raw = exp(-sum(p_k * ln(p_k)))    (entre 1 et 24)
    d_norm = d_raw / 12                 (entre ~0.08 et 2)
    
    Propriétés :
    - d_norm ≈ 1 : système équilibré
    - d_norm ≈ 2 : système diversifié
    - d_norm < 0.5 : système concentré (crise)
    """
    try:
        D = build_discrete_dirac_operator(pentad_graph, active_triplet, beta)
        eigenvals = eigh(D, eigvals_only=True)
        abs_vals = np.abs(eigenvals)
        abs_vals = abs_vals[abs_vals > 1e-12]

        if len(abs_vals) == 0:
            return 0.0

        total = np.sum(abs_vals)
        if total == 0:
            return 0.0

        p = abs_vals / total
        p_nonzero = p[p > 0]
        entropy = -np.sum(p_nonzero * np.log(p_nonzero))

        d_raw = float(np.exp(entropy))
        d_norm = d_raw / N_PENTADS  # Normalisation par 12

        return d_norm
    except Exception:
        return 0.0


def spectral_gap(
    pentad_graph: nx.Graph,
    active_triplet: Set[str],
    beta: float = 1.0,
) -> float:
    try:
        D = build_discrete_dirac_operator(pentad_graph, active_triplet, beta)
        eigenvals = eigh(D, eigvals_only=True)
        abs_vals = np.abs(eigenvals)
        abs_vals = abs_vals[abs_vals > 1e-12]

        if len(abs_vals) == 0:
            return 0.0

        return float(np.min(abs_vals))
    except Exception:
        return 0.0


# ============================================================
# NOYAU ENDORÉGULÉ
# ============================================================

class Regime(Enum):
    SHENG = "Sheng"
    KE = "Ke"
    EQUILIBRE = "Equilibre"


_CORE_LOCK = threading.Lock()


class EconomicCore:
    """
    Noyau endorégulé v6.
    """

    def __init__(self, noise_level: float = 0.0, seed: Optional[int] = None):
        self._rng = np.random.default_rng(seed)

        self.attractors: Dict[str, Set[str]] = {
            'A': {'P1', 'P2', 'P4'}, 'B': {'P1', 'P3', 'P5'}, 'C': {'P2', 'P3', 'P6'},
            'D': {'P4', 'P5', 'N2'}, 'E': {'P5', 'P6', 'N3'}, 'F': {'P1', 'P6', 'N4'},
            'G': {'P2', 'P5', 'N6'}, 'H': {'P3', 'P4', 'N6'}, 'I': {'P1', 'N2', 'N6'},
            'J': {'P1', 'N3', 'N5'}, 'K': {'P2', 'N3', 'N5'}, 'L': {'P3', 'N2', 'N4'},
            'M': {'P4', 'N1', 'N3'}, 'N': {'P4', 'N5', 'N6'}, 'O': {'P5', 'N1', 'N4'},
            'P': {'P6', 'N1', 'N2'}, 'Q': {'P2', 'N1', 'N4'}, 'R': {'P3', 'N1', 'N5'},
            'S': {'P6', 'N5', 'N6'}, 'T': {'N2', 'N3', 'N4'},
        }

        self.current_attractor: str = 'A'

        self.cp = ['P1', 'P3', 'P5', 'P6', 'P2']
        self.cn = ['N1', 'N2', 'N6', 'N5', 'N3']

        self.thresholds = ['P4', 'N4']

        self.pentad_graph: nx.Graph = self._build_pentad_graph()

        self._spectral_dim: Optional[float] = None
        self._spectral_gap: Optional[float] = None

        self.noise_level = noise_level
        self.history: list = []

        self._update_spectral_observables()

    def _build_pentad_graph(self) -> nx.Graph:
        G = nx.Graph()
        all_pentads = set()
        for triplet in self.attractors.values():
            all_pentads.update(triplet)
        G.add_nodes_from(sorted(all_pentads))
        for triplet in self.attractors.values():
            for p1, p2 in combinations(sorted(triplet), 2):
                G.add_edge(p1, p2)
        return G

    def _active_triplet(self) -> Set[str]:
        return self.attractors[self.current_attractor]

    # --------------------------------------------------------
    # Observables
    # --------------------------------------------------------

    def eta_direct(self) -> float:
        triplet = self._active_triplet()
        if not triplet:
            return 0.0
        return sum(PENTAD_POLARITY[p] for p in triplet) / len(triplet)

    def frustration(self) -> int:
        triplet = self._active_triplet()
        E = 0
        for p1, p2 in combinations(self.pentad_graph.nodes(), 2):
            if self.pentad_graph.has_edge(p1, p2):
                s1 = PENTAD_POLARITY[p1] * (+1 if p1 in triplet else -1)
                s2 = PENTAD_POLARITY[p2] * (+1 if p2 in triplet else -1)
                if s1 != s2:
                    E += 1
        return E

    def r_threshold(self) -> float:
        triplet = self._active_triplet()
        r_frustrated = 0
        r_total = 0
        for p in self.thresholds:
            s_p = PENTAD_POLARITY[p] * (+1 if p in triplet else -1)
            for n in self.pentad_graph.neighbors(p):
                s_n = PENTAD_POLARITY[n] * (+1 if n in triplet else -1)
                r_total += 1
                if s_p != s_n:
                    r_frustrated += 1
        if r_total == 0:
            return 0.0
        return r_frustrated / r_total

    def spectral_dimension(self) -> float:
        return self._spectral_dim if self._spectral_dim is not None else 0.0

    def spectral_gap(self) -> float:
        return self._spectral_gap if self._spectral_gap is not None else 0.0

    def _update_spectral_observables(self) -> None:
        try:
            triplet = self._active_triplet()
            d = spectral_dimension(self.pentad_graph, triplet, beta=1.0)
            g = spectral_gap(self.pentad_graph, triplet, beta=1.0)
            self._spectral_dim = d
            self._spectral_gap = g
        except Exception:
            self._spectral_dim = 0.0
            self._spectral_gap = 0.0

    # --------------------------------------------------------
    # Distance et stabilité
    # --------------------------------------------------------

    def attractor_distance(self, a1: str, a2: str) -> int:
        return len(self.attractors[a1] ^ self.attractors[a2])

    def attractor_stability(self, a: str) -> float:
        return attractor_stability(self.attractors[a])

    # --------------------------------------------------------
    # Régulation
    # --------------------------------------------------------

    def _get_target_attractors(self) -> list:
        current = self.current_attractor
        if current in TARGET_ATTRACTORS:
            return TARGET_ATTRACTORS[current]
        return [a for a in self.attractors if a != current]

    def regulate(self, steps: int = 15, noise: float = 0.0, target: Optional[str] = None) -> None:
        original_noise = self.noise_level
        self.noise_level = noise

        if target and target in self.attractors:
            candidates = [target]
        else:
            candidates = self._get_target_attractors()

        best = None
        best_distance = float('inf')
        best_stability = -1.0

        for candidate in candidates:
            dist = self.attractor_distance(self.current_attractor, candidate)
            stab = self.attractor_stability(candidate)
            if dist < best_distance or (dist == best_distance and stab > best_stability):
                best = candidate
                best_distance = dist
                best_stability = stab

        if best and best != self.current_attractor:
            from_attractor = self.current_attractor
            self.current_attractor = best
            self._update_spectral_observables()
            self.history.append({
                'from': from_attractor,
                'to': best,
                'distance': best_distance,
                'stability': best_stability,
            })

        self.noise_level = original_noise

    # --------------------------------------------------------
    # Configuration
    # --------------------------------------------------------

    def set_attractor(self, attractor: str) -> None:
        if attractor not in self.attractors:
            raise ValueError(f"Attracteur inconnu : {attractor}")
        self.current_attractor = attractor
        self._update_spectral_observables()

    def set_from_config(self, config: Dict[str, int]) -> str:
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
        self.current_attractor = best_match
        self._update_spectral_observables()
        return best_match

    def set_from_bits(self, value: int) -> str:
        if not (0 <= value <= 63):
            raise ValueError(f"Value {value} hors limites (0-63)")
        attractor_names = list(self.attractors.keys())
        self.current_attractor = attractor_names[value % 20]
        self._update_spectral_observables()
        return self.current_attractor

    # --------------------------------------------------------
    # Diagnostic
    # --------------------------------------------------------

    def get_regime(self) -> Regime:
        eta = self.eta_direct()
        if eta > 0.1:
            return Regime.SHENG
        elif eta < -0.1:
            return Regime.KE
        else:
            return Regime.EQUILIBRE

    def diagnose(self) -> Dict[str, any]:
        eta = self.eta_direct()
        d = self.spectral_dimension()
        gap = self.spectral_gap()
        r = self.r_threshold()
        frustr = self.frustration()

        diagnostic = {
            'attractor': self.current_attractor,
            'attractor_name': ATTRACTOR_NAMES.get(self.current_attractor, '?'),
            'attractor_polarity': ATTRACTOR_POLARITY.get(self.current_attractor, '?'),
            'attractor_triplet': sorted(self.attractors[self.current_attractor]),
            'attractor_stability': self.attractor_stability(self.current_attractor),
            'eta': eta,
            'd': d,
            'gap': gap,
            'r_threshold': r,
            'frustration': frustr,
            'regime': self.get_regime().value,
            'target_attractors': self._get_target_attractors(),
        }

        # Sévérité (adaptée aux nouvelles plages de d)
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


# ============================================================
# CONFIGURATIONS PRÉDÉFINIES
# ============================================================

def config_chine_2026() -> Dict[str, int]:
    return {
        'P1': -1, 'P2': -1, 'P3': -1, 'P4': -1, 'P5': -1,
        'P6': +1,
        'N1': -1, 'N2': -1, 'N3': -1, 'N4': -1,
        'N5': +1, 'N6': +1,
    }


def config_trente_glorieuses() -> Dict[str, int]:
    return {
        'P1': -1, 'P2': -1, 'P3': -1, 'P4': +1, 'P5': +1,
        'P6': -1,
        'N1': -1, 'N2': +1, 'N3': -1, 'N4': -1,
        'N5': -1, 'N6': -1,
    }


def config_stagflation_1973() -> Dict[str, int]:
    return {
        'P1': -1, 'P2': -1, 'P3': +1, 'P4': -1, 'P5': -1,
        'P6': -1,
        'N1': +1, 'N2': -1, 'N3': -1, 'N4': -1,
        'N5': +1, 'N6': -1,
    }


# ============================================================
# AFFICHAGE
# ============================================================

def print_diagnostic(diag: Dict[str, any], title: str = "Diagnostic"):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

    print(f"\n  Attracteur : {diag['attractor']} — {diag['attractor_name']}")
    print(f"    Polarité  : {diag['attractor_polarity']}")
    print(f"    Triplet   : {diag['attractor_triplet']}")
    print(f"    Stabilité : {diag['attractor_stability']:.2f}")

    print(f"\n  Observables spectrales :")
    print(f"    η (asymétrie)       = {diag['eta']:+.3f}")
    print(f"    d (entropie norm.)  = {diag['d']:.3f}")
    print(f"    gap (écart spectral)= {diag['gap']:.3f}")
    print(f"    R_seuil             = {diag['r_threshold']:.3f}")
    print(f"    Frustration         = {diag['frustration']}")

    print(f"\n  Régime : {diag['regime']}")
    print(f"  État   : {diag['state']} ({diag['severity']})")

    print(f"\n  Attracteurs cibles : {diag['target_attractors']}")


# ============================================================
# CLI
# ============================================================

def parse_args():
    parser = argparse.ArgumentParser(
        description="Noyau endorégulé pour le modèle économique Cl(6,0) — v6"
    )
    parser.add_argument("--steps", type=int, default=15)
    parser.add_argument("--noise", type=float, default=0.0)
    parser.add_argument("--config", type=str, default="chine",
                        help="Config : chine, trente, stagflation, ou liste P6,N5,N6")
    parser.add_argument("--bits", type=int, default=None)
    parser.add_argument("--target", type=str, default=None)
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()

    core = EconomicCore(noise_level=args.noise, seed=42)

    if args.bits is not None:
        attractor = core.set_from_bits(args.bits)
        print(f"Configuration par ID {args.bits} → attracteur {attractor}")
    else:
        config_map = {
            'chine': config_chine_2026,
            'trente': config_trente_glorieuses,
            'stagflation': config_stagflation_1973,
        }
        if args.config in config_map:
            config = config_map[args.config]()
        else:
            pentads = [p.strip() for p in args.config.split(',')]
            config = {p: +1 for p in pentads if p in PENTAD_NAMES}
            if not config:
                print(f"Erreur : configuration inconnue '{args.config}'")
                return 1
        attractor = core.set_from_config(config)

    diag_before = core.diagnose()

    core.regulate(steps=args.steps, noise=args.noise, target=args.target)

    diag_after = core.diagnose()

    if args.json:
        output = {
            'before': diag_before,
            'after': diag_after,
            'steps': args.steps,
            'history': core.history,
        }
        print(json.dumps(output, indent=2, default=str))
    else:
        print_diagnostic(diag_before, "Diagnostic initial")
        print("\n" + ">>> Régulation <<<\n")
        if core.history:
            print("  Transitions :")
            for h in core.history:
                print(f"    {h['from']} → {h['to']} "
                      f"(distance={h['distance']}, stabilité={h['stability']:.2f})")
        else:
            print("  Aucune transition")
        print_diagnostic(diag_after, "Diagnostic final")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())