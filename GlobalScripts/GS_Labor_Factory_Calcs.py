#import GS_PLC_Labor_Parameters
def GS_Labor_Factory_Calcs(attrs):
    ai =  attrs.AI
    ao =  attrs.AO
    di =  attrs.DI
    do =  attrs.DO
    fat=float(attrs.perc_fat)
    Trace.Write("fat:"+str(fat))
    c=int(ai)+int(ao)+int(di)+int(do)
    #Trace.Write("c:"+c)
    if (c*fat/100) > 0 and (c*fat/100) <=1000:
        Trace.Write("inisde if")
        return 80
    elif (c*fat/100) > 1000 and (c*fat/100) <=5000:
        Trace.Write("inisde elif")
        return 160
    else:
        return 360