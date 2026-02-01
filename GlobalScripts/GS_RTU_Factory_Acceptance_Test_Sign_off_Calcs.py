def getAttr(obj, key, index):
    return getattr(obj, "{}{}".format(key, index))

def getFloat(var):
    if var:
        return float(var)
    return 0

def GS_RTU_Factory_Acceptance_Test_Sign_off_Calcs(param):
    calcHours = 0
    p1hrs = dict()
    for i in range(1, param.cg_count + 1):
        ins = getFloat(getAttr(param, 'ins_', i))
        if ins:
            ai = getFloat(getAttr(param, 'ai_', i))
            ao = getFloat(getAttr(param, 'ao_', i))
            di = getFloat(getAttr(param, 'di_', i))
            do = getFloat(getAttr(param, 'do_', i))
            ffio = getFloat(getAttr(param, 'ffio_', i))
            wio = getFloat(getAttr(param, 'wio_', i))
            scab = getFloat(getAttr(param, 'scab_', i))
            cgp1 = (60+scab*180+(ai+ao+di+do)*(3+4)+(ffio+wio)*(2+4))/60
            cgp2 = cgp1 * 0.3 * (ins - 1)


            hws = getAttr(param, 'hws_', i)
            if hws not in ['', 'NA']:
                cgp1 = p1hrs[hws] * 0.6
                cgp2 = p1hrs[hws] * 0.3 * (ins - 1)

            p1hrs['CG'+str(i)] = cgp1
            calcHours += (cgp1 + cgp2)
    return calcHours