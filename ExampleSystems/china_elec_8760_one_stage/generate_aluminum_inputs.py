#!/usr/bin/env python
"""
generate_aluminum_inputs.py

为 china_elec_8760_one_stage（单阶段，8760小时）自动生成/修改铝相关输入：
- system/commodities.json
- system/nodes_1.json
- assets/assets_1/ 下的 aluminumsmelting.json, aluminumrefining.json, aluminaplant.json
- system/time_data.json

假设/约定：
- 只有一个阶段（period 1），对应 2025 年
- 总小时数 = 8760（全年）
- 2025 年总需求固定为 4000 (10kt/年)
- 需求转换：10kt/年 → 8760 小时总吨数
    demand_8760h = value_10kt_per_year * 10_000 * 8760 / 8760 = value_10kt_per_year * 10_000
- 产能极小的省份也包含在资产中，但 existing_capacity 设为 0
"""

import json
import csv
import os
from copy import deepcopy


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 省份到节点名称的映射
PROVINCE_TO_REGION = {
    "Anhui":         ("Region12Anhui",        12),
    "Chongqing":     ("Region22Chongqing",    22),
    "Fujian":        ("Region13Fujian",       13),
    "Gansu":         ("Region28Gansu",        28),
    "Guangdong":     ("Region19Guangdong",    19),
    "Guangxi":       ("Region20Guangxi",      20),
    "Guizhou":       ("Region24Guizhou",      24),
    "Hebei":         ("Region3Hebei",         3),
    "Heilongjiang":  ("Region8Heilongjiang",  8),
    "Henan":         ("Region16Henan",        16),
    "Hubei":         ("Region17Hubei",        17),
    "Hunan":         ("Region18Hunan",        18),
    "InnerMongolia": ("Region5Innermongolia", 5),  # 注意大小写差异
    "Jiangsu":       ("Region10Jiangsu",      10),
    "Jiangxi":       ("Region14Jiangxi",      14),
    "Jilin":         ("Region7Jilin",         7),
    "Liaoning":      ("Region6Liaoning",      6),
    "Ningxia":       ("Region30Ningxia",      30),
    "Qinghai":       ("Region29Qinghai",      29),
    "Shaanxi":       ("Region27Shaanxi",      27),
    "Shandong":      ("Region15Shandong",     15),
    "Shanxi":        ("Region4Shanxi",        4),
    "Sichuan":       ("Region23Sichuan",      23),
    "Tibet":         ("Region26Tibet",        26),
    "Xinjiang":      ("Region31Xinjiang",     31),
    "Yunnan":        ("Region25Yunnan",       25),
    "Zhejiang":      ("Region11Zhejiang",     11),
}


def convert_10kt_per_year_to_8760h_tons(x_10kt_year: float) -> float:
    """8760小时是全年，所以直接乘以10000即可"""
    return x_10kt_year * 10_000.0


def load_total_demand_2025(demand_2025_10kt: float = 4000.0) -> float:
    """返回2025年的8760小时总需求（吨）"""
    return convert_10kt_per_year_to_8760h_tons(demand_2025_10kt)


def load_province_capacity():
    """从CSV读取省份产能数据"""
    # 尝试从当前目录或上级目录的Ver12案例读取数据
    cap_csv_paths = [
        os.path.join(BASE_DIR, "data", "aluminum_demand", "aluminum_capacity_by_province.csv"),
        os.path.join(BASE_DIR, "..", "Ver12_China_elec_multistage_288_7_v1107CO2cap-CO2cap1_CCS", 
                     "data", "aluminum_demand", "aluminum_capacity_by_province.csv"),
    ]
    
    cap_csv_path = None
    for path in cap_csv_paths:
        if os.path.exists(path):
            cap_csv_path = path
            break
    
    if cap_csv_path is None:
        raise FileNotFoundError(
            f"找不到 aluminum_capacity_by_province.csv。"
            f"请确保文件存在于以下位置之一：\n" + "\n".join(cap_csv_paths)
        )
    
    print(f"  读取产能CSV: {cap_csv_path}")
    
    with open(cap_csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    # 自动检测列名（处理可能的BOM或空格）
    if not rows:
        raise ValueError("CSV文件为空")
    
    first_row = rows[0]
    province_col = None
    capacity_col = None
    
    for key in first_row.keys():
        if "province" in key.lower():
            province_col = key
        if "capacity_tons_per_second" in key.lower():
            capacity_col = key
    
    if province_col is None or capacity_col is None:
        raise ValueError(f"CSV文件缺少必要的列。找到的列: {list(first_row.keys())}")
    
    capacity_eps = 1e-4
    province_info = {}
    
    for row in rows:
        prov = row[province_col].strip()
        if prov not in PROVINCE_TO_REGION:
            print(f"  警告: 省份 {prov} 不在映射表中，跳过")
            continue
        
        region_str, region_num = PROVINCE_TO_REGION[prov]
        try:
            cap_tps = float(row[capacity_col])
        except (ValueError, KeyError):
            print(f"  警告: 省份 {prov} 的产能数据无效，设为0")
            cap_tps = 0.0
        
        existing_cap = 0.0 if cap_tps < capacity_eps else cap_tps
        
        province_info[prov] = {
            "province": prov,
            "region_str": region_str,
            "region_num": region_num,
            "existing_capacity": existing_cap,
        }
    
    print(f"  成功加载 {len(province_info)} 个省份的产能数据")
    return province_info


def update_commodities():
    """更新 system/commodities.json"""
    commodities_path = os.path.join(BASE_DIR, "system", "commodities.json")
    print(f"更新 commodities 文件: {commodities_path}")
    
    with open(commodities_path, "r", encoding="utf-8") as f:
        commodities_data = json.load(f)
    
    if "commodities" not in commodities_data:
        raise KeyError('commodities.json 不包含键 "commodities"')
    
    current = set(commodities_data["commodities"])
    to_add = ["Aluminum", "Alumina", "AluminumScrap", "Bauxite", "Graphite"]
    
    for c in to_add:
        if c not in current:
            commodities_data["commodities"].append(c)
    
    with open(commodities_path, "w", encoding="utf-8") as f:
        json.dump(commodities_data, f, indent=4, ensure_ascii=False)
    
    print("  ✓ commodities.json 已更新")


def update_time_data():
    """更新 system/time_data.json"""
    time_data_path = os.path.join(BASE_DIR, "system", "time_data.json")
    print(f"更新 time_data 文件: {time_data_path}")
    
    with open(time_data_path, "r", encoding="utf-8") as f:
        time_data = json.load(f)
    
    # 添加铝相关商品的时间设置
    aluminum_commodities = ["Aluminum", "Alumina", "AluminumScrap", "Bauxite", "Graphite"]
    
    if "HoursPerTimeStep" not in time_data:
        time_data["HoursPerTimeStep"] = {}
    if "HoursPerSubperiod" not in time_data:
        time_data["HoursPerSubperiod"] = {}
    
    for comm in aluminum_commodities:
        time_data["HoursPerTimeStep"][comm] = 1
        time_data["HoursPerSubperiod"][comm] = 8760  # 全年
    
    with open(time_data_path, "w", encoding="utf-8") as f:
        json.dump(time_data, f, indent=4, ensure_ascii=False)
    
    print("  ✓ time_data.json 已更新")


def update_nodes_1(total_demand_8760h: float, province_info: dict):
    """更新 system/nodes_1.json"""
    nodes_path = os.path.join(BASE_DIR, "system", "nodes_1.json")
    print(f"更新 nodes 文件: {nodes_path}")
    
    with open(nodes_path, "r", encoding="utf-8") as f:
        nodes_data = json.load(f)
    
    nodes_vec = list(nodes_data["nodes"])
    
    # 删除已有的铝相关节点
    nodes_vec = [
        n for n in nodes_vec
        if n.get("type", "") not in ("Aluminum", "Alumina", "AluminumScrap", "Bauxite", "Graphite")
    ]
    
    # 添加 Aluminum 节点
    nodes_vec.append({
        "type": "Aluminum",
        "global_data": {
            "time_interval": "Aluminum",
            "constraints": {
                "AggregatedDemandConstraint": True,
            },
        },
        "instance_data": [
            {
                "id": "aluminum_produced",
                "rhs_policy": {
                    "AggregatedDemandConstraint": total_demand_8760h,
                },
            },
        ],
    })
    
    # 添加 Alumina 节点
    nodes_vec.append({
        "type": "Alumina",
        "global_data": {
            "time_interval": "Alumina",
            "constraints": {
                "AggregatedDemandConstraint": True,
            },
        },
        "instance_data": [
            {
                "id": "alumina_produced",
                "rhs_policy": {
                    "AggregatedDemandConstraint": 0,
                },
            },
        ],
    })
    
    # 添加资源节点（AluminumScrap, Bauxite, Graphite）
    for res_type, id_prefix, max_supply in [
        ("AluminumScrap", "aluminumscrap_source", 0.0),
        ("Bauxite", "bauxite_source", 100000.0),
        ("Graphite", "graphite_source", 100000.0),
    ]:
        nodes_vec.append({
            "type": res_type,
            "global_data": {
                "time_interval": res_type,
                "constraints": {
                    "BalanceConstraint": True,
                },
            },
            "instance_data": [
                {
                    "id": f"{id_prefix}_{info['region_str']}",
                    "max_supply": [max_supply],
                    "price_supply": [0],
                }
                for info in province_info.values()
            ],
        })
    
    nodes_data["nodes"] = nodes_vec
    
    with open(nodes_path, "w", encoding="utf-8") as f:
        json.dump(nodes_data, f, indent=4, ensure_ascii=False)
    
    print("  ✓ nodes_1.json 已更新")


def generate_assets(province_info: dict):
    """生成 assets/assets_1/ 下的三个JSON文件"""
    # 从单节点案例读取模板
    single_base = os.path.join(
        BASE_DIR,
        "..",
        "China_elec_multistage_288_7_v1107CO2cap_CCS_singleNode_aluminum",
    )
    single_assets1 = os.path.join(single_base, "assets", "assets_1")
    
    if not os.path.exists(single_assets1):
        raise FileNotFoundError(
            f"找不到单节点案例的 assets 目录: {single_assets1}"
        )
    
    # 读取模板
    with open(os.path.join(single_assets1, "aluminumsmelting.json"), "r", encoding="utf-8") as f:
        smelting_tpl = json.load(f)
    with open(os.path.join(single_assets1, "aluminumrefining.json"), "r", encoding="utf-8") as f:
        refining_tpl = json.load(f)
    with open(os.path.join(single_assets1, "aluminaplant.json"), "r", encoding="utf-8") as f:
        plant_tpl = json.load(f)
    
    smelting_global = smelting_tpl["AluminumSmelting"][0]["global_data"]
    refining_global = refining_tpl["AluminumRefining"][0]["global_data"]
    plant_global = plant_tpl["AluminaPlant"][0]["global_data"]
    
    # 创建 assets_1 目录
    assets_dir = os.path.join(BASE_DIR, "assets", "assets_1")
    os.makedirs(assets_dir, exist_ok=True)
    
    # 生成实例数据
    smelting_instances = []
    refining_instances = []
    plant_instances = []
    
    for info in province_info.values():
        region_str = info["region_str"]
        existing_cap = info["existing_capacity"]
        
        # AluminumSmelting
        smelting_instances.append({
            "id": f"aluminum_smelting_{region_str}",
            "location": region_str,
            "existing_capacity": existing_cap,
            "aluminum_constraints": {
                "MinFlowConstraint": True,
            },
            "edges": {
                "elec_edge": {
                    "start_vertex": f"elec_{region_str}",
                    "end_vertex": f"aluminum_smelting_{region_str}",
                },
                "aluminum_edge": {
                    "start_vertex": f"aluminum_smelting_{region_str}",
                    "end_vertex": "aluminum_produced",
                },
                "alumina_edge": {
                    "start_vertex": "alumina_produced",
                    "end_vertex": f"aluminum_smelting_{region_str}",
                },
                "graphite_edge": {
                    "start_vertex": f"graphite_source_{region_str}",
                    "end_vertex": f"aluminum_smelting_{region_str}",
                },
            },
        })
        
        # AluminumRefining
        refining_instances.append({
            "id": f"aluminum_refining_{region_str}",
            "location": region_str,
            "existing_capacity": 0.0,
            "edges": {
                "elec_edge": {
                    "start_vertex": f"elec_{region_str}",
                    "end_vertex": f"aluminum_refining_{region_str}",
                },
                "aluminum_edge": {
                    "start_vertex": f"aluminum_refining_{region_str}",
                    "end_vertex": "aluminum_produced",
                },
                "aluminumscrap_edge": {
                    "start_vertex": f"aluminumscrap_source_{region_str}",
                    "end_vertex": f"aluminum_refining_{region_str}",
                },
            },
        })
        
        # AluminaPlant
        plant_instances.append({
            "id": f"alumina_plant_{region_str}",
            "location": region_str,
            "existing_capacity": 0.0,
            "edges": {
                "elec_edge": {
                    "start_vertex": f"elec_{region_str}",
                    "end_vertex": f"alumina_plant_{region_str}",
                },
                "alumina_edge": {
                    "start_vertex": f"alumina_plant_{region_str}",
                    "end_vertex": "alumina_produced",
                },
                "bauxite_edge": {
                    "start_vertex": f"bauxite_source_{region_str}",
                    "end_vertex": f"alumina_plant_{region_str}",
                },
                "fuel_edge": {
                    "start_vertex": f"natgas_{region_str}",
                    "end_vertex": f"alumina_plant_{region_str}",
                },
            },
        })
    
    # 写入文件
    smelting_obj = {
        "AluminumSmelting": [
            {
                "type": "AluminumSmelting",
                "global_data": smelting_global,
                "instance_data": smelting_instances,
            },
        ],
    }
    
    refining_obj = {
        "AluminumRefining": [
            {
                "type": "AluminumRefining",
                "global_data": refining_global,
                "instance_data": refining_instances,
            },
        ],
    }
    
    plant_obj = {
        "AluminaPlant": [
            {
                "type": "AluminaPlant",
                "global_data": plant_global,
                "instance_data": plant_instances,
            },
        ],
    }
    
    with open(os.path.join(assets_dir, "aluminumsmelting.json"), "w", encoding="utf-8") as f:
        json.dump(smelting_obj, f, indent=4, ensure_ascii=False)
    
    with open(os.path.join(assets_dir, "aluminumrefining.json"), "w", encoding="utf-8") as f:
        json.dump(refining_obj, f, indent=4, ensure_ascii=False)
    
    with open(os.path.join(assets_dir, "aluminaplant.json"), "w", encoding="utf-8") as f:
        json.dump(plant_obj, f, indent=4, ensure_ascii=False)
    
    print(f"  ✓ 已生成 assets/assets_1/ 下的3个JSON文件")


def main():
    print("Generating aluminum inputs for china_elec_8760_one_stage (Python script)...")
    
    # 2025年总需求（10kt/年）
    demand_2025_10kt = 4000.0
    total_demand_8760h = load_total_demand_2025(demand_2025_10kt)
    print(f"  2025年总需求（8760h，吨）: {total_demand_8760h:.2e}")
    
    # 加载省份产能
    province_info = load_province_capacity()
    
    # 更新文件
    update_commodities()
    update_time_data()
    update_nodes_1(total_demand_8760h, province_info)
    generate_assets(province_info)
    
    print("\n✓ Aluminum inputs generation completed.")


if __name__ == "__main__":
    main()

