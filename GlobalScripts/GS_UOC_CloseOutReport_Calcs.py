def GS_UOC_CloseOutReport_Calcs(attrs):
    sys = int(attrs.sys)
    mar = int (attrs.marshalling_cabinets)
    isi = 1 if int(attrs.is_ios) > 0 else 0 #'is' replaced with 'isi'
    ai = int(attrs.AI)
    ao = int(attrs.AO)
    do = int(attrs.DO)
    di = int(attrs.DI)
    proNIO  = int(attrs.profitnet_IO)
    eIPIO   = int(attrs.ethernet_IO)
    pcdi = int(attrs.peer_pcdi)
    cda = int(attrs.peer_cda)
    wio = ai + ao + do + di
    hio = wio + proNIO + eIPIO
    sio = pcdi + cda
    io = hio + sio
    if io<= 400:
        CP = 8
    elif io > 400 and io<=2000:
        CP = 12
    elif io>2000 and io<= 5000:
        CP = 16
    elif io> 5000:
        CP = 24
    HWHrs = (0.4 * (6 + 0.007 * ( sys * 20 + mar * (40+isi * 10) )))
    
    Hrs = (HWHrs + CP)
    return round(Hrs,2)