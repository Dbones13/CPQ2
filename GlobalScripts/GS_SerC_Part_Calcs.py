#GS_SerC_Part_Calcs
import GS_Get_Set_AtvQty, GS_PS_Exp_Ent_BOM
import GS_C300_MCAR_calcs
import GS_PMIO_Variable
from math import ceil

def getFloat(val):
    if val:
        return float(val)
    return 0

def roundUp(n):
    res = int(n)
    return res if round(res,2) == round(n,2) else res+1

resDict = dict()
def getAttrQty(Product, key):
    global resDict
    pMIOSolutionRequired = Product.Attr('SerC_CG_PM_IO_Solution_required').GetValue()
    if pMIOSolutionRequired == 'Yes':
        if len(resDict) == 0:
            resDict = GS_PMIO_Variable.partCalc(Product)
        #Trace.Write("PMIO param : {} = {}".format(key, int(resDict.get(key, 0))))
        return int(resDict.get(key, 0))
    else:
        #Trace.Write("Non PMIO param : {}".format(key))
        return GS_Get_Set_AtvQty.getAtvQty(Product, "SerC_IO_Params", key)

#CXCPQ-52347
def getParts52347(Product, parts_dict):
    AttrName = "Series_C_CG_Part_Summary"
    cont = "Series_C_CG_Part_Summary_Cont"
    iolAttr = "C300_CG_Total_IO_Load"
    iopAttr = "C300_CG_Total_IO_Point_Load"
    if Product.Name == "Series-C Remote Group":
        cont = "Series_C_RG_Part_Summary_Cont"
        iolAttr = "C300_RG_Total_IO_Load"
        iopAttr = "C300_RG_Total_IO_Point_Load"
        mountingsol = Product.Attr("SerC_IO_Mounting_Solution").GetValue()


    if Product.GetContainerByName(cont).Rows.Count == 0:
        return parts_dict

    iOFamilyType = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
    typeOfController = Product.Attr('SerC_CG_Type_of_Controller_Required').GetValue()
    if iOFamilyType == 'Series C' and typeOfController in ['CN100 I/O HIVE - C300 CEE', 'Control HIVE - Physical', 'Control HIVE - Virtual']:
        X21 = X22 = X23 = W41 = W51 = W61 = W42 = W52 = 0
        Y32 = Y33 = Y21 = Y22 = Y23 = W11 = W21 = W31 = 0
        W12 = W22 = W32 = Z91 = X11 = X12 = X13 = Y71 = 0
        Y72 = Y73 = W81 = W91 = W82 = W92 = W73 = X51 = 0
        X52 = X53 = X41 = X42 = X43 = Y81 = Y82 = Y83 = 0
        V21 = V31 = V13 = V22 = V32 = V43 = Y91 = Y92 = 0
        Y93 = V61 = V71 = V53 = V62 = V72 = V83 = Z11 = 0
        Z12 = Z13 = Z23 = Z31 = Z32 = Z33 = Y43 = Y53 = 0
        Y63 = Z81 = Z82 = Z83 = Z84 = Z85 = Z86 = X33 = 0
        X61 = X62 = X63 = X71 = X72 = X73 = X81 = X82 = 0
        X83 = Z41 = Z51 = Z61 = Z71 = Z42 = Z43 = Z52 = 0
        Z53 = Z62 = Z63 = Z72 = Z73 = V91 = V92 = W62 = 0
        W23 = Y31 = 0

        paramList = ['X21', 'X22', 'X23', 'W41', 'W51', 'W61', 'W42', 'W52']
        paramList.extend(['W62', 'W23', 'Y31', 'Y32', 'Y33', 'Y21', 'Y22', 'Y23'])
        paramList.extend(['W11', 'W21', 'W31', 'W12', 'W22', 'W32', 'Z91', 'X11'])
        paramList.extend(['X12', 'X13', 'Y71', 'Y72', 'Y73', 'W81', 'W91', 'W82'])
        paramList.extend(['W92', 'W73', 'X51', 'X52', 'X53', 'X41', 'X42', 'X43'])
        paramList.extend(['Y81', 'Y82', 'Y83', 'V21', 'V31', 'V13', 'V22', 'V32'])
        paramList.extend(['V43', 'Y91', 'Y92', 'Y93', 'V61', 'V71', 'V53', 'V62'])
        paramList.extend(['V72', 'V83', 'Z11', 'Z12', 'Z13', 'Z23', 'Z31', 'Z32'])
        paramList.extend(['Z33', 'Y43', 'Y53', 'Y63', 'Z81', 'Z82', 'Z83', 'Z84'])
        paramList.extend(['Z85', 'Z86', 'X33', 'X61', 'X62', 'X63', 'X71', 'X72'])
        paramList.extend(['X73', 'X81', 'X82', 'X83', 'Z41', 'Z51', 'Z61', 'Z71'])
        paramList.extend(['Z42', 'Z43', 'Z52', 'Z53', 'Z62', 'Z63', 'Z72', 'Z73'])
        paramList.extend(['V91', 'V92'])

        #Get attribute value quantity and assigned to local variable
        for key in paramList:
            #locals()[key] = GS_Get_Set_AtvQty.getAtvQty(Product, "SerC_IO_Params", key)
			locals()[key] = getAttrQty(Product, key)

        #IOLDict = {"I/O Module": "Experssion to calculate the Total IO Load"}
        IOLDict = dict()
        IOLDict['CC-PAIH01'] = '0'
        IOLDict['CC-PAIH51'] = '1*(X21 + X22 + X23)'
        IOLDict['CC-PAIX01'] = '0'
        IOLDict['CC-PAIX02'] = '1* ((W41+W51+W61) + (W42+W52+W62+W23) + (Y31) + Y32 + Y33)'
        IOLDict['CC-PAIH02'] = '1*(Y21 + Y22 + Y23 + (W11+W21+W31) + (W12+W22+W32+Z91))'
        IOLDict['CC-PAIN01'] = '1*(X11+X12+X13)'
        IOLDict['CC-PAOH01'] = '1*(Y71 + Y72 + Y73 + (W81+W91) + (W82+W92+W73))'
        IOLDict['CC-PAOH51'] = '1*(X51 + X52 + X53)'
        IOLDict['CC-PAOX01'] = '0'
        IOLDict['CC-PAON01'] = '1*((X41) + X42 + X43)'
        IOLDict['CC-PDIL01'] = '1*((Y81) + Y82 + Y83 + (V21+V31) + (V13+V22+V32+V43))'
        IOLDict['CC-PDIL51'] = '0'
        IOLDict['CC-PDIS01'] = '1*(Y91 + Y92 + Y93 + (V61+V71) + (V53+V62+V72+V83))'
        IOLDict['CC-PDIH01'] = '1*(Z11 + Z12 + Z13 + Z23 + Z31 + Z32 + Z33)'
        IOLDict['CC-PDOD51'] = '0'
        IOLDict['CC-PAIM01'] = '1*(Y43 + Y53 + Y63)'
        IOLDict['CC-PUIO01'] = '0'
        IOLDict['CC-PPIX01'] = 'roundUp(1.5*((Z81+Z82+Z83) + (Z84+ Z85+ Z86)))'
        IOLDict['CC-PAIL51'] = '1*X33'
        IOLDict['CC-PUIO31'] = '1*((X61+X62+X63) + (X71+ X72+ X73+ X81+ X82+ X83))'
        IOLDict['CC-PDOB01'] = '1*((Z41+Z51+Z61+Z71) + (Z42 + Z43+ Z52+ Z53+ Z62+ Z63+ Z72+ Z73) + (V91) +V92)'
        IOL = 0
        for key in IOLDict.keys():
            IOL += eval(IOLDict[key])

        Trace.Write("IOL = {}".format(IOL))
        Product.Attr(iolAttr).AssignValue(str(IOL))

        #IOPDict = {"I/O Module": "Total IO Point Load"}
        IOPDict = dict()
        IOPDict['CC-TAIN01'] = 16
        IOPDict['CC-TAIX51'] = 16
        IOPDict['CC-TAIL51'] = 16
        IOPDict['CC-TAON01'] = 16
        IOPDict['CC-TAOX51'] = 16
        IOPDict['CC-TAIN11'] = 16
        IOPDict['CC-TAIX61'] = 16
        IOPDict['CC-TAON11'] = 16
        IOPDict['CC-TAOX61'] = 16
        IOPDict['CC-TUIO41'] = 32
        IOPDict['CC-TUIO31'] = 32
        IOPDict['CC-TUIO11'] = 32
        IOPDict['CC-TUIO01'] = 32
        IOPDict['CC-TAID11'] = 16
        IOPDict['CC-TAOX11'] = 16
        IOPDict['CC-TAID01'] = 16
        IOPDict['CC-TAOX01'] = 16
        IOPDict['CC-TAIM01'] = 64
        IOPDict['CC-TDIL11'] = 32
        IOPDict['CC-TDI120'] = 32
        IOPDict['CC-TDI230'] = 32
        IOPDict['CC-TDOB11'] = 32
        IOPDict['CC-TDIL01'] = 32
        IOPDict['CC-TDI110'] = 32
        IOPDict['CC-TDI151'] = 32
        IOPDict['CC-TDI220'] = 32
        IOPDict['CC-TDOB01'] = 32
        IOPDict['CC-TPIX11'] = 8
        IOPDict['CC-GAIX11'] = 16
        IOPDict['CC-GAIX21'] = 16
        IOPDict['CC-GAOX11'] = 16
        IOPDict['CC-GAOX21'] = 16
        IOPDict['CC-GDIL11'] = 32
        IOPDict['CC-GDIL21'] = 32
        IOPDict['CC-GDIL01'] = 32
        IOPDict['CC-GDOL11'] = 32
        IOPDict['CC-TDOR01'] = 32
        IOPDict['CC-TDOR11'] = 32
        IOPDict['CC-TAIX11'] = 16
        IOPDict['CC-TAIX01'] = 16

        AttrName = "Series_C_CG_Part_Summary"
        if Product.Name == "Series-C Remote Group":
            AttrName = "Series_C_RG_Part_Summary"
        IOP = 0
        for key in IOPDict.keys():
            IOP += IOPDict[key] * GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, key)
        #CXDEV-6971
        ioMount = ""
        if Product.Name == "Series-C Remote Group":
            ioMount = Product.Attr("Dummy_RG_IO_Mounting_Solution").GetValue()
            if ioMount == 'Universal Process Cab - 1.3M':
                CC_PUIO31 =(32* GS_Get_Set_AtvQty.getAtvQty(Product, AttrName,'CC-TUIO41')) +(32* GS_Get_Set_AtvQty.getAtvQty(Product, AttrName,'CC-TUIO31'))
                IOP += CC_PUIO31
        Trace.Write("IOP = {}".format(IOP))
        Product.Attr(iopAttr).AssignValue(str(IOP))

        IOUL = roundUp(float(IOL)/40.0)
        IOPL = roundUp(float(IOP)/1280.0)
        CN100 = max(IOUL, IOPL)

        if ioMount != 'Universal Process Cab - 1.3M':
            parts_dict['CC-IION01'] = CN100
            parts_dict['CC-TION11'] = CN100
            parts_dict['CC-INAM01'] = CN100
            if Product.Name == "Series-C Control Group":
                CN100_IO_HIVE = Product.Attr('SerC_CG_CN100_IO_HIVE_Redundancy').GetValue()
            else:
                CN100_IO_HIVE = Product.Attr('SerC_RG_CN100_I/O_HOVE').GetValue()
                Product.Attr("QTY_CC_TION11").AssignValue(str(CN100))
            if CN100_IO_HIVE == 'Redundant':
                parts_dict['CC-IION01'] = 2 * CN100
                parts_dict['CC-INAM01'] = 2 * CN100

    return parts_dict

#CXCPQ-54609
def getParts54609(Product, parts_dict, AttrName, E, F):
    cabinetAccesAttrName = "SerC_CG_Cabinet_Access"
    if Product.Name == "Series-C Remote Group":
        cabinetAccesAttrName = "SerC_RG_Cabinet_Access"
    cabinetAcces = Product.Attr(cabinetAccesAttrName).GetValue()
    fTALayout = Product.Attr('FTA_Layout').GetValue()

    #Calculate cabinet sides for FTA IOTAs based on UI question FTA Layout
    dict1 = dict()
    dict1['FTASide2Channel'] = 'roundUp(E/4.0)'
    dict1['FTASide3Channel'] = 'roundUp(E/6.0)'
    dict1['FTASide4Channel'] = 'roundUp(E/8.0)'
    G = eval(dict1.get(fTALayout, '0'))

    #Calculate cabinet sides for GIIS FTA IOTAs based on UI question FTA Layout
    dict2 = dict()
    dict2['FTASide2Channel'] = 'roundUp(F/4.0)'
    dict2['FTASide3Channel'] = 'roundUp(F/6.0)'
    dict2['FTASide4Channel'] = 'roundUp(F/6.0)'
    G1 = eval(dict2.get(fTALayout, '0'))

    #Calulate Total Quantity of 51304063-100
    part_number = '51304063-100'
    #qty = GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, part_number)
    #Qty has been updated as per the latest change in the user story - 08/17
    qty = 4 * (G1 + G)
    """if cabinetAcces == 'Single Access':
        qty += 4 * (G1 + G)
    else:
        qty += 4 * (roundUp(G1/2.0) + roundUp(G/2.0))"""

    parts_dict[part_number] = qty

    printList = ['cabinetAcces', 'fTALayout', 'G', 'G1', 'part_number', 'qty', 'E', 'F']
    for var in printList:
        Trace.Write("{}:{}".format(var,locals()[var]))

    return parts_dict

#CXCPQ-54003
def getParts54003(Product, parts_dict, AttrName):
    #Sizes in Inches
    dictIOTASize = {'CC-TION11': 9, 'CC-TCNT01': 9, 'CC-TCF901': 6, 'CC-TNWC01': 9, '8939-HN': 6}

    #Total IOTA Size req. On CCA
    Lo = 0
    for part in dictIOTASize.keys():
        Lo += dictIOTASize[part] * GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, part)

    qty = 0
    part_number = 'CC-MCAR01'
    SUM_HI, SUM_LO, SUM_HI1, SUM_LO1, SUM_HI11, SUM_LO11, SUM_D, HI, LO, LL = GS_C300_MCAR_calcs.mcar_cals(Product)
    mcar01 = SUM_HI + SUM_LO + SUM_HI1 + SUM_LO1
    if Lo > 0:
        qty = roundUp(Lo/36.0) + mcar01
        parts_dict[part_number] = qty

    printList = ['Lo', 'part_number', 'qty', 'mcar01']
    for var in printList:
        Trace.Write("{}:{}".format(var,locals()[var]))

    return parts_dict

#CXCPQ-53733
def getParts53733(Product, parts_dict, AttrName):
    #resDict = {'GX83': x, 'AX83': y, 'GX81': z, 'FX83': a, 'FX81': b, 'BX83': c, 'EX83': d, 'Y81': b, 'Z11': c, 'Z31': d}
    ##resDict = GS_PMIO_Variable.partCalc(Product)

    """X11+X21+X31+X41+Y11+Y31+Y41+Y51+Y71+Y81+Z11+Z31+Z51+Z91+CX81+DX81+FX81+GX81+LX81+MX81+NX81+OX81
    +PX81+QX81+RX81+SX81"""

    paramList = ['X11', 'X21', 'X31', 'X41', 'Y11', 'Y31', 'Y41', 'Y51', 'Y71', 'Z51']
    paramList.extend(['Z91', 'CX81', 'DX81', 'LX81', 'MX81', 'NX81', 'OX81', 'PX81', 'QX81', 'RX81', 'SX81'])

    """X12+X13+X22+X32+X33+X42+X53+X63+X73+X83+X93+Y12+Y13+Y22+Y32+Y42+Y52+Y63+Y72+Y83+Y93+Z13+Z23+Z33
    +Z43+Z52+Z63+Z73+Z83+Z92+AX83+BX83+CX82+DX82+EX83+FX83+GX83+LX83+MX83+NX83+OX83+PX83+QX83+RX82+SX83"""

    paramList1 = ['X12', 'X13', 'X22', 'X32', 'X33', 'X42', 'X53', 'X63', 'X73', 'X83', 'X93']
    paramList1.extend(['Y12', 'Y13', 'Y22', 'Y32', 'Y42', 'Y52', 'Y72', 'Z52', 'Z92', 'CX82'])
    paramList1.extend(['DX82', 'LX83', 'MX83', 'NX83', 'OX83', 'PX83', 'QX83', 'RX82', 'SX83'])

    paramList2 = ['Y63', 'Y83', 'Y93', 'Z13', 'Z23', 'Z33', 'Z43', 'Z63', 'Z73', 'Z83', 'GX83', 'AX83', 'FX83', 'BX83', 'EX83']

    total = 0
    for key in paramList:
        #total += GS_Get_Set_AtvQty.getAtvQty(Product, 'SerC_IO_Params', key)
        total +=  getAttrQty(Product, key)

    for key in ['Y81', 'Z11', 'Z31', 'GX81', 'FX81']:
        total +=  getAttrQty(Product, key)

    Y = 2 * total

    Z = 0
    for key in paramList1:
        #Z += GS_Get_Set_AtvQty.getAtvQty(Product, 'SerC_IO_Params', key)
        Z +=  getAttrQty(Product, key)

    if  len(resDict) > 0:
        for key in paramList2:
            Z += getAttrQty(Product, key)

    if Product.Name == "Series-C Control Group":
        Y1 = roundUp(Y/30.0) *2
        Z1 = roundUp(Z/15.0)
        calculatedValue = roundUp((Y + Z)/30.0)
        qty = Y1
        if(calculatedValue % 2 == 0):
            qty += Z1
    else:
        X = 2 * GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, 'MC-IOLX02')
        X1 = roundUp(X/30.0) * 2
        Y1 = roundUp(Y/28.0) * 2
        Z1 = roundUp(Z/15.0)
        calculatedValue = roundUp ((X + Y + Z)/28.0)
        qty = max(X1, Y1)
        if(calculatedValue % 2 == 0):
            qty += Z1

    part_number = 'MC-HPFX02'
    parts_dict[part_number] = qty
    return parts_dict


def getParts53576(Product, parts_dict, AttrName):
    cabinet_access = "SerC_CG_Cabinet_Access"
    power_system = "SerC_CG_PMIO_Power_System_Type"
    qty_6985_400 = GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, "51196958-400")
    add_qty_51198959_200 = 0
    add_qty_51199607_900 = 0
    if Product.Name == "Series-C Remote Group":
        cabinet_access = "SerC_RG_Cabinet_Access"
        power_system = "SerC_RG_PMIO_Power_System_Type"
        qty_6985_400 = 0
        add_qty_51198959_200 = GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, "51198959-200")
        add_qty_51199607_900 = GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, "51199607-900")
    A = parts_dict.get("MC-HPFX02", 0)
    S = ceil(A/3.0)
    D = ceil(A/6.0)
    C = 0
    if Product.Attr(cabinet_access).GetValue() == "Dual Access":
        B = D * 6
        C = B - A

    aList = ["MC-TAIH02", "MC-TLPA02", "MC-GLFD02", "MC-GPRD02"]
    ftaSizeA = sumOfFTAIOTAs(Product, aList, AttrName) * 6

    bList = ["MC-TAIH12", "MC-TAIH52", "MC-TAIH22", "MC-TAIH62", "MC-TAIL02", "MC-TAOY22", "MC-TAOY52", "MC-TDIY22", "MC-TDIY62", "MC-TDON12", "MC-TDON52", "MC-TDOD13", "MC-TDOD53", "MC-TDOD23", "MC-TDOD63", "MC-TDOA13", "MC-TDOA53", "MC-TDOR12", "MC-TDOR52", "MC-TDOR22", "MC-TDOR62", "MC-TDOY22", "MC-TDOY62", "MC-TDOY23", "MC-TDOY63"]
    ftaSizeB = sumOfFTAIOTAs(Product, bList, AttrName) * 12

    b1List = ["MC-GAIH13", "MC-GAIH14", "MC-GHAO11", "MC-GHAO21", "MC-GDID12", "MC-GDID13", "MC-GDOL12"]
    giisFtaSizeB = sumOfFTAIOTAs(Product, b1List, AttrName) * 12

    cList = ["MC-TDID12", "MC-TDID52", "MC-TDIA12", "MC-TDIA52", "MC-TDIA22", "MC-TDIA62"]
    ftaSizeC = sumOfFTAIOTAs(Product, cList, AttrName) * 18

    E = ceil((ftaSizeA + ftaSizeB + ftaSizeC)/36.0)
    F = ceil(giisFtaSizeB/36.0)

    G = 0
    H = 0
    if Product.Attr("FTA_Layout").GetValue() == "FTASide2Channel" and C <= 3:
        G = ceil(E/4.0)
        H = ceil(F/4.0)
    elif Product.Attr("FTA_Layout").GetValue() == "FTASide3Channel" and C <= 3:
        G = ceil(E/6.0)
        H = ceil(F/6.0)
    elif Product.Attr("FTA_Layout").GetValue() == "FTASide4Channel" and C <= 3:
        G = ceil(E/8.0)
        H = ceil(F/6.0)
    elif Product.Attr("FTA_Layout").GetValue() == "FTASide2Channel" and C > 3:
        G = ceil((E - 4)/4.0)
        H = ceil(F/4.0)
    elif Product.Attr("FTA_Layout").GetValue() == "FTASide3Channel" and C > 3:
        G = ceil((E - 6)/6.0)
        H = ceil(F/6.0)
    elif Product.Attr("FTA_Layout").GetValue() == "FTASide4Channel" and C > 3:
        G = ceil((E - 8)/8.0)
        H = ceil(F/6.0)

    cbds01 = GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, "CC-CBDS01")
    cbdd01 = GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, "CC-CBDD01")
    mcar = parts_dict.get("CC-MCAR01", 0)

    qty = S + G + H
    part = "MU-C8SS01"
    qty2_int=ceil(int(mcar) / 6.0)
    qty2= qty2_int + int(cbds01)
    part2 = "CC-CBDS01"
    if Product.Attr(cabinet_access).GetValue() == "Dual Access":
        qty = D + ceil(G/2.0) + ceil(H/2.0)
        part = "MU-C8DS01"
        qty2_int=ceil(int(mcar) / 12.0)
        qty2 = qty2_int + int(cbdd01)
        part2 = "CC-CBDD01"
    Product.Attr('C300_SerC_PMIO_Cab_Qty').AssignValue(str(qty2_int))
    #below line commented on 08/11
    ##qty_6985_400 = GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, "51196958-400")
    no_of_cab_sides = ceil(A / 3.0)
    tot_HPM_Cap = no_of_cab_sides * 3
    free_HPM = tot_HPM_Cap - A
    parts_dict["MU-C8SS01"] = 0
    parts_dict["MU-C8DS01"] = 0
    parts_dict["MC-PSRB04"] = 0
    parts_dict["MC-PSSX04"] = 0
    parts_dict["MC-PSRX04"] = 0
    parts_dict[part] = qty
    parts_dict["51196958-400"] =  qty + int(qty_6985_400)
    parts_dict["51198959-200"] =  qty + qty2_int + int(add_qty_51198959_200)
    parts_dict["51199607-900"] =  qty + qty2_int + int(add_qty_51199607_900)
    parts_dict["MC-FAN711"] = qty
    parts_dict["MU-CTFP01"] = free_HPM
    parts_dict["MU-CTVF05"] = free_HPM

    if Product.Attr(power_system).GetValue() == "Redundant 20A":
        part, qty = "MC-PSRX04", ceil(A/3.0)
    if Product.Attr(power_system).GetValue() == "Redundant with BBU 20A":
        part, qty = "MC-PSRB04", ceil(A/3.0)
    if Product.Attr(power_system).GetValue() == "Non Redundant 20A":
        part, qty = "MC-PSSX04", ceil(A/3.0)

    parts_dict[part] = qty
    parts_dict[part2] = qty2

    return parts_dict

#CXCPQ-54439
def sumOfFTAIOTAs(Product, list, AttrName):
    total = 0
    for part in list:
        total += GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, part)
    return total

def getParts54439(Product, parts_dict):
    global resDict
    resDict = dict()
    AttrName = "Series_C_CG_Part_Summary"
    cont = "Series_C_CG_Part_Summary_Cont"
    iOMountingSolutionAttrName = "SerC_CG_IO_Mounting_Solution"
    fTAChannelVerticalWidthAttrName = "SerC_CG_FTA_Channel_Vertical_Width"
    if Product.Name == "Series-C Remote Group":
        AttrName = "Series_C_RG_Part_Summary"
        cont = "Series_C_RG_Part_Summary_Cont"
        iOMountingSolutionAttrName = "Dummy_RG_IO_Mounting_Solution"
        fTAChannelVerticalWidthAttrName = "SerC_RG_FTA_Channel_Vertical_Width"

    if Product.GetContainerByName(cont).Rows.Count == 0:
        return parts_dict

    #newExpansion = Product.Attr('New_Expansion').GetValue()
    newExpansion = 'Expansion'
    iOFamilyType = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
    typeOfControllerRequired = Product.Attr('SerC_CG_Type_of_Controller_Required').GetValue()
    iOMountingSolution = Product.Attr(iOMountingSolutionAttrName).GetValue()
    fTAChannelVerticalWidth = Product.Attr(fTAChannelVerticalWidthAttrName).GetValue()
    shieldOption = Product.Attr('Shield_Option').GetValue()
    pMIOSolutionRequired = Product.Attr('SerC_CG_PM_IO_Solution_required').GetValue()
    resetQty = False

    if newExpansion == 'Expansion' and iOFamilyType == 'Series C' and (typeOfControllerRequired == 'C300 CEE' or typeOfControllerRequired == '') and iOMountingSolution == 'Cabinet':
        if pMIOSolutionRequired == 'Yes':
            partDict = {'Shields':{'Narrow':'MU-TMCN02','Wide':'MU-TMCW02'},'No Shields':{'Narrow':'MU-TMCN01','Wide':'MU-TMCW01'}}
            SUM_HI, SUM_LO, SUM_HI1, SUM_LO1, SUM_HI11, SUM_LO11, SUM_D, HI, LO, LL = GS_C300_MCAR_calcs.mcar_cals(Product)
            #reset part qty
            for pn in ['MU-TMCN02', 'MU-TMCW02', 'MU-TMCW01']:
                parts_dict[pn] = 0
            parts_dict['MU-TMCN01'] = SUM_D
            #Part Number
            part_number = partDict[shieldOption][fTAChannelVerticalWidth]
            #Calculate the total size of A Size FTA IOTAs
            listA = ['MC-TAIH02', 'MC-TLPA02', 'MC-GLFD02', 'MC-GPRD02']
            A = sumOfFTAIOTAs(Product, listA, AttrName) * 6

            #Calculate the total size of B Size FTA IOTAs
            listB = ["MC-TAIH12", "MC-TAIH52", "MC-TAIH22", "MC-TAIH62", "MC-TAIL02", "MC-TAOY22", "MC-TAOY52", "MC-TDIY22", "MC-TDIY62", "MC-TDON12", "MC-TDON52", "MC-TDOD13", "MC-TDOD53", "MC-TDOD23", "MC-TDOD63", "MC-TDOA13", "MC-TDOA53", "MC-TDOR12", "MC-TDOR52", "MC-TDOR22", "MC-TDOR62", "MC-TDOY22", "MC-TDOY62", "MC-TDOY23", "MC-TDOY63"]
            B = sumOfFTAIOTAs(Product, listB, AttrName) * 12

            #Calculate total size of B Size GIIS FTA IOTAs
            listB1 = ["MC-GAIH13", "MC-GAIH14", "MC-GHAO11", "MC-GHAO21", "MC-GDID12", "MC-GDID13", "MC-GDOL12"]
            B1 = sumOfFTAIOTAs(Product, listB1, AttrName) * 12

            #Calculate the total size of C Size FTA IOTAs
            listC = ['MC-TDID12', 'MC-TDID52', 'MC-TDIA12', 'MC-TDIA52', 'MC-TDIA22', 'MC-TDIA62']
            C = sumOfFTAIOTAs(Product, listC, AttrName) * 18

            #Calculated Size of FTA IOTAs
            D = A + B + C

            #Calculate total no of FTA Channels
            E = roundUp(D/36.0)

            #Calculate total no of GIIS FTA Channels
            F = roundUp(B1/36.0)

            #Total Quantity
            totalQuantity = E + F
            if part_number == 'MU-TMCN01':
                totalQuantity += SUM_D
            parts_dict[part_number] = totalQuantity

            printList = ['A', 'B', 'B1', 'C', 'D', 'E', 'F', 'totalQuantity', 'part_number']
            for var in printList:
                Trace.Write("{}:{}".format(var,locals()[var]))

            parts_dict = getParts54609(Product, parts_dict, AttrName, E, F)
            parts_dict = getParts54003(Product, parts_dict, AttrName)
            parts_dict = getParts53733(Product, parts_dict, AttrName)
            parts_dict = getParts53576(Product, parts_dict, AttrName)
        else:
            resetQty = True
    else:
        resetQty = True
    if resetQty:
        SUM_HI, SUM_LO, SUM_HI1, SUM_LO1, SUM_HI11, SUM_LO11, SUM_D, HI, LO, LL = GS_C300_MCAR_calcs.mcar_cals(Product)
        mcar01 = SUM_HI + SUM_LO + SUM_HI1 + SUM_LO1
        parts_dict['CC-MCAR01'] = mcar01
        parts_dict['MU-TMCN01'] = SUM_D
        for part in ['MU-TMCN02', 'MU-TMCW02', 'MU-TMCW01', '51304063-100', 'MC-HPFX02', "MU-C8DS01", "MU-C8SS01", "MC-FAN711", "MU-CTVF05", "MU-CTFP01", "MC-PSRB04", "MC-PSSX04", "MC-PSRX04"]:
            #add_qty = GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, str(part))
            parts_dict[part] = 0 #int(add_qty)
    return parts_dict

def getParts51996(Product):
    if Product.Name == "Series-C Control Group":
        iOMountingSolutionAttrName = "SerC_CG_IO_Mounting_Solution"
        cabinet_access = Product.Attr("SerC_CG_Cabinet_Access").GetValue()
        power_system = Product.Attr("SerC_CG_PMIO_Power_System_Type").GetValue()
        CabinetColorDefault = Product.Attr("SerC_CG_Cabinet_Color_Default").GetValue()
        CabinetDoorsDefault = Product.Attr("SerC_CG_Cabinet_Doors_Default").GetValue()
        PowerEntryDefault = Product.Attr("SerC_CG_Power_Entry_Default").GetValue()
        CabinetThermostatDefault = Product.Attr("SerC_CG_Cabinet_Thermostat_Default").GetValue()
        CabinetLightDefault = Product.Attr("SerC_CG_Cabinet_Light_Default").GetValue()
        SiteVol = Product.Attr("CE_Site_Voltage").GetValue()
        FanOption = Product.Attr("SerC_CG_Fan_Option").GetValue()
        CabinetDoorKeylockDefault = Product.Attr("SerC_CG_Cabinet_Door_Keylock _Default").GetValue()
        CabinetHingeTypeDefault = Product.Attr("SerC_CG_Cabinet_Hinge_Type").GetValue()
        CabinetBaseSize = Product.Attr("SerC_CG_Cabinet_Base_Size").GetValue()
        cabinetBase = Product.Attr("SerC_CG_Cabinet_Base_(Plinth)").GetValue()
        PMIOCabQty = getFloat(Product.Attr('C300_SerC_PMIO_Cab_Qty').GetValue())
        partSummaryAttr = "Series_C_CG_Part_Summary"

    elif Product.Name == "Series-C Remote Group":
        iOMountingSolutionAttrName = "Dummy_RG_IO_Mounting_Solution"
        cabinet_access = Product.Attr("SerC_RG_Cabinet_Access").GetValue()
        power_system = Product.Attr("SerC_RG_PMIO_Power_System_Type").GetValue()
        CabinetColorDefault = Product.Attr("SerC_RG_Cabinet_Color_Default").GetValue()
        CabinetDoorsDefault = Product.Attr("SerC_RG_Cabinet_Doors_Default").GetValue()
        PowerEntryDefault = Product.Attr("SerC_RG_Power_Entry_Default").GetValue()
        CabinetThermostatDefault = Product.Attr("SerC_RG_Cabinet_Thermostat_Default").GetValue()
        CabinetLightDefault = Product.Attr("SerC_RG_Cabinet_Light_Default").GetValue()
        SiteVol = Product.Attr("CE_Site_Voltage").GetValue()
        FanOption = Product.Attr("SerC_RG_Fan_Option").GetValue()
        CabinetDoorKeylockDefault = Product.Attr("SerC_RG_Cabinet_Door_Keylock_Default").GetValue()
        CabinetHingeTypeDefault = Product.Attr("SerC_RG_Cabinet_Hinge_Type_Default").GetValue()
        CabinetBaseSize = Product.Attr("SerC_RG_Cabinet_Base_Size").GetValue()
        cabinetBase = Product.Attr("SerC_RG_Cabinet_Base_(Plinth)").GetValue()
        PMIOCabQty = getFloat(Product.Attr('C300_SerC_PMIO_Cab_Qty').GetValue())
        partSummaryAttr = "Series_C_RG_Part_Summary"

    pMIOSolutionRequired = Product.Attr('SerC_CG_PM_IO_Solution_required').GetValue()
    iOFamilyType = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
    typeOfControllerRequired = Product.Attr('SerC_CG_Type_of_Controller_Required').GetValue()
    iOMountingSolution = Product.Attr(iOMountingSolutionAttrName).GetValue()

    if not(iOFamilyType == 'Series C' and (typeOfControllerRequired == 'C300 CEE' or typeOfControllerRequired == '') and iOMountingSolution == 'Cabinet' and pMIOSolutionRequired == 'Yes'):
        return
    Trace.Write("PMIO Cab QTY : {}".format(PMIOCabQty))

    A = PMIOCabQty
    B = int(A) // 4
    rem = A % 4
    E = 1 if rem == 3 else 0
    D = 1 if rem == 2 else 0
    F = 1 if rem == 1 else 0

    GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"51199607-900", PMIOCabQty)
    GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"51198959-200", PMIOCabQty)

    if CabinetColorDefault == "Gray-RAL 7032":
        GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"51197174-200",PMIOCabQty)
    elif CabinetColorDefault == "Custom":
        GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"51197174-100",PMIOCabQty)

    if cabinet_access == "Single Access":

        GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"51121311-200", PMIOCabQty)
        GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"51202335-300", PMIOCabQty)

        if CabinetDoorsDefault == "Double":
            GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"MU-C8DRD1",PMIOCabQty)
        else:
            GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"MU-C8DRS1",PMIOCabQty)

        if CabinetDoorsDefault == "Reverse Front":
            GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"51197150-600",PMIOCabQty)
        elif CabinetDoorsDefault in ["Reverse Rear","Reverse Front & Rear","Standard"]:
            GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"51197150-500",PMIOCabQty)

        if CabinetHingeTypeDefault == "130 Degree":
            GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"51197168-100",PMIOCabQty)
        else:
            GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"51197168-200",PMIOCabQty)

        if CabinetDoorKeylockDefault == "Standard":
            GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"51197165-100",PMIOCabQty)
        else:
            GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"51197165-200",PMIOCabQty)

        if cabinetBase == "Yes" and CabinetBaseSize == "100mm":
            GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"MU-C8SBA1",PMIOCabQty)
        elif cabinetBase == "Yes":
            GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"MU-C8SBA2",PMIOCabQty)

        if FanOption in ["TopCoverPlate","Assembly - Universal Fan","24V Assembly"]:
            GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"51199948-100",PMIOCabQty)

        if SiteVol == "120V" and FanOption == "Assembly":
            GS_PS_Exp_Ent_BOM.addAtvQty(Product, partSummaryAttr, "51199947-175", PMIOCabQty)
        elif SiteVol == "240V" and FanOption == "Assembly":
            GS_PS_Exp_Ent_BOM.addAtvQty(Product, partSummaryAttr, "51199947-275", PMIOCabQty)
        elif FanOption == "Assembly - Universal Fan":
            GS_PS_Exp_Ent_BOM.addAtvQty(Product, partSummaryAttr, "51199947-375", PMIOCabQty)
        elif FanOption == "Grille":
            GS_PS_Exp_Ent_BOM.addAtvQty(Product, partSummaryAttr, "51202397-100", PMIOCabQty)
        elif FanOption == "24V Assembly":
            GS_PS_Exp_Ent_BOM.addAtvQty(Product, partSummaryAttr, "51154692-100", PMIOCabQty)

        if CabinetLightDefault == "Yes":
            GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"MU-CULF01",PMIOCabQty)

        if CabinetThermostatDefault == "Yes":
            GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"MU-C8TRM1",PMIOCabQty)

        if PowerEntryDefault == "Double Pole":
            GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"51403902-100",PMIOCabQty)
        GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"MU-C8SSS1", 2 * (B + D + E + F))

    if cabinet_access == "Dual Access":

        GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"51121311-100", PMIOCabQty)
        GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"51202335-300", 2 * PMIOCabQty)


        if CabinetDoorsDefault == "Double":
            GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"MU-C8DRD1",2 * PMIOCabQty)
        else:
            GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"MU-C8DRS1",2 * PMIOCabQty)

        if CabinetDoorsDefault == "Reverse Front":
            GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"51197150-400",PMIOCabQty)
        elif CabinetDoorsDefault == "Reverse Rear":
            GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"51197150-300",PMIOCabQty)
        elif CabinetDoorsDefault == "Reverse Front & Rear":
            GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"51197150-200",PMIOCabQty)

        if CabinetHingeTypeDefault == "130 Degree":
            GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"51197168-100",2 * PMIOCabQty)
        else:
            GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"51197168-200",2 * PMIOCabQty)

        if CabinetDoorKeylockDefault == "Standard":
            GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"51197165-100",2 * PMIOCabQty)
        else:
            GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"51197165-200",2 * PMIOCabQty)

        if cabinetBase == "Yes" and CabinetBaseSize == "100mm":
            GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"MU-C8DBA1",PMIOCabQty)
        elif cabinetBase == "Yes":
            GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"MU-C8DBA2",PMIOCabQty)

        if FanOption == "TopCoverPlate":
            GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"51199948-100",2 * PMIOCabQty)

        if SiteVol == "120V" and FanOption == "Assembly":
            GS_PS_Exp_Ent_BOM.addAtvQty(Product, partSummaryAttr, "51199947-175", 2 * PMIOCabQty)
        elif SiteVol == "240V" and FanOption == "Assembly":
            GS_PS_Exp_Ent_BOM.addAtvQty(Product, partSummaryAttr, "51199947-275", 2 * PMIOCabQty)
        elif FanOption == "Assembly - Universal Fan":
            GS_PS_Exp_Ent_BOM.addAtvQty(Product, partSummaryAttr, "51199947-375", 2 * PMIOCabQty)
        elif FanOption == "Grille":
            GS_PS_Exp_Ent_BOM.addAtvQty(Product, partSummaryAttr, "51202397-100", 2 * PMIOCabQty)
        elif FanOption == "24V Assembly":
            GS_PS_Exp_Ent_BOM.addAtvQty(Product, partSummaryAttr, "51154692-100", PMIOCabQty)

        if CabinetLightDefault == "Yes":
            GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"MU-CULF01",2 * PMIOCabQty)

        if CabinetThermostatDefault == "Yes":
            GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"MU-C8TRM1",2 * PMIOCabQty)

        if PowerEntryDefault == "Double Pole":
            GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"51403902-100",2 * PMIOCabQty)
        GS_PS_Exp_Ent_BOM.addAtvQty(Product,partSummaryAttr,"MU-C8DSS1", 2 * (B + D + E + F))