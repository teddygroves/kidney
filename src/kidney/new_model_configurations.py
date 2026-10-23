import bambi as bmb

from kidney.paths import PREPARED_FILES_NEW
from kidney.model_configuration import ModelConfig


FORMULA_BASELINE_POWER = bmb.Formula(
    "log_baseline ~ (1|rat) + gtyp + age + sex + gtyp:age + gtyp:sex",
    "sigma ~ band",
)

MODEL_CONFIGS = (
    ModelConfig(
        "baseline_power_vehicle",
        FORMULA_BASELINE_POWER,
        PREPARED_FILES_NEW["baseline_power_vehicle"],
        "log_baseline",
    ),
    ModelConfig(
        "baseline_power_empa",
        FORMULA_BASELINE_POWER,
        PREPARED_FILES_NEW["baseline_power_empa"],
        "log_baseline",
    ),
)
