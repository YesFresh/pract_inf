"""Этап 1. Базовый вариант А: цифровой паспорт скважины."""
import json
from typing import Any

def build_well_passport() -> dict[str, Any]:
    return {
        "well_id": "W-105",
        "field_name": "Приобское",
        "depth_m": 1750,
        "q_liq": 62.5,
        "w_pct": 22.0,
        "is_active": True,
        "pump": {"model": "ЭЦН5-80-1800", "power_kw": 65.0},
    }

def save_to_json(data: dict[str, Any], filename: str = "data.json") -> None:
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def load_from_json(filename: str = "data.json") -> dict[str, Any]:
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)

def print_passport_summary(passport: dict[str, Any]) -> None:
    q_oil = passport["q_liq"] * (1.0 - passport["w_pct"] / 100.0)
    pump = passport["pump"]
    print("=" * 54)
    print(f"ПАСПОРТ СКВАЖИНЫ: {passport['well_id']}")
    print(f"Месторождение: {passport['field_name']}")
    print(f"Глубина: {passport['depth_m']} м")
    print(f"Дебит жидкости: {passport['q_liq']:.2f} м³/сут; обводнённость: {passport['w_pct']:.1f}%")
    print(f"Расчётный дебит нефти: {q_oil:.2f} м³/сут")
    print(f"Насос: {pump['model']}, мощность {pump['power_kw']:.1f} кВт")
    print(f"Статус: {'в работе' if passport['is_active'] else 'не работает'}")
    print("=" * 54)

if __name__ == "__main__":
    passport = build_well_passport()
    save_to_json(passport)
    loaded = load_from_json()
    assert loaded == passport, "После чтения JSON данные изменились"
    print("[OK] data.json записан; обратное чтение прошло без потерь.")
    print_passport_summary(loaded)
