def GS_Labor_Close_Calcs(attrs):
    #CXCPQ-22527
    ai =  attrs.AI
    ao =  attrs.AO
    do =  attrs.DO
    di =  attrs.DI
    if attrs.marshalling_cabinets == '':
        mar = 0
    else:
        mar = int(attrs.marshalling_cabinets)
    sys = attrs.num_cabinet
    C = ai + ao + di + do
    CP = 0
    if C <= 400 :
        CP = 8
    elif C>400 and C <= 2000:
        CP = 12
    elif C > 2000 and C <= 5000:
        CP = 16
    elif C > 5000 :
        CP = 24
    HW_Hrs = 0.4 * (6 + 0.007 * (sys* 20 + mar * 40 ))
    close_hrs = '{0:.2f}'.format(HW_Hrs + CP)
    return close_hrs