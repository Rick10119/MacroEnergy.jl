# 省份名称映射对照表

## 数据文件中的省份名称 → 节点系统中的节点名称

| 数据文件中的省份名 | 节点系统中的节点名 | 节点ID格式 | 是否有产能 | 产能值（吨铝/秒） |
|-------------------|------------------|-----------|-----------|-----------------|
| Anhui | Region12Anhui | elec_Region12Anhui | ✅ | 0.05120898401826484 |
| Chongqing | Region22Chongqing | elec_Region22Chongqing | ✅ | 0.01191494149543379 |
| Fujian | Region13Fujian | elec_Region13Fujian | ✅ | 0.019812835331050226 |
| Gansu | Region28Gansu | elec_Region28Gansu | ✅ | 0.0951675399543379 |
| Guangdong | Region19Guangdong | elec_Region19Guangdong | ✅ | 0.013000630707762558 |
| Guangxi | Region20Guangxi | elec_Region20Guangxi | ✅ | 0.09779885416666667 |
| Guizhou | Region24Guizhou | elec_Region24Guizhou | ✅ | 0.037187805365296804 |
| Hebei | Region3Hebei | elec_Region3Hebei | ✅ | 0.001642351598173516 |
| Heilongjiang | Region8Heilongjiang | elec_Region8Heilongjiang | ✅ | 0.004786900684931507 |
| Henan | Region16Henan | elec_Region16Henan | ✅ | 0.09442137557077626 |
| Hubei | Region17Hubei | elec_Region17Hubei | ✅ | 0.023077798230593607 |
| Hunan | Region18Hunan | elec_Region18Hunan | ✅ | 0.03915981164383562 |
| InnerMongolia | Region5Innermongolia | elec_Region5Innermongolia | ✅ | 0.16037204052511414 |
| Jiangsu | Region10Jiangsu | elec_Region10Jiangsu | ✅ | 0.018573176369863015 |
| Jiangxi | Region14Jiangxi | elec_Region14Jiangxi | ✅ | 0.05098987157534247 |
| Jilin | Region7Jilin | elec_Region7Jilin | ✅ | 0.0026293407534246577 |
| Liaoning | Region6Liaoning | elec_Region6Liaoning | ✅ | 0.017880308219178083 |
| Ningxia | Region30Ningxia | elec_Region30Ningxia | ✅ | 0.028814182363013696 |
| Qinghai | Region29Qinghai | elec_Region29Qinghai | ✅ | 0.05904568350456621 |
| Shaanxi | Region27Shaanxi | elec_Region27Shaanxi | ✅ | 0.03934536529680365 |
| Shandong | Region15Shandong | elec_Region15Shandong | ✅ | 0.16708357163242007 |
| Shanxi | Region4Shanxi | elec_Region4Shanxi | ✅ | 0.02944585616438356 |
| Sichuan | Region23Sichuan | elec_Region23Sichuan | ✅ | 0.03364253710045662 |
| Tibet | Region26Tibet | elec_Region26Tibet | ✅ | 8.290525114155251e-05 |
| Xinjiang | Region31Xinjiang | elec_Region31Xinjiang | ✅ | 0.16993992009132422 |
| Yunnan | Region25Yunnan | elec_Region25Yunnan | ✅ | 0.14626005850456622 |
| Zhejiang | Region11Zhejiang | elec_Region11Zhejiang | ✅ | 0.013655991723744293 |

## ⚠️ 重要注意事项

### 1. 大小写差异
- **数据文件**：`InnerMongolia`（驼峰命名）
- **节点系统**：`Innermongolia`（全小写）
- **处理方式**：在创建节点 ID 时使用 `Innermongolia`

### 2. 系统中有但数据中没有的节点
以下节点在系统中存在，但在 aluminum 数据文件中没有：
- Region1Beijing（北京）
- Region2Tianjin（天津）
- Region9Shanghai（上海）
- Region21Hainan（海南）

**处理方式**：这些节点不需要创建 aluminum 相关的 assets

### 3. 节点 ID 命名规则
在创建 aluminum 相关节点时，使用以下格式：
- `aluminum_smelting_Region{数字}{省份名}`
- `aluminum_refining_Region{数字}{省份名}`
- `alumina_plant_Region{数字}{省份名}`
- `aluminumscrap_source_Region{数字}{省份名}`
- `bauxite_source_Region{数字}{省份名}`
- `graphite_source_Region{数字}{省份名}`

**示例**：
- 山东：`aluminum_smelting_Region15Shandong`
- 内蒙古：`aluminum_smelting_Region5Innermongolia`（注意使用 Innermongolia）

### 4. 产能阈值
- 最小产能：Tibet 只有 8.29e-05 吨铝/秒（非常小）
- 最大产能：Xinjiang 有 0.1699 吨铝/秒
- **建议**：可以考虑设置一个最小阈值，低于该值的省份不创建 assets

## 快速参考：节点编号

| 节点编号 | 省份名（节点中） | 省份名（数据中） | 匹配 |
|---------|----------------|----------------|------|
| Region1 | Beijing | - | ❌ 无数据 |
| Region2 | Tianjin | - | ❌ 无数据 |
| Region3 | Hebei | Hebei | ✅ |
| Region4 | Shanxi | Shanxi | ✅ |
| Region5 | Innermongolia | InnerMongolia | ✅（注意大小写） |
| Region6 | Liaoning | Liaoning | ✅ |
| Region7 | Jilin | Jilin | ✅ |
| Region8 | Heilongjiang | Heilongjiang | ✅ |
| Region9 | Shanghai | - | ❌ 无数据 |
| Region10 | Jiangsu | Jiangsu | ✅ |
| Region11 | Zhejiang | Zhejiang | ✅ |
| Region12 | Anhui | Anhui | ✅ |
| Region13 | Fujian | Fujian | ✅ |
| Region14 | Jiangxi | Jiangxi | ✅ |
| Region15 | Shandong | Shandong | ✅ |
| Region16 | Henan | Henan | ✅ |
| Region17 | Hubei | Hubei | ✅ |
| Region18 | Hunan | Hunan | ✅ |
| Region19 | Guangdong | Guangdong | ✅ |
| Region20 | Guangxi | Guangxi | ✅ |
| Region21 | Hainan | - | ❌ 无数据 |
| Region22 | Chongqing | Chongqing | ✅ |
| Region23 | Sichuan | Sichuan | ✅ |
| Region24 | Guizhou | Guizhou | ✅ |
| Region25 | Yunnan | Yunnan | ✅ |
| Region26 | Tibet | Tibet | ✅ |
| Region27 | Shaanxi | Shaanxi | ✅ |
| Region28 | Gansu | Gansu | ✅ |
| Region29 | Qinghai | Qinghai | ✅ |
| Region30 | Ningxia | Ningxia | ✅ |
| Region31 | Xinjiang | Xinjiang | ✅ |

**总计**：28个省份有数据，27个省份需要创建 aluminum assets（Tibet 产能极小，可能需要排除）

