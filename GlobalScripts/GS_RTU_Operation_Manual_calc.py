def GS_RTU_Operation_Manual_calc(param):
    replica = int(param.rtu)
    if replica < 48:
        cal_hrs = 40
    elif replica >= 48 and replica < 168:
        cal_hrs = 60
    else:
        cal_hrs = 96
    return cal_hrs