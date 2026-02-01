def GS_Labor_Software_Calcs(attrs):
    #Added by Abhijeet - CXCPQ-22526
    #Added by Siddharth - CXCPQ-25780 (PMD System)
    ctr = int(attrs.num_cpm)
    pT =  attrs.process_type
    ai =  attrs.AI
    ao =  attrs.AO
    mm =  int(attrs.MODBUS)
    Swt = int(attrs.num_switches)
    if attrs.engineering_stations == '':
        stn = 0.00
    elif attrs.engineering_stations != '':
        stn = int(attrs.engineering_stations)
    #stn = int(attrs.engineering_stations) # need to be created
    do =  attrs.DO
    di =  attrs.DI
    pT = 0
    odd1 = "{0:.2f}".format((do)/1.2)
    odi1 = "{0:.2f}".format((di - (float(odd1)*1.5))/1.5)
    C = ai + ao + di + do
    if attrs.process_type == 'Continuous' or attrs.process_type == 'Continuous':
        pT = 1
    elif attrs.process_type == 'Continuous + Interlock' or attrs.process_type == 'ContinuousInterlock':
        pT = 1.2
    elif attrs.process_type == 'Continuous + Sequence' or attrs.process_type == 'ContinuousSequence':
        pT = 1.5
    elif attrs.process_type == 'Continuous + Interlock + Sequence' or attrs.process_type == 'ContinuousInterlockSequence':
        pT = 1.8
    elif attrs.process_type == 'None':
        pT = 0
    if C <= 400 :
        base = 24
    elif C>400 and C <= 2000:
        base = 32
    elif C > 2000 and C <= 5000:
        base = 40
    elif C > 5000 :
        base = 64
    odd = float(odd1)
    odi = float(odi1)
    software_hrs = '{0:.2f}'.format(float((base + 5.33 * ctr + pT *(0.1*(ai - ao)+0.6*ao + 0.6*float(odd) + 0.2*float(odi)))*0.6 + 0.5*mm + 1*Swt + 2*stn))
    return software_hrs