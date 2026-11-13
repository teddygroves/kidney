from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
RAW_DIR = ROOT / "data" / "raw"
PREPARED_DIR = ROOT / "data" / "prepared"
RESULTS_DIR = ROOT / "results"
PLOT_DIR = ROOT / "plots"
RAW_DIR_NEW = RAW_DIR / "new"
PREPARED_DIR_NEW = PREPARED_DIR / "new"
RESULTS_DIR_NEW = RESULTS_DIR / "new"
PLOT_DIR_NEW = PLOT_DIR / "new"
RAW_FILES = {
    "body_weight": RAW_DIR / "body_weight.csv",
    "bfi_rec1": RAW_DIR / "meanBFI_rec1Vehicle.csv",
    "bfi_rec2": RAW_DIR / "meanBFI_rec2Empa.csv",
    "bp_rec1": RAW_DIR / "meanBP_rec1Vehicle.csv",
    "bp_rec2": RAW_DIR / "meanBP_rec2Empa.csv",
    "frequency": RAW_DIR / "frequency.csv",
    "power": RAW_DIR / "power.csv",
    "vein_glucose": RAW_DIR / "vein_glucose.csv",
    "biochem_vehicle": RAW_DIR / "biochem_data_vehicle.csv",
    "biochem_change": RAW_DIR / "biochem_data_change_empa_vehicle.csv",
    "baseline_power_lfb": RAW_DIR_NEW / "power_baseline_LowFrqBand_all.csv",
    "baseline_power_cb": RAW_DIR_NEW / "power_baseline_canonBand_all.csv",
    "power_change": RAW_DIR_NEW / "power_change.csv",
    "frequency_new": RAW_DIR_NEW / "frequency.csv",
    "baseline_activity_types": RAW_DIR_NEW / "baseline_activity_types.csv",
}
PREPARED_FILES = {
    "body_weight": PREPARED_DIR / "body_weight.csv",
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
PREPARED_FILES_NEW = {
    "baseline_power_vehicle_cb": PREPARED_DIR_NEW / "baseline_power_vehicle_cb.csv",
    "baseline_power_empa_cb": PREPARED_DIR_NEW / "baseline_power_empa_cb.csv",
    "baseline_power_vehicle_lfb": PREPARED_DIR_NEW / "baseline_power_vehicle_lfb.csv",
    "baseline_power_empa_lfb": PREPARED_DIR_NEW / "baseline_power_empa_lfb.csv",
    
    "power_change_vehicle": PREPARED_DIR_NEW / "power_change_vehicle.csv",
    "power_change_empa": PREPARED_DIR_NEW / "power_change_empa.csv",
    "frequency_vehicle": PREPARED_DIR_NEW / "frequency_vehicle.csv",
    "frequency_empa": PREPARED_DIR_NEW / "frequency_empa.csv",
    **{
        f"{name}_{treatment}_{activity_type}": PREPARED_DIR_NEW
        / f"{name}_{treatment}_{activity_type}.csv"
        for name in ("power_change", "frequency")
        for treatment in ("vehicle", "empa")
        for activity_type in ("single", "double")
    },
    "baseline_activity_types_vehicle": PREPARED_DIR_NEW
    / "baseline_activity_types_vehicle.csv",
    "baseline_activity_types_empa": PREPARED_DIR_NEW
    / "baseline_activity_types_empa.csv",
}
