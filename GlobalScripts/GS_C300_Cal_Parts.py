#39298,39294,39961,39843By Shivani`
import System.Decimal as D
import GS_Get_Set_AtvQty
from math import ceil

def getFloat(var):
    if var:
        return float(var)
    return 0

def abc(value, percent):
    if value:
        return int(D.Ceiling(float(value*(1+(percent/100)))))
    return 0

def most(Product, row, percent):
    prefixmap = {
        'Series-C: HLAI (16) 4-20mA (0-5000)' : 'X1',
        'Series-C: HLAI (16) HART Config/Status (0-5000)' : 'X2',
        'Series-C: LLAI (16) (0-5000)' : 'X3',
        'Series-C: AO (16) (0-5000)' : 'X4',
        'Series-C: AO (16) HART Config/Status (0-5000)' : 'X5'
    }
    io_type = row.GetColumnByName("IO_Type").Value
    pre = prefixmap.get(io_type)

    A11 = abc(getFloat(row.GetColumnByName('Red_IS').Value),percent)
    B11 = abc(getFloat(row.GetColumnByName('Future_Red_IS').Value),percent)
    C11 = abc(getFloat(row.GetColumnByName('Non_Red_IS').Value),percent)
    A12 = abc(getFloat(row.GetColumnByName('Red_NIS').Value),percent)
    B12 = abc(getFloat(row.GetColumnByName('Future_Red_NIS').Value),percent)
    C12 = abc(getFloat(row.GetColumnByName('Non_Red_NIS').Value),percent)
    A13 = abc(getFloat(row.GetColumnByName('Red_ISLTR').Value),percent)
    B13 = abc(getFloat(row.GetColumnByName('Future_Red_ISLTR').Value),percent)
    C13 = abc(getFloat(row.GetColumnByName('Non_Red_ISLTR').Value),percent)


    X41 = D.Ceiling(float(A11/16.0))+D.Ceiling(float(A12/16.0))+D.Ceiling(float(A13/16.0))
    X42 = D.Ceiling(float(B11/16.0))+D.Ceiling(float(B12/16.0))+D.Ceiling(float(B13/16.0))
    X43 = D.Ceiling(float(C11/16.0))+D.Ceiling(float(C12/16.0))+D.Ceiling(float(C13/16.0))
    if pre:
        GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', pre + '1', X41)
        GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', pre + '2', X42)
        GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', pre + '3', X43)
        

    PAON01 = 2.0 * (X41) + X42 + X43
    TAON11 = X41 + X42
    TAON01 = X43

    '''Trace.Write('A11 '+ str(A11))
    Trace.Write('B11 '+ str(B11))
    Trace.Write('C11 '+ str(C11))
    Trace.Write('A12 '+ str(A12))
    Trace.Write('B12 '+ str(B12))
    Trace.Write('C12 '+ str(C12))
    Trace.Write('A13 '+ str(A13))
    Trace.Write('B13 '+ str(B13))
    Trace.Write('C13 '+ str(C13))
    Trace.Write(X41)
    Trace.Write(X42)
    Trace.Write(X43)
    Trace.Write(PAON01)
    Trace.Write(TAON11)
    Trace.Write(TAON01)'''
    return PAON01,TAON11,TAON01
#C300 Bom Cal
def part_qty_IO(Product):

    if Product.Name == "Series-C Control Group":
        Trace.Write(Product.Name)
        Percent_Installed_Spare=getFloat(Product.Attributes.GetByName("SerC_CG_Percent_Installed_Spare").GetValue())
        Trace.Write('Percent_Installed_Spare'+str(Percent_Installed_Spare))
        #io_type = Product.Attributes.GetByName("IO_Type").Value
        io_type = Product.GetContainerByName('C300_C IO MS')
        CC_PAIN01 = CC_TAIN11 = CC_TAIN01= CC_PAIH51 = CC_TAIX61 = CC_TAIX51=CC_PAON01 = CC_TAON11 = CC_TAON01=CC_PAOH51 = CC_TAOX61 = CC_TAOX51=0
        for row in io_type.Rows:
            if row.GetColumnByName("IO_Type").Value=='Series-C: HLAI (16) 4-20mA (0-5000)':
                CC_PAIN01 ,CC_TAIN11 , CC_TAIN01 = most(Product, row , Percent_Installed_Spare)
            if row.GetColumnByName("IO_Type").Value=='Series-C: HLAI (16) HART Config/Status (0-5000)':
                CC_PAIH51,CC_TAIX61, CC_TAIX51 = most(Product, row,Percent_Installed_Spare)
            if row.GetColumnByName("IO_Type").Value=='Series-C: AO (16) (0-5000)':
                CC_PAON01,CC_TAON11,CC_TAON01 = most(Product, row,Percent_Installed_Spare)
            if row.GetColumnByName("IO_Type").Value=='Series-C: AO (16) HART Config/Status (0-5000)':
                CC_PAOH51 , CC_TAOX61 , CC_TAOX51 = most(Product, row,Percent_Installed_Spare)
            if row.GetColumnByName("IO_Type").Value=='Series-C: LLAI (16) (0-5000)':
                dummy_a , dummy_b , dummy_c = most(Product, row,Percent_Installed_Spare)

    elif Product.Name == "Series-C Remote Group":
        Trace.Write(Product.Name)
        Percent_Installed_Spare=getFloat(Product.Attributes.GetByName("SerC_RG_Percent_Installed_Spare(0-100%)").GetValue())
        Trace.Write('Percent_Installed_Spare'+str(Percent_Installed_Spare))
        io_type =Product.GetContainerByName('C300_C IO_RG MS')
        CC_PAIN01 = CC_TAIN11 = CC_TAIN01= CC_PAIH51 = CC_TAIX61 = CC_TAIX51=CC_PAON01 = CC_TAON11 = CC_TAON01=CC_PAOH51 = CC_TAOX61 = CC_TAOX51=0
        for row in io_type.Rows:
            if row.GetColumnByName("IO_Type").Value=='Series-C: HLAI (16) 4-20mA (0-5000)':
                CC_PAIN01 ,CC_TAIN11 , CC_TAIN01 = most(Product, row , Percent_Installed_Spare)
            if row.GetColumnByName("IO_Type").Value=='Series-C: HLAI (16) HART Config/Status (0-5000)':
                CC_PAIH51,CC_TAIX61, CC_TAIX51 = most(Product, row,Percent_Installed_Spare)
            if row.GetColumnByName("IO_Type").Value=='Series-C: AO (16) (0-5000)':
                CC_PAON01,CC_TAON11,CC_TAON01 = most(Product, row,Percent_Installed_Spare)
            if row.GetColumnByName("IO_Type").Value=='Series-C: AO (16) HART Config/Status (0-5000)':
                CC_PAOH51 , CC_TAOX61 , CC_TAOX51 = most(Product, row,Percent_Installed_Spare)
            if row.GetColumnByName("IO_Type").Value=='Series-C: LLAI (16) (0-5000)':
                dummy_a , dummy_b , dummy_c = most(Product, row,Percent_Installed_Spare)

    return int(CC_PAIN01) ,int(CC_TAIN11), int(CC_TAIN01),int(CC_PAIH51),int(CC_TAIX61), int(CC_TAIX51), int(CC_PAON01),int(CC_TAON11),int(CC_TAON01), int(CC_PAOH51) , int(CC_TAOX61) , int(CC_TAOX51)


'''
    Trace.Write('CC_PAOH51 '+str(CC_PAOH51))
    Trace.Write('CC_TAOX61 '+str(CC_TAOX61))
    Trace.Write('CC_TAOX51 '+str(CC_TAOX51))
    Trace.Write('CC_TAON01 '+str(CC_TAON01))
    Trace.Write('CC_TAON11 '+str(CC_TAON11))
    Trace.Write('CC_PAON01 '+str(CC_PAON01))
    Trace.Write('CC_PAIN01 '+str(CC_PAIN01))
    Trace.Write('CC_TAIN11 '+str(CC_TAIN11))
    Trace.Write('CC_TAIN01 '+str(CC_TAIN01))
    Trace.Write('CC_PAIH51 '+str(CC_PAIH51))
    Trace.Write('CC_TAIX61 '+str(CC_TAIX61))
    Trace.Write('CC_TAIX51 '+str(CC_TAIX51))


x=part_qty_IO(Product)
Trace.Write(x)'''
def getpartsseriesc(Product):
    F41 = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','F41')
    F42 = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','F42')
    F43 = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','F43')
    F51 = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','F51')
    F52 = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','F52')
    F53 = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','F53')
    F61 = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','F61')
    F62 = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','F62')
    F63 = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','F63')
    MCTAMR04=MCTAMT04=MCTAMT14=MUKLAM03=MUTMCN01=0
    if Product.Name=="Series-C Control Group" and Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C":
        Trace.Write(Product.Name)
        MCTAMR04 = D.Ceiling(float(F41)/16.0)+D.Ceiling(float(F42)/16.0)+D.Ceiling(float(F43)/16.0)
        MCTAMT04 = D.Ceiling(float(F51)/16.0)+D.Ceiling(float(F52)/16.0)+D.Ceiling(float(F53)/16.0)
        MCTAMT14 = D.Ceiling(float(F61)/16.0)+D.Ceiling(float(F62)/16.0)+D.Ceiling(float(F63)/16.0)
        MUKLAM03 = MCTAMR04+MCTAMT04+MCTAMT14
        #MUTMCN01 = D.Ceiling(float(MCTAMR04+MCTAMT04+MCTAMT14)/3.0)
    elif Product.Name=="Series-C Remote Group" and Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C":
        Trace.Write(Product.Name)
        MCTAMR04 = D.Ceiling(float(F41)/16.0)+D.Ceiling(float(F42)/16.0)+D.Ceiling(float(F43)/16.0)
        MCTAMT04 = D.Ceiling(float(F51)/16.0)+D.Ceiling(float(F52)/16.0)+D.Ceiling(float(F53)/16.0)
        MCTAMT14 = D.Ceiling(float(F61)/16.0)+D.Ceiling(float(F62)/16.0)+D.Ceiling(float(F63)/16.0)
        MUKLAM03 = MCTAMR04+MCTAMT04+MCTAMT14
        #MUTMCN01 = D.Ceiling(float(MCTAMR04+MCTAMT04+MCTAMT14)/3.0)
    return int(MCTAMR04), int(MCTAMT04), int(MCTAMT14) , int(MUKLAM03) #,int(MUTMCN01)

def getparts41456(Product):
    Z61 = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Z61')
    Z62 = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Z62')
    Z63 = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Z63')
    Z71 = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Z71')
    Z72 = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Z72')
    Z73 = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Z73')
    CCSDOR01=CCKREB=0
    IOType=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
    Trace.Write(IOType)
    if Product.Name=="Series-C Control Group" and IOType=="Series C":
        Trace.Write(Product.Name)
        CCSDOR01 = Z61+ Z62+ Z63+ Z71+ Z72+ Z73
        CCKREB = Z61+ Z62+ Z63+ Z71+ Z72+ Z73
    elif Product.Name=="Series-C Remote Group" and IOType=="Series C":
        Cable=Product.Attr('SerC_RG_DO_Relay_Extension_Cable_Length').GetValue()
        Trace.Write(Product.Name)
        CCSDOR01 = Z61+ Z62+ Z63+ Z71+ Z72+ Z73
        #if Cable=="0.5M" or Cable=="1M" or Cable=="2M" or Cable=="5M" or Cable=="10M":
        CCKREB = Z61+ Z62+ Z63+ Z71+ Z72+ Z73

    return int(CCSDOR01),int(CCKREB)

def getPartCCPCNT_SerC_CN100_IOHive_Qty(Product, part):
    # Log.Write("Got Called")
    qty = 0
    cction11 = GS_Get_Set_AtvQty.getAtvQty(Product, 'Series_C_CG_Part_Summary', 'CC-TION11')
    totalIoPointLoad = getFloat(Product.Attr("C300_CG_Total_IO_Point_Load").GetValue())

    container = Product.GetContainerByName("Series_C_Remote_Groups_Cont")
    for row in container.Rows:
        cction11 += getFloat(row["QTY_CC_TION11"])
        totalIoPointLoad += getFloat(row["Total_IO_Point_Load"])
    qty = max(ceil(cction11/10.0), ceil(totalIoPointLoad/900.0))
    if part == "CC-PCNT05":
        qty = max(ceil(cction11/15.0), ceil(totalIoPointLoad/1500.0))
    # Log.Write(str(cction11) + " " + str(totalIoPointLoad) + " " + str(qty))
    return part, "", qty


def getPartCCPCNT_SerC_Cntrl_Hive_Qty(Product, part, memBlockPart):
    qty = 0
   #cction11 = GS_Get_Set_AtvQty.getAtvQty(Product, 'Series_C_CG_Part_Summary', 'CC-TION11')
   #totalIoPointLoad = getFloat(Product.Attr("C300_CG_Total_IO_Point_Load").GetValue())
    totalcontrolcction11 = GS_Get_Set_AtvQty.getAtvQty(Product, 'Series_C_CG_Part_Summary', 'CC-TION11')
    totalRemotecction11= getFloat(Product.Attr("SerC_CG_Total_CN100").GetValue())
    totalIoPointLoad = getFloat(Product.Attr("HCA_Total_IO_Point").GetValue())
    cction11=totalcontrolcction11+totalRemotecction11
    '''
    container = Product.GetContainerByName("Series_C_Remote_Groups_Cont")
    for row in container.Rows:
        cction11 += getFloat(row["QTY_CC_TION11"])
        totalIoPointLoad += getFloat(row["Total_IO_Point_Load"])
    '''
    #CXDEV-8402
    calc_hive_controller = max(ceil(cction11/10.0), totalIoPointLoad)
    #calc_hive_controller = max(ceil(cction11/10.0), ceil(totalIoPointLoad/1000.0))
    Product.Attr("SerC_CG_Number_of_HIVE_Control_Applications(HCA)").AssignValue(str(calc_hive_controller))

    addnl_hive_controller = getFloat(Product.Attr("SerC_CG_Number_of_Extra_HIVE_Control_Applications").GetValue())
    red_hive_controller = getFloat(Product.Attr("SerC_CG_Number_of_Redundant_HIVE_Control_App").GetValue())
    hive_availability = getFloat(Product.Attr("SerC_CG_Control_HIVE_Availability_Level_required").GetValue())

    total_hive_controller = calc_hive_controller + addnl_hive_controller

    qty = ceil((2 * hive_availability + 2 * red_hive_controller + (total_hive_controller - red_hive_controller)) / 2.0)

    return part, memBlockPart, qty


def getPartCCPCNTQty(Product):
    shouldAdd = True
    expRelease = Product.Attr("Experion_PKS_Software_Release").GetValue()
    ioFamily = Product.Attr("SerC_CG_IO_Family_Type").GetValue()
    expRelease = Product.Attr("Experion_PKS_Software_Release").GetValue()
    controllerModuleType = Product.Attr("SerC_CG_C300_Controller_Module_Type").GetValue()
    requiredControllerType = Product.Attr("SerC_CG_Type_of_Controller_Required").GetValue()

    part = "CC-PCNT02"
    memBlockPart = "CC-SCMB02"

    if controllerModuleType == "C300(PCNT05)":
        part = "CC-PCNT05"
        memBlockPart = "CC-SCMB05"

    if ioFamily == "Series-C Mark II" and memBlockPart == "CC-SCMB02":
        memBlockPart = "51454475-100"


    if ioFamily == "Turbomachinery":
        return getPart_CCPCNT_TurboM_Qty(Product)
    elif ioFamily == "Series C" and requiredControllerType == "CN100 I/O HIVE - C300 CEE":
        return getPartCCPCNT_SerC_CN100_IOHive_Qty(Product, part)
    elif ioFamily == "Series C" and requiredControllerType in ("Control HIVE - Physical", "Control HIVE - Virtual"):
        return getPartCCPCNT_SerC_Cntrl_Hive_Qty(Product, part, memBlockPart)

    shouldAdd = (ioFamily == "Series C" and (requiredControllerType == "C300 CEE" or expRelease in ("R510", "R511"))) or ioFamily == "Series-C Mark II"

    if not shouldAdd:
        return part, memBlockPart, 0

    nonRedPGM = getFloat(Product.Attr("SerC_Number_of_Profibus_DP_Slave_devices - Non_Red").GetValue())
    redPGM = getFloat(Product.Attr("SerC_Number_of_Profibus_DP_Slave_devices - Red").GetValue())
    noOfDevices = getFloat(Product.Attr("SerC_Number_of_Devices_per_Profibus_Network (0-32)").GetValue())

    NRCP = getFloat(Product.Attr("SerC_Number_of_Rockwell_ControlLogix_Processors").GetValue())
    NRCPE = getFloat(Product.Attr("SerC_Number of Rockwell Control Processors(NON)").GetValue())
    NPCD = getFloat(Product.Attr("SerC_Number of Process Connected I/O Devices 1").GetValue())
    NME = getFloat(Product.Attr("SerC_Number of Motor Starter IOMs per EIM 255").GetValue())
    RRCP = getFloat(Product.Attr("SerC_NO of Rock Ctrl Processors Redundant0-999NEW").GetValue())
    RRCPE = getFloat(Product.Attr("SerC_Numbe of Rockwelix Proc EIM Redundant 0-10").GetValue())
    RPCD = getFloat(Product.Attr("SerC_Nu of Proc Conn I/O Devi (Redundant ) (0-999)").GetValue())
    RMIE = getFloat(Product.Attr("SerC_Number of Motor Start IOMs per EIM Redun 255").GetValue())
    NID = getFloat(Product.Attr("SerC_Number of Non Redundant EIM for IEC61850").GetValue())
    RID = getFloat(Product.Attr("SerC_Number of Redundant EIM for IEC61850").GetValue())
    NPD = getFloat(Product.Attr("SerC_Number of Non Redund EIM for Profinet Devices").GetValue())
    RPD = getFloat(Product.Attr("SerC_Number of Redundant EIM for Profinet Devices").GetValue())
    NED = getFloat(Product.Attr("SerC_Number of Non Redundant EIM for EIP Device").GetValue())
    RED = getFloat(Product.Attr("SerC_Number of Redunt EIM for EIP Devices (0-300)").GetValue())
    #7707
    REM = getFloat(Product.Attr("SerC_Number_Redundant_EIM_for_Modbus").GetValue())
    NEM = getFloat(Product.Attr("SerC_Number_NonRedundant_EIM_for_Modbus").GetValue())

    qty1 = qty2 = qty3 = totalIoLoad = 0
    for row in Product.GetContainerByName("Series_C_Remote_Groups_Cont").Rows:
        totalIoLoad += getFloat(row["Total_IO_Load"])
    totalIoLoad += getFloat(Product.Attr("C300_CG_Total_IO_Load").GetValue())
    qty1 = ceil(totalIoLoad / 80.0)

    if noOfDevices:
        # Roundup(roundup (N/P,0)+Roundup(roundup(R/P,0)/2,0)/4,0)
        qty2 = ceil((ceil(nonRedPGM/noOfDevices) + ceil(ceil(redPGM/noOfDevices)/2.0))/4.0)
        if part == "CC-PCNT05":
            qty2 = ceil((ceil(nonRedPGM/noOfDevices) + ceil(ceil(redPGM/noOfDevices)/2.0))/8.0)


    # Roundup (((roundup (RRCP/RRCPE,0) + roundup (RPCD/RMIE,0) + RID + RPD + RED) + roundup (NRCP/NRCPE,0) + roundup (NPCD/NME,0) + NID + NPD + NED)/5,0)
    RRCP, RRCPE = (RRCP, RRCPE) if RRCPE else (0, 1)
    RPCD, RMIE = (RPCD, RMIE) if RMIE else (0, 1)
    NRCP, NRCPE = (NRCP, NRCPE) if NRCPE else (0, 1)
    NPCD, NME = (NPCD, NME) if NME else (0, 1)
    qty3 = ceil(((ceil(RRCP/RRCPE) + ceil(RPCD/RMIE) + RID + RPD + RED + REM) + ceil(NRCP/NRCPE) + ceil(NPCD/NME) + NID + NPD + NED + NEM)/5.0)

    qty = max(qty1, qty2, qty3)
    return part, memBlockPart, qty


def getPart_CCPCNT_TurboM_Qty(Product):
    expRelease = Product.Attr("Experion_PKS_Software_Release").GetValue()
    controllerModuleType = Product.Attr("SerC_CG_C300_Controller_Module_Type").GetValue()
    x1=getFloat(Product.GetContainerByName('C300_TurboM_IOM_CG_Cont').Rows[0].GetColumnByName("Red_IOM").Value)
    y1=getFloat(Product.GetContainerByName('C300_TurboM_IOM_CG_Cont').Rows[1].GetColumnByName("Red_IOM").Value)
    z1=getFloat(Product.Attributes.GetByName("SerC_CG_Percent_Installed_Spare").GetValue())
    part = "CC-PCNT02"
    memBlockPart = "CC-SCMB02"
    if expRelease not in ("R510", "R511", "R520", "R530"):
        return part, memBlockPart, 0
    if controllerModuleType == "C300(PCNT05)" and expRelease in ["R520","R530"]:
        part = "CC-PCNT05"
        memBlockPart = "CC-SCMB05"

    totalIoLoad = 0
    f1sum=0
    f2sum=0
    for row in Product.GetContainerByName("Series_C_Remote_Groups_Cont").Rows:
        #Changes done by RDT (Ravika PUpneja)------> CCEECOMMBR-6593
    	f1=GS_Get_Set_AtvQty.getAtvQty(row.Product,"Series_C_RG_Part_Summary",'CC-TSV211')
    	f2=GS_Get_Set_AtvQty.getAtvQty(row.Product,"Series_C_RG_Part_Summary",'CC-TSP411')
    	f1sum=f1sum+f1
    	f2sum=f2sum+f2
	Trace.Write(f1sum)
	Trace.Write(f2sum)

    for row in Product.GetContainerByName("Series_C_Remote_Groups_Cont").Rows:
        if row["Total_IO_Load"] !="":
        	totalIoLoad += float(row["Total_IO_Load"])
        Trace.Write("totalIoLoad"+str(totalIoLoad))
    totalIoLoad += float(Product.Attr("C300_CG_Total_IO_Load").GetValue())
    qty1 = ceil(totalIoLoad / 12.0)

    partQty1 = (ceil(x1 * ( 1 + z1/100.0)))
    qty2 = ceil((partQty1+f1sum) / 8.0)

    partQty2 = (ceil(y1 * ( 1 + z1/100.0)))
    qty3 = ceil((partQty2+f2sum) / 8.0)

    qty4 = ceil(((partQty1+f1sum) + (partQty2+f2sum))/10.0)

    qty = max(qty1, qty2, qty3, qty4)
    return part, memBlockPart, qty

def getPgmEimQty(Product):
    nonRedPGM = getFloat(Product.Attr("SerC_Number_of_Profibus_DP_Slave_devices - Non_Red").GetValue())
    redPGM = getFloat(Product.Attr("SerC_Number_of_Profibus_DP_Slave_devices - Red").GetValue())
    noOfDevices = getFloat(Product.Attr("SerC_Number_of_Devices_per_Profibus_Network (0-32)").GetValue())

    NRCP = getFloat(Product.Attr("SerC_Number_of_Rockwell_ControlLogix_Processors").GetValue())
    NRCPE = getFloat(Product.Attr("SerC_Number of Rockwell Control Processors(NON)").GetValue())
    NPCD = getFloat(Product.Attr("SerC_Number of Process Connected I/O Devices 1").GetValue())
    NME = getFloat(Product.Attr("SerC_Number of Motor Starter IOMs per EIM 255").GetValue())
    RRCP = getFloat(Product.Attr("SerC_NO of Rock Ctrl Processors Redundant0-999NEW").GetValue())
    RRCPE = getFloat(Product.Attr("SerC_Numbe of Rockwelix Proc EIM Redundant 0-10").GetValue())
    RPCD = getFloat(Product.Attr("SerC_Nu of Proc Conn I/O Devi (Redundant ) (0-999)").GetValue())
    RMIE = getFloat(Product.Attr("SerC_Number of Motor Start IOMs per EIM Redun 255").GetValue())
    NID = getFloat(Product.Attr("SerC_Number of Non Redundant EIM for IEC61850").GetValue())
    RID = getFloat(Product.Attr("SerC_Number of Redundant EIM for IEC61850").GetValue())
    NPD = getFloat(Product.Attr("SerC_Number of Non Redund EIM for Profinet Devices").GetValue())
    RPD = getFloat(Product.Attr("SerC_Number of Redundant EIM for Profinet Devices").GetValue())
    NED = getFloat(Product.Attr("SerC_Number of Non Redundant EIM for EIP Device").GetValue())
    RED = getFloat(Product.Attr("SerC_Number of Redunt EIM for EIP Devices (0-300)").GetValue())
    pgm = eim = 0
    A1 = A2 = 0
    if noOfDevices > 0:
    	pgm = ceil(ceil(redPGM/noOfDevices)/2)
    if RRCPE > 0:
        A1 += ceil(RRCP/RRCPE)
    if RMIE > 0:
        A2 +=  ceil(RPCD/RMIE)
    eim = A1 + A2 + RID + RPD + RED
    return int(pgm + eim)