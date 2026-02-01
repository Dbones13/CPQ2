def GS_RTU_Site_Acceptance_Test_Sign_off_Calcs(attrs):
    ctrl_grp_cnt = int(attrs.cg_count)
    Trace.Write("Total Control groups = "+ str(ctrl_grp_cnt))
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
            wio = int(getattr(attrs, str('wio_' + str(i))))
        else:
            wio = 0
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
        if hasattr(attrs, str('ins_' + str(i))):
            ins = float(getattr(attrs, str('ins_' + str(i))))
        else:
            ins = 0.0
        if hasattr(attrs, str('scab_' + str(i))):
            scab = float(getattr(attrs, str('scab_' + str(i))))
        else:
            scab = 0.0
        hws = getattr(attrs,"hws_" + str(i))
        locals()["CG{}_Hrs_P1".format(str(i))] = 0
        locals()["CG{}_Hrs_P2".format(str(i))] = 0
        if (i == 1):
            if int(ins) > 0:
                locals()["CG{}_Hrs_P1".format(str(i))] = 0.3 * ((60+(scab*180)+(ai+ao+di+do)*3+(ffio+wio)*2)/60+(ai+ao+di+do+ffio+wio)*2/60)
                locals()["CG{}_Hrs_P2".format(str(i))] = locals()["CG{}_Hrs_P1".format(str(i))] * 0.3 * (ins-1)
        else:
            if int(ins) > 0 and hws == 'NA':
                locals()["CG{}_Hrs_P1".format(str(i))] = 0.3 * ((60+(scab*180)+(ai+ao+di+do)*3+(ffio+wio)*2)/60+(ai+ao+di+do+ffio+wio)*2/60)
                locals()["CG{}_Hrs_P2".format(str(i))] = locals()["CG{}_Hrs_P1".format(str(i))] * 0.3 * (ins-1)
            elif int(ins) > 0:
                loop_count = i-1
                for j in range(1,loop_count+1):
                    CG = "CG" + str(j)
                    Trace.Write('Comparing Control Group: ' + CG)
                    if hws == CG:
                        Trace.Write("HWS Control Group: " + CG)
                        locals()["CG{}_Hrs_P1".format(str(i))] = locals()["CG{}_Hrs_P1".format(str(j))] * 0.6 # CG2 Hrs P1
                        locals()["CG{}_Hrs_P2".format(str(i))] = locals()["CG{}_Hrs_P1".format(str(j))] * 0.3 *(ins-1) # CG2 Hrs P2
                        break
        i += 1
    calculated_hrs = 0

    for i in range(1,ctrl_grp_cnt+1):
        calculated_hrs += float(locals()["CG{}_Hrs_P1".format(str(i))]) + float(locals()["CG{}_Hrs_P2".format(str(i))])
    return round(calculated_hrs, 2)