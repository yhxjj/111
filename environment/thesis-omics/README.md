# 硕士课题组学统计环境

Python 3.12 独立 venv，不继承系统 site-packages。仅用于定量表下游统计、绘图及本地基因集富集；不是完整原始 LC-MS/蛋白质组检索平台。

在仓库根目录使用：

```bash
source .venv-thesis-omics/bin/activate
python -m pip check
python environment/thesis-omics/smoke_test.py --out work/thesis-omics-validation
```

重新创建（已有环境请勿覆盖，先另选目录）：

```bash
python3.12 -m venv .venv-thesis-omics
.venv-thesis-omics/bin/python -m pip install --only-binary=:all: --retries 0 --timeout 25 -r environment/thesis-omics/requirements.lock.txt
.venv-thesis-omics/bin/python -m pip check
```

安装沿用环境代理及 CA，不永久修改设置；网络失败立即停止，不自动换源或重试。
`requirements.in` 是直接依赖清单，`constraints.txt` 保留原有科学计算核心版本，`requirements.lock.txt` 是本次解析的全部分析依赖精确版本。
锁定版本适用于本次 Python 3.12 Linux 环境，其他平台需重新检查二进制包兼容性；pip 本身不包含在分析依赖锁中。
虚拟环境不提交到 Git，新云任务可能需要重建。

所有测试文件放在 `--out` 指定的独立目录；脚本固定随机种子，只生成模拟数据，不读取科研原始文件。图标题、文件名和 GMT 均标记 SIMULATED。测试期间禁用 Python HTTP 请求和常规 socket 连接。本地 ORA 显式指定 80 个模拟背景基因；GSEA 使用模拟 Welch t 排序、100 次置换和单线程，仅作功能检查，不能用于论文结论。

日常 Skill 调用：先读取 `AGENTS.md`，再由 `.sciagent-skills/registry.yaml` 定位并全文读取目标 `SKILL.md`。调用分析前核对当前解释器为项目 venv；不要把文档加载成功等同于软件或数据库就绪。

## 课题适用边界

- 金钱松根皮、枝皮、身皮：本环境可处理经确认的定量特征表，进行统计/PCA/火山图。三部位若取自同一树，必须按树编号处理配对/重复测量；不能默认样本独立。真实流程需先确认生物学重复、批次、QC、空白、缺失值、归一化及多组比较方案。
- PAA/PAB 抗茄链格孢菌：可处理已质控蛋白定量表，建立含处理和批次的模型。富集需要对应菌株/蛋白数据库版本、蛋白到基因映射、检测背景及真实 GO/KEGG 注释。不得直接使用 human、yeast 或其他物种的基因集代替该菌注释。
- 本地 ORA/GSEA 能运行不表示已有真实菌株 GMT。库名字符串不保证离线可用，离线分析必须提供实际 GMT 或字典并记录来源与版本。ORA 可按上/下调分别测试，不能由富集方向推断整个通路被激活/抑制。
- 未配置 pyopenms、matchms、MaxQuant、R/Bioconductor 或参考数据库；原始质谱峰提取、谱库鉴定、蛋白检索以及真实物种富集仍需专项配置。

运行图形代码时，如宿主 home 只读，为当前命令设置可写的 `MPLCONFIGDIR`、`XDG_CACHE_HOME`；测试脚本已自动设置到测试目录下，不修改永久配置。
