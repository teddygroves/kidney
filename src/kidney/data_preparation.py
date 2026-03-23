import numpy as np
import polars as pl


def standardise(x: pl.Expr) -> pl.Expr:
    """Standardize a polars expression."""
    return (x - x.mean()) / x.std()


def prepare_bfi(raw_rec1: pl.DataFrame, raw_rec2: pl.DataFrame) -> pl.DataFrame:
    """Prepare BFI data from two recording files.

    Args:
        raw_rec1: DataFrame from recording 1 (Vehicle treatment)
        raw_rec2: DataFrame from recording 2 (Empa treatment)

    Returns:
        DataFrame with log-transformed and standardized BFI metrics
    """
    bfi = pl.concat([raw_rec1, raw_rec2])
    bfi = (
        bfi.with_columns(
            bfi_injected=pl.col("bfi_baseline") + pl.col("bfi_change"),
            log_bfi_baseline=np.log(pl.col("bfi_baseline")),
        )
        .with_columns(
            log_bfi_injected=np.log(pl.col("bfi_injected")),
            log_bfi_baseline_std=standardise(pl.col("log_bfi_baseline")),
        )
        .with_columns(
            log_bfi_change=pl.col("log_bfi_injected")
            - pl.col("log_bfi_baseline")
        )
    )
    return bfi


def prepare_blood_pressure(
    raw_rec1: pl.DataFrame, raw_rec2: pl.DataFrame
) -> pl.DataFrame:
    """Prepare blood pressure data from two recording files.

    Args:
        raw_rec1: DataFrame from recording 1 (Vehicle treatment)
        raw_rec2: DataFrame from recording 2 (Empa treatment)

    Returns:
        DataFrame with log-transformed and standardized BP metrics
    """
    bp = pl.concat([raw_rec1, raw_rec2])
    bp = (
        bp.with_columns(
            bp_injected=pl.col("bp_baseline") + pl.col("bp_change"),
            log_bp_baseline=np.log(pl.col("bp_baseline")),
        )
        .with_columns(
            log_bp_injected=np.log(pl.col("bp_injected")),
            log_bp_baseline_std=standardise(pl.col("log_bp_baseline")),
        )
        .with_columns(
            log_bp_change=pl.col("log_bp_injected") - pl.col("log_bp_baseline")
        )
    )
    return bp


def prepare_frequency(raw_df: pl.DataFrame) -> pl.DataFrame:
    """Prepare frequency data from single table.

    Provides both linear and log-transformed versions for modeling flexibility.

    Args:
        raw_df: DataFrame with frequency_vehicle, frequency_empa, frequency_change

    Returns:
        DataFrame with standardized linear and log frequency metrics
    """
    freq = raw_df.with_columns(
        # Linear standardized versions
        frequency_vehicle_std=standardise(pl.col("frequency_vehicle")),
        frequency_empa_std=standardise(pl.col("frequency_empa")),
        frequency_change_std=standardise(pl.col("frequency_change")),
        # Log transformations
        log_frequency_vehicle=np.log(pl.col("frequency_vehicle")),
        log_frequency_empa=np.log(pl.col("frequency_empa")),
    ).with_columns(
        # Log standardized versions
        log_frequency_vehicle_std=standardise(pl.col("log_frequency_vehicle")),
        log_frequency_change=pl.col("log_frequency_empa")
        - pl.col("log_frequency_vehicle"),
    )
    return freq


def prepare_power(raw_df: pl.DataFrame) -> pl.DataFrame:
    """Prepare power data from single table.

    Provides both linear and log-transformed versions for modeling flexibility.
    Uses power_change (difference) consistently with other metrics.

    Args:
        raw_df: DataFrame with power_vehicle, power_empa, power_change

    Returns:
        DataFrame with standardized linear and log power metrics
    """
    power = raw_df.with_columns(
        # Linear standardized versions
        power_vehicle_std=standardise(pl.col("power_vehicle")),
        power_empa_std=standardise(pl.col("power_empa")),
        power_change_std=standardise(pl.col("power_change")),
        # Log transformations
        log_power_vehicle=np.log(pl.col("power_vehicle")),
        log_power_empa=np.log(pl.col("power_empa")),
    ).with_columns(
        # Log standardized versions
        log_power_vehicle_std=standardise(pl.col("log_power_vehicle")),
        log_power_change=pl.col("log_power_empa") - pl.col("log_power_vehicle"),
    )
    return power


def prepare_biochem(
    raw_vein_glucose: pl.DataFrame,
    raw_data_vehicle: pl.DataFrame,
    raw_change_empa_vehicle: pl.DataFrame,
) -> pl.DataFrame:
    out_cols = ["rat", "age", "gtyp", "sex", "stage", "variable", "value"]
    variable_cols = [
        "plasma_na",
        "urine_flow",
        "excretion_na",
        "excretion_glucose",
    ]
    unpivot_index = ["rat", "age", "gtyp", "sex"]
    blood_glucose = raw_vein_glucose.rename(
        {
            "glucose": "value",
            "treatment": "stage",
        }
    ).with_columns(variable=pl.lit("blood_glucose"))[out_cols]
    vehicle = raw_data_vehicle.unpivot(
        on=variable_cols,
        index=unpivot_index,
    ).with_columns(stage=pl.lit("vehicle"))[out_cols]
    change_empa = (
        raw_change_empa_vehicle.rename(lambda col: col.replace("_change", ""))
        .unpivot(on=variable_cols, index=unpivot_index)
        .with_columns(stage=pl.lit("empa_minus_vehicle"))[out_cols]
    )
    empa = (
        vehicle.rename({"value": "vehicle"})
        .join(
            change_empa.rename({"value": "change_empa"}),
            on=unpivot_index + ["variable"],
            how="full",
        )
        .with_columns(
            value=pl.col("vehicle") + pl.col("change_empa"),
            stage=pl.lit("empa"),
        )[out_cols]
    )
    out = pl.concat([blood_glucose, vehicle, change_empa, empa])
    return out


def prepare_blood_glucose(biochem):
    msts = biochem.filter(variable="blood_glucose")
    top_value = (
        msts["value"].max() + 0.5
    )  # assume that oversaturated measurements were at least this high
    all_msts = (
        pl.DataFrame(
            {
                "rat": msts["rat"].unique(),
                "beforeAnesthesia": 1,
                "vehicle": 2,
                "empa": 3,
            }
        )
        .unpivot(index="rat", variable_name="stage", value_name="order")
        .sort("rat", "order")
        .join(
            msts[["rat", "age", "gtyp", "sex"]].unique(), on="rat", how="left"
        )
        .drop("order")
    )
    filter_missing_measurements = ~(
        pl.col("value").is_null()
        & ((pl.col("gtyp") == "fa/+") | (pl.col("rat") == "20240816a"))
    )
    return (
        msts[["rat", "stage", "value"]]
        .join(all_msts, on=("rat", "stage"), how="right")
        .filter(filter_missing_measurements)
        .with_columns(
            too_high=pl.when(pl.col("value").is_null())
            .then(pl.lit("right"))
            .otherwise(pl.lit("none")),
            value=pl.when(pl.col("value").is_null())
            .then(top_value)
            .otherwise(pl.col("value")),
        )
        .with_columns(log_value=np.log(pl.col("value")))
    )


def prepare_biochem_subdf(raw_df, variable, stage):
    out = (
        raw_df.filter(
            pl.col("variable").eq(variable) & pl.col("stage").eq(stage)
        )
        .drop_nulls()
        .sort("gtyp", "age", "sex")
    )
    if stage == "vehicle":
        out = out.with_columns(log_value=np.log(pl.col("value")))
    return out
