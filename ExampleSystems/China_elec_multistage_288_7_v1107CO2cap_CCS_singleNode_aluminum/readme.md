## 山东单省电力多阶段示例（含CO₂约束）

本示例基于 `China_elec_multistage_288_7_v1107CO2cap-传至服务器-CO2cap1_CCS` 案例，已经简化为**仅包含山东省（Region15Shandong）** 的单省电力系统，多规划阶段、多时间片，并考虑燃煤、燃气、电力需求、可再生能源及 CO₂ 排放约束/封存（CCS）等要素。

- **空间范围**：仅保留 `elec_Region15Shandong`、`natgas_Region15Shandong`、`coal_Region15Shandong` 等与山东相关的节点，取消所有跨省输电线路（`transmission.json` 中 `instance_data` 为空），形成单节点电力系统。
- **时间结构**：7 个阶段（对应 `nodes_1.json`–`nodes_7.json` 与 `demand_1.csv`–`demand_7.csv`），每个阶段包含多时段负荷与可再生资源出力时序。
- **资产与资源**：各阶段 `assets_*/thermal.json`、`hydropower.json`、`storage.json`、`vre.json` 中仅保留连接到山东节点的机组、储能和可再生能源。
- **燃料与排放**：`fuel_prices_*.csv` 仅通过 `natgas_Region15Shandong` 和 `coal_Region15Shandong` 列被引用，`CO2` 节点 `co2_sink_national` 提供全局 CO₂ 约束/价格。

该示例可用于在更小规模上测试多阶段规划、CCS 约束以及新能源与储能的协同作用，便于在单省层面快速调试与敏感性分析。