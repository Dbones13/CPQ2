def GS_Labor_Hardware_Calcs(attrs):
    import math
    ai = attrs.AI
    ao = attrs.AO
    di = attrs.DI
    do = attrs.DO
    c = ai+ao+di+do
    iot = float(attrs.iot)
    ld = attrs.loop_drawings
    if ld == 'Yes':
        ld= 1
    else:
        ld=0
    sys= float(attrs.num_cabinet)
    mar= float(attrs.marshalling_cabinets)
    hc=attrs.hrd_design
    if hc=='Complex':
        hc=1.1
    elif hc=='Medium':
        hc=0.7
    else:
        hc=0.5
    ctr=float(attrs.num_cpm)
    Trace.Write("here" +str(iot))
    lt=(10.0*iot*1.3)
    ld=(ld*(20.0+(c*4.0/60.0))*1.3)
    Trace.Write("lt:{0} ld:{1}".format(lt,ld))
    hdd=(math.ceil(14+((sys+mar)*hc*900.0/60.0))+ math.ceil(3.0*ctr*hc*1)+math.ceil(10*c*hc*5.0/60.0)+math.ceil(2*iot*hc*90.0/60.0)*1.3*1.3)

    return hdd+ld+lt
