def GS_RTU_Functional_Design_Spec_Calcs(param):
    replica = int(param.rtu)
    if replica < 48:
        cal_hrs = 24
    elif replica >= 48 and replica < 168:
        cal_hrs = 40
    else:
        cal_hrs = 40
    return cal_hrs