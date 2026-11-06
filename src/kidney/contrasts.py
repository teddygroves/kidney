"""Contrasts between gtyp/age/sex groups, as requested in the brief.

Groups are keyed "gtyp,sex,age", e.g. "fa/fa,male,young". Effects of one
factor are averaged with equal weights over the levels of the other factors.
"""

GTYPS = ("fa/+", "fa/fa")
SEXES = ("female", "male")
AGES = ("adult", "young")

def get_t_groups(idata):
    """Linear predictor of each group relative to fa/+,female,adult.

    Terms shared by all groups (e.g. Intercept, band, activity_type) cancel in
    contrasts, so they are left out.
    """

    def term(name):
        # Each categorical term has a single non-reference level
        return idata.posterior[name].isel({f"{name}_dim": 0}, drop=True)

    g, a, s = term("gtyp"), term("age"), term("sex")
    ga, gs = term("gtyp:age"), term("gtyp:sex")
    return {
        "fa/+,female,adult": 0 * g,
        "fa/+,female,young": a,
        "fa/+,male,adult": s,
        "fa/+,male,young": s + a,
        "fa/fa,female,adult": g,
        "fa/fa,female,young": g + a + ga,
        "fa/fa,male,adult": g + s + gs,
        "fa/fa,male,young": g + s + gs + a + ga,
    }

def get_t_groups_power_baseline(idata, band="canon"):
    """Group predictors relative to fa/+,female,adult within a band.

    Shared terms (Intercept, band) cancel in within-band contrasts.
    """

    def term(name):
        return idata.posterior[name].isel(
            {f"{name}_dim": 0}, drop=True
        )

    g, a, s = term("gtyp"), term("age"), term("sex")
    ga, gs = term("gtyp:age"), term("gtyp:sex")

    if band == "low_frequency":
        g = g + term("band:gtyp")
        a = a + term("band:age")
        s = s + term("band:sex")
        gs = gs + term("band:gtyp:sex")
    elif band != "canon":
        raise ValueError(f"Unknown band: {band}")

    return {
        "fa/+,female,adult": 0 * g,
        "fa/+,female,young": a,
        "fa/+,male,adult": s,
        "fa/+,male,young": s + a,
        "fa/fa,female,adult": g,
        "fa/fa,female,young": g + a + ga,
        "fa/fa,male,adult": g + s + gs,
        "fa/fa,male,young": g + s + gs + a + ga,
    }


def gtyp_diff(t_groups, sexes=SEXES, ages=AGES):
    diffs = [
        t_groups[f"fa/fa,{s},{a}"] - t_groups[f"fa/+,{s},{a}"]
        for s in sexes
        for a in ages
    ]
    return sum(diffs) / len(diffs)


def age_diff(t_groups, gtyps=GTYPS, sexes=SEXES):
    diffs = [
        t_groups[f"{g},{s},young"] - t_groups[f"{g},{s},adult"]
        for g in gtyps
        for s in sexes
    ]
    return sum(diffs) / len(diffs)


def sex_diff(t_groups, gtyps=GTYPS, ages=AGES):
    diffs = [
        t_groups[f"{g},male,{a}"] - t_groups[f"{g},female,{a}"]
        for g in gtyps
        for a in ages
    ]
    return sum(diffs) / len(diffs)


def get_overall_effects(t_groups):
    return {
        "fa/fa - fa/+": gtyp_diff(t_groups),
        "young - adult": age_diff(t_groups),
        "male - female": sex_diff(t_groups),
    }


def get_gtyp_given_sex_age(t_groups):
    return {
        "fa/fa - fa/+, female": gtyp_diff(t_groups, sexes=["female"]),
        "fa/fa - fa/+, male": gtyp_diff(t_groups, sexes=["male"]),
        "fa/fa - fa/+, adult": gtyp_diff(t_groups, ages=["adult"]),
        "fa/fa - fa/+, young": gtyp_diff(t_groups, ages=["young"]),
    }

def get_sex_given_gtyp_age(t_groups):
    return {
        "male - female, fa/fa": sex_diff(t_groups, gtyps=["fa/fa"]),
        "male - female, fa/+": sex_diff(t_groups, gtyps=["fa/+"]),
        "male - female, adult": sex_diff(t_groups, ages=["adult"]),
        "male - female, young": sex_diff(t_groups, ages=["young"]),
    }

def get_age_given_sex_age(t_groups):
    return {
        "young - adult, female": age_diff(t_groups, sexes=["female"]),
        "young - adult, male": age_diff(t_groups, sexes=["male"]),
        "young - adult, fa/+": age_diff(t_groups, gtyps=["fa/+"]),
        "young - adult, fa/fa": age_diff(t_groups, gtyps=["fa/fa"]),
    }