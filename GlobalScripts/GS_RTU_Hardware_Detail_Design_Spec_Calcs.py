def GS_RTU_Hardware_Detail_Design_Spec_Calcs(param):
    replica = int(param.rtu)
    if replica < 48:
        cal_hrs = 50
    elif replica >= 48 and replica < 168:
        cal_hrs = 79
    else:
        cal_hrs= 116
    return cal_hrs