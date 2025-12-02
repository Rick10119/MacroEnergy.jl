# 中国电力系统多阶段规划模型示例

## 系统概述

这是一个基于中国31个省级行政区的电力系统多阶段规划模型示例。该模型包含7个规划期，每个规划期5年，采用Benders分解算法进行优化求解。模型考虑了多种发电技术、储能、输电网络以及CO2排放约束。

## 系统规模

- **地理范围**: 31个省级行政区（北京、天津、河北、山西、内蒙古、辽宁、吉林、黑龙江、上海、江苏、浙江、安徽、福建、江西、山东、河南、湖北、湖南、广东、广西、海南、重庆、四川、贵州、云南、西藏、陕西、甘肃、青海、宁夏、新疆）
- **规划期数**: 7个规划期
- **规划期长度**: 每个规划期5年
- **时间分辨率**: 288小时，分为12个子周期，每个子周期24小时
- **商品类型**: 电力（Electricity）、天然气（NaturalGas）、煤炭（Coal）、CO2、铀（Uranium）

## 目录结构

```text
China_elec_multistage_288_7_v1107CO2cap-noCO2_CCS/
├── assets/                    # 资产配置文件（按规划期组织）
│   ├── assets_1/             # 第1规划期的资产配置
│   │   ├── thermal.json      # 热力发电资产（燃煤、燃气、核电等）
│   │   ├── vre.json          # 可再生能源资产（光伏、风电）
│   │   ├── hydropower.json   # 水电资产
│   │   ├── storage.json      # 储能资产（电池等）
│   │   └── transmission.json # 输电线路资产
│   ├── assets_2/ ... assets_7/  # 第2-7规划期的资产配置
│
├── system/                    # 系统数据文件
│   ├── nodes_1.json ... nodes_7.json  # 各规划期的节点定义（31个电力节点）
│   ├── commodities.json      # 商品定义（电力、天然气、煤炭、CO2、铀）
│   ├── time_data.json        # 时间数据配置（288小时，12个子周期）
│   ├── demand_1.csv ... demand_7.csv  # 各规划期的电力需求时间序列（31个区域）
│   ├── fuel_prices_1.csv ... fuel_prices_7.csv  # 各规划期的燃料价格时间序列
│   └── vre_availability_1.csv ... vre_availability_7.csv  # 各规划期的VRE可用性系数
│
├── settings/                  # 模型配置设置
│   ├── case_settings.json    # 案例设置（规划期长度、贴现率、求解算法）
│   ├── macro_settings.json   # MacroEnergy框架设置（约束缩放、输出格式）
│   └── benders_settings.json # Benders算法设置（最大迭代次数、收敛容差等）
│
├── run.jl                    # 标准运行脚本（使用Gurobi求解器）
├── run_benders.jl           # Benders分解运行脚本（使用Gurobi求解器）
├── run_benders_HiGHS.jl    # Benders分解运行脚本（使用HiGHS求解器）
│
├── results_001/             # 结果输出目录
│   ├── results_period_1/ ... results_period_7/  # 各规划期的结果
│   │   ├── capacity.csv      # 容量投资结果
│   │   ├── costs.csv         # 成本结果
│   │   ├── flows.csv         # 流量结果
│   │   └── undiscounted_costs.csv  # 未贴现成本
│   └── settings.json        # 输出设置
│
└── tmp/                      # 临时文件目录
    └── UserAdditions.jl     # 用户自定义代码
```

## 数据框架说明

### 1. 资产配置（assets/）

每个规划期（assets_1 到 assets_7）包含以下资产类型：

- **thermal.json**: 热力发电资产
  - 燃煤发电、燃气发电、核电等
  - 包含燃料消耗、CO2排放率、运行约束（最小运行时间、爬坡限制等）
  - 支持容量扩展和退役

- **vre.json**: 可变可再生能源资产
  - 集中式光伏（PV_Central）
  - 分布式光伏（PV_Distribution）
  - 陆上风电（Wind_Onshore）
  - 海上风电（Wind_Offshore）
  - 通过vre_availability CSV文件提供可用性系数

- **hydropower.json**: 水电资产
  - 各区域的水电装机容量和可用性

- **storage.json**: 储能资产
  - 电池储能系统
  - 包含充放电效率、容量约束等

- **transmission.json**: 输电线路资产
  - 区域间输电线路
  - 包含线路容量、损耗率、投资成本等

### 2. 系统数据（system/）

- **nodes_X.json**: 定义各规划期的电力节点
  - 31个电力节点，每个节点对应一个省级行政区
  - 包含需求时间序列引用、非服务需求（NSD）约束和价格分段

- **commodities.json**: 定义系统中的商品
  - 电力、天然气、煤炭、CO2、铀

- **time_data.json**: 时间数据配置
  - 总建模小时数：288小时
  - 子周期数：12个
  - 每个子周期：24小时
  - 各商品的时间步长和子周期长度

- **demand_X.csv**: 电力需求时间序列
  - 31列，对应31个区域的电力需求（MW）
  - 288行，对应288个时间步

- **fuel_prices_X.csv**: 燃料价格时间序列
  - 各规划期的燃料价格数据

- **vre_availability_X.csv**: VRE可用性系数
  - 各VRE资产在不同时间步的可用性系数（0-1之间）
  - 包含所有VRE资产（光伏、风电）的可用性数据

### 3. 配置设置（settings/）

- **case_settings.json**:
  - `PeriodLengths`: [5,5,5,5,5,5,5] - 各规划期长度（年）
  - `DiscountRate`: 0.045 - 贴现率（4.5%）
  - `SolutionAlgorithm`: "Benders" - 求解算法（Benders分解）

- **macro_settings.json**:
  - `ConstraintScaling`: true - 启用约束缩放
  - `OutputLayout`: "wide" - 输出格式（宽格式）

- **benders_settings.json**:
  - `MaxIter`: 50 - 最大迭代次数
  - `MaxCpuTime`: 7200 - 最大CPU时间（秒）
  - `ConvTol`: 1e-3 - 收敛容差
  - `StabParam`: 0.5 - 稳定化参数
  - `IntegerInvestment`: false - 是否整数投资决策

## 运行脚本说明

### 1. run.jl

标准运行脚本，使用Gurobi求解器进行单阶段优化：

```julia
using MacroEnergy
using Gurobi

(system, model) = run_case(@__DIR__; 
                    optimizer=Gurobi.Optimizer,
                    optimizer_attributes=("Method" => 2, "Crossover" => 0, "BarConvTol" => 1e-3));
```

### 2. run_benders.jl

使用Benders分解算法，主问题和子问题都使用Gurobi求解器：

```julia
using MacroEnergy
using Gurobi

(system, results) = run_case(@__DIR__;
    planning_optimizer=Gurobi.Optimizer,
    subproblem_optimizer=Gurobi.Optimizer,
    planning_optimizer_attributes=("Method" => 2, "Crossover" => 0, "BarConvTol" => 1e-3),
    subproblem_optimizer_attributes=("Method" => 2, "Crossover" => 1, "BarConvTol" => 1e-3));
```

### 3. run_benders_HiGHS.jl

使用Benders分解算法，主问题和子问题都使用HiGHS求解器（开源求解器）：

```julia
using MacroEnergy
using HiGHS

(system, model) = run_case(@__DIR__;
    planning_optimizer=HiGHS.Optimizer,
    subproblem_optimizer=HiGHS.Optimizer,
    planning_optimizer_attributes=("solver" => "ipm", "run_crossover" => "off", "ipm_optimality_tolerance" => 1e-3),
    subproblem_optimizer_attributes=("solver" => "ipm", "run_crossover" => "on", "ipm_optimality_tolerance" => 1e-3));
```

## 输出结果

运行完成后，结果保存在 `results_001/` 目录下，每个规划期包含：

- **capacity.csv**: 各资产的容量投资和退役决策
- **costs.csv**: 各类成本（投资成本、运行成本、燃料成本等）
- **flows.csv**: 各边的流量（电力流、燃料流、CO2流等）
- **undiscounted_costs.csv**: 未贴现的成本数据

## 模型特点

1. **多阶段规划**: 7个规划期，每个5年，共35年规划期
2. **多区域**: 覆盖中国31个省级行政区
3. **多技术**: 包含传统热力发电、可再生能源、水电、储能等多种技术
4. **CO2约束**: 考虑CO2排放约束（但本案例中不包含CCS技术）
5. **时间分辨率**: 288小时代表性时间序列，12个子周期
6. **Benders分解**: 使用Benders分解算法处理大规模多阶段优化问题

## 注意事项

- 本案例名称中包含"noCO2_CCS"，表示不包含CO2捕获与封存（CCS）技术
- 模型使用Benders分解算法，适合大规模多阶段规划问题
- 需要安装相应的求解器（Gurobi或HiGHS）才能运行
- 各规划期的数据文件需要保持一致的格式和结构
