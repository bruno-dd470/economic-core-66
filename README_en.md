> 🌐 **Languages** : 
> 🇫🇷 [Français](README.md) | 
> 🇬🇧 [English](README.en.md) | 
> 🇨🇳 [中文](README.zh.md)
> 🇷🇺 [Русский](README.ru.md)
# economic_core_66 — Autoregulated Cl(6,6) Core

**Version:** 1.0  
**Date:** September 2026  
**Author:** Bruno DE DOMINICIS  
**License:** MIT  

---

## Table of Contents
1. [Introduction](#1-introduction)
2. [Installation](#2-installation)
3. [Architecture](#3-architecture)
4. [Quick Start](#4-quick-start)
5. [Detailed Modules](#5-detailed-modules)
6. [Examples](#6-examples)
7. [Validation](#7-validation)
8. [API Reference](#8-api-reference)
9. [Limitations and Perspectives](#9-limitations-and-perspectives)
10. [References](#10-references)
- [Appendix A — Glossary](#appendix-a--glossary)
- [Appendix B — Exit Codes](#appendix-b--exit-codes)
- [Appendix C — Versions](#appendix-c--versions)

---

## 1. Introduction

### 1.1. Purpose
`economic_core_66` is an autoregulated core for an economic model based on the Clifford algebra Cl(6,6).  
It integrates:
- The **static backbone Cl(6,0)**: 20 attractors, 12 pentads, spectral observables.
- The **dynamic extension Cl(6,6)**: 144 pentads, 400 joint attractors, transition operator T.
- The **7 spectral thresholds** derived from the exceptional lattice Λ₇₂.
- The **topological tension** $T = \nabla\eta \cdot \nabla R_{seuil}$, normalized to be bounded within $[0, 1[$.

### 1.2. Theoretical Positioning
The model relies on two foundational articles:
1. **AHRN** — *A Unique Arithmetic for Three Ontologies* (June 2026)  
   Provides the 15 universal constants $\beta_k$ and the spectral formula.
2. **144 Pentads** — *WuXing and Cl(6,6)* (April 2026)  
   Provides the Cl(6,6) structure, the T operator, and the 7 thresholds.

The `economic_core_66` package is the operational implementation of these two articles for the economic domain.

### 1.3. Distinction Cl(6,0) vs Cl(6,6)
| Algebra | Signature | Role | Implementation |
| --- | --- | --- | --- |
| **Cl(6,0)** | (6,0) | Static backbone (configurations, attractors) | Integrated in `economic_core_66.py` |
| **Cl(6,6)** | (6,6) | Dynamics (transitions, thresholds) | `economic_core_66.py` |

---

## 2. Installation

### 2.1. Prerequisites
- Python ≥ 3.8
- NumPy ≥ 1.20
- SciPy ≥ 1.6
- NetworkX ≥ 2.5

### 2.2. Installing Dependencies
```bash
pip install numpy scipy networkx
```

### 2.3. File Structure
```text
economic_core_66/
├── foundations_ahrn.py           # AHRN foundations (15 β_k, 7 thresholds, formula)
├── pentads_144.py                # 144 pentads (12 base × 12 spectral sheets)
├── attractors_400.py             # 400 joint attractors (20 eco × 20 geo)
├── operateur_T.py                # Transition operator T
├── seuils_spectraux.py           # Management of the 7 spectral thresholds
├── tension_topologique.py        # Topological tension tensor T (normalized)
├── economic_core_66.py           # Main Cl(6,6) core
├── validation_66.py              # Validation tests
├── economic_core_Cl60.py         # Cl(6,0) backbone (legacy)
├── economic_core_Cl60.md         # Cl(6,0) documentation
├── CCTP-Cl66_économie_chine.md   # Specifications (CCTP)
└── README.md                     # This document
```

### 2.4. Verifying Installation
```bash
python3 validation_66.py
```
If all tests pass, the installation is correct.

---

## 3. Architecture

### 3.1. Layered View
```text
┌──────────────────────────────────────────────────────────────────────┐
│                    economic_core_66.py                               │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  LAYER 0 : FOUNDATIONS (AHRN Article)                          │  │
│  │  Module : foundations_ahrn.py                                  │  │
│  │  - BETA_K (15 values)                                          │  │
│  │  - SEUILS_SPECTRAUX (7 values)                                 │  │
│  │  - spectral_energy()                                           │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                              ↓                                       │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  LAYER 1 : STATIC BACKBONE (Cl(6,0))                           │  │
│  │  Integrated in economic_core_66.py                             │  │
│  │  - 20 attractors (A–T)                                         │  │
│  │  - 12 pentads (P₁..P₆, N₁..N₆)                                │  │
│  │  - Observables (η, d, gap, R_seuil)                            │  │
│  │  - Regulation by attractor distance                            │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                              ↓                                       │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  LAYER 2 : DYNAMIC EXTENSION (144 Pentads Article)             │  │
│  │  Modules : pentads_144.py, attractors_400.py, operateur_T.py   │  │
│  │  - 12 spectral sheets (e₁..e₆, f₁..f₆)                        │  │
│  │  - 144 pentads (12 base × 12 sheets)                           │  │
│  │  - 400 joint attractors (20 eco × 20 geo)                      │  │
│  │  - Operator T (4 components)                                   │  │
│  │  - 7 spectral thresholds                                       │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                              ↓                                       │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  LAYER 3 : VALIDATION                                          │  │
│  │  Module : validation_66.py                                     │  │
│  │  - Unit tests                                                  │  │
│  │  - Integration tests                                           │  │
│  │  - Validation on historical configurations                     │  │
│  └────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
```

### 3.2. Data Flow (China 2026)
1. **Economic Configuration (China 2026)**
2. `set_from_config()` → Attractor **S** (Stasis)
3. `core.diagnose()` → Initial Diagnostic  
   *(η = -0.333, d = 1.500, gap = 0.362, R_seuil = 0.176, Frustration = 20)*
4. `core.regulate_60(steps=15)` → Attractor **E** (Urban Expansion)
5. `core.diagnose()` → Intermediate Diagnostic  
   *(η = +0.333, d = 1.425, gap = 0.303, R_seuil = 0.294, Frustration = 23)*
6. **History Simulation (10 steps)**
7. `core.apply_T('mixed', intensity=1.0)`  
   ├── Sequential crossing of thresholds S1..S7  
   └── Transition E → D (Tempered Growth)
8. `core.diagnose()` → Final Diagnostic  
   *(η = +0.333, d = 1.450, gap = 0.215, R_seuil = 0.529, Frustration = 22)*

---

## 4. Quick Start

### 4.1. Minimal Example
```python
from economic_core_66 import EconomicCore66

# Initialization
core = EconomicCore66(noise_level=0.0, seed=42)

# China 2026 Configuration
config = {
    'P1': -1, 'P2': -1, 'P3': -1, 'P4': -1, 'P5': -1,
    'P6': +1,
    'N1': -1, 'N2': -1, 'N3': -1, 'N4': -1,
    'N5': +1, 'N6': +1,
}
attractor = core.set_from_config(config)
core.set_attractor_geo(attractor)

# Initial diagnostic
core.print_diagnostic()

# Cl(6,0) Regulation
core.regulate_60(steps=15)
core.print_diagnostic()

# History simulation (required for tension calculation)
for i in range(10):
    eta = core.eta_direct() + i * 0.02
    r = core.r_threshold() + i * 0.02
    core.eta_history.append(eta)
    core.r_threshold_history.append(r)

# Cl(6,6) Transition
result = core.apply_T('mixed', intensity=1.0)
print(f"Transition : {result['attracteur_avant']} → {result['attracteur_apres']}")
print(f"Tension : {result['tension']:.6f}")
print(f"Thresholds crossed : {result['seuils_franchis']}")

# Final diagnostic
core.print_diagnostic()

### 4.2. Expected Output
*(See the French README for the full console output example. The structure remains identical, with English labels where applicable in your code).*

---

## 5. Detailed Modules

### 5.1. `foundations_ahrn.py`
**Role:** Provides universal constants and the spectral formula.  
**Constants:** `BETA_K` (15 values), `SEUILS_SPECTRAUX` (7 values), `LAMBDA_NUC`, `LAMBDA_E`, `LAMBDA_ECO`.  
**Functions:** `spectral_energy()`, `spectral_energy_vectorized()`, `validate_foundations()`, `print_validation_report()`.

### 5.2. `pentads_144.py`
**Role:** Constructs the 144 pentads (12 base × 12 spectral sheets).  
**Constants:** `FEUILLETS`, `PENTADES_BASE`, `ATTRACTEURS`, `CEINTURE_POSITIVE`, `CEINTURE_NEGATIVE`, `SEUILS_POLAIRES`.  
**Functions:** `build_144_pentads()`, `build_144_pentads_by_sector()`, `get_pentad()`, `validate_pentads()`.

### 5.3. `attractors_400.py`
**Role:** Constructs the 400 joint attractors (20 eco × 20 geo).  
**Functions:** `build_400_attractors()`, `get_attractor_400()`, `attractor_distance_400()`, `find_nearest_attractor_400()`, `validate_attractors_400()`.

### 5.4. `operateur_T.py`
**Role:** Implements the transition operator T.  
**Class `OperateurT`:** Methods `apply_structure()`, `apply_fire()`, `apply_water()`, `apply_mixed()`, `apply()`, `_choose_best_target()`, `check_conservation()`.  
*Note:* `_choose_best_target` applies a penalty to extreme attractors (3P, 3N), favoring more stable 2P+1N attractors.

### 5.5. `seuils_spectraux.py`
**Role:** Manages the 7 spectral thresholds.  
**Constants:** `SEUILS_SPECTRAUX`, `ROLES_SEUILS`, `CORRESPONDANCE_POLARITE`.  
**Class `GestionnaireSeuils`:** Methods `try_cross()`, `cross_all_possible()`, `get_crossed()`, `get_current_polarity()`.  
*Note:* `cross_all_possible(tension)` crosses **only one** threshold at a time (the next un-crossed one), following the sequence 3P → 2P+1N → 1P+2N → 3N.

### 5.6. `tension_topologique.py`
**Role:** Calculates the topological tension $T = \nabla\eta \cdot \nabla R_{seuil}$, normalized.  
**Formula:** $T_{norm} = \frac{|\nabla\eta \cdot \nabla R_{seuil}| \cdot \alpha}{1 + |\nabla\eta \cdot \nabla R_{seuil}| \cdot \alpha}$  
**Functions:** `compute_topological_tension()`, `check_threshold_crossing()`, `validate_tension()`.  
**Class `SuiviTension`:** Tracks tension over a sliding window.

### 5.7. `economic_core_66.py`
**Role:** Main core integrating all modules.  
**Class `EconomicCore66`:** Methods `set_from_config()`, `regulate_60()`, `apply_T()`, `diagnose()`, `print_diagnostic()`, etc.

---

## 6. Examples

### 6.1. China 2026 (S → E → D)
*(See code snippet in Section 4.1)*  
**Result:** Initial Attractor: S (Stasis) → After regulation: E (Urban Expansion) → Final: D (Tempered Growth).

### 6.2. Les Trente Glorieuses (Post-WWII Boom) (D)
```python
config_trente = {
    'P1': -1, 'P2': -1, 'P3': -1, 'P4': +1, 'P5': +1, 'P6': -1,
    'N1': -1, 'N2': +1, 'N3': -1, 'N4': -1, 'N5': -1, 'N6': -1,
}
core.set_from_config(config_trente)
diag = core.diagnose()
print(f"Attractor : {diag['attractor_eco']}")  # D
```

### 6.3. Stagflation 1973 (R)
```python
config_stag = {
    'P1': -1, 'P2': -1, 'P3': +1, 'P4': -1, 'P5': -1, 'P6': -1,
    'N1': +1, 'N2': -1, 'N3': -1, 'N4': -1, 'N5': +1, 'N6': -1,
}
core.set_from_config(config_stag)
diag = core.diagnose()
print(f"Attractor : {diag['attractor_eco']}")  # R
```

### 6.4. Accessing the 144 Pentads
```python
from pentads_144 import build_144_pentads
pentads = build_144_pentads()
sheng = [p for p in pentads.values() if p['secteur'] == 'Sheng']
ke = [p for p in pentads.values() if p['secteur'] == 'Ke']
print(f"Sheng : {len(sheng)}")  # 72
print(f"Ke    : {len(ke)}")     # 72
```

---

## 7. Validation

### 7.1. Running Tests
```bash
python3 validation_66.py
```

### 7.2. Included Tests
| # | Test | Description | Status | Duration |
|---|---|---|---|---|
| 1 | `test_foundations` | AHRN Foundations | ✓ PASS | ~0.2 ms |
| 2 | `test_144_pentads` | 144 Pentads | ✓ PASS | ~0.3 ms |
| 3 | `test_400_attractors` | 400 Joint Attractors | ✓ PASS | ~5.4 ms |
| 4 | `test_operateur_T` | Operator T | ✓ PASS | ~62.2 ms |
| 5 | `test_seuils_spectraux` | 7 Spectral Thresholds | ✓ PASS | ~0.0 ms |
| 6 | `test_tension_topologique` | Topological Tension T | ✓ PASS | ~0.5 ms |
| 7 | `test_chine_2026` | China 2026 (S → E) | ✓ PASS | ~1.1 ms |
| 8 | `test_trente_glorieuses` | Trente Glorieuses (D) | ✓ PASS | ~1.5 ms |
| 9 | `test_stagflation_1973` | Stagflation 1973 (R) | ✓ PASS | ~0.8 ms |
| 10| `test_full_pipeline` | Full Pipeline | ✓ PASS | ~2.9 ms |
| **Total** | | | **10/10** | **~75 ms** |

**Global Result:** ✓ ALL TESTS PASS

---

## 8. API Reference

### `EconomicCore66`
- `__init__(noise_level=0.0, seed=None)`: Initializes the Cl(6,6) core.
- `set_attractor_eco(attractor: str)`: Sets the economic attractor (A–T).
- `set_attractor_geo(attractor: str)`: Sets the geographic attractor (A–T).
- `set_from_config(config: Dict[str, int]) -> str`: Identifies the attractor from a configuration dict `{pentad: +1 or -1}`.
- `regulate_60(steps: int = 15, target: Optional[str] = None)`: Cl(6,0) regulation by minimal attractor distance.
- `apply_T(composante: str = 'mixed', intensity: float = 1.0) -> Dict`: Applies a T operator component (`'structure'`, `'fire'`, `'water'`, `'mixed'`).
- `diagnose() -> Dict[str, Any]`: Returns a comprehensive diagnostic dictionary containing all observables (`eta`, `d`, `gap`, `r_threshold`, `frustration`, `tension`, `regime`, `severity`, `state`, etc.).
- `print_diagnostic()`: Prints the formatted diagnostic to the console.

---

## 9. Limitations and Perspectives

### 9.1. Current Limitations
- **Observable Approximations:** Some observables (`d`, `gap`) are approximated by simple formulas. A more rigorous implementation would require the complete discrete Dirac operator.
- **Pentad Naming:** Pentad and sheet names are provisional and can be refined.
- **Calibration of `Λ_eco`:** The economic scale constant remains to be calibrated on real-world data.
- **Empirical Validation:** The core has not yet been tested on real economic datasets (e.g., BNS, BPC).
- **`η_66 = 0.000`:** The Cl(6,6) spectral asymmetry currently remains null (formula to be reviewed).

### 9.2. Perspectives
- **Discrete Dirac Operator:** Implement the full Dirac operator on the 144 pentads to rigorously calculate `d` and `gap`.
- **Λ₇₂ Lattice:** Deepen the integration of Λ₇₂ lattice eigenvalues. The 15 $\beta_k$ are already extracted, but finer calibration is needed.
- **Real Data:** Connect the core to real economic data streams.
- **User Interface:** Develop a web interface for model steering.
- **Extension to Other Planes:** Extend the model to other pairs of planes (social/ecological, etc.).

---

## 10. References

### 10.1. Foundational Articles
1. **AHRN** — *A Unique Arithmetic for Three Ontologies: Matter, Life, and Information*  
   Bruno DE DOMINICIS, June 2026. DOI: (pending)
2. **144 Pentads** — *WuXing and Cl(6,6): 144 Pentads for a Unified Relational Physics*  
   Bruno DE DOMINICIS, April 2026. DOI: [10.5281/zenodo.19947629](https://doi.org/10.5281/zenodo.19947629)

### 10.2. Related Work
- Rowlands, P. (2007). *Zero to Infinity: The Foundations of Physics*. World Scientific.
- Nebe, G. (2010). *An extremal even unimodular lattice in dimension 72*. Journal of Number Theory.
- Petit, J.-P. (2024). *A bimetric cosmological model based on Andrei Sakharov's twin universe approach*. European Physical Journal C.

### 10.3. Python Libraries
- [NumPy](https://numpy.org/)
- [SciPy](https://scipy.org/)
- [NetworkX](https://networkx.org/)

---

## Appendix A — Glossary
| Term | Definition |
| --- | --- |
| **Attractor** | Stable state of the economic system (A–T) |
| **Pentad** | Base algebraic unit (P₁..P₆, N₁..N₆) |
| **Spectral Sheet** | Projection on a generator (e₁..e₆, f₁..f₆) |
| **Operator T** | Transition operator (4 components) |
| **Spectral Threshold** | Crossing milestone (S₁..S₇) |
| **Topological Tension** | $T = \nabla\eta \cdot \nabla R_{seuil}$, normalized in $[0, 1[$ |
| **$\beta_k$** | Universal constants (15 values) |

## Appendix B — Exit Codes
| Code | Meaning |
| --- | --- |
| `0` | All tests pass |
| `1` | At least one test fails |

## Appendix C — Versions
| Version | Date | Changes |
| --- | --- | --- |
| 1.0 | September 2026 | Initial version, 10/10 tests validated |
