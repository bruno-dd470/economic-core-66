> 🌐 **语言 / Languages** : 
> 🇫🇷 [Français](README.md) | 
> 🇬🇧 [English](README.en.md) | 
> 🇨🇳 [中文](README.zh.md)
> 🇷🇺 [Русский](README.ru.md)

# economic_core_66 — 自调节 Cl(6,6) 核心

**版本：** 1.0  
**日期：** 2026 年 9 月  
**作者：** Bruno DE DOMINICIS（布鲁诺·德·多米尼西斯）  
**许可证：** MIT  

---

## 目录
1. [简介](#1-简介)
2. [安装](#2-安装)
3. [架构](#3-架构)
4. [快速上手](#4-快速上手)
5. [模块详解](#5-模块详解)
6. [示例](#6-示例)
7. [验证](#7-验证)
8. [API 参考](#8-api-参考)
9. [局限与展望](#9-局限与展望)
10. [参考文献](#10-参考文献)
- [附录 A — 术语表](#附录-a--术语表)
- [附录 B — 退出码](#附录-b--退出码)
- [附录 C — 版本记录](#附录-c--版本记录)

---

## 1. 简介

### 1.1. 项目目标
`economic_core_66` 是一个基于克利福德代数 Cl(6,6) 的自调节经济模型核心。  
它集成了：
- **静态骨架 Cl(6,0)**：20 个吸引子、12 个五元组、谱可观测值。
- **动态扩展 Cl(6,6)**：144 个五元组、400 个联合吸引子、跃迁算子 T。
- **7 个谱阈值**，源自例外格 Λ₇₂。
- **拓扑张力** $T = \nabla\eta \cdot \nabla R_{seuil}$，归一化后取值于 $[0, 1[$。

### 1.2. 理论定位
本模型基于两篇奠基性论文：
1. **AHRN** —《三种本体论的统一算术：物质、生命与信息》（2026 年 6 月）  
   提供 15 个普适常数 $\beta_k$ 与谱公式。
2. **144 五元组** —《五行与 Cl(6,6)：144 个五元组构建统一关系物理学》（2026 年 4 月）  
   提供 Cl(6,6) 结构、T 算子与 7 个阈值。

`economic_core_66` 包是这两篇论文在经济领域的**运算实现**。

### 1.3. Cl(6,0) 与 Cl(6,6) 的区分
| 代数 | 符号 | 角色 | 实现 |
| --- | --- | --- | --- |
| **Cl(6,0)** | (6,0) | 静态骨架（构型、吸引子） | 集成于 `economic_core_66.py` |
| **Cl(6,6)** | (6,6) | 动力学（跃迁、阈值） | `economic_core_66.py` |

---

## 2. 安装

### 2.1. 环境要求
- Python ≥ 3.8
- NumPy ≥ 1.20
- SciPy ≥ 1.6
- NetworkX ≥ 2.5

### 2.2. 安装依赖
```bash
pip install numpy scipy networkx
```

### 2.3. 文件结构
```text
economic_core_66/
├── foundations_ahrn.py           # AHRN 基础（15 个 β_k、7 个阈值、公式）
├── pentads_144.py                # 144 个五元组（12 基底 × 12 谱叶）
├── attractors_400.py             # 400 个联合吸引子（20 经济 × 20 地理）
├── operateur_T.py                # 跃迁算子 T
├── seuils_spectraux.py           # 7 个谱阈值管理
├── tension_topologique.py        # 拓扑张量 T（归一化）
├── economic_core_66.py           # Cl(6,6) 主核心
├── validation_66.py              # 验证测试
├── economic_core_Cl60.py         # Cl(6,0) 骨架（遗留）
├── economic_core_Cl60.md         # Cl(6,0) 文档
├── CCTP-Cl66_économie_chine.md   # 技术规格（CCTP）
└── README.md                     # 本文档
```

### 2.4. 验证安装
```bash
python3 validation_66.py
```
若所有测试通过，则安装正确。

---

## 3. 架构

### 3.1. 分层视图
```text
┌──────────────────────────────────────────────────────────────────────┐
│                    economic_core_66.py                               │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  第 0 层：基础（AHRN 论文）                                     │  │
│  │  模块：foundations_ahrn.py                                     │  │
│  │  - BETA_K（15 个值）                                            │  │
│  │  - SEUILS_SPECTRAUX（7 个值）                                   │  │
│  │  - spectral_energy()                                           │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                              ↓                                       │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  第 1 层：静态骨架（Cl(6,0)）                                   │  │
│  │  集成于 economic_core_66.py                                    │  │
│  │  - 20 个吸引子（A–T）                                           │  │
│  │  - 12 个五元组（P₁..P₆, N₁..N₆）                               │  │
│  │  - 可观测值（η, d, gap, R_seuil）                               │  │
│  │  - 基于吸引子距离的调节                                         │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                              ↓                                       │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  第 2 层：动态扩展（144 五元组论文）                             │  │
│  │  模块：pentads_144.py, attractors_400.py, operateur_T.py       │  │
│  │  - 12 个谱叶（e₁..e₆, f₁..f₆）                                 │  │
│  │  - 144 个五元组（12 基底 × 12 谱叶）                            │  │
│  │  - 400 个联合吸引子（20 经济 × 20 地理）                        │  │
│  │  - 算子 T（4 个分量）                                           │  │
│  │  - 7 个谱阈值                                                   │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                              ↓                                       │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  第 3 层：验证                                                  │  │
│  │  模块：validation_66.py                                        │  │
│  │  - 单元测试                                                     │  │
│  │  - 集成测试                                                     │  │
│  │  - 历史构型验证                                                 │  │
│  └────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
```

### 3.2. 数据流（2026 年中国）
1. **经济构型（2026 年中国）**
2. `set_from_config()` → 吸引子 **S**（稳态）
3. `core.diagnose()` → 初始诊断  
   *(η = -0.333, d = 1.500, gap = 0.362, R_seuil = 0.176, 阻挫度 = 20)*
4. `core.regulate_60(steps=15)` → 吸引子 **E**（城市扩张）
5. `core.diagnose()` → 中间诊断  
   *(η = +0.333, d = 1.425, gap = 0.303, R_seuil = 0.294, 阻挫度 = 23)*
6. **历史模拟（10 步）**
7. `core.apply_T('mixed', intensity=1.0)`  
   ├── 依次跨越阈值 S1..S7  
   └── 跃迁 E → D（温和增长）
8. `core.diagnose()` → 最终诊断  
   *(η = +0.333, d = 1.450, gap = 0.215, R_seuil = 0.529, 阻挫度 = 22)*

---

## 4. 快速上手

### 4.1. 最简示例
```python
from economic_core_66 import EconomicCore66

# 初始化
core = EconomicCore66(noise_level=0.0, seed=42)

# 2026 年中国构型
config = {
    'P1': -1, 'P2': -1, 'P3': -1, 'P4': -1, 'P5': -1,
    'P6': +1,
    'N1': -1, 'N2': -1, 'N3': -1, 'N4': -1,
    'N5': +1, 'N6': +1,
}
attractor = core.set_from_config(config)
core.set_attractor_geo(attractor)

# 初始诊断
core.print_diagnostic()

# Cl(6,0) 调节
core.regulate_60(steps=15)
core.print_diagnostic()

# 历史模拟（计算张力所需）
for i in range(10):
    eta = core.eta_direct() + i * 0.02
    r = core.r_threshold() + i * 0.02
    core.eta_history.append(eta)
    core.r_threshold_history.append(r)

# Cl(6,6) 跃迁
result = core.apply_T('mixed', intensity=1.0)
print(f"跃迁：{result['attracteur_avant']} → {result['attracteur_apres']}")
print(f"张力：{result['tension']:.6f}")
print(f"跨越的阈值：{result['seuils_franchis']}")

# 最终诊断
core.print_diagnostic()

### 4.2. 预期输出
*（参见法文 README 中的完整控制台输出示例，结构相同。）*

---

## 5. 模块详解

### 5.1. `foundations_ahrn.py`
**作用：** 提供普适常数与谱公式。  
**常量：** `BETA_K`（15 个值）、`SEUILS_SPECTRAUX`（7 个值）、`LAMBDA_NUC`、`LAMBDA_E`、`LAMBDA_ECO`。  
**函数：** `spectral_energy()`、`spectral_energy_vectorized()`、`validate_foundations()`、`print_validation_report()`。

### 5.2. `pentads_144.py`
**作用：** 构建 144 个五元组（12 基底 × 12 谱叶）。  
**常量：** `FEUILLETS`、`PENTADES_BASE`、`ATTRACTEURS`、`CEINTURE_POSITIVE`、`CEINTURE_NEGATIVE`、`SEUILS_POLAIRES`。  
**函数：** `build_144_pentads()`、`build_144_pentads_by_sector()`、`get_pentad()`、`validate_pentads()`。

### 5.3. `attractors_400.py`
**作用：** 构建 400 个联合吸引子（20 经济 × 20 地理）。  
**函数：** `build_400_attractors()`、`get_attractor_400()`、`attractor_distance_400()`、`find_nearest_attractor_400()`、`validate_attractors_400()`。

### 5.4. `operateur_T.py`
**作用：** 实现跃迁算子 T。  
**类 `OperateurT`：** 方法 `apply_structure()`、`apply_fire()`、`apply_water()`、`apply_mixed()`、`apply()`、`_choose_best_target()`、`check_conservation()`。  
*注：* `_choose_best_target` 对极端吸引子（3P、3N）施加惩罚，倾向于更稳定的 2P+1N 吸引子。

### 5.5. `seuils_spectraux.py`
**作用：** 管理 7 个谱阈值。  
**常量：** `SEUILS_SPECTRAUX`、`ROLES_SEUILS`、`CORRESPONDANCE_POLARITE`。  
**类 `GestionnaireSeuils`：** 方法 `try_cross()`、`cross_all_possible()`、`get_crossed()`、`get_current_polarity()`。  
*注：* `cross_all_possible(tension)` **每次仅跨越一个**阈值（下一个未跨越的），遵循 3P → 2P+1N → 1P+2N → 3N 序列。

### 5.6. `tension_topologique.py`
**作用：** 计算拓扑张力 $T = \nabla\eta \cdot \nabla R_{seuil}$，归一化。  
**公式：** $T_{norm} = \frac{|\nabla\eta \cdot \nabla R_{seuil}| \cdot \alpha}{1 + |\nabla\eta \cdot \nabla R_{seuil}| \cdot \alpha}$  
**函数：** `compute_topological_tension()`、`check_threshold_crossing()`、`validate_tension()`。  
**类 `SuiviTension`：** 在滑动窗口内追踪张力。

### 5.7. `economic_core_66.py`
**作用：** 集成所有模块的主核心。  
**类 `EconomicCore66`：** 方法 `set_from_config()`、`regulate_60()`、`apply_T()`、`diagnose()`、`print_diagnostic()` 等。

---

## 6. 示例

### 6.1. 2026 年中国（S → E → D）
*（参见第 4.1 节代码片段）*  
**结果：** 初始吸引子：S（稳态）→ 调节后：E（城市扩张）→ 最终：D（温和增长）。

### 6.2. 辉煌三十年（战后繁荣）（D）
```python
config_trente = {
    'P1': -1, 'P2': -1, 'P3': -1, 'P4': +1, 'P5': +1, 'P6': -1,
    'N1': -1, 'N2': +1, 'N3': -1, 'N4': -1, 'N5': -1, 'N6': -1,
}
core.set_from_config(config_trente)
diag = core.diagnose()
print(f"吸引子：{diag['attractor_eco']}")  # D
```

### 6.3. 1973 年滞胀（R）
```python
config_stag = {
    'P1': -1, 'P2': -1, 'P3': +1, 'P4': -1, 'P5': -1, 'P6': -1,
    'N1': +1, 'N2': -1, 'N3': -1, 'N4': -1, 'N5': +1, 'N6': -1,
}
core.set_from_config(config_stag)
diag = core.diagnose()
print(f"吸引子：{diag['attractor_eco']}")  # R
```

### 6.4. 访问 144 个五元组
```python
from pentads_144 import build_144_pentads
pentads = build_144_pentads()
sheng = [p for p in pentads.values() if p['secteur'] == 'Sheng']
ke = [p for p in pentads.values() if p['secteur'] == 'Ke']
print(f"相生（Sheng）：{len(sheng)}")  # 72
print(f"相克（Ke）：{len(ke)}")        # 72
```

---

## 7. 验证

### 7.1. 运行测试
```bash
python3 validation_66.py
```

### 7.2. 包含的测试
| # | 测试 | 描述 | 状态 | 耗时 |
|---|---|---|---|---|
| 1 | `test_foundations` | AHRN 基础 | ✓ 通过 | ~0.2 ms |
| 2 | `test_144_pentads` | 144 个五元组 | ✓ 通过 | ~0.3 ms |
| 3 | `test_400_attractors` | 400 个联合吸引子 | ✓ 通过 | ~5.4 ms |
| 4 | `test_operateur_T` | 算子 T | ✓ 通过 | ~62.2 ms |
| 5 | `test_seuils_spectraux` | 7 个谱阈值 | ✓ 通过 | ~0.0 ms |
| 6 | `test_tension_topologique` | 拓扑张力 T | ✓ 通过 | ~0.5 ms |
| 7 | `test_chine_2026` | 2026 年中国（S → E） | ✓ 通过 | ~1.1 ms |
| 8 | `test_trente_glorieuses` | 辉煌三十年（D） | ✓ 通过 | ~1.5 ms |
| 9 | `test_stagflation_1973` | 1973 年滞胀（R） | ✓ 通过 | ~0.8 ms |
| 10| `test_full_pipeline` | 完整流水线 | ✓ 通过 | ~2.9 ms |
| **总计** | | | **10/10** | **~75 ms** |

**总体结果：** ✓ 所有测试通过

---

## 8. API 参考

### `EconomicCore66`
- `__init__(noise_level=0.0, seed=None)`：初始化 Cl(6,6) 核心。
- `set_attractor_eco(attractor: str)`：设置经济吸引子（A–T）。
- `set_attractor_geo(attractor: str)`：设置地理吸引子（A–T）。
- `set_from_config(config: Dict[str, int]) -> str`：从构型字典 `{五元组: +1 或 -1}` 识别吸引子。
- `regulate_60(steps: int = 15, target: Optional[str] = None)`：基于最小吸引子距离的 Cl(6,0) 调节。
- `apply_T(composante: str = 'mixed', intensity: float = 1.0) -> Dict`：应用 T 算子分量（`'structure'`、`'fire'`、`'water'`、`'mixed'`）。
- `diagnose() -> Dict[str, Any]`：返回包含所有可观测值的完整诊断字典（`eta`、`d`、`gap`、`r_threshold`、`frustration`、`tension`、`regime`、`severity`、`state` 等）。
- `print_diagnostic()`：向控制台打印格式化的诊断信息。

---

## 9. 局限与展望

### 9.1. 当前局限
- **可观测值近似：** 部分可观测值（`d`、`gap`）通过简单公式近似。更严谨的实现需要完整的离散狄拉克算子。
- **五元组命名：** 五元组与谱叶名称为临时命名，可进一步完善。
- **`Λ_eco` 标定：** 经济尺度常数仍需基于真实数据标定。
- **实证验证：** 核心尚未在真实经济数据集（如 BNS、BPC）上测试。
- **`η_66 = 0.000`：** Cl(6,6) 谱不对称性目前仍为零（公式待修订）。

### 9.2. 展望
- **离散狄拉克算子：** 在 144 个五元组上实现完整的狄拉克算子，以严格计算 `d` 与 `gap`。
- **Λ₇₂ 格：** 深化 Λ₇₂ 格本征值的整合。15 个 $\beta_k$ 已提取，但需更精细的标定。
- **真实数据：** 将核心连接到真实经济数据流。
- **用户界面：** 开发用于模型操控的 Web 界面。
- **扩展至其他平面：** 将模型扩展至其他平面对（社会/生态等）。

---

## 10. 参考文献

### 10.1. 奠基性论文
1. **AHRN** —《三种本体论的统一算术：物质、生命与信息》  
   Bruno DE DOMINICIS，2026 年 6 月。DOI：（待定）
2. **144 五元组** —《五行与 Cl(6,6)：144 个五元组构建统一关系物理学》  
   Bruno DE DOMINICIS，2026 年 4 月。DOI：[10.5281/zenodo.19947629](https://doi.org/10.5281/zenodo.19947629)

### 10.2. 相关工作
- Rowlands, P. (2007). *Zero to Infinity: The Foundations of Physics*. World Scientific.
- Nebe, G. (2010). *An extremal even unimodular lattice in dimension 72*. Journal of Number Theory.
- Petit, J.-P. (2024). *A bimetric cosmological model based on Andrei Sakharov's twin universe approach*. European Physical Journal C.

### 10.3. Python 库
- [NumPy](https://numpy.org/)
- [SciPy](https://scipy.org/)
- [NetworkX](https://networkx.org/)

---

## 附录 A — 术语表
| 术语 | 定义 |
| --- | --- |
| **吸引子** | 经济系统的稳定状态（A–T） |
| **五元组** | 基础代数单元（P₁..P₆, N₁..N₆） |
| **谱叶** | 在生成元上的投影（e₁..e₆, f₁..f₆） |
| **算子 T** | 跃迁算子（4 个分量） |
| **谱阈值** | 跨越里程碑（S₁..S₇） |
| **拓扑张力** | $T = \nabla\eta \cdot \nabla R_{seuil}$，归一化于 $[0, 1[$ |
| **β_k** | 普适常数（15 个值） |
| **相生（Sheng）** | 五行中的生成关系，对应 η > 0 |
| **相克（Ke）** | 五行中的克制关系，对应 η < 0 |

## 附录 B — 退出码
| 代码 | 含义 |
| --- | --- |
| `0` | 所有测试通过 |
| `1` | 至少一个测试失败 |

## 附录 C — 版本记录
| 版本 | 日期 | 变更 |
| --- | --- | --- |
| 1.0 | 2026 年 9 月 | 初始版本，10/10 测试验证通过 |
