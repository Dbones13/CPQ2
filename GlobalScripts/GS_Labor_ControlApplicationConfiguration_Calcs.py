def GS_Labor_ControlApplicationConfiguration_Calcs(attrs):
    import math
    ai = attrs.AI
    ao = attrs.AO
    di = attrs.DI
    do = attrs.DO
    cl=float(attrs.total_count_Typicals_Prototypes)
    PIDLoops=float(attrs.PIDLoops)
    AIIndicator=float(attrs.AIIndicator)
    Digital1Loop=float(attrs.Digital1Loop)
    Digital2Loop=float(attrs.Digital2Loop)
    DIIndicator=float(attrs.DIIndicator)
    TPY=float(attrs.TPY)
    TD=cl*300.0/60.0
    HC=math.ceil(io*2.0/60.0)
    IL=math.ceil((AIIndicator+DIIndicator)*20.0/60.0)
    BL=math.ceil((PIDLoops+Digital1Loop+Digital2Loop)*30.0/60.0)
    SL= math.ceil((round(PIDLoops*0.75)+round(Digital1Loop*0.75)+round(Digital2Loop*0.75))*10.0/60.0)
    ML =math.ceil((round(PIDLoops*0.1)+round(Digital1Loop*0.1)+round(Digital2Loop*0.1))*30.0/60.0)
    CL =(round(PIDLoops*0.1)+round(Digital1Loop*0.1)+round(Digital2Loop*0.1))*120.0/60.0
    VL =(round(PIDLoops*0.05)+round(Digital1Loop*0.05)+round(Digital2Loop*0.05))*480.0/60.0
    SEQ = float(attrs.seq)*600.0/60.0
    Comap =math.ceil(((PIDLoops*8+AIIndicator*3+Digital1Loop*8+Digital2Loop*10+DIIndicator*2))*1/60)
    QDB =math.ceil(((PIDLoops*6+AIIndicator*3+Digital1Loop*6+Digital2Loop*8+DIIndicator*2))*3/60)
    calcTPY = math.ceil(TPY*10/60)
    Hrs = TD + HC + IL + BL + SL + ML + CL + VL + SEQ + Comap + QDB + calcTPY
    return Hrs
