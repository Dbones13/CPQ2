def GS_RTU_Project_Close_Out_Report(param):
    replica = int(param.rtu)
    if replica < 48:
        cal_hrs = 8
    elif replica >= 48 and replica < 168:
        cal_hrs = 16
    else:
        cal_hrs = 24
    return cal_hrs