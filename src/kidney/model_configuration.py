from dataclasses import dataclass
from pathlib import Path

import bambi as bmb

from kidney.paths import PREPARED_FILES


@dataclass
class ModelConfig:
    name: str
    formula: str | bmb.Formula
    csv: Path
    outcome: str

    def __post_init__(self):
        if isinstance(self.formula, str):
            self.formula = bmb.Formula(self.formula.format(y=self.outcome))


FORMULA_GAGS = "{y} ~ (1|rat) + gtyp + age + sex + gtyp:age + gtyp:sex"
FORMULA_GAGSGAS = (
    "{y} ~ (1|rat) + gtyp + age + sex + gtyp:age + gtyp:sex + gtyp:age:sex"
)
FORMULA_GAGS_NO_RAT = "{y} ~ gtyp + age + sex + gtyp:age + gtyp:sex"
FORMULA_BLOOD_GLUCOSE = "censored(log_value, too_high) ~ (0 + gtyp|rat) + stage + gtyp + sex + stage:gtyp + stage:sex"
FORMULA_BIOCHEM_ABS = bmb.Formula(
    "log_value ~ gtyp + age + sex + gtyp:age + gtyp:sex",
    "sigma ~ gtyp",
)
FORMULA_EXCRETION_NA_CHANGE = bmb.Formula(
    "value ~ gtyp + age + sex + gtyp:age + gtyp:sex",
    "sigma ~ gtyp",
)

MODEL_CONFIGS = (
    ModelConfig(
        "bfi_vehicle",
        FORMULA_GAGS,
        PREPARED_FILES["bfi_vehicle"],
        "log_bfi_change",
    ),
    ModelConfig(
        "bfi_empa",
        FORMULA_GAGS,
        PREPARED_FILES["bfi_empa"],
        "log_bfi_change",
    ),
    ModelConfig(
        "bfi_baseline",
        FORMULA_GAGS,
        PREPARED_FILES["bfi_vehicle"],
        "log_bfi_baseline",
    ),
    ModelConfig(
        "bfi_baseline_extra_interaction",
        FORMULA_GAGSGAS,
        PREPARED_FILES["bfi_vehicle"],
        "log_bfi_baseline",
    ),
    ModelConfig(
        "bp_vehicle",
        FORMULA_GAGS_NO_RAT,
        PREPARED_FILES["bp_vehicle"],
        "log_bp_change",
    ),
    ModelConfig(
        "bp_empa",
        FORMULA_GAGS_NO_RAT,
        PREPARED_FILES["bp_empa"],
        "log_bp_change",
    ),
    ModelConfig(
        "bp_baseline",
        FORMULA_GAGS_NO_RAT,
        PREPARED_FILES["bp_vehicle"],
        "log_bp_baseline",
    ),
    ModelConfig(
        "frequency",
        FORMULA_GAGS,
        PREPARED_FILES["frequency"],
        "frequency_change",
    ),
    ModelConfig(
        "frequency_baseline",
        FORMULA_GAGS,
        PREPARED_FILES["frequency"],
        "frequency_vehicle",
    ),
    ModelConfig(
        "power",
        FORMULA_GAGS,
        PREPARED_FILES["power"],
        "log_power_change",
    ),
    ModelConfig(
        "power_baseline",
        FORMULA_GAGS,
        PREPARED_FILES["power"],
        "log_power_vehicle",
    ),
    ModelConfig(
        "blood_glucose",
        FORMULA_BLOOD_GLUCOSE,
        PREPARED_FILES["blood_glucose"],
        "",
    ),
    ModelConfig(
        "urine_flow_vehicle",
        FORMULA_BIOCHEM_ABS,
        PREPARED_FILES["urine_flow_vehicle"],
        "",
    ),
    ModelConfig(
        "excretion_glucose_vehicle",
        FORMULA_BIOCHEM_ABS,
        PREPARED_FILES["excretion_glucose_vehicle"],
        "",
    ),
    ModelConfig(
        "excretion_na_vehicle",
        FORMULA_BIOCHEM_ABS,
        PREPARED_FILES["excretion_na_vehicle"],
        "",
    ),
    ModelConfig(
        "plasma_na_vehicle",
        FORMULA_BIOCHEM_ABS,
        PREPARED_FILES["plasma_na_vehicle"],
        "",
    ),
    ModelConfig(
        "urine_flow_empa_minus_vehicle",
        FORMULA_GAGS_NO_RAT,
        PREPARED_FILES["urine_flow_empa_minus_vehicle"],
        "value",
    ),
    ModelConfig(
        "excretion_glucose_empa_minus_vehicle",
        FORMULA_GAGS_NO_RAT,
        PREPARED_FILES["excretion_glucose_empa_minus_vehicle"],
        "value",
    ),
    ModelConfig(
        "excretion_na_empa_minus_vehicle",
        FORMULA_EXCRETION_NA_CHANGE,
        PREPARED_FILES["excretion_na_empa_minus_vehicle"],
        "value",
    ),
    ModelConfig(
        "plasma_na_empa_minus_vehicle",
        FORMULA_GAGS_NO_RAT,
        PREPARED_FILES["plasma_na_empa_minus_vehicle"],
        "value",
    ),
)
