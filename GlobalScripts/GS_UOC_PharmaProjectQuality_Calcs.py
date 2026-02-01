def GS_UOC_PharmaProjectQuality_Calcs(attrs):
    pT = attrs.process_type
    Trace.Write("Process Type:{}".format(pT))
    bpd = attrs.bpd
    Trace.Write("Prjoce Duration:{}".format(bpd))
    Hrs = (bpd * 24 ) if pT == 'BatchPharma' else 0
    return Hrs