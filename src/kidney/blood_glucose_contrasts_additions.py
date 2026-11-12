def get_t_groups_glucose(idata, stage="baseline"):
    """Group log-scale predictors at a glucose stage (rat random effect = 0).

    Reference: baseline, fa/+, female. Assumes treatment-coded Bambi terms.
    """
    if stage not in ("baseline", "vehicle", "empa"):
        raise ValueError(f"Unknown stage: {stage}")

    posterior = idata.posterior

    def coefficient(name, label=None):
        da = posterior[name]
        other_dims = [dim for dim in da.dims if dim not in ("chain", "draw")]
        if label is None:
            if len(other_dims) != 1 or da.sizes[other_dims[0]] != 1:
                raise ValueError(f"Expected one coefficient for {name}: {other_dims}")
            return da.isel({other_dims[0]: 0}, drop=True)
        if len(other_dims) != 1:
            raise ValueError(f"Expected one coefficient dimension for {name}")
        return da.sel({other_dims[0]: label}, drop=True)

    intercept = posterior["Intercept"]
    g = coefficient("gtyp")
    s = coefficient("sex")

    if stage != "baseline":
        intercept = intercept + coefficient("stage", stage)
        g = g + coefficient("stage:gtyp", f"{stage}, fa/fa")
        s = s + coefficient("stage:sex", f"{stage}, M")

    return {
        "fa/+:female": intercept,
        "fa/+:male": intercept + s,
        "fa/fa:female": intercept + g,
        "fa/fa:male": intercept + g + s,
    }


def get_overall_effects_glucose(t_groups):
    """Genotype and sex contrasts, equally averaged over the other factor."""
    return {
        "fa/fa - fa/+": (
            (t_groups["fa/fa:female"] - t_groups["fa/+:female"])
            + (t_groups["fa/fa:male"] - t_groups["fa/+:male"])
        ) / 2,
        "male - female": (
            (t_groups["fa/+:male"] - t_groups["fa/+:female"])
            + (t_groups["fa/fa:male"] - t_groups["fa/fa:female"])
        ) / 2,
    }


def subtract_t_groups_glucose(later, earlier):
    """Paired posterior draws for stage change within each group."""
    if later.keys() != earlier.keys():
        raise ValueError("Group keys do not match")
    return {key: later[key] - earlier[key] for key in later}
