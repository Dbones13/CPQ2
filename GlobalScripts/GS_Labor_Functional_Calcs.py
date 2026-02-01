def GS_Labor_Functional_Calcs(attrs):
    ai = attrs.AI
    ao = attrs.AO
    di = attrs.DI
    do = attrs.DO
    C = ai + ao + di + do
    if C>0 and C<=5000:
        return 24
    else:
        return 40