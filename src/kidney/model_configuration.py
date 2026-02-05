from dataclasses import dataclass
from pathlib import Path

from kidney.paths import PREPARED_FILES as PF


@dataclass
class ModelConfig:
    name: str
    formula: str
    csv: Path
    outcome: str


FORMULA = "{y} ~ (1|rat) + gtyp + age + sex + gtyp:age + gtyp:sex"
FORMULA_GAS = (
    "{y} ~ (1|rat) + gtyp + age + sex + gtyp:age + gtyp:sex + gtyp:age:sex"
)
FORMULA_BP = "{y} ~ gtyp + age + sex + gtyp:age + gtyp:sex"
MODEL_CONFIGS = (
    ModelConfig("bfi_vehicle", FORMULA, PF["bfi_vehicle"], "log_bfi_change"),
    ModelConfig("bfi_empa", FORMULA, PF["bfi_empa"], "log_bfi_change"),
    ModelConfig("bfi_baseline", FORMULA, PF["bfi_vehicle"], "log_bfi_baseline"),
    ModelConfig(
        "bfi_baseline_extra_interaction",
        FORMULA_GAS,
        PF["bfi_vehicle"],
        "log_bfi_baseline",
    ),
    ModelConfig("bp_vehicle", FORMULA_BP, PF["bp_vehicle"], "log_bp_change"),
    ModelConfig("bp_empa", FORMULA_BP, PF["bp_empa"], "log_bp_change"),
    ModelConfig("bp_baseline", FORMULA_BP, PF["bp_vehicle"], "log_bp_baseline"),
    ModelConfig("frequency", FORMULA, PF["frequency"], "frequency_change"),
    ModelConfig(
        "frequency_baseline",
        FORMULA,
        PF["frequency"],
        "frequency_vehicle",
    ),
    ModelConfig("power", FORMULA, PF["power"], "log_power_change"),
    ModelConfig("power_baseline", FORMULA, PF["power"], "log_power_vehicle"),
)
