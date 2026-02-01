def GS_UOC_Labor_BatchDesignWorkshop_Calcs(attrs):
    pT = attrs.process_type
    Hrs = 40 if pT in  ['BatchPharma', 'BatchChemical']  else 0
    return Hrs