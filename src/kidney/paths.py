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
}
