#import getNoOfEDS316Switches
def RoundUp(n):
    if n:
        r = int(n)
    else:
        r = 0
    return r if r == n else r+1
#Trace.Write("Hello: "+str(RoundUp(15/2.0)))
#CXCPQ-31629 - Number of EDS-316 switches
def getNoOfEDS316Switches(Product, PUIOIOTAs, PDIOIOTAs, nonRedRUSIO, redRUSIO):
    W = 0
    if Product.Name == "SM Control Group":
        cont = Product.GetContainerByName('SM_CG_Common_Questions_Cont')
        if cont.Rows.Count > 0:
            #PUIO, RUSIO
            UniversalIOTA = cont.Rows[0].GetColumnByName('SM_Universal_IOTA').DisplayValue
            #Redundant, Redundant A.R.T+
            S300 = cont.Rows[0].GetColumnByName('SM_SCController_Architecture').DisplayValue
            remoteLocation = Product.GetContainerByName('SM_RemoteGroup_Cont').Rows.Count
            x1 = x2 = 0
            if UniversalIOTA == 'PUIO':
                x1 = PUIOIOTAs + PDIOIOTAs
                x2 = 0
            elif UniversalIOTA == 'RUSIO':
                x1 = nonRedRUSIO + redRUSIO
                x2 = PDIOIOTAs

            Y = 2 if S300 == 'Redundant A.R.T+' else 1
            Z = 2 if remoteLocation >= 3 else 0
            #Total IO Modules
            X = x1 + x2
            if X > 0 and remoteLocation > 0:
                W = 2 * RoundUp(float(X+Y+Z)/14.0)
    elif Product.Name == "SM Remote Group":
        UniversalIOTA = Product.Attr('SM_Universal_IOTA_Type').GetValue()
        EnclosureType = Product.Attr('SM_RG_Enclosure_Type').GetValue()
        if EnclosureType == 'Cabinet':
            x1 = x2 = Y = Z = 0
            if UniversalIOTA == 'PUIO':
                x1 = PUIOIOTAs + PDIOIOTAs
                x2 = 0
            elif UniversalIOTA == 'RUSIO':
                x1 = nonRedRUSIO + redRUSIO
                x2 = PDIOIOTAs
            #Total IO Modules
            X = x1 + x2
            if X > 0:
                W = 2 * RoundUp(float(X+Y+Z)/14.0)
    return W

#parts qty
def getQty(partsQty, partName):
    qty = 0
    if partName in partsQty:
        qty = partsQty[partName]
    return int(qty)

def getQty1(partsQty,partName):
    try:
        return int(partsQty[partName]['Quantity'])
    except KeyError:
        return 0

def getRusioFrontCabinetCount(Product, partsQty):
    cabinet = totalIOTA = powerSupply = switches = mcar = integrationBoard = mob3 = cables = utilizedMcar = 0
    #Redundant RUSIO IOTAs
    RRSUIOIOTAs = getQty(partsQty, "FC-IOTA-R24")
    #Trace.Write("RRSUIOIOTAs----->: "+str(RRSUIOIOTAs))
    #RRSUIOIOTAs=int(RRSUIOIOTAs)
    #Non Redundant RUSIO IOTAs
    NRRUSIOIOTAs = getQty(partsQty, "FC-IOTA-NR24")
    Trace.Write("NRRUSIOIOTAs: "+str(NRRUSIOIOTAs))
    #PDIO IOTAs
    PDIOIOTAs = getQty(partsQty, 'FC-TDIO11')
    Trace.Write("PDIOIOTAs: "+str(PDIOIOTAs))
    # Total
    totalNRIOTAs = NRRUSIOIOTAs + PDIOIOTAs
    #Switches
    #'CC-TNWD01' = 'CC-INWM01' = 'CC-INWE01' = '50165649-001' = 0
    for part in ['4600112', '4600136', '4600130', '4600121','CC-TNWD01']:
        switches += getQty(partsQty, part)
    #EDS316
    #switches += 6
    #switches += getNoOfEDS316Switches(Product, 0, PDIOIOTAs, NRRUSIOIOTAs, RRSUIOIOTAs)
    Trace.Write("switches: "+str(switches))
    #Power Supply
    powerSupply += getQty(partsQty, 'FC-PSUNI2424')
    powerSupply += getQty(partsQty, 'QUINT4-PS/24DC/24DC/20/SC')
    #MOB3
    mob3 = getQty(partsQty, '4603323')
    #MCAR
    mcar = getQty(partsQty, 'FC-MCAR-02')
    #Integration Board
    integrationBoard += getQty(partsQty, 'FC-GPCS-RIO16-PF')

    cab = 0
    # powerSupply = 6
    # switches = 6
    red = RRSUIOIOTAs
    non_red = totalNRIOTAs
    utilizedMcar_SPs = 0
    new_cab = 0
    if powerSupply or switches:
        maxPower = RoundUp(powerSupply / 4.0) # 2
        maxSwitch = RoundUp(switches / 6.0) # 1
        maxSide = max(maxPower,maxSwitch) # 2
        cab += maxSide # 2
        print(cab)
        utilizedMcar_SPs = 6 * maxSide # 12
        AllremainingMcar = (cab * 18) - utilizedMcar_SPs # 36-12=24
        #remainingMcar = AllremainingMcar/cab # 24/2 = 12
        # red iotas
        if red > cab * 8 :
            x = red - (cab * 8)
            y = RoundUp(x / 12.0)
            new_cab = cab + y
            remaining_space = new_cab * 18 - ((cab * 6) + (1.5 * red))
            if remaining_space > non_red: # 7
                remaining_space -= non_red
                if remaining_space < 12:
                    new_cab += RoundUp(integrationBoard/12.0)
                else:
                    if integrationBoard > 6:
                        integrationBoard -= 6
                        new_cab += RoundUp(integrationBoard/12.0)

            else:
                m = non_red - remaining_space
                n = RoundUp(m/18.0)
                new_cab = new_cab + n
                remaining_space = new_cab * 18 - ((cab * 6) + (1.5 * red) + non_red)
                if remaining_space < 12:
                    new_cab += RoundUp(integrationBoard/12.0)
                else:
                    if integrationBoard > 6:
                        integrationBoard -= 6
                        new_cab += RoundUp(integrationBoard/12.0)

        else:
            remaining_space = AllremainingMcar - (red * 1.5)
            print(remaining_space)
            if remaining_space > non_red: # 9 < 3
                remaining_space -= non_red # 6
                empty_cab = int(remaining_space/12.0)
                remaining_space -= empty_cab * 12
                if remaining_space in range(6,9):
                    integrationBoard -= 3
                if remaining_space in range(9,12):
                    integrationBoard -= 6
                if empty_cab > 0:
                    if integrationBoard > empty_cab * 9:
                        remaining_integration = integrationBoard - empty_cab * 9
                        new_cab += RoundUp(remaining_integration/12.0) + cab
                    else:
                        new_cab = cab
                else:
                    new_cab += RoundUp(integrationBoard/12.0) + cab


            else:
                x = non_red - remaining_space # 33 - 9
                y = RoundUp(x/18.0) # 2
                new_cab = cab + y # 4
                remaining_space = new_cab * 18 - ((cab * 6) + (1.5 * red) + non_red)
                if remaining_space < 12:
                    new_cab += RoundUp(integrationBoard/12.0)
                else:
                    if integrationBoard > 6:
                        integrationBoard -= 6
                        new_cab += RoundUp(integrationBoard/12.0)
    else:
        new_cab = RoundUp(red/12.0)
        new_space = (new_cab * 18) - (red * 1.5)
        if new_space < non_red:
            non_red -= new_space
            new_cab += RoundUp(non_red/18.0)
            remaining_space = (new_cab * 18) - (red * 1.5) - non_red
            if remaining_space < 12:
                new_cab += RoundUp(integrationBoard/12.0)
            else:
                if integrationBoard > 6:
                    integrationBoard -= 6
                    new_cab += RoundUp(integrationBoard/12.0)
        else:
            new_space -= non_red
            if new_space < 12:
                new_cab += RoundUp(integrationBoard/12.0)
            else:
                if integrationBoard > 6:
                    integrationBoard -= 6
                    new_cab += RoundUp(integrationBoard/12.0)

    cabinet = new_cab
    return int(cabinet), int(powerSupply), int(switches)
def getRusioDualCabinetCount(Product, partsQty):
    cab, ps, switch = getRusioFrontCabinetCount(Product, partsQty)
    cabinet = RoundUp(cab/2.0)
    return int(cabinet), int(ps), int(switch)
#rusio = getRsuioFrontCabinetCount(Product, parts_dict)[0]
#Trace.Write("Fantastic..: "+str(rusio))