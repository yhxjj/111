---
name: "maxquant-proteomics"
description: "定量蛋白质组 MaxQuant 输出处理、proteinGroups 表检查、质控与差异分析。适用于 PAA/PAB 处理组和对照组的蛋白定量；原始谱图检索需单独核实 MaxQuant 和运行时。"
---

# maxquant-proteomics — SciAgent-Skills Codex 入口

本入口用于课题相关工作流的原生发现与按需加载。算法、参数、示例和配套资源以项目锁定版本的 SciAgent-Skills 为来源，不复制或改写上游文档。

## 先加载上游文档

1. 读取本入口相邻引用的 [上游 SKILL.md](../../../.sciagent-skills/skills/proteomics-protein-engineering/maxquant-proteomics/SKILL.md) 全文，再决定分析步骤。
2. 上述链接相对于**本文件所在目录**解析，不是相对于终端当前目录。定位项目根目录时可用 `git rev-parse --show-toplevel`，然后读取项目内 `.sciagent-skills/skills/proteomics-protein-engineering/maxquant-proteomics/SKILL.md`。从仓库任意子目录启动均应使用本文件目录或项目根目录解析。
3. 上游文档引用的 `references/`、`scripts/`、`assets/` 相对于**上游 SKILL.md 所在目录**解析，不能相对于本包装目录解析。
4. 如果上游文件不存在，停止依赖该文档的分析，报告子模块未初始化。由用户授权或任务范围允许时，在项目根运行 `git submodule update --init --recursive`；不得创建伪造文档替代它。

## 执行约定

- 确认数据是原始谱图还是已导出的定量表，核对污染物、反库和鉴定 FDR；明确独立生物学重复、缺失值、归一化及批次。
- 将上游示例视为需适配的示例，执行前确认输入、模型假设与所安装版本的 API。优先遵循项目指令和用户约束。
- 先检查解释器、命令及所需依赖；**入口可发现不代表 Python/R 包、外部软件或数据库已可用**。缺失时列出具体阻塞，不因加载本 Skill 自动执行安装命令。
- 使用独立环境；安装依赖、下载数据库、外部写入需在当前任务授权范围内。网络失败按用户要求停止，不永久修改网络配置。
- 原始科研数据只读，结果另存到任务指定目录；模拟数据及演示输出必须明确标记，不能作为实验结论。
- 记录工具/包版本、数据库版本、关键参数、统计校正及输出位置。不能把差异、谱库匹配或通路富集直接提升为作用机制或直接靶点的因果证据。

## 完成后报告

说明使用的上游流程、实际执行的分析、验证结果、输出路径及未解决依赖。若本次仅检查环境或读取文档，明确没有执行真实分析。
