from pathlib import Path
import bambi as bmb
import polars as pl

from kidney.model_configuration import MODEL_CONFIGS
from kidney.paths import RESULTS_DIR


ROOT = Path(__file__).parent.parent


def main():
    for mc in MODEL_CONFIGS:
        print(f"Analysing {mc.name} data (outcome column: {mc.outcome})")
        msts = pl.read_csv(mc.csv)
        model = bmb.Model(formula=mc.formula, data=msts.to_pandas())
        idata = model.fit(
            target_accept=0.95,
            idata_kwargs={"log_likelihood": True},
        )
        model.predict(
            idata,
            data=msts.to_pandas(),
            kind="response",
            inplace=True,
        )
        model.predict(
            idata,
            data=msts.to_pandas(),
            kind="response_params",
            inplace=True,
        )
        idata.to_netcdf(RESULTS_DIR / f"idata_{mc.name}.nc")


if __name__ == "__main__":
    main()
