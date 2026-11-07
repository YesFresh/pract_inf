"""Этап 2. Валидация паспорта скважины по schema.json."""
import copy
import json
from typing import Any

def load_json_file(filename: str) -> dict[str, Any]:
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)

def validate_by_schema(data: Any, schema: dict[str, Any]) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return False, ["Корневое значение должно быть объектом"]
    required = schema["required"]
    props = schema["properties"]
    for field in required:
        if field not in data:
            errors.append(f"Отсутствует обязательное поле '{field}'")
    for key in data.keys() - props.keys():
        errors.append(f"Неизвестное поле '{key}'")

    for key in ("well_id", "field_name"):
        if key in data:
            value = data[key]
            if not isinstance(value, str) or not value.strip():
                errors.append(f"Поле '{key}' должно быть непустой строкой")

    if "depth_m" in data:
        depth = data["depth_m"]
        rules = props["depth_m"]
        if not isinstance(depth, int) or isinstance(depth, bool):
            errors.append("Поле 'depth_m' должно быть целым числом")
        elif not rules["minimum"] <= depth <= rules["maximum"]:
            errors.append(f"Глубина depth_m={depth} вне границ [{rules['minimum']}; {rules['maximum']}]")

    for key in ("q_liq", "w_pct"):
        if key in data:
            value, limits = data[key], props[key]
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                errors.append(f"Поле '{key}' должно быть числом")
            elif not limits["minimum"] <= value <= limits["maximum"]:
                errors.append(f"Поле '{key}'={value} вне границ [{limits['minimum']}; {limits['maximum']}]")

    if "is_active" in data and not isinstance(data["is_active"], bool):
        errors.append("Поле 'is_active' должно быть логическим значением")

    pump = data.get("pump")
    ps = props["pump"]
    if "pump" in data and not isinstance(pump, dict):
        errors.append("Поле 'pump' должно быть объектом")
    elif "pump" in data:
        for field in ps["required"]:
            if field not in pump:
                errors.append(f"Во вложенном объекте 'pump' отсутствует поле '{field}'")
        for key in pump.keys() - ps["properties"].keys():
            errors.append(f"Неизвестное поле 'pump.{key}'")
        if "model" in pump and (not isinstance(pump["model"], str) or not pump["model"].strip()):
            errors.append("Поле 'pump.model' должно быть непустой строкой")
        if "power_kw" in pump:
            value, limits = pump["power_kw"], ps["properties"]["power_kw"]
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                errors.append("Поле 'pump.power_kw' должно быть числом")
            elif not limits["minimum"] <= value <= limits["maximum"]:
                errors.append(f"Мощность pump.power_kw={value} вне границ [{limits['minimum']}; {limits['maximum']}]")
    return not errors, errors

if __name__ == "__main__":
    contract = load_json_file("schema.json")
    valid = load_json_file("data.json")
    cases = [
        ("Сценарий 1: эталонный data.json", valid),
    ]
    limits = copy.deepcopy(valid); limits["depth_m"] = -100; limits["w_pct"] = 145.0
    cases.append(("Сценарий 2: нарушение границ", limits))
    missing = copy.deepcopy(valid); del missing["well_id"]
    cases.append(("Сценарий 3: отсутствует well_id", missing))
    bad_type = copy.deepcopy(valid); bad_type["pump"]["power_kw"] = "шестьдесят пять"
    cases.append(("Сценарий 4: неверный тип мощности насоса", bad_type))
    broken = copy.deepcopy(valid); del broken["field_name"]; broken["pump"]["power_kw"] = "ошибка"
    cases.append(("Сценарий 5: проверка broken_data.json (2 диверсии)", broken))

    for title, payload in cases:
        ok, errors = validate_by_schema(payload, contract)
        print(f"{title} -> {'VALID' if ok else 'ОТКЛОНЕНО'}")
        for error in errors:
            print(f"  - {error}")
