def GS_RTU_Software_Configuration_Calcs(attrs):
    ctrl_grp_cnt = int(attrs.cg_count)
    Trace.Write("Total Control groups = "+str(ctrl_grp_cnt))
    Hrs = 0.0
    if hasattr(attrs, 'stn'):
        stn = float(attrs.stn)
    else:
        stn = 0.0
    if hasattr(attrs, 'Rswt'):
        rswt = float(attrs.Rswt)
    else:
        rswt = 0.0
    i = 1
    while i <= ctrl_grp_cnt:
        if hasattr(attrs, str('iom_' + str(i))):
            iom = float(getattr(attrs, str('iom_' + str(i))))
        else:
            iom = 0.0
        if hasattr(attrs, str('ai_' + str(i))):
            ai = float(getattr(attrs, str('ai_' + str(i))))
        else:
            ai = 0.0
        if hasattr(attrs, str('ao_' + str(i))):
            ao = float(getattr(attrs, str('ao_' + str(i))))
        else:
            ao = 0.0
        if hasattr(attrs, str('di_' + str(i))):
            di = float(getattr(attrs, str('di_' + str(i))))
        else:
            di = 0.0
        if hasattr(attrs, str('do_' + str(i))):
            do = float(getattr(attrs, str('do_' + str(i))))
        else:
            do = 0.0
        if hasattr(attrs, str('ffio_' + str(i))):
            ffio = float(getattr(attrs, str('ffio_' + str(i))))
        else:
            ffio = 0.0
        if hasattr(attrs, str('wio_' + str(i))):
            wio = float(getattr(attrs, str('wio_' + str(i))))
        else:
            wio = 0.0
        if hasattr(attrs, str('sl_' + str(i))):
            sl = float(getattr(attrs, str('sl_' + str(i))))
        else:
            sl = 0.0
        if hasattr(attrs, str('cl_' + str(i))):
            cl = float(getattr(attrs, str('cl_' + str(i))))
        else:
            cl = 0.0
        if hasattr(attrs, str('se_' + str(i))):
            se = float(getattr(attrs, str('se_' + str(i))))
        else:
            se = 0.0
        if hasattr(attrs, str('ce_' + str(i))):
            ce = float(getattr(attrs, str('ce_' + str(i))))
        else:
            ce = 0.0
        if hasattr(attrs, str('aga_' + str(i))):
            aga = float(getattr(attrs, str('aga_' + str(i))))
        else:
            aga = 0.0
        if hasattr(attrs, str('ins_' + str(i))):
            ins = int(getattr(attrs, str('ins_' + str(i))))
        else:
            ins = 0
        Hrs_tmp_1 = 0.0
        Hrs_tmp_2 = 0.0
        Hrs_tmp_1 = 20+((iom*5+(ai+ao+di+do+ffio+wio)*4+sl*30+cl*90+se*30+ce*90+aga*20+(ffio+wio)*1)/60)*1.3
        Hrs_tmp_2 = Hrs_tmp_1 * 0.1 * (ins-1)
        Hrs = Hrs + Hrs_tmp_1 + Hrs_tmp_2
        i += 1
    Hrs = Hrs + ((stn + rswt)*3*1.3)
    return round(Hrs,2)