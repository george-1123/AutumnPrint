# Autumn-ai · Autumn Print

面向 FDM 打印工作室、打印农场和企业打样中心的 **3D 打印工艺与生产助手**。

围绕一笔打印订单，逐步集成：

**模型与需求 → Orca 真实切片比较 → 首件试打与实测 → 工艺批准 → 批量生产 → 异常补打 → 质量齐套与交付。**

OrcaSlicer 负责实际切片与已有校准能力；Autumn 组织任务、试验、工艺版本、人员协作和生产结果。产品重点是让经过验证的工艺可追溯、可复用，并持续跟进订单中的质量与数量缺口。

前端采用 **Electron + React + TypeScript + Three.js** 桌面工作台。后端以 FastAPI、PostgreSQL、LangGraph 与 Linux Celery/Redis 为基线，原生 Python 现场端负责 Orca 和设备接入；关闭桌面窗口不等于取消生产任务。

## 当前状态

项目处于规划与研究阶段，应用代码尚未实现，暂未提供可运行服务。后续在同一工程中逐阶段交付，保留已有入口、数据与功能。

首个验收场景是一笔 50 套黑色 PETG 卡扣支架订单，每套含 1 个底座与 2 个卡扣。开发过程逐步加入首件装配问题、参数试验、批次失败、模型变更和补打交付。

## 开发与调研

- [从 0 到 1 的集成开发指南](guide.md)：阶段 0–11 的实现内容、版本路线与累计验收。
- [完整技术设计](docs/technical-design.md)：桌面端、Agent、几何、切片、设备、权限、数据与部署。
- [技术选型调研](research/technology-selection.md)：高关注项目、稳定版本、维护信号、官方来源与取舍。
- [业务术语](CONTEXT.md)与[控制端/现场端决策](docs/adr/0001-control-plane-and-edge.md)。
- [OrcaSlicer 源码与产品方向调查](research/printing-orca-direction.md)。
- [打印工作室与 Orca 用户需求](research/printing-user-needs.md)。
- [现有产品、竞争与接入边界](research/printing-ecosystem.md)。

## 首个开发里程碑

建立项目骨架和订单样例，接通固定版本 OrcaSlicer 的实际切片，保存模型、有效配置、输出、警告与估算。之后让 Agent 调用同一工具链比较候选方案，再加入 Electron 工作台、试打和生产闭环。

切片估算、设备状态、实物测量和人员批准分别记录。早期不连接真实打印机；设备接入在对应阶段获得明确授权并完成条件核验后进行。
