# -*- coding: utf-8 -*-
"""
operateur_T.py — Opérateur de transition T.

Ce module implémente l'opérateur de transition T du modèle Cl(6,6),
avec ses 4 composantes :
    T = T_structure + T_fire + T_water + T_mixed

Sources :
    - Article 144 pentades, §8.1 (définition de T)
    - Article 144 pentades, §8.2 (règles de sélection)
    - Article 144 pentades, §10.6.1 (tension topologique)

Structure :
    - T_structure : réforme structurelle (bivecteurs)
    - T_fire      : choc exogène (élément Feu)
    - T_water     : politique monétaire (élément Eau)
    - T_mixed     : RRT complète (couplage des trois)

Note :
    La méthode _choose_best_target utilise une PÉNALITÉ pour les
    attracteurs extrêmes (3P, 3N), ce qui favorise les attracteurs
    2P+1N (plus stables).

Usage :
    from operateur_T import OperateurT
    
    # Supposons core_66 initialisé
    T = OperateurT(core_66)
    
    # Appliquer une composante
    T.apply('structure', intensity=1.0)
    T.apply('mixed', intensity=1.0)
"""

import numpy as np
from typing import Dict, List, Any, Optional, Set, Tuple


# ============================================================
# CONSTANTES DE L'OPÉRATEUR T
# Source : Article 144 pentades, §8.1
# ============================================================

# Composantes de T
COMPOSANTES_T: List[str] = ['structure', 'fire', 'water', 'mixed']

# Rôles physiques des composantes
ROLES_T: Dict[str, str] = {
    'structure': 'Réforme structurelle (bivecteurs)',
    'fire': 'Choc exogène / innovation (élément Feu)',
    'water': 'Politique monétaire (élément Eau)',
    'mixed': 'RRT complète (couplage des trois)',
}

# Seuil associé à chaque composante
SEUIL_PAR_COMPOSANTE: Dict[str, int] = {
    'structure': 4,   # S4 — Couplage entre secteurs
    'fire': 5,        # S5 — Transition Feu
    'water': 6,       # S6 — Transition Eau
    'mixed': 7,       # S7 — Saut d'octave
}

# Intensité par défaut
INTENSITE_DEFAUT: float = 1.0


# ============================================================
# CLASSE PRINCIPALE
# ============================================================

class OperateurT:
    """
    Opérateur de transition T pour le modèle Cl(6,6).

    L'opérateur T agit sur l'état du noyau Cl(6,6) pour produire
    des réarrangements angulaires (transitions entre attracteurs).

    Il se décompose en 4 composantes :
        T = T_structure + T_fire + T_water + T_mixed

    Chaque composante est associée à un seuil spectral :
        - T_structure → S4 (couplage entre secteurs)
        - T_fire      → S5 (transition Feu)
        - T_water     → S6 (transition Eau)
        - T_mixed     → S7 (saut d'octave)
    """

    def __init__(self, core_66):
        """
        Initialise l'opérateur T.

        Args:
            core_66: instance du noyau Cl(6,6) (EconomicCore66)
        """
        self.core = core_66
        self.history: List[Dict[str, Any]] = []
        self.transitions_applied: int = 0

    # --------------------------------------------------------
    # Composante T_structure
    # --------------------------------------------------------

    def apply_structure(self, intensity: float = 1.0) -> Dict[str, Any]:
        """
        Applique T_structure : réforme structurelle.

        T_structure modifie les bivecteurs {B1, B2, B3} de la pentade.
        Cela change l'attracteur cible en modifiant la structure interne.

        Args:
            intensity: intensité de la réforme (0.0 à 1.0)

        Returns:
            dict avec les résultats de la transition
        """
        # État avant
        attracteur_avant = self.core.current_attractor
        eta_avant = self.core.eta_direct()

        # La réforme structurelle change l'attracteur cible
        # vers l'attracteur le plus proche dans la direction "structure"
        # (par exemple, de S vers E, ou de S vers F)
        targets = self._get_targets('structure')
        best_target = self._choose_best_target(targets, intensity)

        if best_target is not None and best_target != attracteur_avant:
            self.core.current_attractor = best_target
            self.core._update_spectral_observables()

        # État après
        attracteur_apres = self.core.current_attractor
        eta_apres = self.core.eta_direct()

        result = {
            'composante': 'structure',
            'intensite': intensity,
            'attracteur_avant': attracteur_avant,
            'attracteur_apres': attracteur_apres,
            'eta_avant': eta_avant,
            'eta_apres': eta_apres,
            'transition': attracteur_avant != attracteur_apres,
            'seuil_associe': SEUIL_PAR_COMPOSANTE['structure'],
        }

        self.history.append(result)
        self.transitions_applied += 1

        return result

    # --------------------------------------------------------
    # Composante T_fire
    # --------------------------------------------------------

    def apply_fire(self, intensity: float = 1.0) -> Dict[str, Any]:
        """
        Applique T_fire : choc exogène / innovation.

        T_fire modifie l'élément Feu (i'v) de la pentade.
        Cela active la transition vers le seuil S5.

        Args:
            intensity: intensité du choc (0.0 à 1.0)

        Returns:
            dict avec les résultats de la transition
        """
        # État avant
        attracteur_avant = self.core.current_attractor
        eta_avant = self.core.eta_direct()

        # T_fire est associé au seuil S5
        seuil = SEUIL_PAR_COMPOSANTE['fire']
        seuil_franchi = self.core.try_cross_threshold(seuil)

        # Si le seuil est franchi, on peut transitionner
        if seuil_franchi:
            targets = self._get_targets('fire')
            best_target = self._choose_best_target(targets, intensity)
            if best_target is not None and best_target != attracteur_avant:
                self.core.current_attractor = best_target
                self.core._update_spectral_observables()

        # État après
        attracteur_apres = self.core.current_attractor
        eta_apres = self.core.eta_direct()

        result = {
            'composante': 'fire',
            'intensite': intensity,
            'attracteur_avant': attracteur_avant,
            'attracteur_apres': attracteur_apres,
            'eta_avant': eta_avant,
            'eta_apres': eta_apres,
            'seuil_associe': seuil,
            'seuil_franchi': seuil_franchi,
            'transition': attracteur_avant != attracteur_apres,
        }

        self.history.append(result)
        self.transitions_applied += 1

        return result

    # --------------------------------------------------------
    # Composante T_water
    # --------------------------------------------------------

    def apply_water(self, intensity: float = 1.0) -> Dict[str, Any]:
        """
        Applique T_water : politique monétaire.

        T_water modifie l'élément Eau (1v) de la pentade.
        Cela active la transition vers le seuil S6.

        Args:
            intensity: intensité de la politique (0.0 à 1.0)

        Returns:
            dict avec les résultats de la transition
        """
        # État avant
        attracteur_avant = self.core.current_attractor
        eta_avant = self.core.eta_direct()

        # T_water est associé au seuil S6
        seuil = SEUIL_PAR_COMPOSANTE['water']
        seuil_franchi = self.core.try_cross_threshold(seuil)

        # Si le seuil est franchi, on peut transitionner
        if seuil_franchi:
            targets = self._get_targets('water')
            best_target = self._choose_best_target(targets, intensity)
            if best_target is not None and best_target != attracteur_avant:
                self.core.current_attractor = best_target
                self.core._update_spectral_observables()

        # État après
        attracteur_apres = self.core.current_attractor
        eta_apres = self.core.eta_direct()

        result = {
            'composante': 'water',
            'intensite': intensity,
            'attracteur_avant': attracteur_avant,
            'attracteur_apres': attracteur_apres,
            'eta_avant': eta_avant,
            'eta_apres': eta_apres,
            'seuil_associe': seuil,
            'seuil_franchi': seuil_franchi,
            'transition': attracteur_avant != attracteur_apres,
        }

        self.history.append(result)
        self.transitions_applied += 1

        return result

    # --------------------------------------------------------
    # Composante T_mixed
    # --------------------------------------------------------

    def apply_mixed(self, intensity: float = 1.0) -> Dict[str, Any]:
        """
        Applique T_mixed : RRT complète (couplage des trois).

        T_mixed couple T_structure, T_fire et T_water.
        Cela active la transition vers le seuil S7.

        Args:
            intensity: intensité de la réforme (0.0 à 1.0)

        Returns:
            dict avec les résultats de la transition
        """
        # État avant
        attracteur_avant = self.core.current_attractor
        eta_avant = self.core.eta_direct()

        # T_mixed est associé au seuil S7
        seuil = SEUIL_PAR_COMPOSANTE['mixed']
        seuil_franchi = self.core.try_cross_threshold(seuil)

        # Si le seuil est franchi, on peut transitionner
        if seuil_franchi:
            targets = self._get_targets('mixed')
            best_target = self._choose_best_target(targets, intensity)
            if best_target is not None and best_target != attracteur_avant:
                self.core.current_attractor = best_target
                self.core._update_spectral_observables()

        # État après
        attracteur_apres = self.core.current_attractor
        eta_apres = self.core.eta_direct()

        result = {
            'composante': 'mixed',
            'intensite': intensity,
            'attracteur_avant': attracteur_avant,
            'attracteur_apres': attracteur_apres,
            'eta_avant': eta_avant,
            'eta_apres': eta_apres,
            'seuil_associe': seuil,
            'seuil_franchi': seuil_franchi,
            'transition': attracteur_avant != attracteur_apres,
        }

        self.history.append(result)
        self.transitions_applied += 1

        return result

    # --------------------------------------------------------
    # Méthode générique
    # --------------------------------------------------------

    def apply(self, composante: str, intensity: float = 1.0) -> Dict[str, Any]:
        """
        Applique une composante de T.

        Args:
            composante: 'structure', 'fire', 'water' ou 'mixed'
            intensity: intensité (0.0 à 1.0)

        Returns:
            dict avec les résultats de la transition
        """
        if composante not in COMPOSANTES_T:
            raise ValueError(
                f"Composante inconnue : {composante}. "
                f"Composantes valides : {COMPOSANTES_T}"
            )

        if composante == 'structure':
            return self.apply_structure(intensity)
        elif composante == 'fire':
            return self.apply_fire(intensity)
        elif composante == 'water':
            return self.apply_water(intensity)
        elif composante == 'mixed':
            return self.apply_mixed(intensity)

    # --------------------------------------------------------
    # Sélection des cibles
    # --------------------------------------------------------

    def _get_targets(self, composante: str) -> List[str]:
        """
        Retourne les attracteurs cibles pour une composante donnée.

        Args:
            composante: 'structure', 'fire', 'water' ou 'mixed'

        Returns:
            liste d'attracteurs cibles
        """
        current = self.core.current_attractor

        # Cibles par défaut selon l'attracteur courant
        targets_map = {
            'S': ['E', 'F', 'D'],
            'T': ['I', 'J', 'K'],
            'R': ['D', 'F', 'E'],
            'A': ['D', 'E', 'F'],
            'C': ['D', 'E', 'F'],
            'N': ['E', 'F', 'D'],
        }

        if current in targets_map:
            targets = targets_map[current]
        else:
            # Tous les autres attracteurs
            targets = [a for a in self.core.attractors if a != current]

        # Filtrer selon la composante
        if composante == 'structure':
            # T_structure privilégie les transitions proches
            return targets
        elif composante == 'fire':
            # T_fire privilégie les transitions avec activation
            return targets
        elif composante == 'water':
            # T_water privilégie les transitions structurelles
            return targets
        elif composante == 'mixed':
            # T_mixed privilégie les transitions globales
            return targets

        return targets
        
    def _choose_best_target(
        self,
        targets: List[str],
        intensity: float = 1.0,
    ) -> Optional[str]:
        """
        Choisit le meilleur attracteur cible parmi les candidats.

        Utilise la distance de Hamming, la stabilité,
        et pénalise les attracteurs extrêmes (3P, 3N).

        Args:
            targets: liste de candidats
            intensity: intensité (filtre les transitions partielles)

        Returns:
            meilleur attracteur cible, ou None
        """
        if not targets:
            return None

        current = self.core.current_attractor

        best_target = None
        best_score = -float('inf')

        # Import local pour éviter les dépendances circulaires
        try:
            from economic_core_66.attractors_400 import ATTRACTOR_POLARITY           
            
        except ImportError:
            ATTRACTOR_POLARITY = {}

        for target in targets:
            if target == current:
                continue

            # Distance de Hamming
            distance = self.core.attractor_distance(current, target)

            # Stabilité de la cible
            stability = self.core.attractor_stability(target)

            # Pénalité pour les attracteurs extrêmes (3P ou 3N)
            polarity = ATTRACTOR_POLARITY.get(target, '?')
            if polarity in ('3P', '3N'):
                extreme_penalty = 2.0
            else:
                extreme_penalty = 0.0

            # Score : distance minimale, stabilité maximale,
            # pénalité pour les extrêmes
            score = -distance + stability * intensity - extreme_penalty

            if score > best_score:
                best_score = score
                best_target = target

        return best_target

    # --------------------------------------------------------
    # Règles de sélection
    # --------------------------------------------------------

    def check_conservation(
        self,
        transition: Dict[str, Any],
    ) -> Dict[str, bool]:
        """
        Vérifie les règles de conservation lors d'une transition.

        Règles :
        1. Conservation du nombre de générateurs
        2. Conservation de la chiralité (via i')
        3. Conservation du moment angulaire
        4. Préservation de la nilpotence

        Args:
            transition: dict avec les infos de la transition

        Returns:
            dict avec les résultats des 4 vérifications
        """
        results = {
            'conservation_generateurs': True,  # À implémenter
            'conservation_chiralite': True,
            'conservation_moment_angulaire': True,
            'preservation_nilpotence': True,
        }

        # Règle 1 : conservation du nombre de générateurs
        # Pour l'instant, on suppose que c'est toujours vrai
        # (à affiner avec la structure des pentades)

        # Règle 2 : conservation de la chiralité
        # Via l'élément Feu (i'v)
        # À implémenter

        # Règle 3 : conservation du moment angulaire
        # [L + σ/2, T] = 0
        # À implémenter

        # Règle 4 : préservation de la nilpotence
        # (g·x)² = 0
        # À implémenter

        return results

    # --------------------------------------------------------
    # Historique et diagnostic
    # --------------------------------------------------------

    def get_history(self) -> List[Dict[str, Any]]:
        """Retourne l'historique des transitions."""
        return self.history

    def get_summary(self) -> Dict[str, Any]:
        """Retourne un résumé des transitions effectuées."""
        summary = {
            'transitions_total': len(self.history),
            'transitions_reussies': sum(
                1 for h in self.history if h.get('transition', False)
            ),
            'par_composante': {},
        }

        for composante in COMPOSANTES_T:
            transitions = [
                h for h in self.history
                if h.get('composante') == composante
            ]
            summary['par_composante'][composante] = {
                'total': len(transitions),
                'reussies': sum(
                    1 for t in transitions if t.get('transition', False)
                ),
            }

        return summary

    def print_history(self) -> None:
        """Affiche l'historique des transitions."""
        print("\n" + "=" * 60)
        print("  HISTORIQUE DES TRANSITIONS")
        print("=" * 60)

        if not self.history:
            print("  Aucune transition effectuée.")
            return

        for i, h in enumerate(self.history, 1):
            print(f"\n  Transition {i} :")
            print(f"    Composante : {h['composante']}")
            print(f"    Intensité  : {h['intensite']:.2f}")
            print(f"    Avant      : {h['attracteur_avant']} "
                  f"(η = {h['eta_avant']:+.3f})")
            print(f"    Après      : {h['attracteur_apres']} "
                  f"(η = {h['eta_apres']:+.3f})")
            print(f"    Transition : {'✓' if h.get('transition', False) else '✗'}")
            if 'seuil_franchi' in h:
                print(f"    Seuil      : S{h['seuil_associe']} "
                      f"({'✓ franchi' if h['seuil_franchi'] else '✗ non franchi'})")

        print("\n" + "-" * 60)
        summary = self.get_summary()
        print(f"  Total transitions : {summary['transitions_total']}")
        print(f"  Réussies          : {summary['transitions_reussies']}")
        print("  Par composante :")
        for comp, stats in summary['par_composante'].items():
            print(f"    {comp:10s} : {stats['reussies']}/{stats['total']}")
        print("=" * 60)


# ============================================================
# FONCTIONS UTILITAIRES
# ============================================================

def apply_all_components(
    T: OperateurT,
    intensity: float = 1.0,
) -> List[Dict[str, Any]]:
    """
    Applique les 4 composantes de T dans l'ordre.

    Args:
        T: instance de OperateurT
        intensity: intensité

    Returns:
        liste des résultats
    """
    results = []
    for composante in COMPOSANTES_T:
        result = T.apply(composante, intensity)
        results.append(result)
    return results


# ============================================================
# POINT D'ENTRÉE
# ============================================================

if __name__ == "__main__":
    # Import du noyau (à créer à l'étape 6)
    try:
        from economic_core_66 import EconomicCore66
        CORE_AVAILABLE = True
    except ImportError:
        CORE_AVAILABLE = False
        print("Note : economic_core_66.py non disponible.")
        print("Utilisation d'un mock pour la démonstration.\n")

    if CORE_AVAILABLE:
        print("=" * 60)
        print("  TEST DE L'OPÉRATEUR T")
        print("=" * 60)

        core = EconomicCore66(noise_level=0.0, seed=42)
        core.set_attractor_eco('S')
        core.set_attractor_geo('S')

        T = OperateurT(core)

        print(f"\n  État initial : {core.current_attractor}")
        print(f"  η = {core.eta_direct():+.3f}")

        # NOUVEAU : simuler l'évolution des historiques
        print(f"\n  >>> Simulation des historiques (10 pas) <<<\n")
        for i in range(10):
            # Faire évoluer η et R_seuil
            core.eta_history.append(core.eta_direct() + i * 0.02)
            core.r_threshold_history.append(core.r_threshold() + i * 0.03)
            tension = core.topological_tension()
            core.suivi_tension.update(
                core.eta_direct() + i * 0.02,
                core.r_threshold() + i * 0.03,
            )
            print(f"    Pas {i}: η = {core.eta_direct() + i * 0.02:+.3f}, "
                  f"R = {core.r_threshold() + i * 0.03:.3f}, "
                  f"T = {tension:.6f}")

        # Appliquer T_mixed
        print(f"\n  >>> Application de T_mixed <<<\n")
        result = T.apply('mixed', intensity=1.0)

        print(f"  Attracteur après : {result['attracteur_apres']}")
        print(f"  η après = {result['eta_apres']:+.3f}")

        # Afficher l'historique
        T.print_history()
    else:
        # Démonstration avec un mock
        print("=" * 60)
        print("  DÉMONSTRATION DE L'OPÉRATEUR T (mock)")
        print("=" * 60)

        class MockCore:
            def __init__(self):
                self.current_attractor = 'S'
                self.attractors = {chr(65+i): set() for i in range(20)}
                self.history = []

            def eta_direct(self):
                return -0.333

            def attractor_distance(self, a, b):
                return abs(ord(a) - ord(b))

            def attractor_stability(self, a):
                return 0.5

            def try_cross_threshold(self, seuil):
                return True

            def _update_spectral_observables(self):
                pass

        core = MockCore()
        T = OperateurT(core)

        print(f"\n  État initial : {core.current_attractor}")
        print(f"  η = {core.eta_direct():+.3f}")

        # Appliquer les composantes
        for comp in COMPOSANTES_T:
            print(f"\n  >>> Application de T_{comp} <<<\n")
            result = T.apply(comp, intensity=1.0)
            print(f"  Attracteur : {result['attracteur_avant']} → "
                  f"{result['attracteur_apres']}")
            print(f"  Transition : {'✓' if result['transition'] else '✗'}")

        # Résumé
        T.print_history()
