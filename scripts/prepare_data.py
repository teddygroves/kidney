import polars as pl

from kidney.data_preparation import (
    prepare_bfi,
    prepare_biochem,
    prepare_biochem_subdf,
    prepare_blood_glucose,
    prepare_blood_pressure,
    prepare_frequency,
    prepare_frequency_new,
    prepare_power,
    prepare_baseline_power_cb,
    prepare_baseline_power_lfb,
    prepare_power_change,
    prepare_baseline_activity_types,
    prepare_body_weight,
)
from kidney.paths import PREPARED_FILES, PREPARED_FILES_NEW, RAW_FILES


def main():
    print("Loading raw data...")
    raw_data = {k: pl.read_csv(v) for k, v in RAW_FILES.items()}

    print("Preparing biochem data...")
    biochem = prepare_biochem(
        raw_data["vein_glucose"],
        raw_data["biochem_vehicle"],
        raw_data["biochem_change"],
    )
    print(f"Writing {PREPARED_FILES['biochem']}...")
    biochem.write_csv(PREPARED_FILES["biochem"])
    blood_glucose = prepare_blood_glucose(biochem)
    print(f"Writing {PREPARED_FILES['blood_glucose']}...")
    blood_glucose.write_csv(PREPARED_FILES["blood_glucose"])
    
    for variable in (
        "urine_flow",
        "excretion_glucose",
        "excretion_na",
        "plasma_na",
    ):
        
        subdf_vehicle = prepare_biochem_subdf(biochem, variable, "vehicle")
        print(f"Writing {PREPARED_FILES[variable + '_vehicle']}...")
        subdf_vehicle.write_csv(PREPARED_FILES[variable + "_vehicle"])
        subdf_change = prepare_biochem_subdf(
            biochem,
            variable,
            "empa_minus_vehicle",
        )
        subdf_log_change = prepare_biochem_subdf(
            biochem,
            variable,
            "log_empa_minus_log_vehicle",
        )
        print(f"Writing {PREPARED_FILES[variable + '_empa_minus_vehicle']}...")
        subdf_change.write_csv(PREPARED_FILES[variable + "_empa_minus_vehicle"])
        print(
            f"Writing {PREPARED_FILES[variable + '_log_empa_minus_log_vehicle']}..."
        )
        subdf_log_change.write_csv(
            PREPARED_FILES[variable + "_log_empa_minus_log_vehicle"]
        )

    print("Preparing Body Weight data...")
    body_weight = prepare_body_weight(raw_data["body_weight"])
    body_weight.write_csv(PREPARED_FILES["body_weight"])
        
    print("Preparing BFI data...")
    bfi = prepare_bfi(raw_data["bfi_rec1"], raw_data["bfi_rec2"])
    print(f"Writing {PREPARED_FILES['bfi']}...")
    bfi.write_csv(PREPARED_FILES["bfi"])
    print(f"Writing {PREPARED_FILES['bfi_empa']}...")
    bfi.filter(treatment="Empa").write_csv(PREPARED_FILES["bfi_empa"])
    print(f"Writing {PREPARED_FILES['bfi_vehicle']}...")
    bfi.filter(treatment="Vehicle").write_csv(PREPARED_FILES["bfi_vehicle"])

    print("Preparing blood pressure data...")
    bp = prepare_blood_pressure(raw_data["bp_rec1"], raw_data["bp_rec2"])
    print(f"Writing {PREPARED_FILES['bp']}...")
    bp.write_csv(PREPARED_FILES["bp"])
    print(f"Writing {PREPARED_FILES['bp_empa']}...")
    bp.filter(treatment="Empa").write_csv(PREPARED_FILES["bp_empa"])
    print(f"Writing {PREPARED_FILES['bp_vehicle']}...")
    bp.filter(treatment="Vehicle").write_csv(PREPARED_FILES["bp_vehicle"])

    print("Preparing frequency data...")
    freq = prepare_frequency(raw_data["frequency"])
    print(f"Writing {PREPARED_FILES['frequency']}...")
    freq.write_csv(PREPARED_FILES["frequency"])

    print("Preparing power data...")
    power = prepare_power(raw_data["power"])
    print(f"Writing {PREPARED_FILES['power']}...")
    power.write_csv(PREPARED_FILES["power"])

    print("Preparing baseline power data - canonical band...")
    baseline_power_vehicle, baseline_power_empa = prepare_baseline_power_cb(cb=raw_data["baseline_power_cb"])
    
    print(f"Writing {PREPARED_FILES_NEW['baseline_power_vehicle_cb']}...")
    baseline_power_vehicle.write_csv(
        PREPARED_FILES_NEW["baseline_power_vehicle_cb"]
    )
    print(f"Writing {PREPARED_FILES_NEW['baseline_power_empa_cb']}...")
    baseline_power_empa.write_csv(PREPARED_FILES_NEW["baseline_power_empa_cb"])

    print("Preparing baseline power data - lowfreq band...")
    baseline_power_vehicle, baseline_power_empa = prepare_baseline_power_lfb(lfb=raw_data["baseline_power_lfb"])
    
    print(f"Writing {PREPARED_FILES_NEW['baseline_power_vehicle_lfb']}...")
    baseline_power_vehicle.write_csv(
        PREPARED_FILES_NEW["baseline_power_vehicle_lfb"]
    )
    print(f"Writing {PREPARED_FILES_NEW['baseline_power_empa_lfb']}...")
    baseline_power_empa.write_csv(PREPARED_FILES_NEW["baseline_power_empa_lfb"])

    print("Preparing power change data...")
    power_change_vehicle, power_change_empa = prepare_power_change(
        raw_data["power_change"]
    )
    
    print(f"Writing {PREPARED_FILES_NEW['power_change_vehicle']}...")
    power_change_vehicle.write_csv(PREPARED_FILES_NEW["power_change_vehicle"])
    print(f"Writing {PREPARED_FILES_NEW['power_change_empa']}...")
    power_change_empa.write_csv(PREPARED_FILES_NEW["power_change_empa"])

    print("Preparing frequency data...")
    frequency_vehicle, frequency_empa = prepare_frequency_new(
        raw_data["frequency_new"]
    )
    print(f"Writing {PREPARED_FILES_NEW['frequency_vehicle']}...")
    frequency_vehicle.write_csv(PREPARED_FILES_NEW["frequency_vehicle"])
    print(f"Writing {PREPARED_FILES_NEW['frequency_empa']}...")
    frequency_empa.write_csv(PREPARED_FILES_NEW["frequency_empa"])

    print("Preparing baseline activity types data...")
    bat_vehicle, bat_empa = prepare_baseline_activity_types(
        raw_data["baseline_activity_types"]
    )
    print(f"Writing {PREPARED_FILES_NEW['baseline_activity_types_vehicle']}...")
    bat_vehicle.write_csv(PREPARED_FILES_NEW["baseline_activity_types_vehicle"])
    print(f"Writing {PREPARED_FILES_NEW['baseline_activity_types_empa']}...")
    bat_empa.write_csv(PREPARED_FILES_NEW["baseline_activity_types_empa"])
    print("Done!")


if __name__ == "__main__":
    main()
