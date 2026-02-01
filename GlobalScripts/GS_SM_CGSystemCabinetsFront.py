def checkForMCARSpace(cab_spaces,switches,IOTAS,PSU,controller):

    if switches or PSU:
        cab_spaces[0][0] = ['True','True','True']
        cab_spaces[0][1] = ['True','True','True']
        switches -=6
        if switches < 0:
            switches = 0
        PSU -=4
        if PSU < 0:
            PSU = 0
    
    if controller:
        for space in range(0,len(cab_spaces)):
            for unit in range(0,len(cab_spaces[space])):
                for unit1 in range(0,len(cab_spaces[space][unit])):
                    if cab_spaces[space][unit][unit1] == False and controller:
                        controller-=1
                        cab_spaces[space][unit][unit1] = True
                        Trace.Write("Cab Space: {}".format(cab_spaces))
    
    if IOTAS:
        for space in range(0,len(cab_spaces)):
            for unit in range(0,len(cab_spaces[space])):
                for unit1 in range(0,len(cab_spaces[space][unit])):
                    if cab_spaces[space][unit][unit1] == False and IOTAS:
                        IOTAS-=1
                        cab_spaces[space][unit][unit1] = True
                        Trace.Write("Cab Space1: {}".format(cab_spaces))
    
    return cab_spaces,IOTAS,controller,PSU,switches
    


def checkForIntegrationBoard(cab_spaces, integrationBoardOccupied):

    if integrationBoardOccupied:
        for space in range(0,len(cab_spaces)):  
            for unit in range(0,len(cab_spaces[space])):
                if cab_spaces[space][unit] == [False, False, False]: 
                    for unit1 in range(0,len(cab_spaces[space][unit])):
                        if cab_spaces[space][unit][unit1] == False and integrationBoardOccupied:
                            integrationBoardOccupied-=1
                            cab_spaces[space][unit][unit1] = True
                            Trace.Write("Cab Space: {}".format(cab_spaces))

    
    return cab_spaces, integrationBoardOccupied

def getCGNoOfSystemCabinetFront(data):
    switches = data['switches'];switches1 = data['switches']
    IOTAS = data['totalIOTA']
    PSU = data['powerSupply'];PSU1 = data['powerSupply']
    controller = data['cpu']
    integrationBoardOccupied = data['integrationBoard']
    cab = 0
    controller *=2
    Trace.Write("Initial Values: Swichtes: {}, PSU: {}, controller: {}, IOTAS: {},Cab: {}, IB: {}".format(switches, PSU, controller , IOTAS,cab,integrationBoardOccupied))

    while 1:
        cab+=1
        cab_spaces = [
            [[False, False, False],[False,False,False],[False,False,False]],
            [[False, False, False],[False,False,False],[False,False,False]]
        ]
        cab_spaces,IOTAS,controller,PSU,switches = checkForMCARSpace(cab_spaces,switches,IOTAS,PSU,controller)

        cab_spaces, integrationBoardOccupied = checkForIntegrationBoard(cab_spaces, integrationBoardOccupied)
        
        Trace.Write("Swichtes: {}, PSU: {}, controller: {}, remainingSpace: {}, IOTAS: {},Cab: {}, IB: {}".format(switches, PSU, controller, str(cab_spaces) , IOTAS,cab,integrationBoardOccupied))
        if switches == 0 and PSU == 0 and controller==0 and IOTAS == 0 and integrationBoardOccupied == 0:
            break
    
    return cab,PSU1,switches1

#a = getCGNoOfSystemCabinetFront({})