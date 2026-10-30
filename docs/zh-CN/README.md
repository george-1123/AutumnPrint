# 文档目录

[English](../en/README.md) | 简体中文

项目尚处于设计阶段，应用代码、安装包与部署未实现。本文是文档导航；每项约定只在下表指定文档维护正文，其他文档通过链接引用。

最新评审：[2026-10-30 从 0 到 1 的架构与功能评审](research/architecture-functional-review-2026-10-30.md)，附 [Agent 一手证据](research/agent-framework-update-2026-10-30.md)和[打印生态证据](research/printing-ecosystem-update-2026-10-30.md)。结论是建议，不代表已接受架构变更或应用验收通过。

## 按问题阅读

| 层次    | 唯一正文来源                                         | 回答的问题                   |
| ----- | ---------------------------------------------- | ----------------------- |
| 需求    | [产品需求](product/requirements.md)                | 为谁做、解决什么、范围和成功标准是什么     |
| 功能    | [功能规格](product/functional-spec.md)             | 用户能做什么、流程/规则/异常及业务验收是什么 |
| 架构    | [架构总览](architecture/overview.md)               | 模块职责、技术、数据所有权及接口如何组织    |
| 运行    | [运行部署](architecture/runtime-and-deployment.md) | 个人/企业分别运行什么、如何启动/恢复/迁移  |
| Agent | [Agent 与工具](architecture/agent-and-tools.md)   | 角色、工具、授权和事实依据如何组织       |
| 工程结构  | [仓库结构](architecture/repository.md)             | 四应用三公共包放哪里、如何依赖与构建      |
| 初始化   | [工程初始化](engineering/bootstrap.md)              | 如何证明四应用和两种模式的工程链路可用     |
| 开发顺序  | [交付计划](engineering/delivery-plan.md)           | 功能按什么依赖与顺序实现            |
| 验证    | [验证计划](engineering/validation.md)              | 如何测试、故障注入、发布与记录证据       |
| 术语    | [领域语言](CONTEXT.md)                             | 业务词汇统一指什么               |
| 决策    | [双模式 ADR](adr/0002-dual-mode-monorepo.md)      | 为什么选择当前方案、付出什么代价        |
| 证据    | [调研目录](research/technology-selection.md)       | 技术和产品判断有哪些来源            |

## 目录与维护规则

```text
docs/zh-CN/                     # 与 docs/en/ 中的相对路径对应
├── README.md
├── project.md
├── CONTEXT.md
├── guide.md                     # 原指南导航
├── technical-design.md          # 原技术设计导航
├── deployment-and-project-structure.md
├── product/
│   ├── requirements.md
│   └── functional-spec.md
├── architecture/
│   ├── overview.md
│   ├── runtime-and-deployment.md
│   ├── agent-and-tools.md
│   └── repository.md
├── engineering/
│   ├── bootstrap.md
│   ├── delivery-plan.md
│   └── validation.md
├── adr/
└── research/
```

先阅读需求和功能，再按需要查架构；开始写代码前阅读仓库结构与初始化。新增或修改功能时维护需求/功能编号，再关联架构、交付和验证，不把技术选择写成用户需求，也不把开发阶段当成功能范围。

原综合文档在各语言目录中保留为[指南导航](guide.md)、[技术设计导航](technical-design.md)和[部署导航](deployment-and-project-structure.md)，不再维护综合正文。研究文档是来源与历史判断，不能覆盖正式需求或架构。[许可证](../en/LICENSE)保留英文原文，不修改法律文本。

## 语言约定

默认英文。仓库根目录仅保留英文 README 入口，其余文档按 `docs/en/` 和 `docs/zh-CN/` 分类，文件名及相对路径一一对应，包括项目概述、术语、架构决策、工程文档和调研。不要添加语言后缀或新的根目录文档。上图展示中文目录，英文目录的 Markdown 文件与之一一对应。

每次修改同时维护中英文，保持 R/F/B 编号、代码、命令、路径、来源链接、日期、数量和决策状态一致。内部链接留在当前语言，语言切换指向对应文档。英文为主要编辑基线，翻译不得形成另一套决策；发现差异时同步修正两份文档。
