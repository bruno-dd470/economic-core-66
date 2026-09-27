# -*- coding: utf-8 -*-
"""
1_foundations_ahrn.py — Fondations extraites de l'article AHRN.

Ce module fournit les constantes universelles et la formule spectrale
extraites de l'article :
    "Une arithmétique unique pour trois ontologies : la matière,
     le vivant et l'information" (AHRN v3, juin 2026)

Contenu :
    - Les 15 constantes universelles β_k
    - Les 7 seuils spectraux S_1..S_7
    - Les constantes d'échelle (Λ_nuc, Λ_e, Λ_eco)
    - La formule spectrale E = Λ · 4^m · Σ ε_k · β_k
    - Les fonctions de validation

Usage :
    from foundations_ahrn import BETA_K, SEUILS_SPECTRAUX, spectral_energy
    
    # Calcul d'une énergie spectrale
    eps = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    E = spectral_energy(eps, m=0, Lambda=7.726)
"""

import numpy as np
from typing import List, Dict, Any, Optional


# ============================================================
# 15 CONSTANTES UNIVERSELLES β_k
# Source : Article AHRN, Chapitre 13, Table §13.1
# ============================================================

BETA_K: np.ndarray = np.array([
    0.06613695904451328,    # β0  — racine 1-2 de Λ72
    0.28174250870863576,    # β1  — racine 14-15
    0.5558698717637468,     # β2  — racine 25
    0.8682439499340019,     # β3  — racine 32
    1.5041139699699269,     # β4  — racine 40
    1.7252596926363315,     # β5  — racine 42
    1.831267929898219,      # β6  — racine 43-44
    2.0174227816393127,     # β7  — racine 47-48
    2.092837042770219,      # β8  — combinaison ternaire
    2.524927313875301,      # β9  — combinaison ternaire
    3.279177783,            # β10 — optimisation
    3.851477234958053,      # β11 — racine 41
    4.571556651552703,      # β12 — racine 43
    4.724739892029763,      # β13 — racine 46
    7.407963149728111,      # β14 — combinaison ternaire
])

# Vérification de la taille
assert len(BETA_K) == 15, f"BETA_K doit avoir 15 éléments, {len(BETA_K)} trouvés"


# ============================================================
# 7 SEUILS SPECTRAUX
# Source : Article AHRN, Chapitre 13, §13.3
#          + Article 144 pentades, §8.2.1
# ============================================================

SEUILS_SPECTRAUX: Dict[int, float] = {
    1: 0.066136959,   # S₁ — Activation minimale
    2: 0.104859650,   # S₂ — Symétrie Sheng/Ke
    3: 0.105819547,   # S₃ — Polarisation
    4: 0.135301748,   # S₄ — Couplage entre secteurs
    5: 0.171977681,   # S₅ — Transition Feu (T_fire)
    6: 0.193287026,   # S₆ — Transition Eau (T_water)
    7: 0.217317880,   # S₇ — Saut d'octave (n → n+1)
}

# Vérification de la taille
assert len(SEUILS_SPECTRAUX) == 7, "SEUILS_SPECTRAUX doit avoir 7 éléments"


# ============================================================
# RÔLES DES SEUILS
# Source : Article 144 pentades, §8.2.1
# ============================================================

ROLES_SEUILS: Dict[int, str] = {
    1: "Activation minimale",
    2: "Symétrie Sheng/Ke",
    3: "Polarisation",
    4: "Couplage entre secteurs",
    5: "Transition Feu (T_fire)",
    6: "Transition Eau (T_water)",
    7: "Saut d'octave (n → n+1)",
}


# ============================================================
# CONSTANTES D'ÉCHELLE
# Source : Article AHRN, Chapitres 8-12
# ============================================================

LAMBDA_NUC: float = 7.726       # MeV — échelle nucléaire
LAMBDA_E: float = 5.950         # eV — échelle électronique/atomique
LAMBDA_BIO: float = 5.950       # eV — échelle biochimique
LAMBDA_ECO: float = 1.23e-3     # PIB/an — échelle économique (à calibrer)


# ============================================================
# FORMULE SPECTRALE UNIVERSELLE
# Source : Article AHRN, Chapitre 8, §8.1
# ============================================================

def spectral_energy(
    epsilon: List[int],
    m: int,
    Lambda: float = LAMBDA_NUC,
) -> float:
    """
    Calcule l'énergie spectrale selon la formule AHRN.

        E = Λ · 4^m · Σ_{k=0}^{14} ε_k · β_k

    Args:
        epsilon: vecteur de 15 coefficients ternaires ∈ {-1, 0, 1}
        m: exposant d'échelle (entier, généralement 0, 1, 2 ou 3)
        Lambda: constante d'échelle (défaut : Λ_nuc = 7.726 MeV)

    Returns:
        E: énergie spectrale (en unités de Λ)

    Raises:
        ValueError: si epsilon n'a pas 15 éléments
        ValueError: si un coefficient n'est pas dans {-1, 0, 1}

    Examples:
        >>> spectral_energy([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 0, 7.726)
        0.5108...
        >>> spectral_energy([1,1,0,0,0,0,0,0,0,0,0,0,0,0,0], 0, 7.726)
        2.687...
    """
    # Validation
    if len(epsilon) != 15:
        raise ValueError(
            f"epsilon doit avoir 15 coefficients, {len(epsilon)} trouvés"
        )

    for i, e in enumerate(epsilon):
        if e not in (-1, 0, 1):
            raise ValueError(
                f"epsilon[{i}] = {e} n'est pas dans {{-1, 0, 1}}"
            )

    # Calcul de la somme ternaire
    delta = sum(e * b for e, b in zip(epsilon, BETA_K))

    # Application du facteur d'échelle
    return Lambda * (4 ** m) * delta


def spectral_energy_vectorized(
    epsilon_matrix: np.ndarray,
    m: int,
    Lambda: float = LAMBDA_NUC,
) -> np.ndarray:
    """
    Version vectorisée de spectral_energy pour un lot de configurations.

    Args:
        epsilon_matrix: matrice (N, 15) de coefficients ternaires
        m: exposant d'échelle
        Lambda: constante d'échelle

    Returns:
        energies: vecteur (N,) des énergies
    """
    if epsilon_matrix.shape[1] != 15:
        raise ValueError(
            f"epsilon_matrix doit avoir 15 colonnes, {epsilon_matrix.shape[1]} trouvées"
        )

    # Produit matriciel : (N, 15) @ (15,) → (N,)
    deltas = epsilon_matrix @ BETA_K

    return Lambda * (4 ** m) * deltas


# ============================================================
# FONCTIONS DE VALIDATION
# ============================================================

def validate_foundations() -> Dict[str, Any]:
    """
    Valide les fondations AHRN.

    Returns:
        dict avec les résultats de validation
    """
    results = {
        'beta_k_count': len(BETA_K),
        'beta_k_ok': len(BETA_K) == 15,
        'seuils_count': len(SEUILS_SPECTRAUX),
        'seuils_ok': len(SEUILS_SPECTRAUX) == 7,
        'seuils_ordered': all(
            SEUILS_SPECTRAUX[i] < SEUILS_SPECTRAUX[i+1]
            for i in range(1, 7)
        ),
    }

    # Test de la formule spectrale
    try:
        # Test 1 : un seul β_k
        eps1 = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        E1 = spectral_energy(eps1, m=0, Lambda=1.0)
        results['formula_test_1'] = abs(E1 - BETA_K[0]) < 1e-10

        # Test 2 : somme de deux β_k
        eps2 = [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        E2 = spectral_energy(eps2, m=0, Lambda=1.0)
        results['formula_test_2'] = abs(E2 - (BETA_K[0] + BETA_K[1])) < 1e-10

        # Test 3 : différence de deux β_k
        eps3 = [1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        E3 = spectral_energy(eps3, m=0, Lambda=1.0)
        results['formula_test_3'] = abs(E3 - (BETA_K[0] - BETA_K[1])) < 1e-10

        # Test 4 : facteur 4^m
        eps4 = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        E4_m0 = spectral_energy(eps4, m=0, Lambda=1.0)
        E4_m1 = spectral_energy(eps4, m=1, Lambda=1.0)
        results['formula_test_4'] = abs(E4_m1 - 4 * E4_m0) < 1e-10

        results['formula_ok'] = all([
            results['formula_test_1'],
            results['formula_test_2'],
            results['formula_test_3'],
            results['formula_test_4'],
        ])

    except Exception as e:
        results['formula_ok'] = False
        results['formula_error'] = str(e)

    # Test de la version vectorisée
    try:
        eps_matrix = np.array([
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ])
        E_vec = spectral_energy_vectorized(eps_matrix, m=0, Lambda=1.0)
        E_manual = np.array([
            BETA_K[0],
            BETA_K[1],
            BETA_K[0] + BETA_K[1],
        ])
        results['vectorized_ok'] = np.allclose(E_vec, E_manual)

    except Exception as e:
        results['vectorized_ok'] = False
        results['vectorized_error'] = str(e)

    # Résultat global
    results['all_ok'] = all([
        results['beta_k_ok'],
        results['seuils_ok'],
        results['seuils_ordered'],
        results.get('formula_ok', False),
        results.get('vectorized_ok', False),
    ])

    return results


def print_validation_report() -> None:
    """Affiche un rapport de validation formaté."""
    print("=" * 60)
    print("  VALIDATION DES FONDATIONS AHRN")
    print("=" * 60)

    results = validate_foundations()

    print(f"\n  Constantes β_k :")
    print(f"    Nombre : {results['beta_k_count']}/15")
    print(f"    Statut : {'✓ OK' if results['beta_k_ok'] else '✗ ÉCHEC'}")

    print(f"\n  Seuils spectraux :")
    print(f"    Nombre : {results['seuils_count']}/7")
    print(f"    Statut : {'✓ OK' if results['seuils_ok'] else '✗ ÉCHEC'}")
    print(f"    Ordonnés : {'✓ OK' if results['seuils_ordered'] else '✗ ÉCHEC'}")

    print(f"\n  Formule spectrale :")
    print(f"    Statut : {'✓ OK' if results.get('formula_ok', False) else '✗ ÉCHEC'}")

    print(f"\n  Version vectorisée :")
    print(f"    Statut : {'✓ OK' if results.get('vectorized_ok', False) else '✗ ÉCHEC'}")

    print(f"\n  RÉSULTAT GLOBAL : "
          f"{'✓ TOUS LES TESTS PASSENT' if results['all_ok'] else '✗ ÉCHEC'}")

    print("=" * 60)


# ============================================================
# POINT D'ENTRÉE
# ============================================================

if __name__ == "__main__":
    # Afficher les constantes
    print("\n" + "=" * 60)
    print("  CONSTANTES UNIVERSELLES β_k")
    print("=" * 60)
    for i, b in enumerate(BETA_K):
        print(f"    β_{i:2d} = {b:.15f}")

    print("\n" + "=" * 60)
    print("  SEUILS SPECTRAUX S_1..S_7")
    print("=" * 60)
    for i, s in SEUILS_SPECTRAUX.items():
        role = ROLES_SEUILS.get(i, "?")
        print(f"    S_{i} = {s:.9f}  — {role}")

    print("\n" + "=" * 60)
    print("  CONSTANTES D'ÉCHELLE")
    print("=" * 60)
    print(f"    Λ_nuc = {LAMBDA_NUC} MeV")
    print(f"    Λ_e   = {LAMBDA_E} eV")
    print(f"    Λ_bio = {LAMBDA_BIO} eV")
    print(f"    Λ_eco = {LAMBDA_ECO} PIB/an")

    # Exemples de calcul
    print("\n" + "=" * 60)
    print("  EXEMPLES DE CALCUL SPECTRAL")
    print("=" * 60)

    examples = [
        ("β_0 seul", [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 0),
        ("β_1 seul", [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 0),
        ("β_0 + β_1", [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 0),
        ("β_0 - β_1", [1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 0),
        ("β_0 (m=1)", [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 1),
        ("β_0 (m=2)", [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 2),
    ]

    for name, eps, m in examples:
        E = spectral_energy(eps, m=m, Lambda=1.0)
        print(f"    {name:20s} (m={m}) → E = {E:.15f}")

    # Validation
    print_validation_report()
