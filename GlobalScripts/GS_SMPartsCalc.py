import GS_Power_Supply_calcs
import GS_Power_Supply_calcs1 as ps_calc1
from GS_SM_RG_Cab_cals import getRusioFrontCabinetCount,getRusioDualCabinetCount
import GS_SMIOComponents

#from GS_SM_CGSystemCabinetsFront import getCGNoOfSystemCabinetFront

def roundup(n):
    res = int(n)
    return res if res == n else res+1

def addParts(parts, qty, desc, parts_dict):
    if parts != '' and qty > 0:
        parts_dict[parts] = {'Quantity' : qty, 'Description': desc}
    return parts_dict

def getPowerSupplyParts(Product, parts_dict):
    #CXCPQ-31160, CXCPQ-31161
    try:
        qty = GS_Power_Supply_calcs.getNoPowerSupply(Product)
        if qty > 0:
            #CCEECOMMBR-6976
            #parts_dict = addParts('5SY4220-7', qty, 'Main Circuit breakers', parts_dict)
            parts_dict = addParts('51454944-100', qty, 'QUINT4-S-ORING/12-24DC/1X40/', parts_dict)
    except Exception as e:
        Trace.Write("Module: GS_SMPartsCalc.getPowerSupplyParts Error:".format(str(e)))

    #CXCPQ-31192
    try:
        qty1 = ps_calc1.getNoPowerSupplies(Product)
        if qty1 > 0:
            qty += qty1
            #CCEECOMMBR-6976
            #parts_dict = addParts('5SY4220-7', qty, 'Main Circuit breakers', parts_dict)
    except Exception as e:
        Trace.Write("Module: GS_SMPartsCalc.getPowerSupplyParts 2 Error:".format(str(e)))

    return parts_dict

def getCGParts(Product, parts_dict):
    distance = switchIOLink = remoteLocation = extendedTemperature  =  conformallyCoated = S300 = KeySwitchModule = ''
    try:
        #UI question - Distance to SM SC UIO/DIO modules- Max Distance
        cabLeftRow = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows[0]
        distance = cabLeftRow.GetColumnByName('Distance_SM_SC_UIO/DIO_modules').DisplayValue
        #UI question - Extended Temperature
        extendedTemperature = cabLeftRow.GetColumnByName('Extended_Temperature').DisplayValue

        #UI question - Conformally Coated
        cabRightRow = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0]
        conformallyCoated = cabRightRow.GetColumnByName('Conformally_Coated').DisplayValue

        #UI question - Key Switch Module
        KeySwitchModule = cabRightRow.GetColumnByName('Key_Switch_Module_Required').DisplayValue

        #UI question - Switch for Safety IO Link
        commonQnRow = Product.GetContainerByName('SM_CG_Common_Questions_Cont').Rows[0]
        switchIOLink = commonQnRow.GetColumnByName('SM_Switch_Safety_IO').DisplayValue

        #UI question - SM Controller Architecture
        cont = Product.GetContainerByName('SM_CG_Common_Questions_Cont')
        S300 = cont.Rows[0].GetColumnByName('SM_SCController_Architecture').DisplayValue
    except Exception as e:
        Trace.Write("Module: GS_SMPartsCalc.getCGParts Error:".format(str(e)))

    #Total No of SM Remote group products added under the SM Control group product
    remoteLocation = Product.GetContainerByName('SM_RemoteGroup_Cont').Rows.Count

    #CXCPQ-33628
    if remoteLocation > 0 and switchIOLink != 'Third Party MOXA':
        qty = 2 * remoteLocation
        part_distance_mapping = {'2km Multi Mode SFP':{'parts':'50154762-002', 'desc':'10/100M SFP Multi mode 2Km'}, '15km Single Mode SFP': {'parts':'50154761-001', 'desc':'10/100M SFP Single mode 15Km'}}
        if distance in part_distance_mapping.keys():
            parts_dict = addParts(part_distance_mapping[distance]['parts'], qty, part_distance_mapping[distance]['desc'], parts_dict)

    if switchIOLink == 'Third Party MOXA':
        #workaround to set defulat distance
        if distance != '< 4 KM' and distance != '>4 KM & <40 KM':
            distance = '>4 KM & <40 KM'

        #CXCPQ-31738
        qty = 0
        parts = desc = ''
        if remoteLocation in [6, 7, 8, 9]:
            qty = 2
        elif remoteLocation in [10, 11, 12, 13]:
            qty = 4
        elif remoteLocation in [14, 15]:
            qty = 6

        if qty > 0:
            if distance == '< 4 KM':
                parts = '4600116'
                desc = 'MOXA Switches(CM-600-4MSC) - Multimode'
            elif distance == '>4 KM & <40 KM':
                parts = '4600131'
                desc = 'MOXA Switches(CM-600-4SSC) - Single mode'

            parts_dict = addParts(parts, qty, desc, parts_dict)

        #CXCPQ-31733
        parts = desc = ''
        qty = 2 if remoteLocation in [3, 4, 6, 7, 8, 10, 11, 12, 14, 15] else 0
        if qty > 0:
            if distance == '< 4 KM':
                parts = '4600117'
                desc = 'MOXA Switches(CM-600-2MSC/2TX) - Multimode'
            elif distance == '>4 KM & <40 KM':
                parts = '4600132'
                desc = 'MOXA Switches(CM-600-2SSC/2TX) - Single mode'

            parts_dict = addParts(parts, qty, desc, parts_dict)

        #CXCPQ-31735
        parts = desc = ''
        qty = 2 if remoteLocation in [5, 9, 13]  else 0
        if qty > 0:
            if distance == '< 4 KM':
                parts = '4600118'
                desc = 'MOXA Switches(CM-600-3MSC/1TX) - Multimode'
            elif distance == '>4 KM & <40 KM':
                parts = '4600133'
                desc = 'MOXA Switches(CM-600-3SSC/1TX) - Single mode'

            parts_dict = addParts(parts, qty, desc, parts_dict)

        #CXCPQ-31709
        parts = desc = ''
        qty = 2 if remoteLocation in [3, 4, 5, 6, 7, 8, 9] else 0
        if qty > 0:
            if extendedTemperature == 'No' and conformallyCoated == 'No':
                parts = '4600113'
                desc = 'Compact Managed Ethernet MOXA Switch(EDS-608)'
            elif extendedTemperature == 'Yes' or conformallyCoated == 'Yes':
                parts = '4600122'
                desc = 'Compact Managed Ethernet MOXA Switch(EDS-608-T)'

            parts_dict = addParts(parts, qty, desc, parts_dict)
        #CXCPQ-31713 Changes HimanshuBatra
        parts = desc = ''
        qty = 2 if remoteLocation in [10, 11, 12, 13, 14, 15 ] else 0
        if qty > 0:
            if extendedTemperature == 'No' and conformallyCoated == 'No':
                parts = '4600114'
                desc = 'MOXA:EDS-616-T-HPS'

            elif extendedTemperature == 'Yes' or conformallyCoated == 'Yes':
                parts = '4600123'
                desc = 'MOXA:EDS-616-T-HPS_C'

            parts_dict = addParts(parts, qty, desc, parts_dict)

        #CXCPQ-31705
        """NonRedundantIOMs = int(Product.Attr('FC_PUIO').GetValue())
        RedundantIOMs = int(Product.Attr('FC_PDIO').GetValue())
        X = NonRedundantIOMs + RedundantIOMs
        Y = 2 if S300 == 'Redundant A.R.T+' else 1
        qty = int((X+Y)/14)
        if qty > 0:
            parts = desc = ''
            if distance == '< 4 KM':
                parts = 'FS-CCI-FOM-05'
                desc = 'SC FO MULTI MODE CABLE SET L=0.5M'
            elif distance == '>4 KM & <40 KM':
                parts = 'FS-CCI-FOS-05'
                desc = 'SC FO SINGLE MODE CABLE SET L=0.5M'
            if parts != '':
                parts_dict = addParts(parts, qty, desc, parts_dict)"""

    #CXCPQ-31519
    parts = desc = ''
    if KeySwitchModule == 'Yes':
        parts = 'FC-SSWM01'
        desc = 'SC SWITCH MODULE PROGRAM/FORCE/RESET'
        contParts = Product.GetContainerByName('SM_CG_PartSummary_Cont')
        partsQty = getPartsQty(contParts)
        qty = getQty(partsQty, 'FC-TCNT11')
        if (qty >0):
            parts_dict = addParts(parts, qty, desc, parts_dict)

    #CXCPQ-31160, CXCPQ-31161
    parts_dict = getPowerSupplyParts(Product, parts_dict)

    return parts_dict

def getRGParts(Product, parts_dict):
    #CXCPQ-31160, CXCPQ-31161
    EnclosureType = Product.Attr('SM_RG_Enclosure_Type').GetValue()
    if EnclosureType == 'Cabinet':
        parts_dict = getPowerSupplyParts(Product, parts_dict)
    return parts_dict

#CXCPQ-31629 - Number of EDS-316 switches
def getNoOfEDS316Switches(Product, PUIOIOTAs, PDIOIOTAs, nonRedRUSIO, redRUSIO):
    W = 0
    if Product.Name == "SM Control Group":
        cont = Product.GetContainerByName('SM_CG_Common_Questions_Cont')
        if cont.Rows.Count > 0:
            #As the EDS316 switches applicable only for Third Party MOXA
            switchIOLink = cont.Rows[0].GetColumnByName('SM_Switch_Safety_IO').DisplayValue
            if switchIOLink != 'Third Party MOXA':
                return 0

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
                W = 2 * roundup(float(X+Y+Z)/14.0)
    elif Product.Name == "SM Remote Group":
        UniversalIOTA = Product.Attr('SM_Universal_IOTA_Type').GetValue()
        EnclosureType = Product.Attr('SM_RG_Enclosure_Type').GetValue()
        #As the EDS316 switches applicable only for Third Party MOXA
        switchIOLink = Product.Attr('SM_CG_Safety_IO_Link').GetValue()
        if switchIOLink != 'Third Party MOXA':
            return 0
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
                W = 2 * roundup(float(X+Y+Z)/14.0)
    return W

#CXCPQ-31795
def getHardwiredMarshallingParts(Product, parts_dict):
    qty = 0
    parts = 'FC-TSRO-0824'
    desc = 'DO(relay) FTA for SIL3 appl. 8ch CC / TSRO'
    IOComp = GS_SMIOComponents.IOComponents(Product)
    columns = []
    UniversalIOTA = MarshallingOption = ''
    if Product.Name == "SM Control Group":
        container_name = 'SM_IO_Count_Digital_Output_Cont'
        container = Product.GetContainerByName(container_name)
        columns =['Red (NIS)','Non Red (NIS)']
        cont = Product.GetContainerByName('SM_CG_Common_Questions_Cont')
        if cont.Rows.Count > 0:
            UniversalIOTA = cont.Rows[0].GetColumnByName('SM_Universal_IOTA').DisplayValue
        contCab = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left')
        if contCab.Rows.Count > 0:
            MarshallingOption = contCab.Rows[0].GetColumnByName('Marshalling_Option').DisplayValue
    elif Product.Name == "SM Remote Group":
        container_name = 'SM_RG_IO_Count_Digital_Output_Cont'
        container = Product.GetContainerByName(container_name)
        columns =['Red_NIS','Non_Red_NIS']
        UniversalIOTA = Product.Attr('SM_Universal_IOTA_Type').GetValue()
        EnclosureType = Product.Attr('SM_RG_Enclosure_Type').GetValue()
        contCab = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left')
        if contCab.Rows.Count > 0 and EnclosureType == 'Cabinet':
            MarshallingOption = contCab.Rows[0].GetColumnByName('Marshalling_Option').DisplayValue

    if len(columns) > 0 and UniversalIOTA == 'PUIO' and MarshallingOption == 'Hardware Marshalling with Other':
        questions = ['SDO(16) SIL 2/3 250Vac/Vdc UIO (0-5000)', 'SDO(16) SIL 2/3 250Vac/Vdc DIO (0-5000)']
        key_column_name = IOComp.getKeyColumnName(container_name)
        for qn in questions:
            row_index = IOComp.getRowIndexNew(container, key_column_name, qn)
            for column_name in columns:
                val = IOComp.getColumnValue(container, row_index, column_name)
                qty += 2 * roundup(float(val)/16.0)

        if qty > 0:
            parts_dict = addParts(parts, qty, desc, parts_dict)

    return parts_dict

#parts dictionary
def getPartsQty(container):
    partsQty = dict()
    if container.Rows.Count > 0:
        for cont_row in container.Rows:
            partName = cont_row.GetColumnByName('CE_Part_Number').Value
            qty = int(cont_row.GetColumnByName('CE_Final_Quantity').Value) if cont_row.GetColumnByName('CE_Final_Quantity').Value.strip() != '' else 0
            partsQty[partName] = qty
    return partsQty

#parts qty
def getQty(partsQty, partName):
    qty = 0
    if partName in partsQty:
        qty = partsQty[partName]
    return qty

def getPuioDualCabinetCount(Product, partsQty):
    cabinet = totalIOTA = powerSupply = switches = cpu = mcar = integrationBoard = mob3 = cables = 0
    PUIOIOTAs = getQty(partsQty, 'FC-TUIO11')
    PDIOIOTAs = getQty(partsQty, 'FC-TDIO11')
    totalIOTA = PUIOIOTAs + PDIOIOTAs

    powerSupply += getQty(partsQty, 'FC-PSUNI2424')
    powerSupply += getQty(partsQty, '50165610-001')

    #EDS316
    switches += getNoOfEDS316Switches(Product, PUIOIOTAs, PDIOIOTAs, 0, 0)
    #EDS608
    switches += getQty(partsQty, '4600113')
    switches += getQty(partsQty, '4600122')
    #EDS616
    switches += getQty(partsQty, '4600114')
    switches += getQty(partsQty, '4600123')
    #CC-TNWD01
    switches += getQty(partsQty, 'CC-TNWD01')

    #Controller (S300)
    cpu = getQty(partsQty, 'FC-TCNT11')

    #Key Switch
    keySwitch = getQty(partsQty, 'FC-SSWM01')

    #MCAR
    mcar = getQty(partsQty, 'FC-MCAR-02')

    #MOB3
    mob3 = getQty(partsQty, '4603323')

    #Integration Board
    integrationBoard += getQty(partsQty, 'FC-GPCS-RIO16-PF')

    #Cables
    cables += getQty(partsQty, 'FS-CCI-HSE-30')
    cables += getQty(partsQty, 'FS-CCI-HSE-08')
    cables += getQty(partsQty, 'FS-CCI-FOM-05')
    cables += getQty(partsQty, 'FS-CCI-FOS-05')

    switches += getQty(partsQty, '4600117')
    switches += getQty(partsQty, '4600132')
    switches += getQty(partsQty, '4600118')
    switches += getQty(partsQty, '4600133')
    switches += getQty(partsQty, '4600116')
    switches += getQty(partsQty, '4600131')

    #calculating the required cabinets
    #no of sides required for switches
    maxSide1 = roundup(switches/6.0)
    #no of sides required for Power Supply
    maxSide2 = roundup(powerSupply/4.0)
    maxSide = max(maxSide1, maxSide2)
    calculatedCabinet = roundup(maxSide/2.0)
    calculatedCabinet = calculatedCabinet if calculatedCabinet > cpu else cpu
    calculatedIOTA = cpu*10 + roundup(maxSide/2.0)*12 +abs((cpu-roundup(maxSide/2.0))*18)
    allowedMcar = maxSide * 2 + roundup(calculatedIOTA/3.0)
    allowedMob3 = 0
    if allowedMcar > mcar:
        allowedMob3 = allowedMcar - mcar
    calculatedIntegrationBoard = allowedMob3 *3
    cabinet1 = calculatedCabinet
    if calculatedIOTA < totalIOTA:
        cabinet1 += roundup( (totalIOTA - calculatedIOTA)/36.0) #18 + 18
    cabinet2 = cabinet1
    if mcar > allowedMcar:
        cabinet2 = roundup((mcar - allowedMcar)/12.0)
    cabinet3 = cabinet2 + roundup(mob3/12.0)
    #allowedIB = roundup(mob3/12.0)*6*3  # 6 mob 3 per
    allowedIB = mob3 * 3 # 3 IB per mob3
    cabinet4 = cabinet3
    if integrationBoard > allowedIB:
        cabinet4 = cabinet1 + roundup((integrationBoard - allowedIB)/12.0)
    cabinet = max(cabinet1, cabinet2, cabinet3, cabinet4)
    return int(cabinet), int(powerSupply), int(switches)

def getCgRusioCabinetCount(product, parts_qty, cpu):
    cabinet = RRUSIOIOTAs = NRRUSIOIOTAs = PDIOIOTAs = switches = powerSupply = integrationBoard = requiredMcar = 0

    #Redundant RUSIO IOTAs
    RRUSIOIOTAs = getQty(parts_qty, "FC-IOTA-R24")
    #Non Redundant RUSIO IOTAs
    NRRUSIOIOTAs = getQty(parts_qty, "FC-IOTA-NR24")
    #PDIO IOTAs
    PDIOIOTAs = getQty(parts_qty, 'FC-TDIO11')
    totalNRIOTAs = NRRUSIOIOTAs + PDIOIOTAs
    #Switches
    for part in ['4600114', '4600123', '4600113', '4600122', '4600131', '4600116', '4600118', '4600133', '4600117', '4600132', 'CC-TNWD01']:
        switches += getQty(parts_qty, part)
    #EDS316
    switches += getNoOfEDS316Switches(product, 0, PDIOIOTAs, NRRUSIOIOTAs, RRUSIOIOTAs)
    #Power Supply
    powerSupply += getQty(parts_qty, 'FC-PSUNI2424')
    powerSupply += getQty(parts_qty, '50165610-001')
    #Integration Board
    integrationBoard += getQty(parts_qty, 'FC-GPCS-RIO16-PF')

    cpu = float(cpu)
    RRUSIOIOTAsPerCab = RRUSIOIOTAs
    totalNRIOTAsPerCab = totalNRIOTAs
    switchesPerCab = switches
    powerSupplyPerCab = powerSupply
    integrationBoardPerCab = integrationBoard
    #Per cabinet qty
    if cpu:
        RRUSIOIOTAsPerCab = roundup(RRUSIOIOTAs/cpu)
        totalNRIOTAsPerCab = roundup(totalNRIOTAs/cpu)
        switchesPerCab = roundup(switches/cpu)
        powerSupplyPerCab = roundup(powerSupply/cpu)
        integrationBoardPerCab = roundup(integrationBoard/cpu)

    switchesSide = roundup(switchesPerCab/6.0)
    powerSupplySide = roundup(powerSupplyPerCab/4.0)
    maxSide = max(switchesSide, powerSupplySide)
    cabinet = maxSide

    mcarAvailable = maxSide * 4
    # MCAR required for controller
    requiredMcar += 1
    if totalNRIOTAsPerCab > 0:
        totalNRIOTAsPerCab -= 1
    # MCAR required by Red. IOTAs
    requiredMcar += roundup(RRUSIOIOTAsPerCab/2.0)
    if RRUSIOIOTAsPerCab % 2 and totalNRIOTAsPerCab > 0:
        totalNRIOTAsPerCab -= 1
    # MCAR required by Non Red. IOTAs and PDIOs
    requiredMcar += roundup(totalNRIOTAsPerCab/3.0)
    # delta of required and available mcar
    deltaMcar = requiredMcar - mcarAvailable
    absDeltaMcar = abs(deltaMcar)

    additionalRequiredCabinets = cabinetWithOnlyPsOrSwitch = pfOnLastCabWithIota = 0
    if deltaMcar <= 0:
        additionalRequiredCabinets = 0
        cabinetWithOnlyPsOrSwitch = absDeltaMcar / 4
        remainingMcarOnLastCabWithIota = absDeltaMcar % 4
        if remainingMcarOnLastCabWithIota == 4:
            pfOnLastCabWithIota = 9
        elif remainingMcarOnLastCabWithIota == 3:
            pfOnLastCabWithIota = 6
        elif remainingMcarOnLastCabWithIota == 2:
            pfOnLastCabWithIota = 3
    else:
        additionalRequiredCabinets = roundup(absDeltaMcar/6.0)
        remainingMcarOnLastCabWithIota = additionalRequiredCabinets * 6 - absDeltaMcar
        if remainingMcarOnLastCabWithIota == 6:
            pfOnLastCabWithIota = 12
        elif remainingMcarOnLastCabWithIota in (5,4,3):
            pfOnLastCabWithIota = 6

    cabinet += additionalRequiredCabinets
    remainingIntegrationBoard = integrationBoardPerCab - (cabinetWithOnlyPsOrSwitch * 9 + pfOnLastCabWithIota)
    if remainingIntegrationBoard > 0:
        cabinet += roundup(remainingIntegrationBoard / 12.0)

    return int(cabinet) * cpu, int(powerSupply), int(switches)


#Calculating cabinet count for the single cabinet access
def getPUIOCabinetCount(Product, partsQty, cpu):

    cabinet = totalIOTA = powerSupply = switches = integrationBoard = PUIOIOTAs = PDIOIOTAs = 0
    #IOTAs
    PUIOIOTAs = getQty(partsQty, 'FC-TUIO11')
    PDIOIOTAs = getQty(partsQty, 'FC-TDIO11')
    totalIOTA = PUIOIOTAs + PDIOIOTAs
    #Power Supply
    for partNumber in ['FC-PSUNI2424', '50165610-001']:
        powerSupply += getQty(partsQty, partNumber)

    #EDS316
    switches += getNoOfEDS316Switches(Product, PUIOIOTAs, PDIOIOTAs, 0, 0)
    #EDS608[4600113, 4600122] EDS616[4600114, 4600123] CC-TNWD01[CC-TNWD01]
    for partNumber in ['4600113', '4600122', '4600114', '4600123', 'CC-TNWD01']:
        switches += getQty(partsQty, partNumber)
    for partNumber in ['4600117', '4600132', '4600118', '4600133', '4600116', '4600131']:
        switches += getQty(partsQty, partNumber)

    #P&F Integration Board
    integrationBoard += getQty(partsQty, 'FC-GPCS-RIO16-PF')

    switchesNew = switches
    powerSupplyNew = powerSupply
    totalIOTANew = totalIOTA
    integrationBoardNew = integrationBoard
    if cpu > 0:
        switchesNew = int(roundup( float(switches)/float(cpu)))
        powerSupplyNew = int(roundup( float(powerSupply)/float(cpu)))
        totalIOTANew = int(roundup( float(totalIOTA)/float(cpu)))
        integrationBoardNew = int(roundup( float(integrationBoard)/float(cpu)))

    #No of sides required for switches
    maxSide1 = roundup(switchesNew/6.0)

    #No of sides required for Power Supply
    maxSide2 = roundup(powerSupplyNew/4.0)

    #Required sides for mounting PS or Switches
    maxSide = max(maxSide1, maxSide2)

    #Total No of (PS or Switches ) modules can be mounted in the calculated cabnites
    totalModulesCanBeMounted = int(maxSide * 12)

    #IOTA Differences
    deltaIOTA = totalIOTANew - totalModulesCanBeMounted

    noOfPFFitInCabinet = 0
    if deltaIOTA <= 0:
        #No additional cabinet is required as the delta IOTA is a negative number
        additionalRequiredCabinets = 0
        unUsedCabinets = int(abs(deltaIOTA)/18)
        #IOTA Modules is available on the last cabinet
        lastCabinetIOTACount = abs(deltaIOTA) % 18
        lastCabinetIOTACount = 12 - lastCabinetIOTACount
    else:
        #Required no of additional cabinets
        additionalRequiredCabinets = roundup(deltaIOTA/18.0) #18
        unUsedCabinets = 0
        #Total Modules can be mounted inside the additional cabinets
        totalModulesCanBeMounted1 = additionalRequiredCabinets * 18
        #IOTA Modules is available on the last cabinet
        lastCabinetIOTACount = deltaIOTA % totalModulesCanBeMounted1

    cabinet = maxSide + additionalRequiredCabinets

    #Required Rows for the P&F integration Board
    if integrationBoardNew > 0:
        noOfPFFitInCabinet = 0
        if lastCabinetIOTACount > 0 and lastCabinetIOTACount < 7 :
            noOfPFFitInCabinet = 6
        #Remaing P&F Integration boards qty that required new cabinet
        deltaPF = integrationBoardNew - noOfPFFitInCabinet
        #Additional Cabinets for P&F
        if deltaPF > 0:
            additionalPFCabinets = roundup(deltaPF/12.0) #12
            cabinet += (additionalPFCabinets - unUsedCabinets) if (additionalPFCabinets - unUsedCabinets) > 0 else 0

    lst = ['PUIOIOTAs', 'PDIOIOTAs', 'totalIOTA', 'totalIOTANew', 'powerSupply', 'powerSupplyNew', 'switches', 'switchesNew', 'integrationBoard', 'integrationBoardNew']
    for var in lst:
        Trace.Write("{}:{}".format(var,locals()[var]))

    return int(cabinet), int(powerSupply), int(switches)

#CXCPQ-32163
def getNumberOfCGCabinet(Product):
    UniversalIOTA = CabinetAccess = ''
    cabinet = totalIOTA = powerSupply = switches = cpu = integrationBoard = PUIOIOTAs = PDIOIOTAs =  0
    switchesNew = powerSupplyNew = totalIOTANew = integrationBoardNew = cpuNew = 0
    cont = Product.GetContainerByName('SM_CG_Common_Questions_Cont')
    contCab = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left')
    contParts = Product.GetContainerByName('SM_CG_PartSummary_Cont')
    if cont.Rows.Count > 0:
        UniversalIOTA = cont.Rows[0].GetColumnByName('SM_Universal_IOTA').DisplayValue
    if contCab.Rows.Count > 0:
        CabinetAccess = contCab.Rows[0].GetColumnByName('Cabinet_Access').DisplayValue

    #get all parts and qty from part summary container
    partsQty = getPartsQty(contParts)
    cpu = getQty(partsQty, 'FC-TCNT11')
    if UniversalIOTA == "PUIO":
        cabinet, powerSupply, switches = getPUIOCabinetCount(Product, partsQty, cpu)
        if cpu > 0 and cabinet >0:
            cabinet *= cpu
        if cabinet >0 and CabinetAccess == "Dual Access":
            cabinet = roundup(cabinet/2.0)
    elif UniversalIOTA == "RUSIO" :
        cabinet, powerSupply, switches = getCgRusioCabinetCount(Product, partsQty, cpu)
        if cabinet > 0 and CabinetAccess == "Dual Access":
            cabinet = roundup(cabinet/2.0)
    return int(cabinet), int(powerSupply), int(switches)

#CXCPQ-32164
def getNumberOfRGCabinet(Product):
    UniversalIOTA = CabinetAccess = ''
    cabinet = totalIOTA = powerSupply = switches = cpu = integrationBoard = PUIOIOTAs = PDIOIOTAs = cables = 0
    UniversalIOTA = Product.Attr('SM_Universal_IOTA_Type').GetValue()
    EnclosureType = Product.Attr('SM_RG_Enclosure_Type').GetValue()
    contCab = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left')
    contParts = Product.GetContainerByName('SM_RG_PartSummary_Cont')
    if contCab.Rows.Count > 0:
        CabinetAccess = contCab.Rows[0].GetColumnByName('Cabinet_Access').DisplayValue
    #get all parts and qty from part summary container
    partsQty = getPartsQty(contParts)

    if UniversalIOTA == "PUIO" and EnclosureType == 'Cabinet':
        cpu = 0
        cabinet, powerSupply, switches = getPUIOCabinetCount(Product, partsQty, cpu)
        if cabinet >0 and CabinetAccess == "Dual Access":
            cabinet = roundup(cabinet/2.0)
    elif UniversalIOTA == "RUSIO" and CabinetAccess == "Dual Access" and EnclosureType == 'Cabinet':
        cabinet, powerSupply, switches = getRusioDualCabinetCount(Product, partsQty)
    elif UniversalIOTA == "RUSIO" and CabinetAccess != "Dual Access" and EnclosureType == 'Cabinet':
        cabinet, powerSupply, switches = getRusioFrontCabinetCount(Product, partsQty)

    return int(cabinet), int(powerSupply), int(switches)