def GS_RTU_Site_Installation(attrs):
    cg_count = attrs.cg_count
    calc = 0
    for i in range(1,cg_count+1):
        ins = float(getattr(attrs,"ins_" + str(i)))
        scab = float(getattr(attrs,"scab_" + str(i)))
        mar = float(getattr(attrs,"mar_" + str(i)))
        calc += (mar+scab)*ins

    calculated_Hrs = 6 + 6*(calc)
    return calculated_Hrs