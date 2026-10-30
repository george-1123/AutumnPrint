# 打印生态更新与架构评审

[English](../../en/research/printing-ecosystem-update-2026-10-30.md) | 简体中文

评审日期：2026-10-30（Asia/Shanghai）。本次读取一手网页资料，未测试二进制、打印机或商业账户。这是研究建议，不修改已接受架构。

## 关注度与发布信号

Star 为 GitHub 实际显示约数，不是精确 API 值或全站排名。月日标签不能证明年份。Orca 发布索引还显示了 21 Nov 的 nightly，与客户端日期冲突，排除该项时间顺序，不编造解释。多数仓库元数据 API 读取失败。

| 项目 | 显示 Star | 发布/活动依据 | 相关性 |
| --- | ---: | --- | --- |
| [OrcaSlicer](https://github.com/OrcaSlicer/OrcaSlicer) | 16.2k | [稳定版 API](https://api.github.com/repos/OrcaSlicer/OrcaSlicer/releases/latest)：v2.4.2，prerelease=false，published_at=2026-07-07T03:33:49Z。[发布索引](https://github.com/OrcaSlicer/OrcaSlicer/releases)：v2.5.0-beta 明确预发布，显示 27 Oct 17:22；alpha 显示 16 Oct | 稳定执行与实验集成分开 |
| [OctoPrint](https://github.com/OctoPrint/OctoPrint) | 9.2k | [1.11.8](https://github.com/OctoPrint/OctoPrint/releases/tag/1.11.8) 标记 Latest，显示 23 Jun；[2.0.0rc7](https://github.com/OctoPrint/OctoPrint/releases) 预发布，显示 20 Oct | 适配按版本，不默认最新 RC |
| [Spoolman](https://github.com/Donkie/Spoolman) | 3.0k | [v0.27.0](https://github.com/Donkie/Spoolman/releases) Latest，显示 25 Sep；增加 NFC/RFID 身份及扫描定位材料卷/耗材 | 实体卷身份比材料名称更有用 |
| [Obico server](https://github.com/TheSpaghettiDetective/obico-server) | 1.9k | 本次未独立确认新的发布日期 | 观察来源，不是质检验收 |
| [Moonraker](https://github.com/Arksine/moonraker) | 1.5k | 本次未独立确认稳定发布日期 | 关注较低但设备协议相关 |

## 新能力：Orca Python 插件

[官方插件指南](https://www.orcaslicer.com/wiki/plugins/plugins_getting_started)明确要求 nightly 或高于 2.4.2 的版本。[2.5 beta 说明](https://github.com/OrcaSlicer/OrcaSlicer/releases/tag/v2.5.0-beta)介绍修改活动预设和后台 Scripts。这是文档能力，不是已测试集成，也不保证稳定 2.4.2 可用。

**推论：** 保留独立现场端/CLI 基线，用同一协议单独评估可选插件桥。分开“已验收稳定引擎/CLI”与“主动选择预发布/插件”两条兼容路径。默认稳定安装包不依赖插件，也无需为聊天界面维护整套 C++ 分叉。

[CLI Actions](https://www.orcaslicer.com/wiki/cli/cli_actions)列出生效配置导出、缓存导出/加载、进度管道、未修复模型信息。为每个二进制生成能力清单，逐项测试实际依赖的选项；最新 Wiki 不证明稳定包包含所有选项。

## 功能比较

[Printago Orders](https://docs.printago.io/docs/commerce/orders)已有 SKU/部件到作业的映射、订单变化调整、失败、缺 SKU 关联、交期及建议增删作业。[SimplyPrint AutoPrint](https://help.simplyprint.io/en/article/autoprint-put-your-printers-on-autopilot-1hssb9u/)说明可用性/清床后自动匹配任务，部分能力受计划限制。上述资料没有展示等同 Autumn 所提“已验证工艺/合格齐套”的实物验收体系。

**推论：** 排队加聊天不足以差异化。应沿同一订单演示首件失败、证据支持的参数试验、限定适用的工艺批准、模型变更、部分合格产出、正确缺口/补打/齐套。对手文档不证明此组合独有或商业上更优。

## 当前文档的优先缺口

| 优先级 | 缺口与影响 | 具体新增验收 |
| --- | --- | --- |
| P1 | F-04 与安装即用缺少经过测试的引擎/预设包契约 | 干净 Windows 不依赖原 Orca 预设导入获准 3MF，保存原始/生效设置，拒绝不支持覆盖，并由目标 Orca 打开导出成果 |
| P1 | F-09/F-10 需要明确订单变化与数量转换 | 版本变化预览增删任务；拒绝重复分配，保留部分合格，测试首件计入及撤销 |
| P1 | ready/设备观察需要适配语义 | [Moonraker](https://moonraker.readthedocs.io/en/latest/external_api/printer/)要求 Klippy 连接且常需 ready；查询字段缺失可能不报错。缺失/过期不能默认就绪 |
| P2 | 材料记录缺操作者身份识别/预留流程 | 识别卷、装载机器、计划预留、实测余量、消耗/退料/纠正并确定唯一账本；可集成 Spoolman 扫描 |
| P2 | 监控可能与健康打印混淆 | [Obico Objects](https://www.obico.io/docs/api/api-objects/)区分启用、未监控原因、置信度和自动暂停；与实物质量及动作拥有者分开记录 |
| P2 | 排队/规划范围较大，人工处置流程不足 | 在追求自主优化前，显示阻塞、证据、下一人、重试/核查选项与版本影响 |

保留控制/现场分离、动作日志、不可变成果、人工实物验收及本地/服务器共用规则。新版本应促成针对性兼容实验，不是按 Star 推翻架构。

本次本地依据：[功能](../product/functional-spec.md)、[运行](../architecture/runtime-and-deployment.md)、[需求](../product/requirements.md)。
