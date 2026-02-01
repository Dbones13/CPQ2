def GS_UOC_PharmaQADocumentation_Calcs(attrs):
    bsd = int(attrs.simple_complexity)
    bmd = int(attrs.medium_complexity)
    bcd = int(attrs.complex_complexity)
    pT = attrs.process_type
    Hrs = ( bsd * 8 + bmd * 22 + bcd * 48) if pT == 'BatchPharma' else 0
    return Hrs