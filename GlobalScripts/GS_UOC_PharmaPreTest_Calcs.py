def GS_UOC_PharmaPreTest_Calcs(attrs):
    bmr = int(attrs.product_master_recipes)
    bpr = int(attrs.product_replicated)
    fat = float(attrs.perc_fat)
    bmu = int(attrs.batch_unit)
    bru = int(attrs.batch_unit_copies)
    F = 9.412 if attrs.process_type in ['Batch - Pharma', 'BatchPharma'] else 6.052
    bcscm = int(attrs.complex_scms)
    bpfat = float(attrs.percentage_pre_fat)
    bco = int(attrs.complex_ops)

    Hrs = (bpfat/100) *(( bmu + bru) *( F * 5 + 26.216 * bcscm) + 6.4 * bmu + 6 * bru + ( bmr + bpr ) * (4.66*5 + 11.55 * bco + 8.9)) if attrs.process_type == 'BatchPharma' else 0
    return round(Hrs,2)