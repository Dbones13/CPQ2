#import GS_PLC_Labor_Parameters
def GS_Labor_Integration_Calcs(attrs):
    ai =  attrs.AI
    ao =  attrs.AO
    di =  attrs.DI
    do =  attrs.DO
    c=ai+ao+di+do
    if  c>0 and c<=1000:
        return 40
    elif c>1000 and c<=5000:
        return 60
    else:
        return 80