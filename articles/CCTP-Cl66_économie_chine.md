# Documentation du plan d'intégration — Article AHRN + Article 144 pentades → Noyau Cl(6,6)

## Document de référence : `PLAN_INTEGRATION_66.md`

---

## 1. Objet du document

Ce document spécifie le plan d'intégration des deux articles théoriques :

1. **Article AHRN** (`article_A_H_R_N_v3_FR.md`) — Fondations arithmétiques universelles
2. **Article 144 pentades** (`144_pentades9_en.md`) — Extension dynamique Cl(6,6)

dans le **noyau économique Cl(6,6)** (`economic_core_66.py`).

Il ne s'agit pas d'un document théorique, mais d'un **cahier des charges technique** destiné à guider l'implémentation.

---

## 2. Contexte et motivation

### 2.1. État actuel

Le noyau `economic_core_v6.py` implémente **Cl(6,0)** — le socle statique :

- 20 attracteurs (A–T)
- 12 pentades (P₁..P₆, N₁..N₆)
- Observables (η, d, gap, R_seuil)
- Régulation par distance d'attracteur

**Limites** :
- Pas de dynamique de transition (opérateur $T$)
- Pas de seuils spectraux (7 seuils $S_1..S_7$)
- Pas d'extension à 144 pentades
- Pas de couplage avec les constantes universelles $\beta_k$

### 2.2. Ce que les articles apportent

| Article | Apport | Section |
|---|---|---|
| **AHRN** | 15 $\beta_k$, formule spectrale, 7 seuils | Chapitres 8, 13, 18 |
| **144 pentades** | 12 feuillets, 144 pentades, opérateur $T$, 400 attracteurs | §2.3, §8.1, §10.6 |

### 2.3. Objectif

Construire `economic_core_66.py` qui :

1. **Intègre** les 15 $\beta_k$ (fondations AHRN)
2. **Étend** le noyau à 144 pentades (dynamique Cl(6,6))
3. **Implémente** l'opérateur $T$ (moteur de transition)
4. **Gère** les 7 seuils spectraux (gating)
5. **Calcule** les observables sur les 144 pentades
6. **Valide** sur la Chine 2026

---

## 3. Architecture du noyau Cl(6,6)

### 3.1. Vue en couches

```
┌──────────────────────────────────────────────────────────────────────┐
│                    economic_core_66.py                                │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  COUCHE 0 : FONDATIONS (Article AHRN)                          │  │
│  │  Module : foundations_ahrn.py                                  │  │
│  │  - BETA_K (15 valeurs)                                         │  │
│  │  - SEUILS_SPECTRAUX (7 valeurs)                                │  │
│  │  - LAMBDA_NUC, LAMBDA_E, LAMBDA_ECO                            │  │
│  │  - spectral_energy()                                           │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                              ↓                                       │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  COUCHE 1 : SOCLE STATIQUE (Cl(6,0))                           │  │
│  │  Module : economic_core_v6.py (existant) + enhancements        │  │
│  │  - 20 attracteurs (A–T)                                        │  │
│  │  - 12 pentades (P₁..P₆, N₁..N₆)                               │  │
│  │  - Observables (η, d, gap, R_seuil)                            │  │
│  │  - Régulation par distance d'attracteur                        │  │
│  │  - Tenseur de tension T_topologique                            │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                              ↓                                       │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  COUCHE 2 : EXTENSION DYNAMIQUE (Article 144 pentades)         │  │
│  │  Modules : pentads_144.py, attractors_400.py, operateur_T.py  │  │
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
│  │  - Test formule AHRN                                           │  │
│  │  - Test 144 pentades                                           │  │
│  │  - Test 400 attracteurs                                        │  │
│  │  - Test Chine 2026                                             │  │
│  └────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
```

### 3.2. Dépendances entre modules

```
foundations_ahrn.py
    ↓
pentads_144.py ← economic_core_v6.py
    ↓
attractors_400.py
    ↓
operateur_T.py
    ↓
seuils_spectraux.py ← tension_topologique.py
    ↓
economic_core_66.py
    ↓
validation_66.py
```

---

## 4. Spécifications détaillées des modules

### 4.1. Module `foundations_ahrn.py`

#### 4.1.1. Rôle

Fournir les **constantes universelles** extraites de l'article AHRN.

#### 4.1.2. Contenu

| Élément | Type | Source | Description |
|---|---|---|---|
| `BETA_K` | `np.array(15)` | AHRN Ch. 13 | Les 15 constantes $\beta_k$ |
| `SEUILS_SPECTRAUX` | `dict` | AHRN Ch. 13 + 144 pentades §8.2.1 | Les 7 seuils $S_1..S_7$ |
| `LAMBDA_NUC` | `float` | AHRN Ch. 8 | Constante d'échelle nucléaire (7.726 MeV) |
| `LAMBDA_E` | `float` | AHRN Ch. 8 | Constante d'échelle électronique (5.950 eV) |
| `LAMBDA_ECO` | `float` | À calibrer | Constante d'échelle économique |
| `spectral_energy()` | `function` | AHRN Ch. 8 | Calcule $E = \Lambda \cdot 4^m \cdot \sum \epsilon_k \beta_k$ |
| `validate_ahrn()` | `function` | AHRN Ch. 8-12 | Valide la formule sur les données |

#### 4.1.3. Interface

```python
# Constantes
BETA_K: np.ndarray  # shape (15,)
SEUILS_SPECTRAUX: Dict[int, float]  # {1: 0.06614, ..., 7: 0.21732}
LAMBDA_NUC: float = 7.726  # MeV
LAMBDA_E: float = 5.950    # eV
LAMBDA_ECO: float = 1.23e-3  # PIB/an (à calibrer)

# Fonctions
def spectral_energy(epsilon: List[int], m: int, Lambda: float) -> float:
    """Calcule E = Λ · 4^m · Σ ε_k · β_k"""

def validate_ahrn() -> Dict[str, float]:
    """Retourne les erreurs sur les 7 domaines AHRN"""
```

#### 4.1.4. Critères de validation

- Les 15 $\beta_k$ doivent correspondre **exactement** à ceux de l'article AHRN.
- Les 7 seuils doivent correspondre **exactement** à ceux de l'article AHRN.
- `spectral_energy()` doit reproduire les valeurs AHRN avec une erreur < 0,1%.

---

### 4.2. Module `pentads_144.py`

#### 4.2.1. Rôle

Construire les **144 pentades** = 12 pentades de base × 12 feuillets spectraux.

#### 4.2.2. Contenu

| Élément | Type | Source | Description |
|---|---|---|---|
| `FEUILLETS` | `dict` | 144 pentades §2.3 | Les 12 feuillets spectraux |
| `PENTADES_BASE` | `dict` | 144 pentades §2.2 | Les 12 pentades de base |
| `CEINTURE_POSITIVE` | `list` | 144 pentades §2.5 | La ceinture $C_P$ |
| `CEINTURE_NEGATIVE` | `list` | 144 pentades §2.5 | La ceinture $C_N$ |
| `SEUILS_POLAIRES` | `list` | 144 pentades §2.5 | Les seuils $P_4, N_4$ |
| `build_144_pentads()` | `function` | 144 pentades §2.3 | Construit les 144 pentades |

#### 4.2.3. Interface

```python
# Structure
FEUILLETS: Dict[str, Dict]  # {'e1': {'secteur': 'Sheng', 'nom': 'Inflation'}, ...}
PENTADES_BASE: Dict[str, Dict]  # {'P1': {'triplet': {...}, 'polarity': +1}, ...}
CEINTURE_POSITIVE: List[str]  # ['P1', 'P3', 'P5', 'P6', 'P2']
CEINTURE_NEGATIVE: List[str]  # ['N1', 'N2', 'N6', 'N5', 'N3']
SEUILS_POLAIRES: List[str]  # ['P4', 'N4']

# Fonction
def build_144_pentads() -> Dict[str, Dict]:
    """Retourne les 144 pentades"""
```

#### 4.2.4. Critères de validation

- `build_144_pentads()` doit retourner **exactement** 144 pentades.
- Chaque pentade doit avoir : `base`, `sheet`, `polarity`, `secteur`.
- Les 12 feuillets doivent être : $e_1..e_6$ (Sheng), $f_1..f_6$ (Ke).

---

### 4.3. Module `attractors_400.py`

#### 4.3.1. Rôle

Construire les **400 attracteurs conjoints** = 20 éco × 20 géo.

#### 4.3.2. Contenu

| Élément | Type | Source | Description |
|---|---|---|---|
| `build_400_attractors()` | `function` | 144 pentades §2.3 | Construit les 400 attracteurs |
| `get_attractor_400()` | `function` | — | Retourne un attracteur spécifique |

#### 4.3.3. Interface

```python
def build_400_attractors() -> Dict[str, Dict]:
    """
    Retourne les 400 attracteurs conjoints.
    
    Structure :
        {
            'A_A': {'eco': 'A', 'geo': 'A', 'triplet_eco': {...}, ...},
            'A_B': {...},
            ...
            'T_T': {...},
        }
    """

def get_attractor_400(key: str) -> Dict:
    """Retourne un attracteur spécifique"""
```

#### 4.3.4. Critères de validation

- `build_400_attractors()` doit retourner **exactement** 400 attracteurs.
- Chaque attracteur doit avoir : `eco`, `geo`, `triplet_eco`, `triplet_geo`.

---

### 4.4. Module `operateur_T.py`

#### 4.4.1. Rôle

Implémenter l'**opérateur de transition $T$** avec ses 4 composantes.

#### 4.4.2. Contenu

| Élément | Type | Source | Description |
|---|---|---|---|
| `OperateurT` | `class` | 144 pentades §8.1 | Opérateur de transition |
| `.apply_structure()` | `method` | 144 pentades §8.1 | $T_{\text{structure}}$ |
| `.apply_fire()` | `method` | 144 pentades §8.1 | $T_{\text{fire}}$ |
| `.apply_water()` | `method` | 144 pentades §8.1 | $T_{\text{water}}$ |
| `.apply_mixed()` | `method` | 144 pentades §8.1 | $T_{\text{mixed}}$ |
| `.check_conservation()` | `method` | 144 pentades §8.2 | Règles de sélection |

#### 4.4.3. Interface

```python
class OperateurT:
    def __init__(self, core_144: 'EconomicCore144'):
        ...
    
    def apply_structure(self, intensity: float = 1.0) -> None:
        """T_structure : réforme structurelle"""
    
    def apply_fire(self, intensity: float = 1.0) -> None:
        """T_fire : choc exogène / innovation"""
    
    def apply_water(self, intensity: float = 1.0) -> None:
        """T_water : politique monétaire"""
    
    def apply_mixed(self, intensity: float = 1.0) -> None:
        """T_mixed : RRT complète"""
    
    def check_conservation(self, transition: Dict) -> bool:
        """Vérifie les 4 règles de conservation"""
    
    def apply(self, component: str, intensity: float = 1.0) -> None:
        """Applique une composante de T"""
```

#### 4.4.4. Critères de validation

- Les 4 composantes doivent être implémentées.
- Les règles de sélection doivent être vérifiées.
- La nilpotence doit être préservée.

---

### 4.5. Module `seuils_spectraux.py`

#### 4.5.1. Rôle

Gérer les **7 seuils spectraux** et leur franchissement.

#### 4.5.2. Contenu

| Élément | Type | Source | Description |
|---|---|---|---|
| `SEUILS_SPECTRAUX` | `dict` | AHRN Ch. 13 | Les 7 seuils |
| `ROLES_SEUILS` | `dict` | 144 pentades §8.2.1 | Rôles des seuils |
| `CORRESPONDANCE_POLARITE` | `dict` | 144 pentades §8.2.2 | Correspondance 3P→3N |
| `can_cross_threshold()` | `function` | — | Vérifie si un seuil est franchi |
| `try_cross_threshold()` | `function` | — | Tente de franchir un seuil |

#### 4.5.3. Interface

```python
SEUILS_SPECTRAUX: Dict[int, float]  # {1: 0.06614, ..., 7: 0.21732}

ROLES_SEUILS: Dict[int, str]  # {1: "Activation minimale", ..., 7: "Saut d'octave"}

CORRESPONDANCE_POLARITE: Dict[str, Dict]  # {'3P': {'condition': ..., 'seuils': []}, ...}

def can_cross_threshold(tension: float, seuil: int) -> bool:
    """Vérifie si T >= S_seuil"""

def try_cross_threshold(tension: float, seuil: int) -> bool:
    """Tente de franchir un seuil"""
```

#### 4.5.4. Critères de validation

- Les 7 seuils doivent correspondre aux valeurs AHRN.
- Le franchissement doit être cohérent avec la polarité 3P→3N.

---

### 4.6. Module `tension_topologique.py`

#### 4.6.1. Rôle

Calculer la **tension topologique $\mathcal{T}$** qui détermine le franchissement des seuils.

#### 4.6.2. Contenu

| Élément | Type | Source | Description |
|---|---|---|---|
| `compute_topological_tension()` | `function` | 144 pentades §10.6.1 | Calcule $\mathcal{T} = \nabla \eta \cdot \nabla R_{\text{seuil}}$ |

#### 4.6.3. Interface

```python
def compute_topological_tension(
    eta_history: List[float],
    r_threshold_history: List[float],
    window: int = 10
) -> float:
    """
    Calcule T = ∇η · ∇R_seuil.
    
    Args:
        eta_history: historique de η
        r_threshold_history: historique de R_seuil
        window: taille de la fenêtre (défaut 10)
    
    Returns:
        tension: valeur de T
    """
```

#### 4.6.4. Critères de validation

- La tension doit être calculée sur une fenêtre glissante.
- Le résultat doit être cohérent avec les valeurs de seuil.

---

### 4.7. Module `economic_core_66.py`

#### 4.7.1. Rôle

**Noyau principal** qui intègre tous les modules.

#### 4.7.2. Contenu

| Élément | Type | Description |
|---|---|---|
| `EconomicCore66` | `class` | Noyau complet Cl(6,6) |
| `.core_60` | `attribute` | Socle statique (Cl(6,0)) |
| `.pentads_144` | `attribute` | 144 pentades |
| `.attractors_400` | `attribute` | 400 attracteurs |
| `.operateur_T` | `attribute` | Opérateur de transition |
| `.tension_history` | `attribute` | Historique de la tension |
| `.threshold_crossings` | `attribute` | Seuils franchis |

#### 4.7.3. Interface

```python
class EconomicCore66:
    def __init__(self, noise_level: float = 0.0, seed: Optional[int] = None):
        ...
    
    # Méthodes Cl(6,0)
    def set_attractor_eco(self, attractor: str) -> None:
        ...
    
    def set_attractor_geo(self, attractor: str) -> None:
        ...
    
    # Méthodes Cl(6,6)
    def apply_T(self, component: str, intensity: float = 1.0) -> None:
        ...
    
    def try_cross_threshold(self, seuil: int) -> bool:
        ...
    
    # Observables
    def eta_66(self) -> float:
        ...
    
    def d_66(self) -> float:
        ...
    
    def gap_66(self) -> float:
        ...
    
    def r_threshold_66(self) -> float:
        ...
    
    def topological_tension(self) -> float:
        ...
    
    # Diagnostic
    def diagnose(self) -> Dict[str, any]:
        ...
```

#### 4.7.4. Critères de validation

- Les observables Cl(6,6) doivent être calculées sur les 144 pentades.
- Le franchissement des seuils doit être cohérent avec la tension.
- Le diagnostic doit identifier l'attracteur dominant.

---

### 4.8. Module `validation_66.py`

#### 4.8.1. Rôle

**Valider** l'intégration complète.

#### 4.8.2. Contenu

| Élément | Type | Source | Description |
|---|---|---|---|
| `test_foundations()` | `function` | AHRN | Test des fondations |
| `test_144_pentads()` | `function` | 144 pentades | Test des 144 pentades |
| `test_400_attractors()` | `function` | 144 pentades | Test des 400 attracteurs |
| `test_chine_2026()` | `function` | — | Test complet Chine 2026 |

#### 4.8.3. Interface

```python
def test_foundations() -> None:
    """Test des fondations AHRN"""

def test_144_pentads() -> None:
    """Test des 144 pentades"""

def test_400_attractors() -> None:
    """Test des 400 attracteurs"""

def test_chine_2026() -> None:
    """Test complet sur la Chine 2026"""

if __name__ == "__main__":
    test_foundations()
    test_144_pentads()
    test_400_attractors()
    test_chine_2026()
```

#### 4.8.4. Critères de validation

- Tous les tests doivent passer.
- La transition S → E doit être validée.
- Les observables doivent être dans les plages attendues.

---

## 5. Flux de données

### 5.1. Diagnostic initial

```
Configuration économique
    ↓
set_attractor_eco() → Attracteur S
    ↓
core_60.diagnose()
    ↓
{η, d, gap, R_seuil, attracteur}
```

### 5.2. Régulation Cl(6,0)

```
État initial
    ↓
core_60.regulate(steps=15)
    ↓
État régulé (E)
```

### 5.3. Transition Cl(6,6)

```
État régulé
    ↓
operateur_T.apply_mixed(intensity=1.0)
    ↓
Nouvel état
```

### 5.4. Franchissement des seuils

```
Tension topologique T
    ↓
can_cross_threshold(T, seuil)
    ↓
Si True : try_cross_threshold(T, seuil)
    ↓
Seuil franchi
```

### 5.5. Validation

```
État final
    ↓
diagnose()
    ↓
{η, d, gap, R_seuil, seuils franchis}
```

---

## 6. Tests et validation

### 6.1. Tests unitaires

| Test | Module | Critère |
|---|---|---|
| `test_beta_k` | `foundations_ahrn` | 15 $\beta_k$ corrects |
| `test_seuils` | `foundations_ahrn` | 7 seuils corrects |
| `test_spectral_energy` | `foundations_ahrn` | Formule correcte |
| `test_144_pentads` | `pentads_144` | 144 pentades |
| `test_400_attractors` | `attractors_400` | 400 attracteurs |
| `test_T_structure` | `operateur_T` | $T_{\text{structure}}$ fonctionne |
| `test_T_fire` | `operateur_T` | $T_{\text{fire}}$ fonctionne |
| `test_T_water` | `operateur_T` | $T_{\text{water}}$ fonctionne |
| `test_T_mixed` | `operateur_T` | $T_{\text{mixed}}$ fonctionne |
| `test_thresholds` | `seuils_spectraux` | Franchissement correct |
| `test_tension` | `tension_topologique` | Tension correcte |

### 6.2. Tests d'intégration

| Test | Description | Critère |
|---|---|---|
| `test_chine_2026` | Validation Chine 2026 | S → E |
| `test_trente_glorieuses` | Validation Trente Glorieuses | D |
| `test_stagflation` | Validation Stagflation 1973 | R |

### 6.3. Critères de succès

| Test | Critère | Tolérance |
|---|---|---|
| Formule AHRN | Erreur < 0,1% | — |
| 144 pentades | 144 exactes | — |
| 400 attracteurs | 400 exacts | — |
| Chine 2026 | η ≈ −0,45 | ±0,15 |
| Chine 2026 | d ≈ 1,9 | ±0,5 |
| Chine 2026 | gap ≈ 0,10 | ±0,05 |
| Chine 2026 | R_seuil ≈ 0,78 | ±0,20 |
| Chine 2026 | Transition S → E | Exacte |
| Seuils franchis | S₅, S₆, S₇ | — |

---

## 7. Calendrier de développement

| Phase | Module | Durée | Livrable |
|---|---|---|---|
| 1 | `foundations_ahrn.py` | 1 j | Fondations AHRN |
| 2 | `pentads_144.py` | 2 j | 144 pentades |
| 3 | `attractors_400.py` | 2 j | 400 attracteurs |
| 4 | `operateur_T.py` | 3 j | Opérateur T |
| 5 | `seuils_spectraux.py` + `tension_topologique.py` | 2 j | Seuils |
| 6 | `economic_core_66.py` | 3 j | Noyau complet |
| 7 | `validation_66.py` | 2 j | Tests |
| 8 | `README_economic_core_66.md` | 2 j | Documentation |
| **Total** | — | **17 j** | — |

---

## 8. Risques et mitigation

| Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|
| Les 144 pentades ne convergent pas | Moyenne | Élevé | Tester sur cas simples |
| L'opérateur $T$ ne fonctionne pas | Haute | Élevé | Commencer par $T_{\text{structure}}$ seul |
| Les seuils ne sont pas franchissables | Moyenne | Moyen | Calibrer les valeurs |
| Les 400 attracteurs sont ingérables | Basse | Moyen | Utiliser des indexes |
| Le noyau est trop lent | Basse | Faible | Optimiser le code |
| La formule AHRN ne s'applique pas | Basse | Élevé | Vérifier sur données AHRN |

---

## 9. Livrables

| Livrable | Description | Priorité |
|---|---|---|
| `foundations_ahrn.py` | 15 $\beta_k$, 7 seuils | Haute |
| `pentads_144.py` | 144 pentades | Haute |
| `attractors_400.py` | 400 attracteurs | Haute |
| `operateur_T.py` | Opérateur T | Haute |
| `seuils_spectraux.py` | 7 seuils | Haute |
| `tension_topologique.py` | Tenseur $\mathcal{T}$ | Haute |
| `economic_core_66.py` | Noyau complet | Haute |
| `validation_66.py` | Tests | Haute |
| `README_economic_core_66.md` | Documentation | Moyenne |
| `article_economic_core_66.md` | Publication | Basse |

---

## 10. Références croisées

### 10.1. Article AHRN

| Section | Contenu | Utilisation |
|---|---|---|
| Ch. 8 | Formule spectrale | `foundations_ahrn.py` |
| Ch. 13 | 15 $\beta_k$ | `foundations_ahrn.py` |
| Ch. 13 | 7 seuils | `foundations_ahrn.py`, `seuils_spectraux.py` |
| Ch. 18 | Centroïdes de Clifford | Justification |

### 10.2. Article 144 pentades

| Section | Contenu | Utilisation |
|---|---|---|
| §2.3 | 12 feuillets | `pentads_144.py` |
| §2.3 | 144 pentades | `pentads_144.py` |
| §2.5 | Graphe dual Γ | `pentads_144.py` |
| §8.1 | Opérateur $T$ | `operateur_T.py` |
| §8.2 | Règles de sélection | `operateur_T.py` |
| §8.2.1 | 7 seuils | `seuils_spectraux.py` |
| §10.6.1 | Tenseur $\mathcal{T}$ | `tension_topologique.py` |

### 10.3. Noyau v6

| Section | Contenu | Utilisation |
|---|---|---|
| `economic_core_v6.py` | Socle Cl(6,0) | `economic_core_66.py` |

---

## 11. Conclusion

Ce plan d'intégration définit précisément :

1. **L'architecture** en 4 couches du noyau Cl(6,6).
2. **Les modules** à développer avec leurs interfaces.
3. **Les flux de données** entre modules.
4. **Les tests** et critères de validation.
5. **Le calendrier** de développement (17 jours).
6. **Les risques** et leur mitigation.

Il constitue la **référence technique** pour l'implémentation du noyau Cl(6,6) intégrant les deux articles.

---

## 12. Prochaines étapes

| Étape | Action | Priorité |
|---|---|---|
| 1 | Rédiger `foundations_ahrn.py` | Haute |
| 2 | Rédiger `pentads_144.py` | Haute |
| 3 | Rédiger `attractors_400.py` | Haute |
| 4 | Rédiger `operateur_T.py` | Haute |
| 5 | Rédiger `seuils_spectraux.py` | Haute |
| 6 | Rédiger `tension_topologique.py` | Haute |
| 7 | Rédiger `economic_core_66.py` | Haute |
| 8 | Rédiger `validation_66.py` | Haute |
| 9 | Rédiger `README_economic_core_66.md` | Moyenne |
| 10 | Préparer la publication | Basse |

---

**Fin du document de plan d'intégration.**
