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
uv run jupyter execute notebooks/analyse\ fits.ipynb
uv run jupyter execute notebooks/biochem.ipynb
uv run jupyter execute notebooks/blood\ glucose.ipynb
uv run jupyter execute notebooks/analyse\ fits-bfi.ipynb
uv run jupyter execute notebooks/analyse\ fits-BloodGlucose.ipynb
uv run jupyter execute notebooks/analyse\ fits-bp.ipynb
uv run jupyter execute notebooks/analyse\ fits-ExcretionGlucose.ipynb
uv run jupyter execute notebooks/analyse\ fits-ExcretionNa.ipynb
uv run jupyter execute notebooks/analyse\ fits-freq.ipynb
uv run jupyter execute notebooks/analyse\ fits-PlasmaNa.ipynb
uv run jupyter execute notebooks/analyse\ fits-pow.ipynb
uv run jupyter execute notebooks/analyse\ fits-UrineFlow.ipynb
uv run jupyter execute notebooks/new/analyse\ fits\ baseline\ power.ipynb
uv run jupyter execute notebooks/new/analyse\ fits\ power\ change.ipynb
uv run jupyter execute notebooks/new/analyse\ fits\ frequency\ baseline.ipynb
uv run jupyter execute notebooks/new/analyse\ fits\ frequency\ change.ipynb
uv run jupyter execute notebooks/new/analyse\ fits\ baseline\ activity\ types.ipynb

echo "Analysis pipeline completed successfully!"
