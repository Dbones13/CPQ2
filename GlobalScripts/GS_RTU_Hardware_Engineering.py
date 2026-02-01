def GS_RTU_Hardware_Engineering(attrs):
    LTp = int(attrs.LTp)
    if attrs.Loop == 'Yes':
        loop_hrs_1 = (8+LTp*10)*1.3
    else:
        loop_hrs_1 = 0
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
        if attrs.Loop == 'Yes':
            locals()["lp_{}".format(str(i))] = (ai+ao+di+do)*ins
        else:
            locals()["lp_{}".format(str(i))] = 0
        ioFlag = False
        cabFlag = False
        if (i == 1):
            #IO Hrs
            if int(ins) > 0:
                locals()["io{}_hrs".format(str(i))] = (2+(ai+ao+di+do)*1/60+8 + (ai+ao+di+do)*3/60) * (1+0.1*(ins - 1)) # IO1
                ioFlag = True
            else:
                locals()["io{}_hrs".format(str(i))] = 0
                ioFlag = True
            # Cab Hrs
            if int(ins) > 0 and int(scab) > 0:
                locals()["cab{}_hrs".format(str(i))] =  97.5*(1+0.1*(ins * scab - 1)) # CAB1
                cabFlag = True
            else:
                locals()["cab{}_hrs".format(str(i))] = 0
                cabFlag = True
        else:
            #IO Hrs
            if int(ins) > 0 and hws == 'NA':
                locals()["io{}_hrs".format(str(i))] =  (2+(ai+ao+di+do) * 1/60+8 + (ai+ao+di+do) * 3/60) * (1+0.1*(ins - 1))
                ioFlag = True
            elif int(ins) > 0:
                loop_count = i-1
                for j in range(1,loop_count+1):
                    CG = "CG" + str(j)
                    Trace.Write('Comparing Control Group: ' + CG)
                    if hws == CG:
                        Trace.Write("HWS Control Group: " + CG)
                        # Getting the specific Control Group's ins,ai,ao,di,do 
                        ins_j = float(getattr(attrs,"ins_" + str(j)))
                        ai_j = float(getattr(attrs,"ai_" + str(j)))
                        ao_j= float(getattr(attrs,"ao_" + str(j)))
                        di_j = float(getattr(attrs,"di_" + str(j)))
                        do_j = float(getattr(attrs,"do_" + str(j)))
                        locals()["io{}_hrs".format(str(i))] =  (2+(ai_j+ao_j+di_j+do_j)*1/60+8 + (ai_j+ao_j+di_j+do_j)*3/60)*(0.3+0.1*(ins - 1))
                        ioFlag = True
            #CAB Hrs
            if int(ins) > 0 and int(scab) > 0 and hws == 'NA':
                locals()["cab{}_hrs".format(str(i))] = 97.5*(1+0.1*(ins * scab - 1))
                cabFlag = True
            elif int(ins) > 0 and int(scab)> 0:
                locals()["cab{}_hrs".format(str(i))] = 97.5*(0.3+0.1*(ins * scab - 1))
                cabFlag = True
            else:
                locals()["cab{}_hrs".format(str(i))] = 0
                cabFlag = True

        if not ioFlag:
            locals()["io{}_hrs".format(str(i))] =0
        if not cabFlag:
            locals()["cab{}_hrs".format(str(i))] =0
        
        locals()["CG{}_Hrs".format(str(i))] = locals()["cab{}_hrs".format(str(i))] + locals()["io{}_hrs".format(str(i))]
    ttl_calculated_hrs = 0
    loop_hrs_2 = 0
    for i in range(1,cg_count+1):
        loop_hrs_2 += locals()["lp_{}".format(str(i))]
        ttl_calculated_hrs += float(locals()["CG{}_Hrs".format(str(i))])
    if attrs.Loop == 'Yes':
        final_loop_hrs = loop_hrs_1 + (30 + (loop_hrs_2)*4/60) * 1.3
    else:
        final_loop_hrs = 0
    ttl_calculated_hrs += final_loop_hrs
    return ttl_calculated_hrs