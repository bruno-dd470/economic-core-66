# -*- coding: utf-8 -*-
"""
tension_topologique.py — Tenseur de tension topologique.

Ce module calcule la tension topologique T qui détermine le
franchissement des seuils spectraux.

Source :
    - Article 144 pentades, §10.6.1

Formule :
    T_brute = |∇η · ∇R_seuil| · alpha
    T_norm = T_brute / (1 + T_brute)

    où :
        - η : asymétrie spectrale
        - R_seuil : fraction de tension sur les seuils polaires
        - alpha : facteur de normalisation (défaut 50.0)

    La normalisation borne T dans [0, 1[.

Usage :
    from tension_topologique import compute_topological_tension
    
    tension = compute_topological_tension(eta_history, r_history)
"""

import numpy as np
from typing import List, Dict, Any, Optional, Deque
from collections import deque


# ============================================================
# CALCUL DE LA TENSION TOPOLOGIQUE
# Source : Article 144 pentades, §10.6.1
# ============================================================

def compute_topological_tension(
    eta_history: List[float],
    r_threshold_history: List[float],
    window: int = 10,
    alpha: float = 50.0,  # Facteur de normalisation
) -> float:
    """
    Calcule la tension topologique T = alpha * (∇η · ∇R_seuil).

    Args:
        eta_history: historique de η
        r_threshold_history: historique de R_seuil
        window: taille de la fenêtre glissante (défaut 10)
        alpha: facteur de normalisation (défaut 50.0)

    Returns:
        tension: valeur de T

    Examples:
        >>> eta = [-0.3, -0.35, -0.4, -0.45, -0.5]
        >>> r = [0.3, 0.35, 0.4, 0.45, 0.5]
        >>> t = compute_topological_tension(eta, r)
        >>> t > 0
        True
    """
    # Validation
    if len(eta_history) < 2 or len(r_threshold_history) < 2:
        return 0.0

    # Utiliser la fenêtre glissante
    eta_window = np.array(eta_history[-window:])
    r_window = np.array(r_threshold_history[-window:])

    # Vérifier que les deux historiques ont la même longueur
    min_len = min(len(eta_window), len(r_window))
    eta_window = eta_window[-min_len:]
    r_window = r_window[-min_len:]

    if min_len < 2:
        return 0.0

    # Calcul des gradients
    grad_eta = np.gradient(eta_window)
    grad_r = np.gradient(r_window)

    # Produit scalaire
    tension = np.dot(grad_eta, grad_r)

    # Normalisation pour borner à [0, 1[
    tension_abs = np.abs(tension) * alpha
    tension_normalized = tension_abs / (1.0 + tension_abs)

    return float(tension_normalized)


def compute_tension_from_core(core, window: int = 10) -> float:
    """
    Calcule la tension topologique à partir du noyau Cl(6,6).

    Args:
        core: instance du noyau (EconomicCore66)
        window: taille de la fenêtre glissante

    Returns:
        tension: valeur de T
    """
    if not hasattr(core, 'eta_history') or not hasattr(core, 'r_threshold_history'):
        return 0.0

    return compute_topological_tension(
        core.eta_history,
        core.r_threshold_history,
        window=window,
    )


# ============================================================
# CLASSE DE SUIVI DE LA TENSION
# ============================================================

class SuiviTension:
    """
    Suivi de la tension topologique au cours du temps.

    Maintient un historique glissant de η et R_seuil,
    et calcule la tension à chaque pas.
    """

    def __init__(self, window: int = 10):
        self.window = window
        self.eta_history: Deque[float] = deque(maxlen=window)
        self.r_history: Deque[float] = deque(maxlen=window)
        self.tension_history: List[float] = []

    def update(self, eta: float, r_threshold: float) -> float:
        """
        Met à jour les historiques et calcule la tension.

        Args:
            eta: valeur actuelle de η
            r_threshold: valeur actuelle de R_seuil

        Returns:
            tension: valeur actuelle de T
        """
        self.eta_history.append(eta)
        self.r_history.append(r_threshold)

        tension = compute_topological_tension(
            list(self.eta_history),
            list(self.r_history),
            window=self.window,
        )

        self.tension_history.append(tension)
        return tension

    def current_tension(self) -> float:
        """Retourne la tension actuelle."""
        if not self.tension_history:
            return 0.0
        return self.tension_history[-1]

    def max_tension(self) -> float:
        """Retourne la tension maximale observée."""
        if not self.tension_history:
            return 0.0
        return max(self.tension_history)

    def mean_tension(self) -> float:
        """Retourne la tension moyenne."""
        if not self.tension_history:
            return 0.0
        return float(np.mean(self.tension_history))

    def get_summary(self) -> Dict[str, Any]:
        """Retourne un résumé."""
        return {
            'n_updates': len(self.tension_history),
            'current': self.current_tension(),
            'max': self.max_tension(),
            'mean': self.mean_tension(),
            'eta_history': list(self.eta_history),
            'r_history': list(self.r_history),
            'tension_history': self.tension_history[-10:],
        }

    def reset(self) -> None:
        """Réinitialise le suivi."""
        self.eta_history.clear()
        self.r_history.clear()
        self.tension_history.clear()

    def print_status(self) -> None:
        """Affiche l'état du suivi."""
        print("\n" + "=" * 60)
        print("  SUIVI DE LA TENSION TOPOLOGIQUE")
        print("=" * 60)
        print(f"  Fenêtre : {self.window}")
        print(f"  Mises à jour : {len(self.tension_history)}")
        print(f"  Tension actuelle : {self.current_tension():.6f}")
        print(f"  Tension maximale : {self.max_tension():.6f}")
        print(f"  Tension moyenne  : {self.mean_tension():.6f}")

        if self.tension_history:
            print(f"\n  10 dernières tensions :")
            for i, t in enumerate(self.tension_history[-10:], 1):
                print(f"    {i:2d}. T = {t:.6f}")

        print("=" * 60)


# ============================================================
# INTÉGRATION AVEC LES SEUILS
# ============================================================

def check_threshold_crossing(
    tension: float,
    seuil: int,
    seuils_spectraux: Optional[Dict[int, float]] = None,
) -> bool:
    """
    Vérifie si un seuil peut être franchi compte tenu de la tension.

    Args:
        tension: valeur de T
        seuil: numéro du seuil
        seuils_spectraux: dict des seuils (si None, import par défaut)

    Returns:
        True si le seuil peut être franchi
    """
    if seuils_spectraux is None:
        from economic_core_66.seuils_spectraux import SEUILS_SPECTRAUX               
        seuils_spectraux = SEUILS_SPECTRAUX

    if seuil not in seuils_spectraux:
        raise ValueError(f"Seuil invalide : {seuil}")

    return tension >= seuils_spectraux[seuil]


# ============================================================
# VALIDATION
# ============================================================

def validate_tension() -> Dict[str, Any]:
    """Valide le calcul de la tension."""
    results = {}

    # Test 1 : tension nulle si historiques vides
    try:
        t = compute_topological_tension([], [])
        results['empty_ok'] = (t == 0.0)
    except Exception:
        results['empty_ok'] = False

    # Test 2 : tension nulle si historiques constants
    try:
        eta = [0.5] * 5
        r = [0.5] * 5
        t = compute_topological_tension(eta, r)
        results['constant_ok'] = (t < 1e-10)
    except Exception:
        results['constant_ok'] = False

    # Test 3 : tension positive si η et R varient
    try:
        eta = [-0.3, -0.35, -0.4, -0.45, -0.5]
        r = [0.3, 0.35, 0.4, 0.45, 0.5]
        t = compute_topological_tension(eta, r)
        results['varying_ok'] = (t > 0)
    except Exception:
        results['varying_ok'] = False

    # Test 4 : SuiviTension
    try:
        suivi = SuiviTension(window=5)
        for i in range(10):
            suivi.update(-0.3 - i*0.01, 0.3 + i*0.01)
        results['suivi_ok'] = (len(suivi.tension_history) == 10)
    except Exception:
        results['suivi_ok'] = False

    # Test 5 : check_threshold_crossing
    try:
        assert check_threshold_crossing(0.22, 7)
        assert not check_threshold_crossing(0.05, 7)
        results['check_crossing_ok'] = True
    except (AssertionError, ImportError):
        results['check_crossing_ok'] = False

    results['all_ok'] = all(results.values())
    return results


def print_validation_report() -> None:
    """Affiche un rapport de validation."""
    print("=" * 60)
    print("  VALIDATION DE LA TENSION TOPOLOGIQUE")
    print("=" * 60)

    results = validate_tension()

    for key, val in results.items():
        if key != 'all_ok':
            status = '✓' if val else '✗'
            print(f"    {key:25s} : {status}")

    print(f"\n  RÉSULTAT GLOBAL : "
          f"{'✓ TOUS LES TESTS PASSENT' if results['all_ok'] else '✗ ÉCHEC'}")
    print("=" * 60)


# ============================================================
# POINT D'ENTRÉE
# ============================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  DÉMONSTRATION DE LA TENSION TOPOLOGIQUE")
    print("=" * 60)

    # Simulation d'une progression
    print("\n  Simulation de la tension :")
    print("  " + "-" * 56)

    suivi = SuiviTension(window=10)

    # Simuler une crise progressive
    for i in range(20):
        # η diminue (crise)
        eta = -0.2 - i * 0.02
        # R_seuil augmente (tension)
        r = 0.2 + i * 0.025

        tension = suivi.update(eta, r)

        if i % 5 == 0 or i == 19:
            print(f"  Pas {i:2d} : η = {eta:+.3f}, R = {r:.3f}, "
                  f"T = {tension:.6f}")

    suivi.print_status()

    # Validation
    print_validation_report()
