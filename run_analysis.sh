#!/bin/bash

# Exit on error
set -e

echo "Starting kidney data analysis pipeline..."

echo "Step 1: Preparing data..."
uv run scripts/prepare_data.py

echo "Step 2: Fitting models..."
uv run scripts/run_mcmc.py

echo "Step 3: Executing notebook..."
uv run jupyter execute notebooks/analyse\ fits.ipynb

echo "Analysis pipeline completed successfully!"
