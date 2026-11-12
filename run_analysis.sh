#!/bin/bash

# Exit on error
set -e

echo "Starting kidney data analysis pipeline..."

echo "Step 1: Preparing data..."
uv run scripts/prepare_data.py

echo "Step 2: Fitting models..."
uv run scripts/run_mcmc.py
uv run scripts/run_mcmc_new.py

echo "Step 3: Executing notebook..."
uv run jupyter execute notebooks/analyse\ fits-BloodGlucose_overall_effects.ipynb
uv run jupyter execute notebooks/analyse\ fits.ipynb
uv run jupyter execute notebooks/ppc_biochem_bodyweight.ipynb
uv run jupyter execute notebooks/blood\ glucose.ipynb
uv run jupyter execute notebooks/analyse\ fits-bfi-new.ipynb
uv run jupyter execute notebooks/analyse\ fits-BodyWeight_overall_effects.ipynb
uv run jupyter execute notebooks/analyse\ fits-BloodGlucose_overall_effects.ipynb
uv run jupyter execute notebooks/analyse\ fits-bp_overall_effects.ipynb
uv run jupyter execute notebooks/analyse\ fits-ExcretionGlucose_overall_effects.ipynb
uv run jupyter execute notebooks/analyse\ fits-ExcretionNa_overall_effects.ipynb
uv run jupyter execute notebooks/analyse\ fits-freq.ipynb
uv run jupyter execute notebooks/analyse\ fits-PlasmaNa_overall_effects.ipynb
uv run jupyter execute notebooks/analyse\ fits-pow.ipynb
uv run jupyter execute notebooks/analyse\ fits-UrineFlow_overall_effects.ipynb
uv run jupyter execute notebooks/new/analyse\ fits\ baseline\ power.ipynb
uv run jupyter execute notebooks/new/analyse\ fits\ power\ change.ipynb
uv run jupyter execute notebooks/new/analyse\ fits\ frequency\ baseline.ipynb
uv run jupyter execute notebooks/new/analyse\ fits\ frequency\ change.ipynb
uv run jupyter execute notebooks/new/analyse\ fits\ baseline\ activity\ types.ipynb

echo "Analysis pipeline completed successfully!"
