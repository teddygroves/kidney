import polars as pl
from kidney.paths import RAW_FILES, PREPARED_FILES
from kidney.data_preparation import (
    prepare_bfi,
    prepare_blood_pressure,
    prepare_frequency,
    prepare_power,
)


def main():
    print("Loading raw data...")
    raw_data = {
        "bfi_rec1": pl.read_csv(RAW_FILES["bfi_rec1"]),
        "bfi_rec2": pl.read_csv(RAW_FILES["bfi_rec2"]),
        "bp_rec1": pl.read_csv(RAW_FILES["bp_rec1"]),
        "bp_rec2": pl.read_csv(RAW_FILES["bp_rec2"]),
        "frequency": pl.read_csv(RAW_FILES["frequency"]),
        "power": pl.read_csv(RAW_FILES["power"]),
    }

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

    print("Done!")


if __name__ == "__main__":
    main()
