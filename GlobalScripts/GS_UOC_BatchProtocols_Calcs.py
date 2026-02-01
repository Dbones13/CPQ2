def GS_UOC_BatchProtocols_Calcs(attrs):
    pT = attrs.process_type
    bmr = int(attrs.product_master_recipes)
    bpr = int(attrs.product_replicated)
    Hrs =  int(bmr*12 + bpr*6 ) if pT in  ['BatchPharma', 'BatchChemical']  else 0
    return Hrs