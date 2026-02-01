def GS_Labor_Operation_Calcs(attrs):
    #CXCPQ-22528
    AI = attrs.AI
    AO = attrs.AO
    DO = attrs.DO
    DI = attrs.DI
    #C = 0
    C = AI + AO + DI + DO
    if (C <= 400):
        operation_hrs = 20
    elif (C > 400 and C <= 2000):
        operation_hrs = 30
    elif (C > 2000 and C <= 5000):
        operation_hrs = 40
    elif (C > 5000):
        operation_hrs = 100
    return operation_hrs