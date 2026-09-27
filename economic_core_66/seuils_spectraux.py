# -*- coding: utf-8 -*-
"""
seuils_spectraux.py — Gestion des 7 seuils spectraux.

Ce module gère les 7 seuils spectraux du modèle Cl(6,6) et leur
franchissement.

Sources :
    - Article AHRN, Chapitre 13, §13.3 (valeurs des seuils)
    - Article 144 pentades, §8.2.1 (rôles des seuils)
    - Article 144 pentades, §8.2.2 (correspondance polarité)

Structure :
    - 7 seuils S_1..S_7
    - 4 stades de polarité (3P, 2P+1N, 1P+2N, 3N)
    - Règles de franchissement

Note :
    La méthode GestionnaireSeuils.cross_all_possible(tension) franchit
    UN SEUL seuil à la fois (le prochain non franchi), conformément à
    la séquence 3P → 2P+1N → 1P+2N → 3N.

Usage :
    from seuils_spectraux import (
        SEUILS_SPECTRAUX, ROLES_SEUILS,
        can_cross_threshold, get_seuils_for_polarity
    )
    
    # Vérifier si un seuil peut être franchi
    if can_cross_threshold(tension=0.18, seuil=5):
        print("Seuil S5 franchi")
"""

from typing import Dict, List, Any, Optional


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
# CORRESPONDANCE POLARITÉ ↔ SEUILS
# Source : Article 144 pentades, §8.2.2
# ============================================================

CORRESPONDANCE_POLARITE: Dict[str, Dict[str, Any]] = {
    '3P': {
        'condition': 'T < S1',
        'seuils': [],
        'description': 'Sheng pur — aucun seuil franchi',
    },
    '2P+1N': {
        'condition': 'S1 <= T < S5',
        'seuils': [1, 2, 3, 4],
        'description': 'Mélange faible — seuils S1 à S4',
    },
    '1P+2N': {
        'condition': 'S5 <= T < S7',
        'seuils': [5, 6],
        'description': 'Mélange fort — seuils S5 et S6',
    },
    '3N': {
        'condition': 'T >= S7',
        'seuils': [7],
        'description': 'Ke pur — saut d\'octave S7',
    },
}


# ============================================================
# FONCTIONS DE FRANCHISSEMENT
# ============================================================

def can_cross_threshold(tension: float, seuil: int) -> bool:
    """
    Vérifie si un seuil peut être franchi.

    La condition est : T >= S_seuil

    Args:
        tension: valeur de la tension topologique T
        seuil: numéro du seuil (1 à 7)

    Returns:
        True si le seuil peut être franchi

    Raises:
        ValueError: si le seuil n'est pas dans {1..7}
    """
    if seuil not in SEUILS_SPECTRAUX:
        raise ValueError(
            f"Seuil invalide : {seuil}. Valeurs valides : 1 à 7"
        )

    return tension >= SEUILS_SPECTRAUX[seuil]


def try_cross_threshold(tension: float, seuil: int) -> bool:
    """
    Tente de franchir un seuil.

    Args:
        tension: valeur de la tension topologique T
        seuil: numéro du seuil (1 à 7)

    Returns:
        True si le seuil est franchi
    """
    return can_cross_threshold(tension, seuil)


def get_next_threshold(tension: float) -> Optional[int]:
    """
    Retourne le prochain seuil franchissable.

    Args:
        tension: valeur de la tension topologique T

    Returns:
        Numéro du prochain seuil, ou None si tous sont franchis
    """
    for seuil in sorted(SEUILS_SPECTRAUX.keys()):
        if not can_cross_threshold(tension, seuil):
            return seuil
    return None


def get_crossed_thresholds(tension: float) -> List[int]:
    """
    Retourne la liste des seuils franchis.

    Args:
        tension: valeur de la tension topologique T

    Returns:
        Liste des seuils franchis
    """
    return [
        seuil for seuil in sorted(SEUILS_SPECTRAUX.keys())
        if can_cross_threshold(tension, seuil)
    ]


def get_polarity_from_tension(tension: float) -> str:
    """
    Retourne la polarité correspondant à une tension.

    Args:
        tension: valeur de la tension topologique T

    Returns:
        Polarité : '3P', '2P+1N', '1P+2N' ou '3N'
    """
    if tension < SEUILS_SPECTRAUX[1]:
        return '3P'
    elif tension < SEUILS_SPECTRAUX[5]:
        return '2P+1N'
    elif tension < SEUILS_SPECTRAUX[7]:
        return '1P+2N'
    else:
        return '3N'


def get_seuils_for_polarity(polarity: str) -> List[int]:
    """
    Retourne les seuils associés à une polarité.

    Args:
        polarity: '3P', '2P+1N', '1P+2N' ou '3N'

    Returns:
        Liste des seuils associés
    """
    if polarity not in CORRESPONDANCE_POLARITE:
        raise ValueError(
            f"Polarité inconnue : {polarity}. "
            f"Valeurs valides : {list(CORRESPONDANCE_POLARITE.keys())}"
        )
    return CORRESPONDANCE_POLARITE[polarity]['seuils']


# ============================================================
# CLASSE DE GESTION DES SEUILS
# ============================================================

class GestionnaireSeuils:
    """
    Gestionnaire des 7 seuils spectraux.

    Suit l'état de franchissement des seuils et fournit
    des méthodes pour les manipuler.
    """

    def __init__(self):
        self.crossed: Dict[int, bool] = {
            i: False for i in SEUILS_SPECTRAUX
        }
        self.crossing_history: List[Dict[str, Any]] = []

    def try_cross(self, tension: float, seuil: int) -> bool:
        """
        Tente de franchir un seuil.

        Args:
            tension: valeur de la tension topologique T
            seuil: numéro du seuil

        Returns:
            True si le seuil est franchi (ou déjà franchi)
        """
        if self.crossed.get(seuil, False):
            return True  # Déjà franchi

        if can_cross_threshold(tension, seuil):
            self.crossed[seuil] = True
            self.crossing_history.append({
                'seuil': seuil,
                'valeur': SEUILS_SPECTRAUX[seuil],
                'tension': tension,
                'franchi': True,
            })
            return True

        return False

    def cross_all_possible(self, tension: float) -> List[int]:
        """
        Franchit UN seul seuil (le prochain non franchi).

        Args:
            tension: valeur de la tension topologique T

        Returns:
            Liste des seuils nouvellement franchis (au plus 1)
        """
        newly_crossed = []
        for seuil in sorted(SEUILS_SPECTRAUX.keys()):
            if not self.crossed[seuil]:
                if can_cross_threshold(tension, seuil):
                    self.crossed[seuil] = True
                    newly_crossed.append(seuil)
                    self.crossing_history.append({
                        'seuil': seuil,
                        'valeur': SEUILS_SPECTRAUX[seuil],
                        'tension': tension,
                        'franchi': True,
                    })
                    # Sortir après le premier seuil franchi
                    break
        return newly_crossed

    def get_crossed(self) -> List[int]:
        """Retourne la liste des seuils franchis."""
        return [s for s, c in self.crossed.items() if c]

    def get_pending(self) -> List[int]:
        """Retourne la liste des seuils non franchis."""
        return [s for s, c in self.crossed.items() if not c]

    def get_current_polarity(self) -> str:
        """Retourne la polarité actuelle selon les seuils franchis."""
        crossed = self.get_crossed()
        if 7 in crossed:
            return '3N'
        elif 5 in crossed or 6 in crossed:
            return '1P+2N'
        elif any(s in crossed for s in [1, 2, 3, 4]):
            return '2P+1N'
        else:
            return '3P'

    def reset(self) -> None:
        """Réinitialise l'état des seuils."""
        self.crossed = {i: False for i in SEUILS_SPECTRAUX}
        self.crossing_history = []

    def get_summary(self) -> Dict[str, Any]:
        """Retourne un résumé de l'état des seuils."""
        return {
            'crossed': self.get_crossed(),
            'pending': self.get_pending(),
            'polarity': self.get_current_polarity(),
            'n_crossed': len(self.get_crossed()),
            'n_total': 7,
        }

    def print_status(self) -> None:
        """Affiche l'état des seuils."""
        print("\n" + "=" * 60)
        print("  ÉTAT DES 7 SEUILS SPECTRAUX")
        print("=" * 60)

        for seuil in sorted(SEUILS_SPECTRAUX.keys()):
            status = "✓ franchi" if self.crossed[seuil] else "✗ non franchi"
            print(f"    S{seuil} = {SEUILS_SPECTRAUX[seuil]:.9f}  "
                  f"— {ROLES_SEUILS[seuil]:30s} {status}")

        print(f"\n  Polarité actuelle : {self.get_current_polarity()}")
        print(f"  Seuils franchis   : {self.get_crossed()}")
        print(f"  Seuils en attente : {self.get_pending()}")
        print("=" * 60)


# ============================================================
# VALIDATION
# ============================================================

def validate_seuils() -> Dict[str, Any]:
    """Valide la structure des seuils spectraux."""
    results = {
        'n_seuils': len(SEUILS_SPECTRAUX),
        'n_seuils_ok': len(SEUILS_SPECTRAUX) == 7,
        'ordered': all(
            SEUILS_SPECTRAUX[i] < SEUILS_SPECTRAUX[i+1]
            for i in range(1, 7)
        ),
    }

    # Test can_cross_threshold
    try:
        # T = 0.0 → aucun seuil
        assert not can_cross_threshold(0.0, 1)
        # T = 0.07 → S1 franchi
        assert can_cross_threshold(0.07, 1)
        assert not can_cross_threshold(0.07, 2)
        # T = 0.18 → S5 franchi
        assert can_cross_threshold(0.18, 5)
        assert not can_cross_threshold(0.18, 6)
        # T = 0.22 → tous franchis
        assert can_cross_threshold(0.22, 7)
        results['can_cross_ok'] = True
    except AssertionError:
        results['can_cross_ok'] = False

    # Test get_polarity
    try:
        assert get_polarity_from_tension(0.0) == '3P'
        assert get_polarity_from_tension(0.10) == '2P+1N'
        assert get_polarity_from_tension(0.18) == '1P+2N'
        assert get_polarity_from_tension(0.22) == '3N'
        results['polarity_ok'] = True
    except AssertionError:
        results['polarity_ok'] = False

    # Test 4 : GestionnaireSeuils
    try:
        g = GestionnaireSeuils()
        g.try_cross(0.07, 1)
        assert 1 in g.get_crossed()
        assert 2 in g.get_pending()

        # Franchir les 6 seuils restants un par un
        for s in range(2, 8):
            g.try_cross(0.22, s)
        assert len(g.get_crossed()) == 7
        assert g.get_current_polarity() == '3N'
        results['gestionnaire_ok'] = True
    except AssertionError:
        results['gestionnaire_ok'] = False
        
    # Test 5 : can_cross_threshold
    try:
        assert can_cross_threshold(0.22, 7)
        assert not can_cross_threshold(0.05, 7)
        results['can_cross_ok'] = True
    except (AssertionError, ImportError):
        results['can_cross_ok'] = False

    # Calcul de all_ok : tous les tests doivent passer
    results['all_ok'] = all(
        v for k, v in results.items() if k != 'all_ok'
    )

    return results


def print_validation_report() -> None:
    """Affiche un rapport de validation."""
    print("=" * 60)
    print("  VALIDATION DES SEUILS SPECTRAUX")
    print("=" * 60)

    results = validate_seuils()

    print(f"\n  Nombre de seuils : {results['n_seuils']}/7")
    print(f"  Ordonnés         : {'✓' if results['ordered'] else '✗'}")
    print(f"  can_cross        : {'✓' if results['can_cross_ok'] else '✗'}")
    print(f"  Polarité         : {'✓' if results['polarity_ok'] else '✗'}")
    print(f"  Gestionnaire     : {'✓' if results['gestionnaire_ok'] else '✗'}")

    print(f"\n  RÉSULTAT GLOBAL : "
          f"{'✓ TOUS LES TESTS PASSENT' if results['all_ok'] else '✗ ÉCHEC'}")
    print("=" * 60)


# ============================================================
# POINT D'ENTRÉE
# ============================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  LES 7 SEUILS SPECTRAUX")
    print("=" * 60)
    for seuil, valeur in SEUILS_SPECTRAUX.items():
        print(f"    S{seuil} = {valeur:.9f}  — {ROLES_SEUILS[seuil]}")

    print("\n" + "=" * 60)
    print("  CORRESPONDANCE POLARITÉ ↔ SEUILS")
    print("=" * 60)
    for pol, info in CORRESPONDANCE_POLARITE.items():
        print(f"    {pol:8s} : {info['condition']:20s} "
              f"→ seuils {info['seuils']}")

    # Démonstration du gestionnaire
    print("\n" + "=" * 60)
    print("  DÉMONSTRATION DU GESTIONNAIRE")
    print("=" * 60)

    g = GestionnaireSeuils()

    # Simuler une progression de tension
    tensions = [0.05, 0.10, 0.15, 0.20, 0.25]
    for t in tensions:
        newly = g.cross_all_possible(t)
        print(f"\n  Tension T = {t:.3f} → nouveaux seuils franchis : {newly}")
        g.print_status()

    # Validation
    print_validation_report()
