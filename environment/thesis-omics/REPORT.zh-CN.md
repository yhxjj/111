# 硕士课题代谢组学与蛋白质组学环境配置报告

日期：2026-11-02（北京时间）。本次完成独立 Python 下游统计分析环境，所有验证使用模拟数据，不构成任何科研结果。

## 环境检查与安装

- 起始工作目录 `/workspace`，项目 `/workspace/111`；原分支 `work`，基线提交 `04d5206707abb4f331eb7b8f017f9364939c7d6b`。
- 已新建本地分支 `codex/thesis-omics-environment` 保存配置，未推送 GitHub，未修改远程 main。
- Python 3.12.14；初始未激活 venv，项目没有既有虚拟环境。
- 创建 `/workspace/111/.venv-thesis-omics`；`include-system-site-packages = false`，与系统包隔离。
- 系统原有 131 个发行包，安装前后包名及版本完全一致；系统 Python 未改动。原环境 pip check 也通过。
- statsmodels、patsy、gseapy 原先缺失，现已在项目 venv 安装成功。
- 安装前使用 pip dry-run 解析全部依赖、检查 Requires-Python 和二进制 wheel；所有 34 个分析依赖均兼容 Python 3.12。直接锁定原有 NumPy、pandas、SciPy、Matplotlib、Seaborn、scikit-learn、openpyxl 版本，未对系统包做升级。
- 安装保留继承的代理及 CA；使用命令级网络权限，`--retries 0 --timeout 25`，未遇到代理限制，未修改永久代理或换源。
- 安装后 pip check：`No broken requirements found.`

## 显式 Skill 加载

按 `AGENTS.md → .sciagent-skills/registry.yaml → SKILL.md` 全文读取 statistical-analysis、statsmodels-statistical-modeling、gseapy-gene-enrichment、kegg-pathway-analysis、omics-plotting。
上游固定提交 `55c1bd3e863d11bf5a853d24bcdda10c88e6eddf`。文件路径和 SHA-256 见 `skill-sources.json`。本次不依赖原生自动发现，也未把文件可读称为原生发现成功。

## 核心软件版本

| 软件包 | 版本 | 状态 |
|---|---|---|
| numpy | 2.3.5 | 已安装，可导入 |
| pandas | 2.2.3 | 已安装，可导入 |
| scipy | 1.17.0 | 已安装，可导入 |
| statsmodels | 0.15.0 | 已安装，可导入 |
| patsy | 1.0.3 | 已安装，可导入 |
| gseapy | 1.3.2 | 已安装，可导入 |
| matplotlib | 3.10.8 | 已安装，可导入 |
| seaborn | 0.13.2 | 已安装，可导入 |
| scikit-learn | 1.8.0 | 已安装，可导入 |
| openpyxl | 3.1.5 | 已安装，可导入 |
| requests | 2.34.2 | 已安装，可导入 |

完整 34 项分析依赖版本在 `requirements.lock.txt`；安装后的实际包清单在证据文件 `installed-freeze.txt`，包括 pip 与构建工具以外的已安装包。

## 功能测试结果

测试脚本 `smoke_test.py` 使用固定种子 20261102，16 个模拟样本（每组 8 个）、80 个模拟 log2 强度特征。数据和文件名全部标记 SIMULATED；没有读取实验数据。

| 测试 | 结果 | 实际验证范围 |
|---|---|---|
| Welch 双侧 t 检验 | 通过 | 80 个模拟特征，独立样本、非等方差 |
| BH 多重检验校正 | 通过 | q 值范围/有限值检查，并与已知校正结果核对 |
| statsmodels OLS | 通过 | 处理组 + 批次公式，HC3 稳健标准误，系数与区间有限 |
| Patsy | 通过 | 显式构建设计矩阵（16×3）和响应矩阵 |
| PCA | 通过 | 标准化后 PCA，PC1/PC2 解释方差约 30.48%/10.76%，PNG/PDF 成功 |
| 火山图 | 通过 | 用实际模拟 Welch/BH 结果绘图，阈值 q<0.05 且绝对 log2FC≥1，PNG/PDF 成功 |
| GSEApy 本地 ORA | 通过 | 实际读取模拟 GMT，显式 80 个模拟背景基因，返回 2 项有交集的条目 |
| GSEApy 本地 prerank | 通过 | 相同本地 GMT，模拟 Welch t 排序，3 项结果，100 次置换、单线程、固定种子 |

富集测试禁止 Python HTTP 请求和常规 socket 连接，未使用在线 Enrichr、KEGG 或任何人类基因集。GMT 仅含人工 SIM_GENE ID 和 SIMULATED_SET 名称，无物种含义。100 次置换只用于软件测试；真实研究须预先确定排名、基因集大小阈值、置换次数和多重校正方案。

## 两个课题现在能做什么

**金钱松三部位 LC-MS 代谢组：** 对已经过确认的定量特征表，可运行统计模型、适用设计下的 Welch 检验/BH 校正、PCA 和火山图。真实分析前需确认树编号、独立生物学重复、三部位是否来自同一棵树、QC/空白、批次、归一化和缺失值处理。若来自同一树，按配对/重复测量设计处理；本次独立两组 Welch 测试不是三部位分析方案。尚未安装原始质谱峰提取和谱库鉴定工具。

**PAA/PAB 抗茄链格孢菌蛋白组：** 对已质控的蛋白定量表，可进行处理/批次建模、PCA、适当的差异比较和绘图。GSEApy 本地 ORA/GSEA 软件已可运行，但真实富集尚缺经核实的菌株/物种基因集、蛋白到基因映射、注释版本和实际检测背景。不会将人类或其他物种通路当作该菌注释。ORA 可分上/下调运行；富集及蛋白丰度变化本身不能证明作用机制、直接靶点或整个通路的激活/抑制。

**尚未配置或验证：** pyopenms、matchms、MaxQuant、R/Bioconductor、原始质谱数据库检索、真实菌株 GO/KEGG 注释、在线 KEGG/Enrichr API。当前是下游表格分析环境，不是从仪器原始文件到论文结果的完整平台。

## 日常使用与复现

在项目根目录执行：

```bash
source .venv-thesis-omics/bin/activate
python -m pip check
python environment/thesis-omics/smoke_test.py --out work/thesis-omics-validation
```

每次任务先显式加载目标 Skill，再核对 `sys.executable` 是否属于项目 venv。只读科研原始文件，把正式输出另存。新云工作区不保证保留 venv；按 README 的精确版本锁重建，不提交虚拟环境到 Git。全部测试原始输出位于 `work/thesis-omics-validation/`；安装日志和预检证据位于 `work/omics-setup/`，两者均已排除 Git 跟踪。

本地归档 `work/thesis-omics-environment.zip` 包含配置、脚本、版本锁、中文报告、模拟测试输入/结果/PNG/PDF 和运行证据，不包含虚拟环境或任何科研原始数据。当前云执行器无法写入聊天附件输出目录，报告已保存在项目内。
