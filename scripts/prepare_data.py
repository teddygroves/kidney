from pathlib import Path
import numpy as np
import polars as pl

HERE = Path(__file__).parent
ROOT = HERE.parent
RAW_DIR = ROOT / "data" / "raw"
PREPARED_DIR = ROOT / "data" / "prepared"
RAW_FILES = {
    "bfi_rec1": RAW_DIR / "meanBFI_rec1Vehicle.csv",
    "bfi_rec2": RAW_DIR / "meanBFI_rec2Empa.csv",
}
PREPARED_FILES = {"bfi": PREPARED_DIR / "bfi.csv"}


def standardise(x: pl.Expr):
    return (x - x.mean()) / x.std()


def main():
    print(f"readiing {RAW_FILES['bfi_rec1']}...")
    bfi_rec1 = pl.read_csv(RAW_FILES["bfi_rec1"])
    print(f"readiing {RAW_FILES['bfi_rec2']}...")
    bfi_rec2 = pl.read_csv(RAW_FILES["bfi_rec2"])
    bfi = pl.concat([bfi_rec1, bfi_rec2])
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
            log_bfi_change=pl.col("log_bfi_injected") - pl.col("log_bfi_baseline")
        )
    )
    print(f"writing {PREPARED_FILES['bfi']}...")
    bfi.write_csv(PREPARED_FILES["bfi"])


if __name__ == "__main__":
    main()
