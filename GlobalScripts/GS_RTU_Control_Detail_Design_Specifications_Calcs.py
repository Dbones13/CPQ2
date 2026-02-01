def GS_RTU_Control_Detail_Design_Specifications_Calcs(par):
    replica = int(par.rtu)
    if replica < 48:
        cal_hrs = 50
    elif replica >= 48 and replica < 168:
        cal_hrs = 79
    else:
        cal_hrs = 116
    return cal_hrs