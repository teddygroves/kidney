DEFAULT_FORMULA = "{y} ~ (1|rat) + gtyp + age + sex + gtyp:age + gtyp:sex"
FORMULA_BP = "{y} ~ gtyp + age + sex + gtyp:age + gtyp:sex"
ANALYSIS_TO_FORMULA = {
    "bfi_vehicle": DEFAULT_FORMULA,
    "bfi_empa": DEFAULT_FORMULA,
    "bp_vehicle": FORMULA_BP,
    "bp_empa": FORMULA_BP,
    "frequency": DEFAULT_FORMULA,
    "power": DEFAULT_FORMULA,
}
ANALYSIS_TO_OUTCOME = {
    "bfi_vehicle": "bfi_change",
    "bfi_empa": "bfi_change",
    "bp_vehicle": "bp_change",
    "bp_empa": "bp_change",
    "frequency": "frequency_change",
    "power": "power_change",
}
