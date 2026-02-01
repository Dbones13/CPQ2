#import GS_PLC_Labor_Parameters
def GS_Labor_Acceptance_Calcs(attrs):
    ai =  attrs.AI
    ao =  attrs.AO
    di =  attrs.DI
    do =  attrs.DO
    fat=attrs.perc_fat
    c=ai+ao+di+do
    if (c*fat/100) > 0 and (c*fat/100) <=1000:
        return 80
    elif (c*fat/100) > 1000 and (c*fat/100) <=5000:
        return 160
    else:
        return 360