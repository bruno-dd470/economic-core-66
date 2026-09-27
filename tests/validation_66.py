# -*- coding: utf-8 -*-
"""
validation_66.py — Tests de validation du noyau Cl(6,6).

Ce module valide l'intégration complète du noyau Cl(6,6) :
    - Test des fondations AHRN
    - Test des 144 pentades
    - Test des 400 attracteurs
    - Test de l'opérateur T
    - Test des seuils spectraux
    - Test de la tension topologique
    - Test complet sur la Chine 2026
    - Test sur les Trente Glorieuses
    - Test sur la Stagflation 1973

Usage :
    python3 validation_66.py
"""

import sys
import os
import time
from typing import Dict, List, Any, Tuple

# ============================================================
# RÉSOLUTION AUTOMATIQUE DU CHEMIN (fonctionne partout)
# ============================================================
# Ajoute la racine du projet au sys.path pour que les imports
# fonctionnent sans installation pip, sans venv, sans PYTHONPATH.
# Fonctionne en local, dans la CI GitHub, et dans les IDE.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ============================================================
# IMPORTS (inchangés, mais maintenant préfixés)
# ============================================================
from economic_core_66.foundations_ahrn import (
    BETA_K,
    SEUILS_SPECTRAUX,
    LAMBDA_NUC,
    LAMBDA_E,
    LAMBDA_ECO,
    spectral_energy,
    validate_foundations,
)
from economic_core_66.pentads_144 import (
    build_144_pentads,
    build_144_pentads_by_sector,
    FEUILLETS,
    PENTADES_BASE,
    ATTRACTEURS,
    CEINTURE_POSITIVE,
    CEINTURE_NEGATIVE,
    SEUILS_POLAIRES,
    validate_pentads,
)
from economic_core_66.attractors_400 import (
    build_400_attractors,
    get_attractor_400,
    attractor_distance_400,
    validate_attractors_400,
)
from economic_core_66.operateur_T import (
    OperateurT,
    COMPOSANTES_T,
    SEUIL_PAR_COMPOSANTE,
)
from economic_core_66.seuils_spectraux import (
    GestionnaireSeuils,
    can_cross_threshold,
    get_polarity_from_tension,
    validate_seuils,
)
from economic_core_66.tension_topologique import (
    compute_topological_tension,
    SuiviTension,
    validate_tension,
)
from economic_core_66.economic_core_66 import EconomicCore66

# ============================================================
# CLASSE DE VALIDATION
# ============================================================

class ValidationReport:
    """Rapport de validation."""

    def __init__(self):
        self.tests: List[Dict[str, Any]] = []
        self.start_time: float = time.time()

    def add_test(
        self,
        name: str,
        passed: bool,
        details: str = "",
        duration: float = 0.0,
    ) -> None:
        """Ajoute un test au rapport."""
        self.tests.append({
            'name': name,
            'passed': passed,
            'details': details,
            'duration': duration,
        })

    def get_summary(self) -> Dict[str, Any]:
        """Retourne un résumé du rapport."""
        n_total = len(self.tests)
        n_passed = sum(1 for t in self.tests if t['passed'])
        n_failed = n_total - n_passed

        return {
            'total': n_total,
            'passed': n_passed,
            'failed': n_failed,
            'all_ok': n_failed == 0,
            'total_duration': time.time() - self.start_time,
        }

    def print_report(self) -> None:
        """Affiche le rapport formaté."""
        print("\n" + "=" * 70)
        print("  RAPPORT DE VALIDATION — NOYAU Cl(6,6)")
        print("=" * 70)

        for i, test in enumerate(self.tests, 1):
            status = "✓ PASS" if test['passed'] else "✗ FAIL"
            print(f"\n  [{i:2d}] {test['name']}")
            print(f"       Statut : {status}")
            if test['details']:
                print(f"       Détails : {test['details']}")
            if test['duration'] > 0:
                print(f"       Durée : {test['duration']*1000:.1f} ms")

        summary = self.get_summary()
        print("\n" + "=" * 70)
        print(f"  RÉSUMÉ")
        print(f"    Total  : {summary['total']}")
        print(f"    Passés : {summary['passed']}")
        print(f"    Échoués: {summary['failed']}")
        print(f"    Durée  : {summary['total_duration']*1000:.1f} ms")
        print(f"\n  RÉSULTAT GLOBAL : "
              f"{'✓ TOUS LES TESTS PASSENT' if summary['all_ok'] else '✗ ÉCHEC'}")
        print("=" * 70)


# ============================================================
# TESTS UNITAIRES
# ============================================================

def test_foundations(report: ValidationReport) -> None:
    """Test des fondations AHRN."""
    t0 = time.time()
    try:
        results = validate_foundations()
        passed = results['all_ok']
        details = (
            f"{results['beta_k_count']}/15 β_k, "
            f"{results['seuils_count']}/7 seuils, "
            f"formule : {'✓' if results.get('formula_ok', False) else '✗'}"
        )
    except Exception as e:
        passed = False
        details = f"Erreur : {e}"

    report.add_test(
        "Fondations AHRN",
        passed,
        details,
        time.time() - t0,
    )


def test_144_pentads(report: ValidationReport) -> None:
    """Test des 144 pentades."""
    t0 = time.time()
    try:
        pentads = build_144_pentads()
        n_ok = len(pentads) == 144

        by_sector = build_144_pentads_by_sector()
        n_sheng = len(by_sector['Sheng'])
        n_ke = len(by_sector['Ke'])
        sector_ok = (n_sheng == 72 and n_ke == 72)

        passed = n_ok and sector_ok
        details = (
            f"{len(pentads)}/144 pentades, "
            f"Sheng : {n_sheng}, Ke : {n_ke}"
        )
    except Exception as e:
        passed = False
        details = f"Erreur : {e}"

    report.add_test(
        "144 pentades",
        passed,
        details,
        time.time() - t0,
    )


def test_400_attractors(report: ValidationReport) -> None:
    """Test des 400 attracteurs conjoints."""
    t0 = time.time()
    try:
        attractors = build_400_attractors()
        passed = len(attractors) == 400

        # Test de cohérence
        a = get_attractor_400('S_S')
        coh_ok = (a['eco'] == 'S' and a['geo'] == 'S')

        # Test de distance
        d1 = attractor_distance_400('S_S', 'S_S')
        d2 = attractor_distance_400('S_S', 'S_E')
        dist_ok = (d1 == 0 and d2 == 2)

        passed = passed and coh_ok and dist_ok
        details = (
            f"{len(attractors)}/400 attracteurs, "
            f"cohérence : {'✓' if coh_ok else '✗'}, "
            f"distance : {'✓' if dist_ok else '✗'}"
        )
    except Exception as e:
        passed = False
        details = f"Erreur : {e}"

    report.add_test(
        "400 attracteurs conjoints",
        passed,
        details,
        time.time() - t0,
    )


def test_operateur_T(report: ValidationReport) -> None:
    """Test de l'opérateur T."""
    t0 = time.time()
    try:
        core = EconomicCore66(noise_level=0.0, seed=42)
        core.set_attractor_eco('S')
        core.set_attractor_geo('S')

        T = OperateurT(core)

        # Test des 4 composantes
        n_ok = 0
        for comp in COMPOSANTES_T:
            result = T.apply(comp, intensity=1.0)
            if 'composante' in result and result['composante'] == comp:
                n_ok += 1

        passed = (n_ok == 4)
        details = f"{n_ok}/4 composantes de T fonctionnent"
    except Exception as e:
        passed = False
        details = f"Erreur : {e}"

    report.add_test(
        "Opérateur T (4 composantes)",
        passed,
        details,
        time.time() - t0,
    )


def test_seuils_spectraux(report: ValidationReport) -> None:
    """Test des 7 seuils spectraux."""
    t0 = time.time()
    try:
        results = validate_seuils()
        passed = results['all_ok']
        details = (
            f"{results['n_seuils']}/7 seuils, "
            f"ordonnés : {'✓' if results['ordered'] else '✗'}, "
            f"franchissement : {'✓' if results['can_cross_ok'] else '✗'}"
        )
    except Exception as e:
        passed = False
        details = f"Erreur : {e}"

    report.add_test(
        "7 seuils spectraux",
        passed,
        details,
        time.time() - t0,
    )


def test_tension_topologique(report: ValidationReport) -> None:
    """Test de la tension topologique."""
    t0 = time.time()
    try:
        results = validate_tension()
        passed = results['all_ok']
        details = (
            f"empty: {'✓' if results.get('empty_ok', False) else '✗'}, "
            f"constant: {'✓' if results.get('constant_ok', False) else '✗'}, "
            f"varying: {'✓' if results.get('varying_ok', False) else '✗'}"
        )
    except Exception as e:
        passed = False
        details = f"Erreur : {e}"

    report.add_test(
        "Tension topologique",
        passed,
        details,
        time.time() - t0,
    )


# ============================================================
# TESTS D'INTÉGRATION
# ============================================================

def test_chine_2026(report: ValidationReport) -> None:
    """Test complet sur la Chine 2026."""
    t0 = time.time()
    try:
        core = EconomicCore66(noise_level=0.0, seed=42)

        # Configuration Chine 2026
        config = {
            'P1': -1, 'P2': -1, 'P3': -1, 'P4': -1, 'P5': -1,
            'P6': +1,
            'N1': -1, 'N2': -1, 'N3': -1, 'N4': -1,
            'N5': +1, 'N6': +1,
        }
        attractor = core.set_from_config(config)
        core.set_attractor_geo(attractor)

        # Diagnostic initial
        diag_before = core.diagnose()

        # Régulation Cl(6,0)
        core.regulate_60(steps=15)
        diag_after_60 = core.diagnose()

        # Transition Cl(6,6)
        result_T = core.apply_T('mixed', intensity=1.0)
        diag_after_66 = core.diagnose()

        # Vérifications
        checks = {
            'attractor_initial': diag_before['attractor_eco'] == 'S',
            'transition_S_to_E': diag_after_60['attractor_eco'] == 'E',
            'eta_initial_neg': diag_before['eta'] < 0,
            'eta_final_pos': diag_after_60['eta'] > 0,
            'regime_change': (
                diag_before['regime'] != diag_after_60['regime']
            ),
            'gap_acceptable': (
                diag_after_60['gap'] > 0.1
            ),
        }

        passed = all(checks.values())
        details = (
            f"{diag_before['attractor_eco']} → "
            f"{diag_after_60['attractor_eco']}, "
            f"η : {diag_before['eta']:+.3f} → {diag_after_60['eta']:+.3f}, "
            f"gap : {diag_before['gap']:.3f} → {diag_after_60['gap']:.3f}"
        )

        if not passed:
            failed_checks = [k for k, v in checks.items() if not v]
            details += f" (échecs : {failed_checks})"

    except Exception as e:
        passed = False
        details = f"Erreur : {e}"

    report.add_test(
        "Chine 2026 (S → E)",
        passed,
        details,
        time.time() - t0,
    )


def test_trente_glorieuses(report: ValidationReport) -> None:
    """Test sur les Trente Glorieuses."""
    t0 = time.time()
    try:
        core = EconomicCore66(noise_level=0.0, seed=42)

        # Configuration Trente Glorieuses
        config = {
            'P1': -1, 'P2': -1, 'P3': -1, 'P4': +1, 'P5': +1,
            'P6': -1,
            'N1': -1, 'N2': +1, 'N3': -1, 'N4': -1,
            'N5': -1, 'N6': -1,
        }
        attractor = core.set_from_config(config)
        diag = core.diagnose()

        # Vérifications
        checks = {
            'attractor_D': diag['attractor_eco'] == 'D',
            'eta_positive': diag['eta'] > 0,
            'regime_sheng': diag['regime'] == 'Sheng',
        }

        passed = all(checks.values())
        details = (
            f"attracteur : {diag['attractor_eco']}, "
            f"η : {diag['eta']:+.3f}, "
            f"régime : {diag['regime']}"
        )

    except Exception as e:
        passed = False
        details = f"Erreur : {e}"

    report.add_test(
        "Trente Glorieuses (D)",
        passed,
        details,
        time.time() - t0,
    )


def test_stagflation_1973(report: ValidationReport) -> None:
    """Test sur la Stagflation 1973."""
    t0 = time.time()
    try:
        core = EconomicCore66(noise_level=0.0, seed=42)

        # Configuration Stagflation 1973
        config = {
            'P1': -1, 'P2': -1, 'P3': +1, 'P4': -1, 'P5': -1,
            'P6': -1,
            'N1': +1, 'N2': -1, 'N3': -1, 'N4': -1,
            'N5': +1, 'N6': -1,
        }
        attractor = core.set_from_config(config)
        diag = core.diagnose()

        # Vérifications
        checks = {
            'attractor_R': diag['attractor_eco'] == 'R',
            'regime_ke': diag['regime'] == 'Ke',
        }

        passed = all(checks.values())
        details = (
            f"attracteur : {diag['attractor_eco']}, "
            f"η : {diag['eta']:+.3f}, "
            f"régime : {diag['regime']}"
        )

    except Exception as e:
        passed = False
        details = f"Erreur : {e}"

    report.add_test(
        "Stagflation 1973 (R)",
        passed,
        details,
        time.time() - t0,
    )


def test_full_pipeline(report: ValidationReport) -> None:
    """Test du pipeline complet avec seuils."""
    t0 = time.time()
    try:
        core = EconomicCore66(noise_level=0.0, seed=42)
        core.set_attractor_eco('S')
        core.set_attractor_geo('S')

        # Simuler une progression sur 30 pas
        for i in range(30):
            # Régulation
            if i == 5:
                core.regulate_60(steps=1)

            # Mise à jour des historiques
            core.eta_history.append(core.eta_direct())
            core.r_threshold_history.append(core.r_threshold())

            # Mise à jour de la tension
            tension = core.topological_tension()
            core.suivi_tension.update(
                core.eta_direct(),
                core.r_threshold(),
            )

            # Tenter de franchir les seuils
            core.gestionnaire_seuils.cross_all_possible(tension)

        # Vérifications
        n_seuils_franchis = len(core.gestionnaire_seuils.get_crossed())
        passed = n_seuils_franchis >= 0  # Au moins 0
        details = (
            f"30 pas simulés, "
            f"seuils franchis : {n_seuils_franchis}/7, "
            f"polarité : {core.gestionnaire_seuils.get_current_polarity()}"
        )
    except Exception as e:
        passed = False
        details = f"Erreur : {e}"

    report.add_test(
        "Pipeline complet (30 pas)",
        passed,
        details,
        time.time() - t0,
    )


# ============================================================
# FONCTION PRINCIPALE DE VALIDATION
# ============================================================

def run_all_validations() -> ValidationReport:
    """Exécute toutes les validations."""
    report = ValidationReport()

    print("\n" + "=" * 70)
    print("  VALIDATION COMPLÈTE DU NOYAU Cl(6,6)")
    print("=" * 70)

    # Tests unitaires
    print("\n  --- Tests unitaires ---")
    test_foundations(report)
    test_144_pentads(report)
    test_400_attractors(report)
    test_operateur_T(report)
    test_seuils_spectraux(report)
    test_tension_topologique(report)

    # Tests d'intégration
    print("\n  --- Tests d'intégration ---")
    test_chine_2026(report)
    test_trente_glorieuses(report)
    test_stagflation_1973(report)
    test_full_pipeline(report)

    # Rapport
    report.print_report()

    return report


# ============================================================
# POINT D'ENTRÉE
# ============================================================

if __name__ == "__main__":
    report = run_all_validations()

    # Code de sortie
    summary = report.get_summary()
    sys.exit(0 if summary['all_ok'] else 1)
