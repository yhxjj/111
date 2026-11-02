# 毕业课题 Codex 原生 Skill 入口

## 配置范围

本项目将下面 10 个 SciAgent-Skills 包装为项目级 Codex Skill。
每个入口为 `.agents/skills/<名称>/SKILL.md`，包含 YAML `name` 和 `description`、课题适用边界、上游文档加载方法、依赖检查和结果报告要求。它们不是仅有索引的占位文件，实际工作流通过相对路径按需加载上游完整正文。

上游仍由 Git 子模块 `.sciagent-skills` 管理，固定提交为
`55c1bd3e863d11bf5a853d24bcdda10c88e6eddf`。本次不修改子模块内容、AGENTS.md 或原有 Skill。

## Codex 规范依据

官方说明：https://developers.openai.com/codex/skills

- 项目级扫描位置为当前工作目录到 Git 仓库根目录之间各级 `.agents/skills`。
- 每个 Skill 目录必须有 `SKILL.md`，YAML frontmatter 至少含 `name`、`description`；`agents/openai.yaml` 是可选元数据，本次无需添加。
- Codex CLI/IDE 中可通过 `/skills` 查看列表、通过 `$名称` 显式调用。
- 官方说明支持自动检测更改；如果列表没有刷新，应重新启动 Codex。
- 本次检查 CLI 版本为 `codex-cli 0.163.0`。

**从本仓库根目录或其子目录启动 Codex。** 从仓库的父目录或旁边的 scratch/work 目录启动时，不能指望自动发现本仓库的项目级 Skill。先进入克隆的项目根目录，再运行 `codex`；包装文件内不包含工作区绝对路径。

## 入口清单

所有名称和源路径均以 `registry.yaml` 的实际条目为准；本次 10 个请求名称全部匹配。

| 名称 | 主要用途 | 本次静态验证 |
|---|---|---|
| pyopenms-mass-spectrometry | 代谢组/蛋白组 mzML 处理、峰提取与特征关联 | 通过 |
| matchms-spectral-matching | MS/MS 谱图处理与谱库匹配 | 通过 |
| hmdb-database | HMDB 本地 XML 与代谢物辅助注释 | 通过 |
| maxquant-proteomics | MaxQuant 输出、蛋白定量表与质控流程 | 通过 |
| uniprot-protein-database | 蛋白 ID 映射和物种限定注释 | 通过 |
| statistical-analysis | 统计设计、检验选择与报告 | 通过 |
| statsmodels-statistical-modeling | 统计建模、协变量和模型诊断 | 通过 |
| gseapy-gene-enrichment | 蛋白/基因 GO、KEGG ORA 与 GSEA | 通过 |
| kegg-pathway-analysis | 通路方案、物种、映射与背景核对 | 通过 |
| omics-plotting | PCA、火山图、热图及富集图 | 通过 |

上游正文引用均采用 `../../../.sciagent-skills/skills/.../SKILL.md`，相对于**包装文件所在目录**解析。上游正文引用的附属资源则相对于**上游文档目录**解析。包装要求先读取全文，不直接把文档中的演示代码或人体示例用于植物/真菌课题。

新克隆项目后，先在项目根执行：

```bash
git submodule update --init --recursive
```

如果子模块缺失，入口本身可能仍被发现，但其上游工作流无法使用；必须报告缺失，不得将其视作完整可用。

## 本次验证及限制（2026-11-02）

- 10/10 包装文件均可读取，frontmatter 名称正确、描述非空且少于 1024 字符。
- 10/10 上游相对路径均实际解析到当前子模块中的非空完整 SKILL.md，且与 registry 条目及上游 frontmatter 名称一致。
- 包装文件无当前工作区绝对路径，也没有复制完整上游仓库。
- 对修改前的 819 个现有文件（原 Skill、AGENTS.md、.gitmodules）执行哈希核对，均保持不变。
- 已检查子模块 Git 状态和指针，未修改上游内容。
- `git diff --check` 通过。

**动态发现尚未验证成功。** 已尝试使用当前 Codex app-server 的 `skills/list` 原生扫描接口进行强制重载；本机 app-server 无法初始化，首先报告无法在只读的 `/home/agent/.codex` 下初始化 SQLite 状态。仅对该验证进程指定工作目录内的状态与日志目录后，仍返回 `Read-only file system (os error 30)`。未修改用户 home、永久 Codex 配置或网络配置。执行器 Skill 列表接口仍返回空列表。

因此本次可确认的是“项目级原生入口已按规范配置并通过静态验证”，不能声称“当前聊天原生选择器已刷新”或“已实际调用原生 Skill 完成分析”。请在本仓库重新打开 Codex 任务后查看 `/skills`，确认这 10 个名称可选择；如果仍未出现，先核对任务根目录和宿主 Skill 发现能力。刷新前可继续明确读取包装文件或上游文件。

## 软件依赖与数据边界

Skill 文档注册与分析软件安装是两件事；本次未安装 Python/R 包、MaxQuant 或数据库，未读取真实实验数据进行分析。

当前 Python 环境检查：

- 可用：pandas 2.2.3、NumPy 2.3.5、SciPy 1.17.0、Matplotlib 3.10.8、Seaborn 0.13.2、scikit-learn 1.8.0、openpyxl 3.1.5、lxml 6.1.1。
- 缺失：pyopenms、matchms、statsmodels、patsy、gseapy、requests、可选的 pymaxquant。
- PATH 中未找到：R、Rscript、conda、MaxQuant/MaxQuantCmd、dotnet。这不等于断言机器所有目录均无这些软件。
- 未下载或验证：HMDB XML、参考谱库、菌株蛋白数据库、UniProt/GO/KEGG 注释映射及本地 GMT 基因集；网络 API 的可用性也不包含在文件注册验证中。

金钱松代谢物不能以 HMDB 的人体覆盖范围作为完整植物鉴定依据；茄链格孢菌富集需匹配菌株/物种、ID 映射和实际检测背景。数据库名称字符串并不保证离线可用。统计和绘图 Skill 的基本部分可使用现有依赖，但任何具体工作流仍须逐项预检。

## 使用示例与更新

刷新列表后，在 Codex CLI/IDE 中：

```text
$pyopenms-mass-spectrometry 请先检查 LC-MS 数据处理所需条件，暂不读取真实数据。
$maxquant-proteomics 请先核对蛋白定量表分析方案及缺失依赖。
$omics-plotting 请根据已确认的数据结构选择图形，先不要运行。
```

将来更新子模块后，应重新核对 registry 名称、源路径和上游资源；入口有效不意味着上游 API 示例与当前安装版本必然兼容。所有科研原始文件只读，输出另存，并记录版本、参数和校正方法。

分支：`codex/thesis-native-skills`。此配置通过分支提交供审阅，不直接提交或合并到 main。
