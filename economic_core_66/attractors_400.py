# -*- coding: utf-8 -*-
"""
attractors_400.py — Structure des 400 attracteurs conjoints.

Ce module construit les 400 attracteurs conjoints du modèle Cl(6,6),
obtenus par produit cartésien des 20 attracteurs économiques et des
20 attracteurs géographiques.

Sources :
    - Article 144 pentades, §2.3 (produit tensoriel)
    - economic_core_66.py (20 attracteurs, intégré)
    - pentads_144.py (12 pentades de base)

Structure :
    - 20 attracteurs économiques : A..T
    - 20 attracteurs géographiques : A..T
    - 400 attracteurs conjoints = 20 × 20

Usage :
    from attractors_400 import build_400_attractors, get_attractor_400
    
    attractors = build_400_attractors()
    print(len(attractors))  # 400
    
    a = get_attractor_400('S_S')  # Chine 2026
    print(a['eco'], a['geo'])  # S S
"""

import numpy as np
from typing import Dict, List, Set, Any, Optional, Tuple
from itertools import product
from economic_core_66.pentads_144 import ATTRACTEURS, SIGNATURES_POLARITE

# ============================================================
# NOMS DES 20 ATTRACTEURS (économie et géographie)
# Source : economic_core_v6.py
# ============================================================

ATTRACTOR_NAMES: Dict[str, str] = {
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

ATTRACTOR_POLARITY: Dict[str, str] = {
    'A': '3P', 'B': '3P', 'C': '3P',
    'D': '2P+1N', 'E': '2P+1N', 'F': '2P+1N', 'G': '2P+1N', 'H': '2P+1N',
    'I': '1P+2N', 'J': '1P+2N', 'K': '1P+2N', 'L': '1P+2N', 'M': '1P+2N',
    'N': '1P+2N', 'O': '1P+2N', 'P': '1P+2N', 'Q': '1P+2N', 'R': '1P+2N',
    'S': '1P+2N',
    'T': '3N',
}


# ============================================================
# CONSTRUCTION DES 400 ATTRACTEURS CONJOINTS
# Source : Article 144 pentades, §2.3
# ============================================================
#
# Chaque attracteur conjoint est le produit tensoriel :
#     E_{i,j} = A_i^{(éco)} ⊗ A_j^{(géo)}
#
# où A_i^{(éco)} et A_j^{(géo)} sont des attracteurs de Cl(6,0).
#
# L'attracteur conjoint est identifié par la clé "A_i_A_j"
# (par exemple "S_S" pour la Chine 2026).
# ============================================================

def build_400_attractors() -> Dict[str, Dict[str, Any]]:
    """
    Construit les 400 attracteurs conjoints = 20 éco × 20 géo.

    Returns:
        dict {clé: {'eco': ..., 'geo': ..., 'triplet_eco': ...,
                     'triplet_geo': ..., 'polarity_eco': ...,
                     'polarity_geo': ..., 'name_eco': ...,
                     'name_geo': ..., 'polarity_combined': ...}}

    Examples:
        >>> attractors = build_400_attractors()
        >>> len(attractors)
        400
        >>> 'S_S' in attractors
        True
        >>> attractors['S_S']['eco']
        'S'
        >>> attractors['S_S']['geo']
        'S'
    """
    attractors_400 = {}

    eco_names = list(ATTRACTEURS.keys())  # A..T
    geo_names = list(ATTRACTEURS.keys())  # A..T

    for eco, geo in product(eco_names, geo_names):
        key = f"{eco}_{geo}"

        triplet_eco = ATTRACTEURS[eco]
        triplet_geo = ATTRACTEURS[geo]

        polarity_eco = ATTRACTOR_POLARITY[eco]
        polarity_geo = ATTRACTOR_POLARITY[geo]

        # Polarité combinée : produit des signatures
        # 3P × 3P = 3P+3P (6P)
        # etc.
        polarity_combined = f"{polarity_eco} ⊗ {polarity_geo}"

        attractors_400[key] = {
            'eco': eco,
            'geo': geo,
            'triplet_eco': triplet_eco,
            'triplet_geo': triplet_geo,
            'polarity_eco': polarity_eco,
            'polarity_geo': polarity_geo,
            'polarity_combined': polarity_combined,
            'name_eco': ATTRACTOR_NAMES[eco],
            'name_geo': ATTRACTOR_NAMES[geo],
            'name_combined': f"{ATTRACTOR_NAMES[eco]} / {ATTRACTOR_NAMES[geo]}",
            # Triplet conjoint : union des deux triplets (6 pentades)
            'triplet_combined': triplet_eco | triplet_geo,
        }

    return attractors_400


def build_400_attractors_by_polarity() -> Dict[str, Dict[str, Any]]:
    """
    Construit les 400 attracteurs et les organise par polarité combinée.

    Returns:
        dict {polarity_combined: {clé: ...}}
    """
    attractors = build_400_attractors()

    by_polarity = {}
    for key, info in attractors.items():
        pol = info['polarity_combined']
        if pol not in by_polarity:
            by_polarity[pol] = {}
        by_polarity[pol][key] = info

    return by_polarity


def get_attractor_400(key: str) -> Dict[str, Any]:
    """
    Retourne un attracteur conjoint spécifique.

    Args:
        key: clé de la forme "A_i_A_j" (par exemple "S_S")

    Returns:
        dict avec les informations de l'attracteur conjoint

    Raises:
        ValueError: si la clé est invalide
    """
    parts = key.split('_')
    if len(parts) != 2:
        raise ValueError(
            f"Clé invalide : {key}. Format attendu : 'A_i_A_j'"
        )

    eco, geo = parts
    if eco not in ATTRACTEURS:
        raise ValueError(f"Attracteur économique inconnu : {eco}")
    if geo not in ATTRACTEURS:
        raise ValueError(f"Attracteur géographique inconnu : {geo}")

    attractors = build_400_attractors()
    return attractors[key]


def get_attractors_for_eco(eco: str) -> Dict[str, Dict[str, Any]]:
    """
    Retourne tous les attracteurs conjoints pour un attracteur
    économique donné.

    Args:
        eco: nom de l'attracteur économique (A..T)

    Returns:
        dict {clé: ...} des 20 attracteurs conjoints
    """
    if eco not in ATTRACTEURS:
        raise ValueError(f"Attracteur économique inconnu : {eco}")

    attractors = build_400_attractors()
    return {
        key: info for key, info in attractors.items()
        if info['eco'] == eco
    }


def get_attractors_for_geo(geo: str) -> Dict[str, Dict[str, Any]]:
    """
    Retourne tous les attracteurs conjoints pour un attracteur
    géographique donné.

    Args:
        geo: nom de l'attracteur géographique (A..T)

    Returns:
        dict {clé: ...} des 20 attracteurs conjoints
    """
    if geo not in ATTRACTEURS:
        raise ValueError(f"Attracteur géographique inconnu : {geo}")

    attractors = build_400_attractors()
    return {
        key: info for key, info in attractors.items()
        if info['geo'] == geo
    }


# ============================================================
# DISTANCES ET TRANSITIONS
# ============================================================

def attractor_distance_400(key1: str, key2: str) -> int:
    """
    Distance de Hamming entre deux attracteurs conjoints.

    La distance est le nombre de pentades qui diffèrent entre
    les deux triplets combinés.

    Args:
        key1: clé du premier attracteur (par ex. "S_S")
        key2: clé du deuxième attracteur (par ex. "E_E")

    Returns:
        distance: nombre de pentades qui diffèrent (0 à 6)
    """
    a1 = get_attractor_400(key1)
    a2 = get_attractor_400(key2)

    triplet1 = a1['triplet_combined']
    triplet2 = a2['triplet_combined']

    return len(triplet1 ^ triplet2)


def find_nearest_attractor_400(
    key: str,
    candidates: Optional[List[str]] = None,
) -> Tuple[str, int]:
    """
    Trouve l'attracteur conjoint le plus proche.

    Args:
        key: clé de l'attracteur de départ
        candidates: liste de clés candidates (si None, tous les 400)

    Returns:
        (clé_la_plus_proche, distance)
    """
    if candidates is None:
        candidates = list(build_400_attractors().keys())

    best_key = key
    best_distance = float('inf')

    for candidate in candidates:
        if candidate == key:
            continue
        dist = attractor_distance_400(key, candidate)
        if dist < best_distance:
            best_distance = dist
            best_key = candidate

    return best_key, best_distance


# ============================================================
# FONCTIONS DE VALIDATION
# ============================================================

def validate_attractors_400() -> Dict[str, Any]:
    """
    Valide la structure des 400 attracteurs conjoints.

    Returns:
        dict avec les résultats de validation
    """
    results = {}

    # Test 1 : construction des 400 attracteurs
    try:
        attractors = build_400_attractors()
        results['attractors_400_count'] = len(attractors)
        results['attractors_400_ok'] = len(attractors) == 400
    except Exception as e:
        results['attractors_400_ok'] = False
        results['attractors_400_error'] = str(e)

    # Test 2 : cohérence des clés
    try:
        attractors = build_400_attractors()
        keys_ok = True
        for key, info in attractors.items():
            expected_key = f"{info['eco']}_{info['geo']}"
            if key != expected_key:
                keys_ok = False
                break
        results['keys_ok'] = keys_ok
    except Exception as e:
        results['keys_ok'] = False
        results['keys_error'] = str(e)

    # Test 3 : cohérence des triplets
    try:
        attractors = build_400_attractors()
        triplets_ok = True
        for key, info in attractors.items():
            expected_triplet = info['triplet_eco'] | info['triplet_geo']
            if info['triplet_combined'] != expected_triplet:
                triplets_ok = False
                break
        results['triplets_ok'] = triplets_ok
    except Exception as e:
        results['triplets_ok'] = False
        results['triplets_error'] = str(e)

    # Test 4 : répartition par polarité
    try:
        by_polarity = build_400_attractors_by_polarity()
        # Il doit y avoir 4 polarités × 4 polarités = 16 combinaisons
        results['polarity_combinations'] = len(by_polarity)
        results['polarity_ok'] = len(by_polarity) == 16
    except Exception as e:
        results['polarity_ok'] = False
        results['polarity_error'] = str(e)

    # Test 5 : get_attractor_400
    try:
        a = get_attractor_400('S_S')
        results['get_ok'] = (a['eco'] == 'S' and a['geo'] == 'S')
    except Exception as e:
        results['get_ok'] = False
        results['get_error'] = str(e)

    # Test 6 : get_attractors_for_eco
    try:
        eco_attractors = get_attractors_for_eco('S')
        results['eco_count'] = len(eco_attractors)
        results['eco_ok'] = len(eco_attractors) == 20
    except Exception as e:
        results['eco_ok'] = False
        results['eco_error'] = str(e)

    # Test 7 : get_attractors_for_geo
    try:
        geo_attractors = get_attractors_for_geo('S')
        results['geo_count'] = len(geo_attractors)
        results['geo_ok'] = len(geo_attractors) == 20
    except Exception as e:
        results['geo_ok'] = False
        results['geo_error'] = str(e)

    # Test 8 : distance entre attracteurs
    try:
        # S_S et S_S → distance 0
        d1 = attractor_distance_400('S_S', 'S_S')
        # S_S et S_E → distance 2 (E = {P5,P6,N3}, S = {P6,N5,N6})
        # Triplet combiné S_S = {P6,N5,N6} ∪ {P6,N5,N6} = {P6,N5,N6}
        # Triplet combiné S_E = {P6,N5,N6} ∪ {P5,P6,N3} = {P5,P6,N3,N5,N6}
        # Différence symétrique = {P5,N3} → distance 2
        d2 = attractor_distance_400('S_S', 'S_E')
        results['distance_ok'] = (d1 == 0 and d2 == 2)
    except Exception as e:
        results['distance_ok'] = False
        results['distance_error'] = str(e)

    # Résultat global
    results['all_ok'] = all([
        results.get('attractors_400_ok', False),
        results.get('keys_ok', False),
        results.get('triplets_ok', False),
        results.get('polarity_ok', False),
        results.get('get_ok', False),
        results.get('eco_ok', False),
        results.get('geo_ok', False),
        results.get('distance_ok', False),
    ])

    return results


def print_validation_report() -> None:
    """Affiche un rapport de validation formaté."""
    print("=" * 60)
    print("  VALIDATION DES 400 ATTRACTEURS CONJOINTS")
    print("=" * 60)

    results = validate_attractors_400()

    print(f"\n  400 attracteurs :")
    print(f"    Nombre : {results.get('attractors_400_count', 0)}/400")
    print(f"    Statut : {'✓ OK' if results.get('attractors_400_ok', False) else '✗ ÉCHEC'}")

    print(f"\n  Cohérence des clés :")
    print(f"    Statut : {'✓ OK' if results.get('keys_ok', False) else '✗ ÉCHEC'}")

    print(f"\n  Cohérence des triplets :")
    print(f"    Statut : {'✓ OK' if results.get('triplets_ok', False) else '✗ ÉCHEC'}")

    print(f"\n  Répartition par polarité :")
    print(f"    Combinaisons : {results.get('polarity_combinations', 0)}/16")
    print(f"    Statut : {'✓ OK' if results.get('polarity_ok', False) else '✗ ÉCHEC'}")

    print(f"\n  Fonction get_attractor_400 :")
    print(f"    Statut : {'✓ OK' if results.get('get_ok', False) else '✗ ÉCHEC'}")

    print(f"\n  Filtres par attracteur :")
    print(f"    Éco : {results.get('eco_count', 0)}/20 "
          f"{'✓ OK' if results.get('eco_ok', False) else '✗ ÉCHEC'}")
    print(f"    Géo : {results.get('geo_count', 0)}/20 "
          f"{'✓ OK' if results.get('geo_ok', False) else '✗ ÉCHEC'}")

    print(f"\n  Distances :")
    print(f"    Statut : {'✓ OK' if results.get('distance_ok', False) else '✗ ÉCHEC'}")

    print(f"\n  RÉSULTAT GLOBAL : "
          f"{'✓ TOUS LES TESTS PASSENT' if results['all_ok'] else '✗ ÉCHEC'}")

    print("=" * 60)


# ============================================================
# POINT D'ENTRÉE
# ============================================================

if __name__ == "__main__":
    # Afficher les 20 attracteurs
    print("\n" + "=" * 60)
    print("  20 ATTRACTEURS (ÉCO ET GÉO)")
    print("=" * 60)
    for name, info in ATTRACTOR_NAMES.items():
        pol = ATTRACTOR_POLARITY[name]
        triplet = sorted(ATTRACTEURS[name])
        print(f"    {name} ({pol:6s}) — {info:45s} {triplet}")

    # Construire les 400 attracteurs
    print("\n" + "=" * 60)
    print("  CONSTRUCTION DES 400 ATTRACTEURS CONJOINTS")
    print("=" * 60)
    attractors = build_400_attractors()
    print(f"    Nombre total : {len(attractors)}")

    # Afficher des exemples
    print(f"\n    Exemples :")
    for key in ['A_A', 'S_S', 'T_T', 'S_E', 'E_S', 'S_F', 'F_S']:
        a = attractors[key]
        print(f"      {key:6s} → éco={a['eco']} ({a['polarity_eco']}), "
              f"géo={a['geo']} ({a['polarity_geo']})")
        print(f"              triplet combiné : {sorted(a['triplet_combined'])}")

    # Répartition par polarité combinée
    print("\n" + "=" * 60)
    print("  RÉPARTITION PAR POLARITÉ COMBINÉE")
    print("=" * 60)
    by_polarity = build_400_attractors_by_polarity()
    for pol, group in sorted(by_polarity.items()):
        print(f"    {pol:20s} → {len(group)} attracteurs")

    # Test de distance
    print("\n" + "=" * 60)
    print("  TEST DE DISTANCE")
    print("=" * 60)
    print(f"    d(S_S, S_S) = {attractor_distance_400('S_S', 'S_S')}")
    print(f"    d(S_S, S_E) = {attractor_distance_400('S_S', 'S_E')}")
    print(f"    d(S_S, E_E) = {attractor_distance_400('S_S', 'E_E')}")
    print(f"    d(S_S, T_T) = {attractor_distance_400('S_S', 'T_T')}")

    # Test de recherche du plus proche
    print("\n" + "=" * 60)
    print("  RECHERCHE DU PLUS PROCHE DEPUIS S_S")
    print("=" * 60)
    # Cibles : E, F, D
    candidates = ['E_E', 'F_F', 'D_D', 'E_F', 'F_E', 'E_D', 'D_E', 'F_D', 'D_F']
    nearest, dist = find_nearest_attractor_400('S_S', candidates)
    print(f"    Depuis S_S, cible la plus proche : {nearest} (distance {dist})")

    # Validation
    print_validation_report()
