def GS_RTU_System_Integration_Internal_Test_Pre_Fat(attrs):
    cg_count = attrs.cg_count
    for i in range(1,cg_count+1):
        ins = float(getattr(attrs,"ins_" + str(i)))
        scab = float(getattr(attrs,"scab_" + str(i)))
        ai = float(getattr(attrs,"ai_" + str(i)))
        ao = float(getattr(attrs,"ao_" + str(i)))
        di = float(getattr(attrs,"di_" + str(i)))
        do = float(getattr(attrs,"do_" + str(i)))
        wio = float(getattr(attrs,"wio_" + str(i)))
        ffio = float(getattr(attrs,"ffio_" + str(i)))
        hws = getattr(attrs,"hws_" + str(i))
        smFlag = False
        if (i == 1):
            if int(ins) > 0:
                locals()["CG{}_Hrs_P1".format(str(i))] =(90+scab*240+(ai+ao+di+do)*(4+4) +(ffio+wio)*(3+4))/60
                locals()["CG{}_Hrs_P2".format(str(i))] = locals()["CG{}_Hrs_P1".format(str(i))] * 0.5 *(ins-1)
                smFlag = True
            else:
                locals()["CG{}_Hrs_P1".format(str(i))] =0
                locals()["CG{}_Hrs_P2".format(str(i))] =0
                smFlag = True
        else:
            if int(ins) > 0 and hws == 'NA':
                locals()["CG{}_Hrs_P1".format(str(i))] = (90+scab*240+(ai+ao+di+do) *(4+4) +(ffio+wio) *(3+4))/60
                locals()["CG{}_Hrs_P2".format(str(i))] = locals()["CG{}_Hrs_P1".format(str(i))] * 0.5 *(ins-1)
                smFlag = True
            elif int(ins) > 0:
                loop_count = i-1
                for j in range(1,loop_count+1):
                    CG = "CG" + str(j)
                    Trace.Write('Comparing Control Group: ' + CG)
                    if hws == CG:
                        Trace.Write("HWS Control Group: " + CG)
                        locals()["CG{}_Hrs_P1".format(str(i))] = locals()["CG{}_Hrs_P1".format(str(j))] *0.8 # CG2 Hrs P1
                        locals()["CG{}_Hrs_P2".format(str(i))] = locals()["CG{}_Hrs_P1".format(str(j))] * 0.5 *(ins-1) # CG2 Hrs P2
                        smFlag = True
                        break
        if not smFlag:
            locals()["CG{}_Hrs_P1".format(str(i))] =0
            locals()["CG{}_Hrs_P2".format(str(i))] =0
        
    calculated_hrs = 0

    for i in range(1,cg_count+1):
        calculated_hrs += float(locals()["CG{}_Hrs_P1".format(str(i))]) + float(locals()["CG{}_Hrs_P2".format(str(i))])
    return calculated_hrs