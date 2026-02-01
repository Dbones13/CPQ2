def GS_RTU_Procure_Materials_Services_calcs(par):
    replica = int(par.rtu)
    if replica < 48:
        cal_hrs = 20
    elif replica >= 48 and replica < 168:
        cal_hrs = 30
    else:
        cal_hrs = 40
    return cal_hrs