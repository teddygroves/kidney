import bambi as bmb

from kidney.paths import PREPARED_FILES_NEW
from kidney.model_configuration import ModelConfig


FORMULA_BASELINE_POWER = bmb.Formula(
    "log_baseline ~ (1|rat) + gtyp + age + sex + gtyp:age + gtyp:sex",
)
FORMULA_POWER_CHANGE = bmb.Formula(
    "ln_change ~ (1|rat) + gtyp + age + sex + gtyp:age + gtyp:sex",
)
FORMULA_FREQUENCY_BASELINE = bmb.Formula(
    "baseline ~ (1|rat) + gtyp + age + sex + gtyp:age + gtyp:sex",
)
FORMULA_FREQUENCY_CHANGE = bmb.Formula(
    "ln_change ~ (1|rat) + gtyp + age + sex + gtyp:age + gtyp:sex",
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
    
    *(
        ModelConfig(
            f"power_change_{treatment}_{activity_type}",
            FORMULA_POWER_CHANGE,
            PREPARED_FILES_NEW[f"power_change_{treatment}_{activity_type}"],
            "ln_change",
        )
        for treatment in ("vehicle", "empa")
        for activity_type in ("single", "double")
    ),
    *(
        ModelConfig(
            f"frequency_{treatment}_{stage}_{activity_type}",
            formula,
            PREPARED_FILES_NEW[f"frequency_{treatment}_{activity_type}"],
            outcome,
        )
        for stage, formula, outcome in (
            ("baseline", FORMULA_FREQUENCY_BASELINE, "baseline"),
            ("change", FORMULA_FREQUENCY_CHANGE, "ln_change"),
        )
        for treatment in ("vehicle", "empa")
        for activity_type in ("single", "double")
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
