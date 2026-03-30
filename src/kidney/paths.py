from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
RAW_DIR = ROOT / "data" / "raw"
PREPARED_DIR = ROOT / "data" / "prepared"
RESULTS_DIR = ROOT / "results"
PLOT_DIR = ROOT / "plots"
RAW_FILES = {
    "bfi_rec1": RAW_DIR / "meanBFI_rec1Vehicle.csv",
    "bfi_rec2": RAW_DIR / "meanBFI_rec2Empa.csv",
    "bp_rec1": RAW_DIR / "meanBP_rec1Vehicle.csv",
    "bp_rec2": RAW_DIR / "meanBP_rec2Empa.csv",
    "frequency": RAW_DIR / "frequency.csv",
    "power": RAW_DIR / "power.csv",
    "vein_glucose": RAW_DIR / "vein_glucose.csv",
    "biochem_vehicle": RAW_DIR / "biochem_data_vehicle.csv",
    "biochem_change": RAW_DIR / "biochem_data_change_empa_vehicle.csv",
}
PREPARED_FILES = {
    "bfi": PREPARED_DIR / "bfi.csv",
    "bfi_empa": PREPARED_DIR / "bfi_empa.csv",
    "bfi_vehicle": PREPARED_DIR / "bfi_vehicle.csv",
    "bp": PREPARED_DIR / "bp.csv",
    "bp_empa": PREPARED_DIR / "bp_empa.csv",
    "bp_vehicle": PREPARED_DIR / "bp_vehicle.csv",
    "frequency": PREPARED_DIR / "frequency.csv",
    "power": PREPARED_DIR / "power.csv",
    "biochem": PREPARED_DIR / "biochem.csv",
    "blood_glucose": PREPARED_DIR / "blood_glucose.csv",
    "urine_flow_vehicle": PREPARED_DIR / "urine_flow_vehicle.csv",
    "excretion_glucose_vehicle": PREPARED_DIR / "excretion_glucose_vehicle.csv",
    "excretion_na_vehicle": PREPARED_DIR / "excretion_na_vehicle.csv",
    "plasma_na_vehicle": PREPARED_DIR / "plasma_na_vehicle.csv",
    "urine_flow_empa_minus_vehicle": PREPARED_DIR
    / "urine_flow_empa_minus_vehicle.csv",
    "excretion_glucose_empa_minus_vehicle": PREPARED_DIR
    / "excretion_glucose_empa_minus_vehicle.csv",
    "excretion_na_empa_minus_vehicle": PREPARED_DIR
    / "excretion_na_empa_minus_vehicle.csv",
    "plasma_na_empa_minus_vehicle": PREPARED_DIR
    / "plasma_na_empa_minus_vehicle.csv",
    "urine_flow_log_empa_minus_log_vehicle": PREPARED_DIR
    / "urine_flow_log_empa_minus_log_vehicle.csv",
    "excretion_glucose_log_empa_minus_log_vehicle": PREPARED_DIR
    / "excretion_glucose_log_empa_minus_log_vehicle.csv",
    "excretion_na_log_empa_minus_log_vehicle": PREPARED_DIR
    / "excretion_na_log_empa_minus_log_vehicle.csv",
    "plasma_na_log_empa_minus_log_vehicle": PREPARED_DIR
    / "plasma_na_log_empa_minus_log_vehicle.csv",
}
