# economic_core_66 — Noyau endorégulé Cl(6,6)

> 🌐 **Langues / Languages** : 
> 🇫🇷 [Français](README.md) | 
> 🇬🇧 [English](README.en.md) | 
> 🇨🇳 [中文](README.zh.md) | 
> 🇷🇺 [Русский](README.ru.md)

**Version :** 1.0  
**Date :** Septembre 2026  
**Auteur :** Bruno DE DOMINICIS  
**Licence :** MIT  

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
- [Annexe A — Glossaire](#annexe-a--glossaire)
- [Annexe B — Codes de sortie](#annexe-b--codes-de-sortie)
- [Annexe C — Versions](#annexe-c--versions)

---

## 1. Introduction

### 1.1. Objet
`economic_core_66` est un noyau endorégulé pour le modèle économique fondé sur l'algèbre de Clifford Cl(6,6).  
Il intègre :
- Le **socle statique Cl(6,0)** : 20 attracteurs, 12 pentades, observables spectrales.
- L'**extension dynamique Cl(6,6)** : 144 pentades, 400 attracteurs conjoints, opérateur de transition T.
- Les **7 seuils spectraux** issus du réseau exceptionnel Λ₇₂.
- La **tension topologique** $T = \nabla\eta \cdot \nabla R_{seuil}$, normalisée pour être bornée dans $[0, 1[$.

### 1.2. Positionnement théorique
Le modèle repose sur deux articles fondateurs :
1. **AHRN** — *Une arithmétique unique pour trois ontologies* (juin 2026)  
   Fournit les 15 constantes universelles $\beta_k$ et la formule spectrale.
2. **144 pentades** — *WuXing and Cl(6,6)* (avril 2026)  
   Fournit la structure Cl(6,6), l'opérateur T et les 7 seuils.

Le noyau `economic_core_66` est l'**implémentation opérationnelle** de ces deux articles pour le domaine économique.

### 1.3. Distinction Cl(6,0) vs Cl(6,6)
| Algèbre | Signature | Rôle | Implémentation |
| --- | --- | --- | --- |
| **Cl(6,0)** | (6,0) | Socle statique (configurations, attracteurs) | Intégré dans `economic_core_66.py` |
| **Cl(6,6)** | (6,6) | Dynamique (transitions, seuils) | `economic_core_66.py` |

---

## 2. Installation

### 2.1. Prérequis
- Python ≥ 3.8
- NumPy ≥ 1.20
- SciPy ≥ 1.6
- NetworkX ≥ 2.5

### 2.2. Installation des dépendances
```bash
pip install numpy scipy networkx
```

### 2.3. Structure des fichiers
```text
economic_core_66/
├── foundations_ahrn.py           # Fondations AHRN (15 β_k, 7 seuils, formule)
├── pentads_144.py                # 144 pentades (12 base × 12 feuillets)
├── attractors_400.py             # 400 attracteurs conjoints (20 éco × 20 géo)
├── operateur_T.py                # Opérateur de transition T
├── seuils_spectraux.py           # Gestion des 7 seuils
├── tension_topologique.py        # Tenseur de tension T (normalisé)
├── economic_core_66.py           # Noyau principal Cl(6,6)
├── validation_66.py              # Tests de validation
├── economic_core_Cl60.py         # Socle Cl(6,0) (legacy)
├── economic_core_Cl60.md         # Documentation Cl(6,0)
├── CCTP-Cl66_économie_chine.md   # Cahier des charges (CCTP)
└── README.md                     # Ce document
```

### 2.4. Vérification de l'installation
```bash
python3 validation_66.py
```
Si tous les tests passent, l'installation est correcte.

---

## 3. Architecture

### 3.1. Vue en couches
```text
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
│  │  - 12 feuillets spectraux (e₁..e₆, f₁..f₆)                    │  │
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
1. **Configuration économique (Chine 2026)**
2. `set_from_config()` → Attracteur **S** (Stase)
3. `core.diagnose()` → Diagnostic initial  
   *(η = -0.333, d = 1.500, gap = 0.362, R_seuil = 0.176, Frustration = 20)*
4. `core.regulate_60(steps=15)` → Attracteur **E** (Expansion urbaine)
5. `core.diagnose()` → Diagnostic intermédiaire  
   *(η = +0.333, d = 1.425, gap = 0.303, R_seuil = 0.294, Frustration = 23)*
6. **Simulation des historiques (10 pas)**
7. `core.apply_T('mixed', intensity=1.0)`  
   ├── Franchissement séquentiel des seuils S1..S7  
   └── Transition E → D (Croissance tempérée)
8. `core.diagnose()` → Diagnostic final  
   *(η = +0.333, d = 1.450, gap = 0.215, R_seuil = 0.529, Frustration = 22)*

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


### 4.2. Résultat attendu
**Attracteur initial** : S (Stase) → **Après régulation** : E (Expansion urbaine) → **Final** : D (Croissance tempérée).

---

## 5. Modules détaillés

### 5.1. `foundations_ahrn.py`
**Rôle :** Fournit les constantes universelles et la formule spectrale.  
**Constantes :** `BETA_K` (15 valeurs), `SEUILS_SPECTRAUX` (7 valeurs), `LAMBDA_NUC`, `LAMBDA_E`, `LAMBDA_ECO`.  
**Fonctions :** `spectral_energy()`, `spectral_energy_vectorized()`, `validate_foundations()`, `print_validation_report()`.

### 5.2. `pentads_144.py`
**Rôle :** Construit les 144 pentades (12 base × 12 feuillets).  
**Constantes :** `FEUILLETS`, `PENTADES_BASE`, `ATTRACTEURS`, `CEINTURE_POSITIVE`, `CEINTURE_NEGATIVE`, `SEUILS_POLAIRES`.  
**Fonctions :** `build_144_pentads()`, `build_144_pentads_by_sector()`, `get_pentad()`, `validate_pentads()`.

### 5.3. `attractors_400.py`
**Rôle :** Construit les 400 attracteurs conjoints (20 éco × 20 géo).  
**Fonctions :** `build_400_attractors()`, `get_attractor_400()`, `attractor_distance_400()`, `find_nearest_attractor_400()`, `validate_attractors_400()`.

### 5.4. `operateur_T.py`
**Rôle :** Implémente l'opérateur de transition T.  
**Classe `OperateurT` :** Méthodes `apply_structure()`, `apply_fire()`, `apply_water()`, `apply_mixed()`, `apply()`, `_choose_best_target()`, `check_conservation()`.  
*Note :* `_choose_best_target` applique une pénalité aux attracteurs extrêmes (3P, 3N), favorisant les attracteurs 2P+1N plus stables.

### 5.5. `seuils_spectraux.py`
**Rôle :** Gère les 7 seuils spectraux.  
**Constantes :** `SEUILS_SPECTRAUX`, `ROLES_SEUILS`, `CORRESPONDANCE_POLARITE`.  
**Classe `GestionnaireSeuils` :** Méthodes `try_cross()`, `cross_all_possible()`, `get_crossed()`, `get_current_polarity()`.  
*Note :* `cross_all_possible(tension)` franchit **un seul seuil à la fois** (le prochain non franchi), conformément à la séquence 3P → 2P+1N → 1P+2N → 3N.

### 5.6. `tension_topologique.py`
**Rôle :** Calcule la tension topologique $T = \nabla\eta \cdot \nabla R_{seuil}$, normalisée.  
**Formule :** $T_{norm} = \frac{|\nabla\eta \cdot \nabla R_{seuil}| \cdot \alpha}{1 + |\nabla\eta \cdot \nabla R_{seuil}| \cdot \alpha}$  
**Fonctions :** `compute_topological_tension()`, `check_threshold_crossing()`, `validate_tension()`.  
**Classe `SuiviTension` :** Suit la tension dans une fenêtre glissante.

### 5.7. `economic_core_66.py`
**Rôle :** Noyau principal intégrant tous les modules.  
**Classe `EconomicCore66` :** Méthodes `set_from_config()`, `regulate_60()`, `apply_T()`, `diagnose()`, `print_diagnostic()`, etc.

---

## 6. Exemples

### 6.1. Chine 2026 (S → E → D)
*(Voir le fragment de code de la section 4.1)*  
**Résultat :** Attracteur initial : S (Stase) → Après régulation : E (Expansion urbaine) → Final : D (Croissance tempérée).

### 6.2. Trente Glorieuses (D)
```python
config_trente = {
    'P1': -1, 'P2': -1, 'P3': -1, 'P4': +1, 'P5': +1, 'P6': -1,
    'N1': -1, 'N2': +1, 'N3': -1, 'N4': -1, 'N5': -1, 'N6': -1,
}
core.set_from_config(config_trente)
diag = core.diagnose()
print(f"Attracteur : {diag['attractor_eco']}")  # D
```

### 6.3. Stagflation 1973 (R)
```python
config_stag = {
    'P1': -1, 'P2': -1, 'P3': +1, 'P4': -1, 'P5': -1, 'P6': -1,
    'N1': +1, 'N2': -1, 'N3': -1, 'N4': -1, 'N5': +1, 'N6': -1,
}
core.set_from_config(config_stag)
diag = core.diagnose()
print(f"Attracteur : {diag['attractor_eco']}")  # R
```

### 6.4. Accès aux 144 pentades
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

### 7.1. Exécution des tests
```bash
python3 validation_66.py
```

### 7.2. Tests inclus
| # | Test | Description | Statut | Durée |
|---|---|---|---|---|
| 1 | `test_foundations` | Fondations AHRN | ✓ PASS | ~0.2 ms |
| 2 | `test_144_pentads` | 144 pentades | ✓ PASS | ~0.3 ms |
| 3 | `test_400_attractors` | 400 attracteurs conjoints | ✓ PASS | ~5.4 ms |
| 4 | `test_operateur_T` | Opérateur T | ✓ PASS | ~62.2 ms |
| 5 | `test_seuils_spectraux` | 7 seuils spectraux | ✓ PASS | ~0.0 ms |
| 6 | `test_tension_topologique` | Tension topologique T | ✓ PASS | ~0.5 ms |
| 7 | `test_chine_2026` | Chine 2026 (S → E) | ✓ PASS | ~1.1 ms |
| 8 | `test_trente_glorieuses` | Trente Glorieuses (D) | ✓ PASS | ~1.5 ms |
| 9 | `test_stagflation_1973` | Stagflation 1973 (R) | ✓ PASS | ~0.8 ms |
| 10| `test_full_pipeline` | Pipeline complet (30 pas) | ✓ PASS | ~2.9 ms |
| **Total** | | | **10/10** | **~75 ms** |

**Résultat global :** ✓ TOUS LES TESTS PASSENT

---

## 8. API Reference

### `EconomicCore66`
- `__init__(noise_level=0.0, seed=None)` : Initialise le noyau Cl(6,6).
- `set_attractor_eco(attractor: str)` : Définit l'attracteur économique (A–T).
- `set_attractor_geo(attractor: str)` : Définit l'attracteur géographique (A–T).
- `set_from_config(config: Dict[str, int]) -> str` : Identifie l'attracteur depuis un dict de configuration `{pentade: +1 ou -1}`.
- `regulate_60(steps: int = 15, target: Optional[str] = None)` : Régulation Cl(6,0) par distance minimale d'attracteur.
- `apply_T(composante: str = 'mixed', intensity: float = 1.0) -> Dict` : Applique une composante de l'opérateur T (`'structure'`, `'fire'`, `'water'`, `'mixed'`).
- `diagnose() -> Dict[str, Any]` : Retourne un dict de diagnostic complet contenant toutes les observables (`eta`, `d`, `gap`, `r_threshold`, `frustration`, `tension`, `regime`, `severity`, `state`, etc.).
- `print_diagnostic()` : Affiche le diagnostic formaté dans la console.

---

## 9. Limites et perspectives

### 9.1. Limites actuelles
- **Approximations des observables** : Certaines observables (`d`, `gap`) sont approximées par des formules simples. Une implémentation plus rigoureuse nécessiterait l'opérateur de Dirac discret complet.
- **Noms des pentades** : Les noms des pentades et feuillets sont provisoires et peuvent être affinés.
- **Calibration de `Λ_eco`** : La constante d'échelle économique reste à calibrer sur des données réelles.
- **Validation empirique** : Le noyau n'a pas encore été testé sur des données économiques réelles (BNS, BPC).
- **`η_66 = 0.000`** : L'asymétrie spectrale Cl(6,6) reste nulle (formule à revoir).

### 9.2. Perspectives
- **Opérateur de Dirac discret** : Implémenter l'opérateur de Dirac complet sur les 144 pentades pour calculer `d` et `gap` rigoureusement.
- **Réseau Λ₇₂** : Approfondir l'intégration des valeurs propres du réseau Λ₇₂. Les 15 $\beta_k$ sont déjà extraites, mais une calibration plus fine reste à faire.
- **Données réelles** : Connecter le noyau aux flux de données économiques réelles.
- **Interface utilisateur** : Développer une interface web pour le pilotage du modèle.
- **Extension à d'autres plans** : Étendre le modèle à d'autres paires de plans (social/écologique, etc.).

---

## 10. Références

### 10.1. Articles fondateurs
1. **AHRN** — *Une arithmétique unique pour trois ontologies : la matière, le vivant et l'information*  
   Bruno DE DOMINICIS, juin 2026. DOI : (en cours d'attribution)
2. **144 pentades** — *WuXing and Cl(6,6): 144 Pentads for a Unified Relational Physics*  
   Bruno DE DOMINICIS, avril 2026. DOI : [10.5281/zenodo.19947629](https://doi.org/10.5281/zenodo.19947629)

### 10.2. Travaux connexes
- Rowlands, P. (2007). *Zero to Infinity: The Foundations of Physics*. World Scientific.
- Nebe, G. (2010). *An extremal even unimodular lattice in dimension 72*. Journal of Number Theory.
- Petit, J.-P. (2024). *A bimetric cosmological model based on Andrei Sakharov's twin universe approach*. European Physical Journal C.

### 10.3. Bibliothèques Python
- [NumPy](https://numpy.org/)
- [SciPy](https://scipy.org/)
- [NetworkX](https://networkx.org/)

---

## Annexe A — Glossaire
| Terme | Définition |
| --- | --- |
| **Attracteur** | État stable du système économique (A–T) |
| **Pentade** | Unité algébrique de base (P₁..P₆, N₁..N₆) |
| **Feuillet spectral** | Projection sur un générateur (e₁..e₆, f₁..f₆) |
| **Opérateur T** | Opérateur de transition (4 composantes) |
| **Seuil spectral** | Palier de franchissement (S₁..S₇) |
| **Tension topologique** | $T = \nabla\eta \cdot \nabla R_{seuil}$, normalisée dans $[0, 1[$ |
| **β_k** | Constantes universelles (15 valeurs) |
| **Sheng** | Relation génératrice du WuXing, correspond à η > 0 |
| **Ke** | Relation de contrôle du WuXing, correspond à η < 0 |

## Annexe B — Codes de sortie
| Code | Signification |
| --- | --- |
| `0` | Tous les tests passent |
| `1` | Au moins un test échoue |

## Annexe C — Versions
| Version | Date | Changements |
| --- | --- | --- |
| 1.0 | Septembre 2026 | Version initiale, 10/10 tests validés |

---
