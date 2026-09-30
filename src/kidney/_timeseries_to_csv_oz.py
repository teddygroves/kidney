import pandas as pd
import numpy as np

TIME_STGAES_TGF = dict(
    baseline = dict(t=slice(None, 0)),
    response = dict(t=slice(400, 800)), # We expect maximal power change in this time interval, based on how the average power changes with time. 
                                        # After this time, power may start to increase in some vessels.
)

TIME_STGAES_BFI = dict(
    baseline = dict(t=slice(None, 0)),
    response = dict(t=slice(400, None)), # We expect mean BFI to show maximal change here.
)

INDEX_COLUMNS = ['rat', 'age', 'sex', 'gtyp', 'treatment', 'vessel', 'band', 'activity_type']

def time_series_to_csv(data, time_stages_sele):
    results = []
    for rat, d in data.items():
        for stage, time_selection in time_stages_sele.items():
            d_mean = d.to_dataset()[['power_norm', 'frequency', 'bfi_orig', 'blood_pressure']].sel(time_selection).mean('t')

            r = d_mean.to_dataframe().reset_index()

            r['stage'] = stage
            r['rat'] = rat
            r['treatment'] = d_mean.attrs['treatment']
            r['sex'] = d_mean.attrs['sex']
            r['age'] = d_mean.attrs['age']
            r['gtyp'] = d_mean.attrs['gtyp']

            if rat == '20241021a': # Add 'band' manually since only one band was analyzed in this rat
                r['band'] = 'canonical'

            results.append(r)
    return pd.concat(results)

def make_table_with_bfi_response(data):
    table_long = time_series_to_csv(data, TIME_STGAES_BFI)
    x = table_long.pivot(values='bfi_orig', columns='stage', index=INDEX_COLUMNS).reset_index()
    x = x.drop(columns=['band']).drop_duplicates() # Band doesn't matter for mean BFI, only for oscillation power and frequency
    x['change'] = x.response - x.baseline
    x['change_rel'] = x.change / x.baseline
    return x

def make_table_with_bp_response(data, time_stages):
    table_long = time_series_to_csv(data, time_stages)
    x = table_long.pivot(values='blood_pressure', columns='stage', index=INDEX_COLUMNS).reset_index()
    x = x.drop(columns=['band']).drop_duplicates() # Band doesn't matter for mean BFI, only for oscillation power and frequency
    x['change'] = x.response - x.baseline
    x['change_rel'] = x.change / x.baseline
    return x.drop(columns=['vessel', 'activity_type']).drop_duplicates().reset_index() # one value per rat


def make_table_with_power_response(data):
    table_long = time_series_to_csv(data, TIME_STGAES_TGF)
    x = table_long.pivot(values='power_norm', columns='stage', index=INDEX_COLUMNS).reset_index()
    x['change'] = x.response / x.baseline
    x['change_log'] = np.log10( x.change )
    x['baseline_log'] = np.log10( x.baseline )
    return x

def make_table_with_frequency_response(data):
    table_long = time_series_to_csv(data, TIME_STGAES_TGF)
    x = table_long.pivot(values='frequency', columns='stage', index=INDEX_COLUMNS).reset_index()
    x['change'] = x.response - x.baseline
    return x
