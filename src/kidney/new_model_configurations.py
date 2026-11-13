import bambi as bmb

from kidney.paths import PREPARED_FILES_NEW
from kidney.model_configuration import ModelConfig


FORMULA_BASELINE_POWER = bmb.Formula(
    "log_baseline ~ (1|rat) + gtyp + age + sex + gtyp:age + gtyp:sex",
)
FORMULA_POWER_CHANGE = bmb.Formula(
    "ln_change ~ (1|rat) + activity_type + gtyp + age + sex + gtyp:age + gtyp:sex",
)
FORMULA_FREQUENCY_BASELINE = bmb.Formula(
    "baseline ~ (1|rat) + activity_type + gtyp + age + sex + gtyp:age + gtyp:sex",
)
FORMULA_FREQUENCY_CHANGE = bmb.Formula(
    "ln_change ~ (1|rat) + activity_type + gtyp + age + sex + gtyp:age + gtyp:sex",
)
FORMULA_BAT = bmb.Formula(
    "c(canonical, double, subthreshold, beats) ~ (1|rat) + gtyp + age + sex"
    " + gtyp:age + gtyp:sex",
)
PRIORS_BAT = {
    term: bmb.Prior("Normal", mu=0, sigma=1.5)
    for term in ("gtyp", "age", "sex", "gtyp:age", "gtyp:sex")
}

MODEL_CONFIGS = (
    ModelConfig(
        "baseline_power_vehicle_cb",
        FORMULA_BASELINE_POWER,
        PREPARED_FILES_NEW["baseline_power_vehicle_cb"],
        "log_baseline",
    ),
    ModelConfig(
        "baseline_power_empa_cb",
        FORMULA_BASELINE_POWER,
        PREPARED_FILES_NEW["baseline_power_empa_cb"],
        "log_baseline",
    ),
    
    ModelConfig(
        "baseline_power_vehicle_lfb",
        FORMULA_BASELINE_POWER,
        PREPARED_FILES_NEW["baseline_power_vehicle_lfb"],
        "log_baseline",
    ),
    ModelConfig(
        "baseline_power_empa_lfb",
        FORMULA_BASELINE_POWER,
        PREPARED_FILES_NEW["baseline_power_empa_lfb"],
        "log_baseline",
    ),
    
    ModelConfig(
        "power_change_vehicle",
        FORMULA_POWER_CHANGE,
        PREPARED_FILES_NEW["power_change_vehicle"],
        "ln_change",
    ),
    ModelConfig(
        "power_change_empa",
        FORMULA_POWER_CHANGE,
        PREPARED_FILES_NEW["power_change_empa"],
        "ln_change",
    ),
    ModelConfig(
        "frequency_vehicle_baseline",
        FORMULA_FREQUENCY_BASELINE,
        PREPARED_FILES_NEW["frequency_vehicle"],
        "baseline",
    ),
    ModelConfig(
        "frequency_vehicle_change",
        FORMULA_FREQUENCY_CHANGE,
        PREPARED_FILES_NEW["frequency_vehicle"],
        "ln_change",
    ),
    ModelConfig(
        "frequency_empa_baseline",
        FORMULA_FREQUENCY_BASELINE,
        PREPARED_FILES_NEW["frequency_empa"],
        "baseline",
    ),
    ModelConfig(
        "frequency_empa_change",
        FORMULA_FREQUENCY_CHANGE,
        PREPARED_FILES_NEW["frequency_empa"],
        "ln_change",
    ),
    ModelConfig(
        "baseline_activity_types_vehicle",
        FORMULA_BAT,
        PREPARED_FILES_NEW["baseline_activity_types_vehicle"],
        "activity type counts",
        family="multinomial",
        priors=PRIORS_BAT,
    ),
    ModelConfig(
        "baseline_activity_types_empa",
        FORMULA_BAT,
        PREPARED_FILES_NEW["baseline_activity_types_empa"],
        "activity type counts",
        family="multinomial",
        priors=PRIORS_BAT,
    ),
)
