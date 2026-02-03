from pathlib import Path
import bambi as bmb
import polars as pl

from kidney.model_configuration import ANALYSIS_TO_OUTCOME, ANALYSIS_TO_FORMULA
from kidney.paths import PREPARED_DIR, RESULTS_DIR


ROOT = Path(__file__).parent.parent


def main():
    for analysis, outcome in ANALYSIS_TO_OUTCOME.items():
        formula = ANALYSIS_TO_FORMULA[analysis]
        print(f"Analysing {analysis} data (outcome column: {outcome})")
        msts = pl.read_csv(PREPARED_DIR / f"{analysis}.csv")
        for lin_or_log, ycol in (("lin", outcome), ("log", "log_" + outcome)):
            bmb_formula = bmb.Formula(formula.format(y=ycol))
            model = bmb.Model(formula=bmb_formula, data=msts.to_pandas())
            idata = model.fit(
                target_accept_prob=0.95,
                idata_kwargs={"log_likelihood": True},
            )
            model.predict(
                idata,
                data=msts.to_pandas(),
                kind="response",
                inplace=True,
            )
            idata.to_netcdf(RESULTS_DIR / f"idata_{analysis}_{lin_or_log}.nc")


if __name__ == "__main__":
    main()
