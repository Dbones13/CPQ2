def GS_Labor_Procedure_Calcs(attrs):
    ai = attrs.AI
    ao = attrs.AO
    di = attrs.DI
    do = attrs.DO
    C = ai + ao + di + do
    if C>0 and C<=1000:
        return 48
    elif C>1000 and C<=5000:
        return 64
    else:
        return 80