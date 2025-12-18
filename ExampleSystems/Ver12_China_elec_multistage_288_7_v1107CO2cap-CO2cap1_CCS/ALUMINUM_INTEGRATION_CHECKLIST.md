# Aluminum 集成检查清单

## 概述
根据 `China_elec_multistage_288_7_v1107CO2cap_CCS_singleNode_aluminum` 的写法，将 aluminum 添加到 `Ver12_China_elec_multistage_288_7_v1107CO2cap-CO2cap1_CCS` 中。

**关键差异**：
- 源系统：单节点（Region15Shandong）
- 目标系统：31节点（中国各省）
- 数据来源：`data/aluminum_demand/` 中的分省数据（单位：吨铝/秒）

---

## 一、省份名称与节点名称映射关系

### 需要检查的映射（省份名 → 节点名）

| 省份数据中的名称 | 节点名称格式 | 对应节点ID | 状态 |
|-----------------|------------|-----------|------|
| Anhui | Region12Anhui | elec_Region12Anhui | ⚠️ 需确认 |
| Chongqing | Region22Chongqing | elec_Region22Chongqing | ⚠️ 需确认 |
| Fujian | Region13Fujian | elec_Region13Fujian | ⚠️ 需确认 |
| Gansu | Region28Gansu | elec_Region28Gansu | ⚠️ 需确认 |
| Guangdong | Region19Guangdong | elec_Region19Guangdong | ⚠️ 需确认 |
| Guangxi | Region20Guangxi | elec_Region20Guangxi | ⚠️ 需确认 |
| Guizhou | Region24Guizhou | elec_Region24Guizhou | ⚠️ 需确认 |
| Hebei | Region3Hebei | elec_Region3Hebei | ⚠️ 需确认 |
| Heilongjiang | Region8Heilongjiang | elec_Region8Heilongjiang | ⚠️ 需确认 |
| Henan | Region16Henan | elec_Region16Henan | ⚠️ 需确认 |
| Hubei | Region17Hubei | elec_Region17Hubei | ⚠️ 需确认 |
| Hunan | Region18Hunan | elec_Region18Hunan | ⚠️ 需确认 |
| InnerMongolia | Region5Innermongolia | elec_Region5Innermongolia | ⚠️ 需确认（注意大小写） |
| Jiangsu | Region10Jiangsu | elec_Region10Jiangsu | ⚠️ 需确认 |
| Jiangxi | Region14Jiangxi | elec_Region14Jiangxi | ⚠️ 需确认 |
| Jilin | Region7Jilin | elec_Region7Jilin | ⚠️ 需确认 |
| Liaoning | Region6Liaoning | elec_Region6Liaoning | ⚠️ 需确认 |
| Ningxia | Region30Ningxia | elec_Region30Ningxia | ⚠️ 需确认 |
| Qinghai | Region29Qinghai | elec_Region29Qinghai | ⚠️ 需确认 |
| Shaanxi | Region27Shaanxi | elec_Region27Shaanxi | ⚠️ 需确认 |
| Shandong | Region15Shandong | elec_Region15Shandong | ⚠️ 需确认 |
| Shanxi | Region4Shanxi | elec_Region4Shanxi | ⚠️ 需确认 |
| Sichuan | Region23Sichuan | elec_Region23Sichuan | ⚠️ 需确认 |
| Tibet | Region26Tibet | elec_Region26Tibet | ⚠️ 需确认 |
| Xinjiang | Region31Xinjiang | elec_Region31Xinjiang | ⚠️ 需确认 |
| Yunnan | Region25Yunnan | elec_Region25Yunnan | ⚠️ 需确认 |
| Zhejiang | Region11Zhejiang | elec_Region11Zhejiang | ⚠️ 需确认 |

**注意**：
- 数据文件中有28个省份，但系统有31个节点（包括北京、天津、上海、海南）
- 需要确认哪些省份有 aluminum 产能/需求，哪些没有
- InnerMongolia 在数据中是 "InnerMongolia"，节点中是 "Innermongolia"（大小写不同）

---

## 二、需要修改的文件清单

### 1. 系统配置文件

#### 1.1 `system/commodities.json`
**操作**：添加新的商品类型
**需要添加**：
- "Aluminum"
- "Alumina"
- "AluminumScrap"
- "Bauxite"
- "Graphite"

**当前状态**：只有 Electricity, NaturalGas, Coal, CO2, Uranium

---

#### 1.2 `system/nodes_1.json` 到 `system/nodes_7.json`（7个文件）
**操作**：为每个时期添加新的节点类型

**需要添加的节点类型**：

1. **Aluminum 节点**（需求节点）
   - `id`: "aluminum_produced"
   - `type`: "Aluminum"
   - `time_interval`: "Aluminum"
   - `constraints`: {"AggregatedDemandConstraint": true}
   - `rhs_policy`: {"AggregatedDemandConstraint": <从需求数据计算>}
   - 注意：需求值需要从 `aluminum_demand_by_province.csv` 中按时期和场景汇总

2. **Alumina 节点**（需求节点）
   - `id`: "alumina_produced"
   - `type`: "Alumina"
   - `time_interval`: "Alumina"
   - `constraints`: {"AggregatedDemandConstraint": true}
   - `rhs_policy`: {"AggregatedDemandConstraint": 0}（或根据需求设置）

3. **AluminumScrap 节点**（资源节点，每个有产能的省份一个）
   - `type`: "AluminumScrap"
   - `time_interval`: "AluminumScrap"
   - `constraints`: {"BalanceConstraint": true}
   - `instance_data`: 为每个有产能的省份创建
     - `id`: "aluminumscrap_source_Region{数字}{省份名}"
     - `max_supply`: [<从数据获取或设置默认值>]
     - `price_supply`: [0]

4. **Bauxite 节点**（资源节点，每个有产能的省份一个）
   - `type`: "Bauxite"
   - `time_interval`: "Bauxite"
   - `constraints`: {"BalanceConstraint": true}
   - `instance_data`: 为每个有产能的省份创建
     - `id`: "bauxite_source_Region{数字}{省份名}"
     - `max_supply`: [100000]（或根据实际情况）
     - `price_supply`: [0]

5. **Graphite 节点**（资源节点，每个有产能的省份一个）
   - `type`: "Graphite"
   - `time_interval`: "Graphite"
   - `constraints`: {"BalanceConstraint": true}
   - `instance_data`: 为每个有产能的省份创建
     - `id`: "graphite_source_Region{数字}{省份名}"
     - `max_supply`: [100000]（或根据实际情况）
     - `price_supply`: [0]

**注意**：需要为每个时期（1-7）分别设置，需求值可能不同

---

### 2. Assets 文件（每个时期需要3个文件）

#### 2.1 `assets/assets_1/` 到 `assets/assets_7/`（7个文件夹）

每个文件夹需要添加3个新文件：

1. **`aluminumsmelting.json`**
   - 从单节点系统复制 `global_data` 部分（保持不变）
   - `instance_data` 部分需要为每个有产能的省份创建实例
   - 每个实例需要：
     - `id`: "aluminum_smelting_Region{数字}{省份名}"
     - `location`: "Region{数字}{省份名}"
     - `existing_capacity`: <从 `aluminum_capacity_by_province.csv` 读取，单位：吨铝/秒>
     - `aluminum_constraints`: {"MinFlowConstraint": true}
     - `edges`: 需要连接到对应的节点
       - `elec_edge`: 连接到 "elec_Region{数字}{省份名}"
       - `aluminum_edge`: 连接到 "aluminum_produced"
       - `alumina_edge`: 从 "alumina_produced" 连接
       - `graphite_edge`: 从 "graphite_source_Region{数字}{省份名}" 连接

2. **`aluminumrefining.json`**
   - 从单节点系统复制 `global_data` 部分
   - `instance_data` 部分需要为每个有产能的省份创建实例
   - 每个实例需要：
     - `id`: "aluminum_refining_Region{数字}{省份名}"
     - `location`: "Region{数字}{省份名}"
     - `existing_capacity`: 0（或根据实际情况）
     - `edges`: 连接到对应的节点

3. **`aluminaplant.json`**
   - 从单节点系统复制 `global_data` 部分
   - `instance_data` 部分需要为每个有产能的省份创建实例
   - 每个实例需要：
     - `id`: "alumina_plant_Region{数字}{省份名}"
     - `location`: "Region{数字}{省份名}"
     - `existing_capacity`: 0（或根据实际情况）
     - `edges`: 连接到对应的节点
       - `fuel_edge`: 连接到 "natgas_Region{数字}{省份名}"

---

## 三、数据准备

### 3.1 检查数据文件
- ✅ `data/aluminum_demand/aluminum_capacity_by_province.csv` - 已存在
- ✅ `data/aluminum_demand/aluminum_demand_by_province.csv` - 已存在

### 3.2 需要处理的数据
1. **现有装机容量**（`aluminum_capacity_by_province.csv`）
   - 列：`Province`, `Capacity_10kt_per_year`, `Capacity_tons_per_second`
   - 使用 `Capacity_tons_per_second` 列作为 `existing_capacity`

2. **需求数据**（`aluminum_demand_by_province.csv`）
   - 列：`Province`, `Year`, `Scenario`, `Demand_tons_per_second`
   - 需要按时期（Period）和场景（Scenario）汇总
   - 时期对应关系需要确认（Year 2025, 2030, 2035, 2040, 2045, 2050, 2055, 2060 → Period 1-7）

---

## 四、实施步骤

### 步骤 1：验证省份名称映射
- [ ] 确认所有28个省份在数据中的名称与节点名称的对应关系
- [ ] 特别检查 InnerMongolia/Innermongolia 的大小写
- [ ] 确认哪些省份有 aluminum 产能（从 capacity 文件检查）
- [ ] 确认哪些省份有 aluminum 需求（从 demand 文件检查）

### 步骤 2：更新 commodities.json
- [ ] 添加 5 个新商品类型

### 步骤 3：更新 nodes 文件（7个文件）
- [ ] 为每个时期添加 Aluminum 需求节点
- [ ] 为每个时期添加 Alumina 需求节点
- [ ] 为每个有产能的省份添加 AluminumScrap 资源节点
- [ ] 为每个有产能的省份添加 Bauxite 资源节点
- [ ] 为每个有产能的省份添加 Graphite 资源节点
- [ ] 计算每个时期的 Aluminum 总需求（从 demand 文件）

### 步骤 4：创建 assets 文件（21个文件 = 7个时期 × 3个文件类型）
- [ ] 为每个时期创建 `aluminumsmelting.json`
  - [ ] 复制 global_data
  - [ ] 为每个有产能的省份创建 instance_data
  - [ ] 设置 existing_capacity（从 capacity 文件）
- [ ] 为每个时期创建 `aluminumrefining.json`
- [ ] 为每个时期创建 `aluminaplant.json`

### 步骤 5：验证
- [ ] 检查所有 JSON 文件格式正确
- [ ] 检查所有节点 ID 和边连接正确
- [ ] 检查单位一致性（吨铝/秒）
- [ ] 检查时期对应关系正确

---

## 五、注意事项

1. **单位统一**：所有数据单位已统一为"吨铝/秒"，直接使用即可

2. **时期对应**：
   - Period 1 → Year 2025?
   - Period 2 → Year 2030?
   - Period 3 → Year 2035?
   - Period 4 → Year 2040?
   - Period 5 → Year 2045?
   - Period 6 → Year 2050?
   - Period 7 → Year 2055 或 2060?
   - **需要确认**

3. **场景选择**：
   - demand 文件中有 low, mid, high 三个场景
   - **需要确认使用哪个场景**

4. **省份筛选**：
   - 只对有产能或需求的省份创建 assets
   - 从 capacity 文件可以知道哪些省份有产能
   - 从 demand 文件可以知道哪些省份有需求

5. **节点命名一致性**：
   - 确保所有节点 ID 使用相同的命名格式
   - 确保所有边连接使用正确的节点 ID

---

## 六、待确认问题

1. ⚠️ **时期与年份的对应关系**：Period 1-7 对应哪些年份？
2. ⚠️ **场景选择**：使用 low/mid/high 哪个场景？
3. ⚠️ **省份名称映射**：InnerMongolia vs Innermongolia 的大小写问题
4. ⚠️ **需求汇总**：Aluminum 总需求是按时期汇总所有省份，还是按其他方式？
5. ⚠️ **AluminumScrap 供应量**：单节点系统设置为 11，多节点系统如何设置？
6. ⚠️ **Alumina 需求**：单节点系统设置为 0，多节点系统是否也设为 0？

---

## 七、参考文件

### 源系统（单节点）
- `China_elec_multistage_288_7_v1107CO2cap_CCS_singleNode_aluminum/assets/assets_1/aluminumsmelting.json`
- `China_elec_multistage_288_7_v1107CO2cap_CCS_singleNode_aluminum/assets/assets_1/aluminumrefining.json`
- `China_elec_multistage_288_7_v1107CO2cap_CCS_singleNode_aluminum/assets/assets_1/aluminaplant.json`
- `China_elec_multistage_288_7_v1107CO2cap_CCS_singleNode_aluminum/system/commodities.json`
- `China_elec_multistage_288_7_v1107CO2cap_CCS_singleNode_aluminum/system/nodes_1.json`

### 目标系统（31节点）
- `Ver12_China_elec_multistage_288_7_v1107CO2cap-CO2cap1_CCS/data/aluminum_demand/aluminum_capacity_by_province.csv`
- `Ver12_China_elec_multistage_288_7_v1107CO2cap-CO2cap1_CCS/data/aluminum_demand/aluminum_demand_by_province.csv`
- `Ver12_China_elec_multistage_288_7_v1107CO2cap-CO2cap1_CCS/system/nodes_1.json`

