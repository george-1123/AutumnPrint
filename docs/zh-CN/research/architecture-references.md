# 架构参考项目

[English](../../en/research/architecture-references.md) | 简体中文

来源：原技术设计的调研摘录。保留 2026-10-29 的研究语境，不代表重新核验或必须引入这些项目。正式方案见[架构总览](../architecture/overview.md)。

## 高关注项目如何参考

| 参考项目 | 学习内容 | 在 Autumn 中的处理 |
| --- | --- | --- |
| OpenClaw / Hermes | 本地运行、工具策略、历史信息与技能 | 借鉴机制；不直接开放通用 Shell 或任意设备操作 |
| DeerFlow | 长任务、受限子 Agent、成果、任务工作台 | 借鉴交互和组织方式，围绕打印业务实现 |
| OpenHands | 控制界面与执行后端拆分、隔离工作区 | 用于中心/现场端设计参考，不引入编码 Agent 充当生产控制器 |
| LangGraph | 节点、分支、中断与持久 checkpoint | 采用其图运行能力，业务状态由本项目拥有 |
| OrcaSlicer | 配置、切片、校准、设备适配经验 | 通过固定版本工具接入，避免初期维护大型 C++ 分叉 |
| Printago / SimplyPrint | 订单、队列、材料匹配、清床与生产交接 | 对照已有能力；若已作为机群调度方，则 Autumn 通过其接口工作 |
| Trimesh / PyMeshLab | 几何事实和限定修复能力 | 由工具返回检查证据，不让语言模型虚构几何结果 |

这些是有官方来源的代表性样本，不是全 GitHub 排名。关注度和更新时间均不足以证明对物理生产的可靠性。

## Orca 集成与资料依据

- [整套技术设计与模块边界](../architecture/overview.md)。
- [高关注项目、近期版本与选型依据](technology-selection.md)。
- [业务术语与边界](../CONTEXT.md)。
- [OrcaSlicer 官方项目](https://github.com/OrcaSlicer/OrcaSlicer)。
- [CLI 使用说明](https://www.orcaslicer.com/wiki/cli/cli_mode)。
- [校准指南](https://www.orcaslicer.com/wiki/guides/calibration_guide)。
- [本项目的源码与产品方向调查](printing-orca-direction.md)。
- [从业者需求证据](printing-user-needs.md)。
- [现有产品与接入边界](printing-ecosystem.md)。

本次研究确认的本地源码路径为 `D:\project\OrcaSlicer-main\OrcaSlicer-main`，当时版本标记为 `2.5.0-dev`。它是资料来源，当前指南不要求修改这个项目，也不等同于已安装可运行引擎。实施时以选定二进制的实际能力为准。

首期通过独立适配器调度 Orca，保留原有 GUI 便于人工检查。需要内嵌体验时再评估目标版本的插件能力。复用、修改或分发 Orca 及其组件前核查对应许可证，不仅凭调用方式推断适用义务。
