def GS_Labor_Installation_Calcs(attrs):
    #Added by Abhijeet CXCPQ-22530
    if attrs.marshalling_cabinets == '':
        mar = 0
    elif attrs.marshalling_cabinets != '':
        mar = int(attrs.marshalling_cabinets)
    sys = attrs.num_cabinet
    installation_hrs1 = '{0:.2f}'.format(float(6 * (mar + sys)))
    installation_hrs = float(installation_hrs1)
    return installation_hrs