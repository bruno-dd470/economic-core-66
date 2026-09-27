# -*- coding: utf-8 -*-
"""
pentads_144.py — Structure des 144 pentades.

Ce module construit les 144 pentades du modèle Cl(6,6), obtenues
par produit des 12 pentades de base et des 12 feuillets spectraux.

Sources :
    - Article 144 pentades, §2.2 (12 pentades de base)
    - Article 144 pentades, §2.3 (12 feuillets spectraux)
    - Article 144 pentades, §2.5 (graphe dual Γ)
    - economic_core_66.py (20 attracteurs, intégré)

Structure :
    - 12 pentades de base : P_1..P_6 (Sheng) + N_1..N_6 (Ke)
    - 12 feuillets spectraux : e_1..e_6 (Sheng) + f_1..f_6 (Ke)
    - 144 pentades = 12 base × 12 feuillets

Usage :
    from pentads_144 import build_144_pentads, FEUILLETS, PENTADES_BASE
    
    pentads = build_144_pentads()
    print(len(pentads))  # 144
"""

import numpy as np
from typing import Dict, List, Set, Any, Optional


# ============================================================
# 12 FEUILLETS SPECTRAUX
# Source : Article 144 pentades, §2.3
# ============================================================
#
# Les 12 feuillets spectraux sont les 12 générateurs de Cl(6,6) :
#   - 6 générateurs cosmiques (Sheng, η > 0) : e_1..e_6
#   - 6 générateurs anti-cosmiques (Ke, η < 0) : f_1..f_6
#
# Chaque feuillet correspond à une "projection" des pentades de base
# sur un des 12 générateurs.
#
# Transposition économique :
#   - e_1..e_6 : variables économiques (flux)
#   - f_1..f_6 : variables géographiques (contraintes)
# ============================================================

FEUILLETS: Dict[str, Dict[str, str]] = {
    # --- Secteur Sheng (cosmique, η > 0) ---
    'e1': {'secteur': 'Sheng', 'polarite': '+', 'nom': 'Inflation'},
    'e2': {'secteur': 'Sheng', 'polarite': '+', 'nom': 'Salaire réel'},
    'e3': {'secteur': 'Sheng', 'polarite': '+', 'nom': 'Profits'},
    'e4': {'secteur': 'Sheng', 'polarite': '+', 'nom': 'Rachat'},
    'e5': {'secteur': 'Sheng', 'polarite': '+', 'nom': 'Dispersion'},
    'e6': {'secteur': 'Sheng', 'polarite': '+', 'nom': 'Régime foncier'},
    # --- Secteur Ke (anti-cosmique, η < 0) ---
    'f1': {'secteur': 'Ke', 'polarite': '-', 'nom': 'Rente foncière'},
    'f2': {'secteur': 'Ke', 'polarite': '-', 'nom': 'Capital fixe bâti'},
    'f3': {'secteur': 'Ke', 'polarite': '-', 'nom': 'Institutionnel spatial'},
    'f4': {'secteur': 'Ke', 'polarite': '-', 'nom': 'Hiérarchie rang-taille'},
    'f5': {'secteur': 'Ke', 'polarite': '-', 'nom': 'Contrainte morphologique'},
    'f6': {'secteur': 'Ke', 'polarite': '-', 'nom': 'Maillage infrastructurel'},
}

# Vérification
assert len(FEUILLETS) == 12, "FEUILLETS doit avoir 12 éléments"


# ============================================================
# 12 PENTADES DE BASE
# Source : Article 144 pentades, §2.2
# ============================================================
#
# Chaque pentade de base est un ensemble de 5 éléments de Cl(6,0),
# structuré en 3 rôles physiques :
#   - Structure : 3 bivecteurs {B_1, B_2, B_3}
#   - Fire      : élément axial F = i'v
#   - Water     : élément polaire S = 1v
#
# Note : dans ce module, nous représentons chaque pentade par son
# symbole (P_1..P_6, N_1..N_6) et sa polarité. La structure algébrique
# détaillée est donnée dans l'article 144 pentades, §2.2.
# ============================================================

PENTADES_BASE: Dict[str, Dict[str, Any]] = {
    # --- Pentades positives (Sheng) ---
    'P1': {
        'polarity': +1,
        'secteur': 'Sheng',
        'structure': ['iI', 'iJ', 'iK'],
        'fire': "i'k",
        'water': '1j',
        'nom': 'Keynésianisme',
    },
    'P2': {
        'polarity': +1,
        'secteur': 'Sheng',
        'structure': ['jI', 'jJ', 'jK'],
        'fire': "i'i",
        'water': '1k',
        'nom': 'Marché libéral',
    },
    'P3': {
        'polarity': +1,
        'secteur': 'Sheng',
        'structure': ['kI', 'kJ', 'kK'],
        'fire': "i'j",
        'water': '1i',
        'nom': 'Endettement',
    },
    'P4': {
        'polarity': +1,
        'secteur': 'Sheng',
        'structure': ["i'Ii", "i'Ij", "i'Ik"],
        'fire': "i'K",
        'water': '1J',
        'nom': 'Exportation',
    },
    'P5': {
        'polarity': +1,
        'secteur': 'Sheng',
        'structure': ["i'Ji", "i'Jj", "i'Jk"],
        'fire': "i'I",
        'water': '1K',
        'nom': 'Phase nodale',
    },
    'P6': {
        'polarity': +1,
        'secteur': 'Sheng',
        'structure': ["i'Ki", "i'Kj", "i'Kk"],
        'fire': "i'J",
        'water': '1I',
        'nom': 'Consommation',
    },
    # --- Pentades négatives (Ke) ---
    'N1': {
        'polarity': -1,
        'secteur': 'Ke',
        'structure': ['-iI', '-iJ', '-iK'],
        'fire': "-i'k",
        'water': '-1j',
        'nom': 'Austérité salariale',
    },
    'N2': {
        'polarity': -1,
        'secteur': 'Ke',
        'structure': ['-jI', '-jJ', '-jK'],
        'fire': "-i'i",
        'water': '-1k',
        'nom': 'Rigidité',
    },
    'N3': {
        'polarity': -1,
        'secteur': 'Ke',
        'structure': ['-kI', '-kJ', '-kK'],
        'fire': "-i'j",
        'water': '-1i',
        'nom': 'Désendettement',
    },
    'N4': {
        'polarity': -1,
        'secteur': 'Ke',
        'structure': ["-i'Ii", "-i'Ij", "-i'Ik"],
        'fire': "-i'K",
        'water': '-1J',
        'nom': 'Protectionnisme',
    },
    'N5': {
        'polarity': -1,
        'secteur': 'Ke',
        'structure': ["-i'Ji", "-i'Jj", "-i'Jk"],
        'fire': "-i'I",
        'water': '-1K',
        'nom': 'Stase',
    },
    'N6': {
        'polarity': -1,
        'secteur': 'Ke',
        'structure': ["-i'Ki", "-i'Kj", "-i'Kk"],
        'fire': "-i'J",
        'water': '-1I',
        'nom': 'Austérité intérieure',
    },
}

# Vérification
assert len(PENTADES_BASE) == 12, "PENTADES_BASE doit avoir 12 éléments"
assert all(p in PENTADES_BASE for p in ['P1', 'P2', 'P3', 'P4', 'P5', 'P6'])
assert all(p in PENTADES_BASE for p in ['N1', 'N2', 'N3', 'N4', 'N5', 'N6'])


# ============================================================
# GRAPHE DUAL Γ
# Source : Article 144 pentades, §2.5
# ============================================================
#
# Le graphe dual Γ des 12 pentades de base contient :
#   - 2 ceintures tropicales disjointes (C_P et C_N)
#   - 2 seuils polaires (P_4 et N_4) exclus des ceintures
# ============================================================

# Ceinture positive (Sheng)
CEINTURE_POSITIVE: List[str] = ['P1', 'P3', 'P5', 'P6', 'P2']

# Ceinture négative (Ke)
CEINTURE_NEGATIVE: List[str] = ['N1', 'N2', 'N6', 'N5', 'N3']

# Seuils polaires
SEUILS_POLAIRES: List[str] = ['P4', 'N4']

# Vérification : les ceintures sont disjointes et excluent les seuils
assert len(CEINTURE_POSITIVE) == 5
assert len(CEINTURE_NEGATIVE) == 5
assert len(SEUILS_POLAIRES) == 2
assert set(CEINTURE_POSITIVE).isdisjoint(set(CEINTURE_NEGATIVE))
assert set(CEINTURE_POSITIVE).isdisjoint(set(SEUILS_POLAIRES))
assert set(CEINTURE_NEGATIVE).isdisjoint(set(SEUILS_POLAIRES))


# ============================================================
# 20 ATTRACTEURS
# Source : economic_core_v6.py + Article 144 pentades, §2.6.2
# ============================================================
#
# Chaque attracteur est un triplet de pentades de base.
# Les 20 attracteurs sont répartis selon 4 signatures de polarité.
# ============================================================

ATTRACTEURS: Dict[str, Set[str]] = {
    # --- Signature 3P (3 positifs) ---
    'A': {'P1', 'P2', 'P4'},
    'B': {'P1', 'P3', 'P5'},
    'C': {'P2', 'P3', 'P6'},
    # --- Signature 2P+1N ---
    'D': {'P4', 'P5', 'N2'},
    'E': {'P5', 'P6', 'N3'},
    'F': {'P1', 'P6', 'N4'},
    'G': {'P2', 'P5', 'N6'},
    'H': {'P3', 'P4', 'N6'},
    # --- Signature 1P+2N ---
    'I': {'P1', 'N2', 'N6'},
    'J': {'P1', 'N3', 'N5'},
    'K': {'P2', 'N3', 'N5'},
    'L': {'P3', 'N2', 'N4'},
    'M': {'P4', 'N1', 'N3'},
    'N': {'P4', 'N5', 'N6'},
    'O': {'P5', 'N1', 'N4'},
    'P': {'P6', 'N1', 'N2'},
    'Q': {'P2', 'N1', 'N4'},
    'R': {'P3', 'N1', 'N5'},
    'S': {'P6', 'N5', 'N6'},
    # --- Signature 3N (3 négatifs) ---
    'T': {'N2', 'N3', 'N4'},
}

# Vérification
assert len(ATTRACTEURS) == 20, "ATTRACTEURS doit avoir 20 éléments"


# ============================================================
# SIGNATURES DE POLARITÉ
# Source : Article 144 pentades, §2.6.2
# ============================================================

SIGNATURES_POLARITE: Dict[str, Dict[str, Any]] = {
    '3P': {
        'count': 3,
        'attracteurs': ['A', 'B', 'C'],
        'description': 'Trois pentades positives (Sheng pur)',
    },
    '2P+1N': {
        'count': 5,
        'attracteurs': ['D', 'E', 'F', 'G', 'H'],
        'description': 'Deux positives, une négative (mélange faible)',
    },
    '1P+2N': {
        'count': 11,
        'attracteurs': ['I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S'],
        'description': 'Une positive, deux négatives (mélange fort)',
    },
    '3N': {
        'count': 1,
        'attracteurs': ['T'],
        'description': 'Trois pentades négatives (Ke pur)',
    },
}

# Vérification
total_attracteurs = sum(s['count'] for s in SIGNATURES_POLARITE.values())
assert total_attracteurs == 20, f"Total signatures = {total_attracteurs}, attendu 20"


# ============================================================
# FONCTION DE CONSTRUCTION DES 144 PENTADES
# Source : Article 144 pentades, §2.3
# ============================================================

def build_144_pentads() -> Dict[str, Dict[str, Any]]:
    """
    Construit les 144 pentades = 12 base × 12 feuillets.

    Chaque pentade est identifiée par une clé de la forme "{base}_{feuillet}",
    par exemple "P1_e1" ou "N5_f3".

    Returns:
        dict {clé: {'base': ..., 'feuillet': ..., 'polarity': ...,
                     'secteur': ..., 'nom': ...}}

    Examples:
        >>> pentads = build_144_pentads()
        >>> len(pentads)
        144
        >>> 'P1_e1' in pentads
        True
        >>> pentads['P1_e1']['polarity']
        1
        >>> pentads['N5_f3']['secteur']
        'Ke'
    """
    pentads = {}

    for base_name, base_info in PENTADES_BASE.items():
        base_polarity = base_info['polarity']
        base_secteur = base_info['secteur']
        base_nom = base_info['nom']

        for sheet_name, sheet_info in FEUILLETS.items():
            key = f"{base_name}_{sheet_name}"

            # La polarité effective est le produit de la polarité de base
            # et de la polarité du feuillet (Sheng = +1, Ke = -1)
            sheet_polarity = +1 if sheet_info['polarite'] == '+' else -1
            effective_polarity = base_polarity * sheet_polarity

            pentads[key] = {
                'base': base_name,
                'feuillet': sheet_name,
                'polarity': effective_polarity,
                'secteur': base_secteur if effective_polarity > 0 else (
                    'Sheng' if sheet_info['secteur'] == 'Sheng' else 'Ke'
                ),
                'nom': base_nom,
                'nom_feuillet': sheet_info['nom'],
                'secteur_base': base_secteur,
                'secteur_feuillet': sheet_info['secteur'],
            }

    return pentads


def build_144_pentads_by_sector() -> Dict[str, Dict[str, Any]]:
    """
    Construit les 144 pentades et les organise par secteur.

    Returns:
        dict {'Sheng': {...}, 'Ke': {...}}
    """
    pentads = build_144_pentads()

    by_sector = {'Sheng': {}, 'Ke': {}}
    for key, info in pentads.items():
        if info['polarity'] > 0:
            by_sector['Sheng'][key] = info
        else:
            by_sector['Ke'][key] = info

    return by_sector


def get_pentad(base: str, feuillet: str) -> Dict[str, Any]:
    """
    Retourne une pentade spécifique.

    Args:
        base: nom de la pentade de base (P1..P6, N1..N6)
        feuillet: nom du feuillet (e1..e6, f1..f6)

    Returns:
        dict avec les informations de la pentade
    """
    if base not in PENTADES_BASE:
        raise ValueError(f"Pentade de base inconnue : {base}")
    if feuillet not in FEUILLETS:
        raise ValueError(f"Feuillet inconnu : {feuillet}")

    key = f"{base}_{feuillet}"
    pentads = build_144_pentads()
    return pentads[key]


# ============================================================
# FONCTIONS DE VALIDATION
# ============================================================

def validate_pentads() -> Dict[str, Any]:
    """
    Valide la structure des 144 pentades.

    Returns:
        dict avec les résultats de validation
    """
    results = {
        'feuillets_count': len(FEUILLETS),
        'feuillets_ok': len(FEUILLETS) == 12,
        'pentades_base_count': len(PENTADES_BASE),
        'pentades_base_ok': len(PENTADES_BASE) == 12,
        'attracteurs_count': len(ATTRACTEURS),
        'attracteurs_ok': len(ATTRACTEURS) == 20,
        'ceintures_ok': (
            len(CEINTURE_POSITIVE) == 5
            and len(CEINTURE_NEGATIVE) == 5
            and len(SEUILS_POLAIRES) == 2
        ),
    }

    # Test de la construction des 144 pentades
    try:
        pentads = build_144_pentads()
        results['pentads_144_count'] = len(pentads)
        results['pentads_144_ok'] = len(pentads) == 144

        # Vérifier qu'il y a bien 12 pentades de base
        base_set = set(p['base'] for p in pentads.values())
        results['base_set_ok'] = len(base_set) == 12

        # Vérifier qu'il y a bien 12 feuillets
        sheet_set = set(p['feuillet'] for p in pentads.values())
        results['sheet_set_ok'] = len(sheet_set) == 12

        # Vérifier la cohérence polarité
        polarity_ok = True
        for p in pentads.values():
            base_info = PENTADES_BASE[p['base']]
            sheet_info = FEUILLETS[p['feuillet']]
            sheet_pol = +1 if sheet_info['polarite'] == '+' else -1
            expected = base_info['polarity'] * sheet_pol
            if p['polarity'] != expected:
                polarity_ok = False
                break
        results['polarity_ok'] = polarity_ok

    except Exception as e:
        results['pentads_144_ok'] = False
        results['pentads_144_error'] = str(e)

    # Test de la construction par secteur
    try:
        by_sector = build_144_pentads_by_sector()
        total = len(by_sector['Sheng']) + len(by_sector['Ke'])
        results['by_sector_ok'] = (total == 144)
        results['sheng_count'] = len(by_sector['Sheng'])
        results['ke_count'] = len(by_sector['Ke'])
    except Exception as e:
        results['by_sector_ok'] = False
        results['by_sector_error'] = str(e)

    # Test de la fonction get_pentad
    try:
        p = get_pentad('P1', 'e1')
        results['get_pentad_ok'] = (p['base'] == 'P1' and p['feuillet'] == 'e1')
    except Exception as e:
        results['get_pentad_ok'] = False
        results['get_pentad_error'] = str(e)

    # Résultat global
    results['all_ok'] = all([
        results['feuillets_ok'],
        results['pentades_base_ok'],
        results['attracteurs_ok'],
        results['ceintures_ok'],
        results.get('pentads_144_ok', False),
        results.get('base_set_ok', False),
        results.get('sheet_set_ok', False),
        results.get('polarity_ok', False),
        results.get('by_sector_ok', False),
        results.get('get_pentad_ok', False),
    ])

    return results


def print_validation_report() -> None:
    """Affiche un rapport de validation formaté."""
    print("=" * 60)
    print("  VALIDATION DES 144 PENTADES")
    print("=" * 60)

    results = validate_pentads()

    print(f"\n  Feuillets spectraux :")
    print(f"    Nombre : {results['feuillets_count']}/12")
    print(f"    Statut : {'✓ OK' if results['feuillets_ok'] else '✗ ÉCHEC'}")

    print(f"\n  Pentades de base :")
    print(f"    Nombre : {results['pentades_base_count']}/12")
    print(f"    Statut : {'✓ OK' if results['pentades_base_ok'] else '✗ ÉCHEC'}")

    print(f"\n  Attracteurs :")
    print(f"    Nombre : {results['attracteurs_count']}/20")
    print(f"    Statut : {'✓ OK' if results['attracteurs_ok'] else '✗ ÉCHEC'}")

    print(f"\n  Ceintures tropicales :")
    print(f"    C_P : {len(CEINTURE_POSITIVE)} pentades")
    print(f"    C_N : {len(CEINTURE_NEGATIVE)} pentades")
    print(f"    Seuils : {len(SEUILS_POLAIRES)} pentades")
    print(f"    Statut : {'✓ OK' if results['ceintures_ok'] else '✗ ÉCHEC'}")

    print(f"\n  144 pentades :")
    print(f"    Nombre : {results.get('pentads_144_count', 0)}/144")
    print(f"    Statut : {'✓ OK' if results.get('pentads_144_ok', False) else '✗ ÉCHEC'}")
    print(f"    12 bases distinctes : {'✓ OK' if results.get('base_set_ok', False) else '✗ ÉCHEC'}")
    print(f"    12 feuillets distincts : {'✓ OK' if results.get('sheet_set_ok', False) else '✗ ÉCHEC'}")
    print(f"    Polarité cohérente : {'✓ OK' if results.get('polarity_ok', False) else '✗ ÉCHEC'}")

    print(f"\n  Répartition par secteur :")
    print(f"    Sheng : {results.get('sheng_count', 0)} pentades")
    print(f"    Ke    : {results.get('ke_count', 0)} pentades")
    print(f"    Statut : {'✓ OK' if results.get('by_sector_ok', False) else '✗ ÉCHEC'}")

    print(f"\n  Fonction get_pentad :")
    print(f"    Statut : {'✓ OK' if results.get('get_pentad_ok', False) else '✗ ÉCHEC'}")

    print(f"\n  RÉSULTAT GLOBAL : "
          f"{'✓ TOUS LES TESTS PASSENT' if results['all_ok'] else '✗ ÉCHEC'}")

    print("=" * 60)


# ============================================================
# POINT D'ENTRÉE
# ============================================================

if __name__ == "__main__":
    # Afficher les feuillets
    print("\n" + "=" * 60)
    print("  12 FEUILLETS SPECTRAUX")
    print("=" * 60)
    for name, info in FEUILLETS.items():
        print(f"    {name:3s} [{info['secteur']:5s}] ({info['polarite']}) "
              f"— {info['nom']}")

    # Afficher les pentades de base
    print("\n" + "=" * 60)
    print("  12 PENTADES DE BASE")
    print("=" * 60)
    for name, info in PENTADES_BASE.items():
        sign = '+' if info['polarity'] > 0 else '-'
        print(f"    {name:3s} ({sign}) [{info['secteur']:5s}] "
              f"— {info['nom']}")

    # Afficher les ceintures
    print("\n" + "=" * 60)
    print("  GRAPHE DUAL Γ — CEINTURES TROPICALES")
    print("=" * 60)
    print(f"    C_P (Sheng) : {' → '.join(CEINTURE_POSITIVE)} → {CEINTURE_POSITIVE[0]}")
    print(f"    C_N (Ke)    : {' → '.join(CEINTURE_NEGATIVE)} → {CEINTURE_NEGATIVE[0]}")
    print(f"    Seuils polaires : {SEUILS_POLAIRES}")

    # Afficher les attracteurs
    print("\n" + "=" * 60)
    print("  20 ATTRACTEURS")
    print("=" * 60)
    for sig, info in SIGNATURES_POLARITE.items():
        print(f"\n    Signature {sig} ({info['count']} attracteurs) :")
        for att in info['attracteurs']:
            triplet = ATTRACTEURS[att]
            print(f"      {att} : {sorted(triplet)}")

    # Construire les 144 pentades
    print("\n" + "=" * 60)
    print("  CONSTRUCTION DES 144 PENTADES")
    print("=" * 60)
    pentads = build_144_pentads()
    print(f"    Nombre total : {len(pentads)}")

    # Afficher quelques exemples
    print(f"\n    Exemples :")
    for key in ['P1_e1', 'P1_f1', 'N5_e3', 'N5_f3', 'P6_e5', 'N6_f5']:
        p = pentads[key]
        sign = '+' if p['polarity'] > 0 else '-'
        print(f"      {key:8s} → ({sign}) [{p['secteur']:5s}] "
              f"{p['nom']} × {p['nom_feuillet']}")

    # Répartition par secteur
    print("\n" + "=" * 60)
    print("  RÉPARTITION PAR SECTEUR")
    print("=" * 60)
    by_sector = build_144_pentads_by_sector()
    print(f"    Sheng : {len(by_sector['Sheng'])} pentades")
    print(f"    Ke    : {len(by_sector['Ke'])} pentades")
    print(f"    Total : {len(by_sector['Sheng']) + len(by_sector['Ke'])}")

    # Validation
    print_validation_report()
