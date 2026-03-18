from dataclasses import dataclass
from pathlib import Path

from kidney.paths import PREPARED_FILES as PF


@dataclass
class ModelConfig:
    name: str
    formula: str
    csv: Path
    outcome: str


FORMULA_GAGS = "{y} ~ (1|rat) + gtyp + age + sex + gtyp:age + gtyp:sex"
FORMULA_GAGSGAS = (
    "{y} ~ (1|rat) + gtyp + age + sex + gtyp:age + gtyp:sex + gtyp:age:sex"
)
FORMULA_GAGS_NO_RAT = "{y} ~ gtyp + age + sex + gtyp:age + gtyp:sex"
MODEL_CONFIGS = (
    ModelConfig(
        "bfi_vehicle",
        FORMULA_GAGS,
        PF["bfi_vehicle"],
        "log_bfi_change",
    ),
    ModelConfig(
        "bfi_empa",
        FORMULA_GAGS,
        PF["bfi_empa"],
        "log_bfi_change",
    ),
    ModelConfig(
        "bfi_baseline",
        FORMULA_GAGS,
        PF["bfi_vehicle"],
        "log_bfi_baseline",
    ),
    ModelConfig(
        "bfi_baseline_extra_interaction",
        FORMULA_GAGSGAS,
        PF["bfi_vehicle"],
        "log_bfi_baseline",
    ),
    ModelConfig(
        "bp_vehicle",
        FORMULA_GAGS_NO_RAT,
        PF["bp_vehicle"],
        "log_bp_change",
    ),
    ModelConfig(
        "bp_empa",
        FORMULA_GAGS_NO_RAT,
        PF["bp_empa"],
        "log_bp_change",
    ),
    ModelConfig(
        "bp_baseline",
        FORMULA_GAGS_NO_RAT,
        PF["bp_vehicle"],
        "log_bp_baseline",
    ),
    ModelConfig(
        "frequency",
        FORMULA_GAGS,
        PF["frequency"],
        "frequency_change",
    ),
    ModelConfig(
        "frequency_baseline",
        FORMULA_GAGS,
        PF["frequency"],
        "frequency_vehicle",
    ),
    ModelConfig(
        "power",
        FORMULA_GAGS,
        PF["power"],
        "log_power_change",
    ),
    ModelConfig(
        "power_baseline",
        FORMULA_GAGS,
        PF["power"],
        "log_power_vehicle",
    ),
)
