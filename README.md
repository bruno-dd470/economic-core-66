# README.md

---

# economic_core_66 — Noyau endorégulé Cl(6,6)

**Version** : 1.0  
**Date** : Septembre 2026  
**Auteur** : Bruno DE DOMINICIS  
**Licence** : MIT

---

## Table des matières

1. [Introduction](#1-introduction)
2. [Installation](#2-installation)
3. [Architecture](#3-architecture)
4. [Utilisation rapide](#4-utilisation-rapide)
5. [Modules détaillés](#5-modules-détaillés)
6. [Exemples](#6-exemples)
7. [Validation](#7-validation)
8. [API Reference](#8-api-reference)
9. [Limites et perspectives](#9-limites-et-perspectives)
10. [Références](#10-références)

---

## 1. Introduction

### 1.1. Objet

`economic_core_66` est un **noyau endorégulé** pour le modèle économique fondé sur l'algèbre de Clifford **Cl(6,6)**.

Ce noyau intègre :

- Le **socle statique Cl(6,0)** : 20 attracteurs, 12 pentades, observables spectrales.
- L'**extension dynamique Cl(6,6)** : 144 pentades, 400 attracteurs conjoints, opérateur de transition T.
- Les **7 seuils spectraux** issus du réseau exceptionnel Λ₇₂.
- La **tension topologique** T = ∇η · ∇R_seuil, **normalisée** pour être bornée dans [0, 1[.

### 1.2. Positionnement théorique

Le modèle repose sur **deux articles fondateurs** :

1. **AHRN** — *Une arithmétique unique pour trois ontologies* (juin 2026)  
   Fournit les 15 constantes universelles β_k et la formule spectrale.

2. **144 pentades** — *WuXing and Cl(6,6)* (avril 2026)  
   Fournit la structure Cl(6,6), l'opérateur T et les 7 seuils.

Le noyau `economic_core_66` est l'**implémentation opérationnelle** de ces deux articles pour le domaine économique.

### 1.3. Distinction Cl(6,0) vs Cl(6,6)

| Algèbre | Signature | Rôle | Implémentation |
|---|---|---|---|
| **Cl(6,0)** | (6,0) | Socle statique (configurations, attracteurs) | Intégré dans `economic_core_66.py` |
| **Cl(6,6)** | (6,6) | Dynamique (transitions, seuils) | `economic_core_66.py` |

---

## 2. Installation

### 2.1. Prérequis

- **Python** ≥ 3.8
- **NumPy** ≥ 1.20
- **SciPy** ≥ 1.6
- **NetworkX** ≥ 2.5

### 2.2. Installation des dépendances

```bash
pip install numpy scipy networkx
```

### 2.3. Structure des fichiers

```
economic_core_66/
├── foundations_ahrn.py           # Fondations AHRN (15 β_k, 7 seuils, formule)
├── pentads_144.py                # 144 pentades (12 base × 12 feuillets)
├── attractors_400.py             # 400 attracteurs conjoints (20 éco × 20 géo)
├── operateur_T.py                # Opérateur de transition T
├── seuils_spectraux.py           # Gestion des 7 seuils
├── tension_topologique.py        # Tenseur de tension T (normalisé)
├── economic_core_66.py           # Noyau principal Cl(6,6)
├── validation_66.py              # Tests de validation
├── economic_core_Cl60.py         # Socle Cl(6,0) (existant)
├── economic_core_Cl60.md         # Documentation Cl(6,0)
├── CCTP-Cl66_économie_chine.md   # Cahier des charges
└── README.md                      # Ce document
```

### 2.4. Vérification de l'installation

```bash
python3 validation_66.py
```

Si tous les tests passent, l'installation est correcte.

---

## 3. Architecture

### 3.1. Vue en couches

```
┌──────────────────────────────────────────────────────────────────────┐
│                    economic_core_66.py                               │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  COUCHE 0 : FONDATIONS (Article AHRN)                          │  │
│  │  Module : foundations_ahrn.py                                  │  │
│  │  - BETA_K (15 valeurs)                                         │  │
│  │  - SEUILS_SPECTRAUX (7 valeurs)                                │  │
│  │  - spectral_energy()                                           │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                              ↓                                       │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  COUCHE 1 : SOCLE STATIQUE (Cl(6,0))                           │  │
│  │  Intégré dans economic_core_66.py                              │  │
│  │  - 20 attracteurs (A–T)                                        │  │
│  │  - 12 pentades (P₁..P₆, N₁..N₆)                                │  │
│  │  - Observables (η, d, gap, R_seuil)                            │  │
│  │  - Régulation par distance d'attracteur                        │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                              ↓                                       │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  COUCHE 2 : EXTENSION DYNAMIQUE (Article 144 pentades)         │  │
│  │  Modules : pentads_144.py, attractors_400.py, operateur_T.py   │  │
│  │  - 12 feuillets spectraux (e₁..e₆, f₁..f₆)                     │  │
│  │  - 144 pentades (12 base × 12 feuillets)                       │  │
│  │  - 400 attracteurs conjoints (20 éco × 20 géo)                 │  │
│  │  - Opérateur T (4 composantes)                                 │  │
│  │  - 7 seuils spectraux                                          │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                              ↓                                       │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  COUCHE 3 : VALIDATION                                         │  │
│  │  Module : validation_66.py                                     │  │
│  │  - Tests unitaires                                             │  │
│  │  - Tests d'intégration                                         │  │
│  │  - Validation sur configurations historiques                   │  │
│  └────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
```

### 3.2. Flux de données (Chine 2026)

```
Configuration économique (Chine 2026)
    ↓
set_from_config() → Attracteur S (Stase)
    ↓
core.diagnose() → Diagnostic initial
    (η = -0.333, d = 1.500, gap = 0.362, R_seuil = 0.176, Frustration = 20)
    ↓
core.regulate_60(steps=15) → Attracteur E (Expansion urbaine)
    ↓
core.diagnose() → Diagnostic intermédiaire
    (η = +0.333, d = 1.425, gap = 0.303, R_seuil = 0.294, Frustration = 23)
    ↓
Simulation des historiques (10 pas)
    ↓
core.apply_T('mixed', intensity=1.0)
    ├── Franchissement séquentiel des seuils S1..S7
    └── Transition E → D (Croissance tempérée)
    ↓
core.diagnose() → Diagnostic final
    (η = +0.333, d = 1.450, gap = 0.215, R_seuil = 0.529, Frustration = 22)
```

---

## 4. Utilisation rapide

### 4.1. Exemple minimal

```python
from economic_core_66 import EconomicCore66

# Initialisation
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
core.print_diagnostic()

# Régulation Cl(6,0)
core.regulate_60(steps=15)
core.print_diagnostic()

# Simulation des historiques (nécessaire pour la tension)
for i in range(10):
    eta = core.eta_direct() + i * 0.02
    r = core.r_threshold() + i * 0.02
    core.eta_history.append(eta)
    core.r_threshold_history.append(r)

# Transition Cl(6,6)
result = core.apply_T('mixed', intensity=1.0)
print(f"Transition : {result['attracteur_avant']} → {result['attracteur_apres']}")
print(f"Tension : {result['tension']:.6f}")
print(f"Seuils franchis : {result['seuils_franchis']}")

# Diagnostic final
core.print_diagnostic()
```

### 4.2. Sortie attendue

```
============================================================
  DIAGNOSTIC Cl(6,6)
============================================================

  Attracteur conjoint : S_S
    Éco : S — Stase
          (1P+2N)
    Géo : S — Stase
          (1P+2N)
    Stabilité : 0.50

  Observables Cl(6,0) :
    η        = -0.333
    d        = 1.500
    gap      = 0.362
    R_seuil  = 0.176
    Frustration = 20

  Observables Cl(6,6) :
    η_66     = +0.000
    d_66     = 1.500
    gap_66   = 0.362
    R_66     = 0.176

  Tension topologique : 0.000000

  Seuils franchis : []
  Polarité spectrale : 3P
  Régime : Ke
  État : TRANSITION (modéré)
============================================================

  >>> Régulation Cl(6,0) <<<

============================================================
  DIAGNOSTIC Cl(6,6)
============================================================

  Attracteur conjoint : E_S
    Éco : E — Expansion urbaine
          (2P+1N)
    Géo : S — Stase
          (1P+2N)
    Stabilité : 0.50

  Observables Cl(6,0) :
    η        = +0.333
    d        = 1.425
    gap      = 0.303
    R_seuil  = 0.294
    Frustration = 23

  Observables Cl(6,6) :
    η_66     = -0.000
    d_66     = 1.425
    gap_66   = 0.303
    R_66     = 0.294

  Tension topologique : 0.000000

  Seuils franchis : []
  Polarité spectrale : 3P
  Régime : Sheng
  État : TRANSITION (modéré)
============================================================

  >>> Simulation des historiques <<<

    Pas 0: η = +0.333, R = 0.294, T = 0.000000
    Pas 1: η = +0.353, R = 0.314, T = 0.038462
    Pas 2: η = +0.373, R = 0.334, T = 0.056604
    ...
    Pas 9: η = +0.513, R = 0.474, T = 0.166667

  >>> Transition Cl(6,6) : T_mixed <<<

  Transition : E → D
  Tension : 0.677419
  Seuils franchis : [1, 2, 3, 4, 5, 6, 7]

============================================================
  DIAGNOSTIC Cl(6,6)
============================================================

  Attracteur conjoint : D_S
    Éco : D — Croissance tempérée
          (2P+1N)
    Géo : S — Stase
          (1P+2N)
    Stabilité : 0.50

  Observables Cl(6,0) :
    η        = +0.333
    d        = 1.450
    gap      = 0.215
    R_seuil  = 0.529
    Frustration = 22

  Observables Cl(6,6) :
    η_66     = -0.000
    d_66     = 1.450
    gap_66   = 0.215
    R_66     = 0.529

  Tension topologique : 0.677419

  Seuils franchis : [1, 2, 3, 4, 5, 6, 7]
  Polarité spectrale : 3N
  Régime : Sheng
  État : TRANSITION (modéré)
============================================================
```

---

## 5. Modules détaillés

### 5.1. `foundations_ahrn.py`

**Rôle** : Fournit les constantes universelles et la formule spectrale.

**Constantes** :

| Élément | Type | Description |
|---|---|---|
| `BETA_K` | `np.array(15)` | Les 15 constantes universelles β_k |
| `SEUILS_SPECTRAUX` | `dict` | Les 7 seuils S₁..S₇ |
| `LAMBDA_NUC` | `float` | Constante nucléaire (7.726 MeV) |
| `LAMBDA_E` | `float` | Constante électronique (5.950 eV) |
| `LAMBDA_ECO` | `float` | Constante économique (à calibrer) |

**Fonctions** :

| Fonction | Signature |
|---|---|
| `spectral_energy()` | `(epsilon, m, Lambda) -> float` |
| `spectral_energy_vectorized()` | `(epsilon_matrix, m, Lambda) -> np.ndarray` |
| `validate_foundations()` | `() -> Dict` |
| `print_validation_report()` | `() -> None` |

**Exemple** :

```python
from foundations_ahrn import spectral_energy

# Calcul d'une énergie spectrale
eps = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
E = spectral_energy(eps, m=0, Lambda=7.726)
print(f"E = {E:.6f} MeV")  # E = 0.510957 MeV
```

### 5.2. `pentads_144.py`

**Rôle** : Construit les 144 pentades (12 base × 12 feuillets).

**Constantes** :

| Élément | Type | Description |
|---|---|---|
| `FEUILLETS` | `dict` | Les 12 feuillets spectraux |
| `PENTADES_BASE` | `dict` | Les 12 pentades de base |
| `ATTRACTEURS` | `dict` | Les 20 attracteurs (A–T) |
| `CEINTURE_POSITIVE` | `list` | Ceinture C_P |
| `CEINTURE_NEGATIVE` | `list` | Ceinture C_N |
| `SEUILS_POLAIRES` | `list` | Seuils P₄, N₄ |

**Fonctions** :

| Fonction | Signature |
|---|---|
| `build_144_pentads()` | `() -> Dict` |
| `build_144_pentads_by_sector()` | `() -> Dict` |
| `get_pentad()` | `(base, feuillet) -> Dict` |
| `validate_pentads()` | `() -> Dict` |
| `print_validation_report()` | `() -> None` |

**Exemple** :

```python
from pentads_144 import build_144_pentads

pentads = build_144_pentads()
print(f"Nombre de pentades : {len(pentads)}")  # 144

# Accès à une pentade
p = pentads['P1_e1']
print(f"P1_e1 : {p['nom']} × {p['nom_feuillet']}")  # Keynésianisme × Inflation
```

### 5.3. `attractors_400.py`

**Rôle** : Construit les 400 attracteurs conjoints (20 éco × 20 géo).

**Fonctions** :

| Fonction | Signature |
|---|---|
| `build_400_attractors()` | `() -> Dict` |
| `build_400_attractors_by_polarity()` | `() -> Dict` |
| `get_attractor_400()` | `(key) -> Dict` |
| `get_attractors_for_eco()` | `(eco) -> Dict` |
| `get_attractors_for_geo()` | `(geo) -> Dict` |
| `attractor_distance_400()` | `(key1, key2) -> int` |
| `find_nearest_attractor_400()` | `(key, candidates) -> Tuple` |
| `validate_attractors_400()` | `() -> Dict` |
| `print_validation_report()` | `() -> None` |

**Exemple** :

```python
from attractors_400 import build_400_attractors, get_attractor_400

attractors = build_400_attractors()
print(f"Nombre d'attracteurs : {len(attractors)}")  # 400

# Attracteur Chine 2026
a = get_attractor_400('S_S')
print(f"S_S : {a['name_combined']}")  # Stase / Stase
```

### 5.4. `operateur_T.py`

**Rôle** : Implémente l'opérateur de transition T.

**Classes** :

| Classe | Méthode | Signature |
|---|---|---|
| `OperateurT` | `__init__()` | `(core_66)` |
| | `apply_structure()` | `(intensity=1.0) -> Dict` |
| | `apply_fire()` | `(intensity=1.0) -> Dict` |
| | `apply_water()` | `(intensity=1.0) -> Dict` |
| | `apply_mixed()` | `(intensity=1.0) -> Dict` |
| | `apply()` | `(composante, intensity=1.0) -> Dict` |
| | `_get_targets()` | `(composante) -> List` |
| | `_choose_best_target()` | `(targets, intensity=1.0) -> Optional[str]` |
| | `check_conservation()` | `(transition) -> Dict` |
| | `get_history()` | `() -> List` |
| | `get_summary()` | `() -> Dict` |
| | `print_history()` | `() -> None` |

**Note** : `_choose_best_target` utilise une **pénalité** pour les attracteurs extrêmes (3P, 3N), ce qui favorise les attracteurs 2P+1N (plus stables).

**Exemple** :

```python
from operateur_T import OperateurT

T = OperateurT(core)

# T.apply() ne transitionne que si le seuil associé est franchi
result = T.apply('mixed', intensity=1.0)

if result['transition']:
    print(f"Transition : {result['attracteur_avant']} → {result['attracteur_apres']}")
else:
    print(f"Pas de transition (seuil S{result['seuil_associe']} non franchi)")
```

### 5.5. `seuils_spectraux.py`

**Rôle** : Gère les 7 seuils spectraux.

**Constantes** :

| Élément | Type | Description |
|---|---|---|
| `SEUILS_SPECTRAUX` | `dict` | Les 7 seuils |
| `ROLES_SEUILS` | `dict` | Rôles des seuils |
| `CORRESPONDANCE_POLARITE` | `dict` | Correspondance 3P→3N |

**Fonctions** :

| Fonction | Signature |
|---|---|
| `can_cross_threshold()` | `(tension, seuil) -> bool` |
| `try_cross_threshold()` | `(tension, seuil) -> bool` |
| `get_next_threshold()` | `(tension) -> Optional[int]` |
| `get_crossed_thresholds()` | `(tension) -> List[int]` |
| `get_polarity_from_tension()` | `(tension) -> str` |
| `get_seuils_for_polarity()` | `(polarity) -> List[int]` |

**Classe `GestionnaireSeuils`** :

| Méthode | Signature |
|---|---|
| `__init__()` | `()` |
| `try_cross()` | `(tension, seuil) -> bool` |
| `cross_all_possible()` | `(tension) -> List[int]` |
| `get_crossed()` | `() -> List[int]` |
| `get_pending()` | `() -> List[int]` |
| `get_current_polarity()` | `() -> str` |
| `reset()` | `() -> None` |
| `get_summary()` | `() -> Dict` |
| `print_status()` | `() -> None` |

**Note importante** : `cross_all_possible(tension)` franchit **un seul seuil** à la fois (le prochain non franchi), conformément à la séquence 3P → 2P+1N → 1P+2N → 3N.

**Exemple** :

```python
from seuils_spectraux import can_cross_threshold, GestionnaireSeuils

# Vérifier un seuil individuellement
if can_cross_threshold(tension=0.18, seuil=5):
    print("Seuil S5 franchi")

# Franchir les seuils SÉQUENTIELLEMENT
g = GestionnaireSeuils()
for tension in [0.10, 0.22]:
    newly = g.cross_all_possible(tension)
    print(f"T = {tension} → seuils nouvellement franchis : {newly}")
    print(f"  Seuils cumulés : {g.get_crossed()}")
    print(f"  Polarité : {g.get_current_polarity()}")
```

### 5.6. `tension_topologique.py`

**Rôle** : Calcule la tension topologique T = ∇η · ∇R_seuil, **normalisée**.

**Formule** :

```
T_brute = |∇η · ∇R_seuil| · alpha
T_norm = T_brute / (1 + T_brute)
```

La normalisation borne T dans [0, 1[.

**Fonctions** :

| Fonction | Signature |
|---|---|
| `compute_topological_tension()` | `(eta_history, r_history, window=10, alpha=50.0) -> float` |
| `compute_tension_from_core()` | `(core, window=10) -> float` |
| `check_threshold_crossing()` | `(tension, seuil, seuils_spectraux=None) -> bool` |
| `validate_tension()` | `() -> Dict` |
| `print_validation_report()` | `() -> None` |

**Classe `SuiviTension`** :

| Méthode | Signature |
|---|---|
| `__init__()` | `(window=10)` |
| `update()` | `(eta, r_threshold) -> float` |
| `current_tension()` | `() -> float` |
| `max_tension()` | `() -> float` |
| `mean_tension()` | `() -> float` |
| `get_summary()` | `() -> Dict` |
| `reset()` | `() -> None` |
| `print_status()` | `() -> None` |

**Exemple** :

```python
from tension_topologique import compute_topological_tension

# Note : la tension est normalisée (bornée à [0, 1[)
eta_history = [-0.3, -0.32, -0.34, -0.36, -0.38]
r_history = [0.3, 0.32, 0.34, 0.36, 0.38]

tension = compute_topological_tension(eta_history, r_history)
print(f"Tension T = {tension:.6f}")  # T < 1
```

### 5.7. `economic_core_66.py`

**Rôle** : Noyau principal intégrant tous les modules.

**Classe `EconomicCore66`** :

| Méthode | Signature |
|---|---|
| `__init__()` | `(noise_level=0.0, seed=None)` |
| `set_attractor_eco()` | `(attractor) -> None` |
| `set_attractor_geo()` | `(attractor) -> None` |
| `set_attractor_400()` | `(key) -> None` |
| `set_from_config()` | `(config) -> str` |
| `eta_direct()` | `() -> float` |
| `eta_66()` | `() -> float` |
| `d_66()` | `() -> float` |
| `gap_66()` | `() -> float` |
| `r_threshold_66()` | `() -> float` |
| `topological_tension()` | `() -> float` |
| `attractor_distance()` | `(a1, a2) -> int` |
| `attractor_stability()` | `(attractor) -> float` |
| `regulate_60()` | `(steps=15, target=None) -> None` |
| `apply_T()` | `(composante='mixed', intensity=1.0) -> Dict` |
| `try_cross_threshold()` | `(seuil) -> bool` |
| `regulate_and_apply_T()` | `(steps_60=15, composante_T='mixed', intensity_T=1.0) -> Dict` |
| `get_regime()` | `() -> str` |
| `diagnose()` | `() -> Dict` |
| `get_history()` | `() -> List` |
| `get_full_history()` | `() -> Dict` |
| `reset()` | `() -> None` |
| `print_diagnostic()` | `() -> None` |

**Propriété** :

| Propriété | Type | Description |
|---|---|---|
| `current_attractor` | `str` | Attracteur économique courant (compatibilité operateur_T) |

---

## 6. Exemples

### 6.1. Chine 2026 (S → E → D)

```python
from economic_core_66 import EconomicCore66

core = EconomicCore66(noise_level=0.0, seed=42)

config_chine = {
    'P1': -1, 'P2': -1, 'P3': -1, 'P4': -1, 'P5': -1,
    'P6': +1,
    'N1': -1, 'N2': -1, 'N3': -1, 'N4': -1,
    'N5': +1, 'N6': +1,
}

core.set_from_config(config_chine)
core.set_attractor_geo('S')

# Régulation Cl(6,0)
core.regulate_60(steps=15)

# Simulation des historiques
for i in range(10):
    eta = core.eta_direct() + i * 0.02
    r = core.r_threshold() + i * 0.02
    core.eta_history.append(eta)
    core.r_threshold_history.append(r)

# Transition Cl(6,6)
result = core.apply_T('mixed', intensity=1.0)

# Diagnostic
core.print_diagnostic()
```

**Résultat** :
- Attracteur initial : S (Stase)
- Attracteur après régulation : E (Expansion urbaine)
- Attracteur final : D (Croissance tempérée)

### 6.2. Trente Glorieuses (D)

```python
config_trente = {
    'P1': -1, 'P2': -1, 'P3': -1, 'P4': +1, 'P5': +1,
    'P6': -1,
    'N1': -1, 'N2': +1, 'N3': -1, 'N4': -1,
    'N5': -1, 'N6': -1,
}

core.set_from_config(config_trente)
diag = core.diagnose()
print(f"Attracteur : {diag['attractor_eco']}")  # D
```

### 6.3. Stagflation 1973 (R)

```python
config_stag = {
    'P1': -1, 'P2': -1, 'P3': +1, 'P4': -1, 'P5': -1,
    'P6': -1,
    'N1': +1, 'N2': -1, 'N3': -1, 'N4': -1,
    'N5': +1, 'N6': -1,
}

core.set_from_config(config_stag)
diag = core.diagnose()
print(f"Attracteur : {diag['attractor_eco']}")  # R
```

### 6.4. Accès aux 144 pentades

```python
from pentads_144 import build_144_pentads

pentads = build_144_pentads()

# Filtrer par secteur
sheng = [p for p in pentads.values() if p['secteur'] == 'Sheng']
ke = [p for p in pentads.values() if p['secteur'] == 'Ke']

print(f"Sheng : {len(sheng)}")  # 72
print(f"Ke : {len(ke)}")        # 72
```

### 6.5. Utilisation des seuils (franchissement séquentiel)

```python
from seuils_spectraux import GestionnaireSeuils

g = GestionnaireSeuils()

# Franchir les seuils UN PAR UN
newly = g.cross_all_possible(tension=0.10)
print(f"Seuils nouvellement franchis : {newly}")  # [1]
print(f"Seuils cumulés : {g.get_crossed()}")      # [1]

newly = g.cross_all_possible(tension=0.22)
print(f"Seuils nouvellement franchis : {newly}")  # [2]
print(f"Seuils cumulés : {g.get_crossed()}")      # [1, 2]
print(f"Polarité : {g.get_current_polarity()}")   # 2P+1N
```

---

## 7. Validation

### 7.1. Exécution des tests

```bash
python3 validation_66.py
```

### 7.2. Tests inclus

| # | Test | Description | Statut | Durée |
|---|---|---|---|---|
| 1 | `test_foundations` | Fondations AHRN | ✓ PASS | 0.2 ms |
| 2 | `test_144_pentads` | 144 pentades | ✓ PASS | 0.3 ms |
| 3 | `test_400_attractors` | 400 attracteurs | ✓ PASS | 5.4 ms |
| 4 | `test_operateur_T` | Opérateur T | ✓ PASS | 62.2 ms |
| 5 | `test_seuils_spectraux` | 7 seuils | ✓ PASS | 0.0 ms |
| 6 | `test_tension_topologique` | Tension T | ✓ PASS | 0.5 ms |
| 7 | `test_chine_2026` | Chine 2026 (S → E) | ✓ PASS | 1.1 ms |
| 8 | `test_trente_glorieuses` | Trente Glorieuses (D) | ✓ PASS | 1.5 ms |
| 9 | `test_stagflation_1973` | Stagflation 1973 (R) | ✓ PASS | 0.8 ms |
| 10 | `test_full_pipeline` | Pipeline complet | ✓ PASS | 2.9 ms |
| **Total** | | | **10/10** | **~75 ms** |

**Résultat global** : ✓ TOUS LES TESTS PASSENT

### 7.3. Interprétation des résultats

- **Tous les tests passent** → Le noyau est fonctionnel.
- **Certains tests échouent** → Vérifier les dépendances et les versions.

---

## 8. API Reference

### 8.1. `EconomicCore66`

#### `__init__(noise_level=0.0, seed=None)`

Initialise le noyau Cl(6,6).

**Paramètres** :
- `noise_level` (float) : niveau de bruit stochastique (défaut 0.0)
- `seed` (Optional[int]) : graine aléatoire (défaut None)

**Retour** : `None`

#### `set_attractor_eco(attractor: str) -> None`

Définit l'attracteur économique.

**Paramètres** :
- `attractor` (str) : nom de l'attracteur (A–T)

#### `set_attractor_geo(attractor: str) -> None`

Définit l'attracteur géographique.

#### `set_from_config(config: Dict[str, int]) -> str`

Identifie l'attracteur depuis une configuration.

**Paramètres** :
- `config` (Dict[str, int]) : `{pentade: +1 (active) ou -1 (inactive)}`

**Retour** : nom de l'attracteur identifié (str)

#### `regulate_60(steps: int = 15, target: Optional[str] = None) -> None`

Régulation Cl(6,0) par distance minimale.

#### `apply_T(composante: str = 'mixed', intensity: float = 1.0) -> Dict[str, Any]`

Applique une composante de T.

**Paramètres** :
- `composante` (str) : `'structure'`, `'fire'`, `'water'`, `'mixed'`
- `intensity` (float) : intensité (0.0 à 1.0)

**Retour** : dict avec les résultats

#### `diagnose() -> Dict[str, Any]`

Diagnostic complet.

**Retour** : dict avec toutes les observables

Structure du dict retourné :
```python
{
    'attractor_eco': str,
    'attractor_geo': str,
    'attractor_400': str,
    'attractor_name_eco': str,
    'attractor_name_geo': str,
    'polarity_eco': str,
    'polarity_geo': str,
    'eta': float,
    'eta_66': float,
    'd': float,
    'd_66': float,
    'gap': float,
    'gap_66': float,
    'r_threshold': float,
    'r_threshold_66': float,
    'frustration': int,
    'tension': float,
    'regime': str,
    'seuils_franchis': List[int],
    'polarite_spectrale': str,
    'stability': float,
    'severity': str,
    'state': str,
}
```

#### `print_diagnostic() -> None`

Affiche le diagnostic formaté.

---

## 9. Limites et perspectives

### 9.1. Limites actuelles

0. **Dans cette première version heuristique**, Cl(6,6) est utilisé comme langage ontologique, pas comme moteur de calcul.

1. **Approximations des observables** : Certaines observables (`d`, `gap`) sont approximées par des formules simples. Une implémentation plus rigoureuse nécessiterait l'opérateur de Dirac discret complet.

2. **Noms des pentades** : Les noms des pentades et feuillets sont provisoires et peuvent être affinés.

3. **Calibration de `Λ_eco`** : La constante d'échelle économique reste à calibrer sur des données réelles.

4. **Validation empirique** : Le noyau n'a pas encore été testé sur des données économiques réelles (BNS, BPC).

5. **`η_66 = 0.000`** : L'asymétrie spectrale Cl(6,6) reste nulle (formule à revoir).

### 9.2. Perspectives

0. **Modules de calcul Clifford** : Pour une version prédictive/physique, implémenter un véritable moteur cliffordien.

1. **Opérateur de Dirac discret** : Implémenter l'opérateur de Dirac complet sur les 144 pentades pour calculer `d` et `gap` rigoureusement.

2. **Réseau Λ₇₂** : Approfondir l'intégration des valeurs propres du réseau Λ₇₂. Les 15 β_k sont déjà extraites, mais une calibration plus fine reste à faire.

3. **Données réelles** : Connecter le noyau aux données économiques réelles (BNS, BPC).

4. **Interface utilisateur** : Développer une interface web pour le pilotage.

5. **Extension à d'autres plans** : Étendre le modèle à d'autres paires de plans (social/écologique, etc.).

---

## 10. Références

### 10.1. Articles fondateurs

1. **AHRN** — *Une arithmétique unique pour trois ontologies : la matière, le vivant et l'information*  
   Bruno DE DOMINICIS, juin 2026  
   DOI : (en cours d'attribution)

2. **144 pentades** — *WuXing and Cl(6,6): 144 Pentads for a Unified Relational Physics*  
   Bruno DE DOMINICIS, avril 2026  
   DOI : [10.5281/zenodo.19947629](https://doi.org/10.5281/zenodo.19947629)

### 10.2. Travaux connexes

3. **Rowlands, P.** (2007). *Zero to Infinity: The Foundations of Physics*. World Scientific.

4. **Nebe, G.** (2010). *An extremal even unimodular lattice in dimension 72*. Journal of Number Theory.

5. **Petit, J.-P.** (2024). *A bimetric cosmological model based on Andrei Sakharov's twin universe approach*. European Physical Journal C.

### 10.3. Bibliothèques Python

- **NumPy** : https://numpy.org/
- **SciPy** : https://scipy.org/
- **NetworkX** : https://networkx.org/

---

## Annexe A — Glossaire

| Terme | Définition |
|---|---|
| **Attracteur** | État stable du système économique (A–T) |
| **Pentade** | Unité algébrique de base (P₁..P₆, N₁..N₆) |
| **Feuillet spectral** | Projection sur un générateur (e₁..e₆, f₁..f₆) |
| **Opérateur T** | Opérateur de transition (4 composantes) |
| **Seuil spectral** | Palier de franchissement (S₁..S₇) |
| **Tension topologique** | T = ∇η · ∇R_seuil, normalisée dans [0, 1[ |
| **β_k** | Constantes universelles (15 valeurs) |

---

## Annexe B — Codes de sortie

| Code | Signification |
|---|---|
| 0 | Tous les tests passent |
| 1 | Au moins un test échoue |

---

## Annexe C — Versions

| Version | Date | Changements |
|---|---|---|
| 1.0 | Septembre 2026 | Version initiale, 10/10 tests validés |

---

**Fin du README.**

