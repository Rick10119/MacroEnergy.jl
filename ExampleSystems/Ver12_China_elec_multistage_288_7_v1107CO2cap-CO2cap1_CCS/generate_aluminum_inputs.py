#!/usr/bin/env python
"""
generate_aluminum_inputs.py

基于单节点铝案例和 Ver12 的数据结构，用 Python 自动生成 / 修改 Ver12 中的铝相关输入：
- system/commodities.json
- system/nodes_1.json ~ system/nodes_7.json
- assets/assets_1 ~ assets/assets_7 下的
  aluminumsmelting.json, aluminumrefining.json, aluminaplant.json

假设 / 约定：
- 使用 primary_aluminum_demand["mid"][year] 作为总铝需求（单位：10kt/年）
- 年份与 period 对应：
    period 1 → 2025
    period 2 → 2030
    period 3 → 2035
    period 4 → 2040
    period 5 → 2045
    period 6 → 2050
    period 7 → 2055
- 2025 年总需求固定为 4000 (10kt/年)，不从 JSON 读
- 需求转换：10kt/年 → 288 小时总吨数
    demand_288h = value_10kt_per_year * 10_000 * 288 / 8760
- 产能极小的省份也包含在资产中，但 existing_capacity 设为 0
"""

import json
import csv
import os
from copy import deepcopy


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 省份到节点名称的映射（与 PROVINCE_MAPPING.md 保持一致）
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


def convert_10kt_per_year_to_288h_tons(x_10kt_year: float) -> float:
    return x_10kt_year * 10_000.0 * 288.0 / 8760.0


def load_total_demand_per_period(demand_2025_10kt: float = 4000.0) -> dict:
    """读取 primary_aluminum_demand["mid"] 并转换为每个 period 的 288h 总需求（吨）"""
    demand_json_path = os.path.join(
        BASE_DIR,
        "data",
        "aluminum_demand",
        "aluminum_demand_all_scenarios.json",
    )
    with open(demand_json_path, "r", encoding="utf-8") as f:
        demand_data = json.load(f)

    prim_d = demand_data["primary_aluminum_demand"]["mid"]

    period_year_map = {
        1: "2025",
        2: "2030",
        3: "2035",
        4: "2040",
        5: "2045",
        6: "2050",
        7: "2055",
    }

    total = {}
    for p, ystr in period_year_map.items():
        if ystr == "2025":
            v_10kt = float(demand_2025_10kt)
        else:
            if ystr not in prim_d:
                raise KeyError(f"primary_aluminum_demand['mid'] 中缺少年份 {ystr}")
            v_10kt = float(prim_d[ystr])
        total[p] = convert_10kt_per_year_to_288h_tons(v_10kt)
    return total


def load_province_capacity() -> dict:
    """读取每个省份的 existing_capacity（吨/小时），小于阈值的记为 0"""
    cap_csv_path = os.path.join(
        BASE_DIR,
        "data",
        "aluminum_demand",
        "aluminum_capacity_by_province.csv",
    )
    capacity_eps = 1e-4  # 吨/小时的阈值
    info = {}
    with open(cap_csv_path, "r", encoding="utf-8-sig") as f:  # utf-8-sig 自动处理BOM
        reader = csv.DictReader(f)
        # 处理可能存在的 BOM 或不同拼写
        fieldnames = [fn for fn in (reader.fieldnames or [])]
        def _match(colname: str, target: str) -> bool:
            return colname.strip().lstrip("\ufeff").lower() == target.lower()

        prov_key = None
        cap_key = None
        for fn in fieldnames:
            fn_clean = fn.strip().lstrip("\ufeff")
            if prov_key is None and _match(fn_clean, "Province"):
                prov_key = fn
            # 支持多种可能的列名：Capacity_ton_per_h, Capacity_tons_per_hour, Capacity_tons_per_second
            if cap_key is None:
                if _match(fn_clean, "Capacity_ton_per_h") or \
                   _match(fn_clean, "Capacity_tons_per_hour") or \
                   _match(fn_clean, "Capacity_tons_per_second"):
                    cap_key = fn

        if prov_key is None or cap_key is None:
            raise KeyError(
                f"在 {cap_csv_path} 的表头中找不到 'Province' 或容量列，实际列名: {fieldnames}"
            )

        # 检查是否需要单位转换（如果列名是 tons_per_second，需要转换为 tons_per_hour）
        needs_conversion = "tons_per_second" in cap_key.lower() or "ton_per_second" in cap_key.lower()

        for row in reader:
            if not row:  # 跳过空行
                continue
            prov = row.get(prov_key, "").strip()
            if not prov:
                continue
            if prov not in PROVINCE_TO_REGION:
                # 允许静默跳过
                continue
            region_str, region_num = PROVINCE_TO_REGION[prov]
            cap_val = row.get(cap_key, "")
            if cap_val is None or cap_val == "":
                continue
            cap_value = float(cap_val)
            # 如果需要转换（从吨/秒到吨/小时）
            if needs_conversion:
                cap_value = cap_value * 3600.0  # 1 吨/秒 = 3600 吨/小时
            existing_cap = 0.0 if cap_value < capacity_eps else cap_value
            info[prov] = {
                "province": prov,
                "region_str": region_str,
                "region_num": region_num,
                "existing_capacity": existing_cap,  # 单位：吨/小时
            }
    return info


def update_commodities():
    path = os.path.join(BASE_DIR, "system", "commodities.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "commodities" not in data or not isinstance(data["commodities"], list):
        raise ValueError("commodities.json 不包含列表键 'commodities'")

    current = set(data["commodities"])
    to_add = ["Aluminum", "Alumina", "AluminumScrap", "Bauxite", "Graphite"]
    for c in to_add:
        if c not in current:
            data["commodities"].append(c)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def aluminum_node_block(total_demand_288h: float) -> dict:
    return {
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
                    "AggregatedDemandConstraint": total_demand_288h,
                },
            }
        ],
    }


def alumina_node_block() -> dict:
    return {
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
            }
        ],
    }


def resource_node_block(res_type: str, id_prefix: str, province_info: dict, max_supply: float) -> dict:
    return {
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
    }


def update_nodes_files(total_demand: dict, province_info: dict):
    for p in range(1, 8):
        path = os.path.join(BASE_DIR, "system", f"nodes_{p}.json")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        nodes = data.get("nodes", [])

        # 删除旧的铝相关节点（如果存在）
        aluminum_types = {"Aluminum", "Alumina", "AluminumScrap", "Bauxite", "Graphite"}
        nodes = [n for n in nodes if n.get("type") not in aluminum_types]

        # 添加新的节点
        nodes.append(aluminum_node_block(total_demand[p]))
        nodes.append(alumina_node_block())
        nodes.append(resource_node_block("AluminumScrap", "aluminumscrap_source", province_info, max_supply=0.0))
        nodes.append(resource_node_block("Bauxite", "bauxite_source", province_info, max_supply=100_000.0))
        nodes.append(resource_node_block("Graphite", "graphite_source", province_info, max_supply=100_000.0))

        data["nodes"] = nodes
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


def load_single_node_templates():
    """从单节点案例读取 AluminumSmelting / Refining / AluminaPlant 的 global_data 模板"""
    single_base = os.path.join(
        BASE_DIR,
        "..",
        "China_elec_multistage_288_7_v1107CO2cap_CCS_singleNode_aluminum",
    )
    assets1 = os.path.join(single_base, "assets", "assets_1")

    def _load(path, top_key):
        with open(path, "r", encoding="utf-8") as f:
            d = json.load(f)
        # 结构类似：{ "AluminumSmelting": [ { "type": "...", "global_data": {...}, ... } ] }
        return d[top_key][0]["global_data"]

    smelting_global = _load(os.path.join(assets1, "aluminumsmelting.json"), "AluminumSmelting")
    refining_global = _load(os.path.join(assets1, "aluminumrefining.json"), "AluminumRefining")
    plant_global = _load(os.path.join(assets1, "aluminaplant.json"), "AluminaPlant")
    return smelting_global, refining_global, plant_global


def build_smelting_instances(province_info: dict) -> list:
    inst = []
    for info in province_info.values():
        r = info["region_str"]
        inst.append(
            {
                "id": f"aluminum_smelting_{r}",
                "location": r,
                "existing_capacity": info["existing_capacity"],
                "aluminum_constraints": {
                    "MinFlowConstraint": True,
                },
                "edges": {
                    "elec_edge": {
                        "start_vertex": f"elec_{r}",
                        "end_vertex": f"aluminum_smelting_{r}",
                    },
                    "aluminum_edge": {
                        "start_vertex": f"aluminum_smelting_{r}",
                        "end_vertex": "aluminum_produced",
                    },
                    "alumina_edge": {
                        "start_vertex": "alumina_produced",
                        "end_vertex": f"aluminum_smelting_{r}",
                    },
                    "graphite_edge": {
                        "start_vertex": f"graphite_source_{r}",
                        "end_vertex": f"aluminum_smelting_{r}",
                    },
                },
            }
        )
    return inst


def build_refining_instances(province_info: dict) -> list:
    inst = []
    for info in province_info.values():
        r = info["region_str"]
        inst.append(
            {
                "id": f"aluminum_refining_{r}",
                "location": r,
                "existing_capacity": 0.0,
                "edges": {
                    "elec_edge": {
                        "start_vertex": f"elec_{r}",
                        "end_vertex": f"aluminum_refining_{r}",
                    },
                    "aluminum_edge": {
                        "start_vertex": f"aluminum_refining_{r}",
                        "end_vertex": "aluminum_produced",
                    },
                    "aluminumscrap_edge": {
                        "start_vertex": f"aluminumscrap_source_{r}",
                        "end_vertex": f"aluminum_refining_{r}",
                    },
                },
            }
        )
    return inst


def build_plant_instances(province_info: dict) -> list:
    inst = []
    for info in province_info.values():
        r = info["region_str"]
        inst.append(
            {
                "id": f"alumina_plant_{r}",
                "location": r,
                "existing_capacity": 0.0,
                "edges": {
                    "elec_edge": {
                        "start_vertex": f"elec_{r}",
                        "end_vertex": f"alumina_plant_{r}",
                    },
                    "alumina_edge": {
                        "start_vertex": f"alumina_plant_{r}",
                        "end_vertex": "alumina_produced",
                    },
                    "bauxite_edge": {
                        "start_vertex": f"bauxite_source_{r}",
                        "end_vertex": f"alumina_plant_{r}",
                    },
                    "fuel_edge": {
                        "start_vertex": f"natgas_{r}",
                        "end_vertex": f"alumina_plant_{r}",
                    },
                },
            }
        )
    return inst


def generate_assets(province_info: dict):
    smelting_global, refining_global, plant_global = load_single_node_templates()

    for p in range(1, 8):
        assets_dir = os.path.join(BASE_DIR, "assets", f"assets_{p}")
        os.makedirs(assets_dir, exist_ok=True)

        # AluminumSmelting
        smelting_obj = {
            "AluminumSmelting": [
                {
                    "type": "AluminumSmelting",
                    "global_data": deepcopy(smelting_global),
                    "instance_data": build_smelting_instances(province_info),
                }
            ]
        }
        with open(os.path.join(assets_dir, "aluminumsmelting.json"), "w", encoding="utf-8") as f:
            json.dump(smelting_obj, f, indent=2, ensure_ascii=False)

        # AluminumRefining
        refining_obj = {
            "AluminumRefining": [
                {
                    "type": "AluminumRefining",
                    "global_data": deepcopy(refining_global),
                    "instance_data": build_refining_instances(province_info),
                }
            ]
        }
        with open(os.path.join(assets_dir, "aluminumrefining.json"), "w", encoding="utf-8") as f:
            json.dump(refining_obj, f, indent=2, ensure_ascii=False)

        # AluminaPlant
        plant_obj = {
            "AluminaPlant": [
                {
                    "type": "AluminaPlant",
                    "global_data": deepcopy(plant_global),
                    "instance_data": build_plant_instances(province_info),
                }
            ]
        }
        with open(os.path.join(assets_dir, "aluminaplant.json"), "w", encoding="utf-8") as f:
            json.dump(plant_obj, f, indent=2, ensure_ascii=False)


def main():
    print("Generating aluminum inputs for Ver12 (Python script)...")
    total_demand = load_total_demand_per_period(demand_2025_10kt=4000.0)
    print("  Total primary aluminum demand per period (288h tons):")
    for p in sorted(total_demand):
        print(f"    period {p}: {total_demand[p]:.5g}")

    province_info = load_province_capacity()
    print(f"  Provinces with capacity & mapping: {len(province_info)}")

    update_commodities()
    update_nodes_files(total_demand, province_info)
    generate_assets(province_info)

    # 同时更新 time_data.json，加入铝相关 commodities 的时间步信息
    time_data_path = os.path.join(BASE_DIR, "system", "time_data.json")
    if os.path.exists(time_data_path):
        with open(time_data_path, "r", encoding="utf-8") as f:
            td = json.load(f)
        # 仿照单节点案例：所有新 commodity 都是 1 小时时间步、每子期 24 小时，总共 288 小时
        hours_per_ts = td.get("HoursPerTimeStep", {})
        hours_per_sp = td.get("HoursPerSubperiod", {})
        for k in ["Aluminum", "Alumina", "AluminumScrap", "Bauxite", "Graphite"]:
            hours_per_ts.setdefault(k, 1)
            hours_per_sp.setdefault(k, 24)
        td["HoursPerTimeStep"] = hours_per_ts
        td["HoursPerSubperiod"] = hours_per_sp
        td.setdefault("NumberOfSubperiods", 12)
        td.setdefault("TotalHoursModeled", 288)
        with open(time_data_path, "w", encoding="utf-8") as f:
            json.dump(td, f, indent=2, ensure_ascii=False)

    print("Done. commodities.json, nodes_*.json, and assets_*/aluminum*.json have been updated/created.")


if __name__ == "__main__":
    main()


