# Autumn-ai · Autumn Print

[English](../en/project.md) | 简体中文

面向个人 FDM 用户、打印工作室、打印农场和企业打样中心的 **3D 打印工艺与生产助手**。

围绕订单串联模型与需求、真实切片比较、首件试打、工艺批准、批量生产、异常补打和质量交付。

## 当前状态

项目处于设计与研究阶段，尚无应用代码、可运行服务或安装包。文档中的目录、命令、功能和验收均为待实现目标。

产品提供个人本地与企业服务器两种模式，共用业务 Agent；现场端执行 Orca、几何和设备工具。个人目标为安装后配置大模型 API 即可使用；企业用户连接服务器并登录。

## 文档入口

完整阅读顺序和正文归属见[文档目录](README.md)。

| 关注点 | 文档 |
| --- | --- |
| 用户、目标与产品范围 | [产品需求](product/requirements.md) |
| 完整功能、流程与业务验收 | [功能规格](product/functional-spec.md) |
| 系统、技术、数据和接口 | [架构总览](architecture/overview.md) |
| 本地/企业运行与恢复 | [运行部署](architecture/runtime-and-deployment.md) |
| Agent、工具与授权 | [Agent 与工具](architecture/agent-and-tools.md) |
| 应用目录和包依赖 | [仓库结构](architecture/repository.md) |
| 从零建立可运行工程 | [工程初始化](engineering/bootstrap.md) |
| 功能开发顺序 | [交付计划](engineering/delivery-plan.md) |
| 测试、故障与发布检查 | [验证计划](engineering/validation.md) |

## 术语、决策与依据

- [业务术语](CONTEXT.md)、[双模式及单仓库决策](adr/0002-dual-mode-monorepo.md)。
- [技术选型调研](research/technology-selection.md)、[架构参考项目](research/architecture-references.md)。
- [Orca 源码与方向](research/printing-orca-direction.md)、[用户需求证据](research/printing-user-needs.md)、[产品生态](research/printing-ecosystem.md)。

调研保存来源和历史判断，正式需求与架构以上述对应文档为准。原综合指南与技术设计路径保留为导航，不再维护重复正文。

默认英文；文档在 `docs/en/` 与 `docs/zh-CN/` 中使用对应文件名，中英同步维护编号、命令、来源链接、日期与决策状态。内部链接保持当前语言，通过顶部链接切换。仓库根目录只保留 README 入口。
