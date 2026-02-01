import System.Decimal as D
#import sys
from GS_SM_Load_SM_RIO_cabinet_summary_Calc import Load_SM_RIO_cabinet_summary_CG_RG_Calc
def Roundup(n):
    Trace.Write(n)
    res= int(n)
    return res if res == n else res+1

def getNoPowerSupplies(Product,parts_dict,cabinet_calculated=False):
    Nos_PSU_Types = 0
    if Product.Name in ["SM Control Group", "R2Q SM Control Group"]:
        cabVolRow = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows[0]
        cabFeederVoltage = cabVolRow.GetColumnByName('Cabinet_Feeder_Voltage').DisplayValue
        cabPowSupRow = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows[0]
        cabPowerSupply = cabPowSupRow.GetColumnByName('Power_Supply').DisplayValue
        iota = Product.GetContainerByName("SM_CG_Common_Questions_Cont").Rows[0]
        iota1 = iota.GetColumnByName('SM_Universal_IOTA').DisplayValue
        if cabFeederVoltage != "Externally Sourced 24VDC":
            #Product.Messages.Add("Total Load : {} , cabinet calculated : {}".format(Load_SM_RIO_cabinet_summary_CG_RG_Calc(Product,parts_dict,cabinet_calculated), cabinet_calculated))
            Power_calculation_VA = Roundup(Load_SM_RIO_cabinet_summary_CG_RG_Calc(Product,parts_dict,cabinet_calculated)*24)
            Total_load_VA = float(Power_calculation_VA/.87)
            if cabPowerSupply == "Redundant":
                Nos_PSU_Types = 2*(Roundup(Total_load_VA/(24*24)))
            elif cabPowerSupply == "Non Redundant":
                Nos_PSU_Types = Roundup(Total_load_VA/(24*24))
    elif Product.Name == "SM Remote Group":
        cabVolRow = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0]
        cabFeederVoltage = cabVolRow.GetColumnByName('Cabinet_Feeder_Voltage').DisplayValue
        EnclosureType= Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0]
        EnclosureTypeValue = EnclosureType.GetColumnByName('Enclosure_Type').DisplayValue
        cabPowSupRow = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0]
        cabPowerSupply = cabPowSupRow.GetColumnByName('Power_Supply').DisplayValue
        iota1 = Product.Attr("SM_Universal_IOTA_Type").GetValue()
        if EnclosureTypeValue == "Cabinet" and cabFeederVoltage != "Externally Sourced 24VDC":
            #Product.Messages.Add("Total Load : {} , cabinet calculated : {}".format(Load_SM_RIO_cabinet_summary_CG_RG_Calc(Product,parts_dict,cabinet_calculated), cabinet_calculated))
            Power_calculation_VA = Roundup(Load_SM_RIO_cabinet_summary_CG_RG_Calc(Product,parts_dict,cabinet_calculated)*24)
            Total_load_VA = float(Power_calculation_VA/.87)
            if cabPowerSupply == "Redundant":
                Nos_PSU_Types = 2*(Roundup(Total_load_VA/(24*24)))
            elif cabPowerSupply == "Non Redundant":
                Nos_PSU_Types = Roundup(Total_load_VA/(24*24))
    return Nos_PSU_Types

# 31191 and 31192
def getPwrSupParts(Product, parts_dict, cabinet_calculated=False):
    try:
        qty = getNoPowerSupplies(Product, parts_dict, cabinet_calculated)
        if qty > 0:
            parts_dict["FC-PSUNI2424"] = {'Quantity' : qty, 'Description':  'PSU 115/230VAC,24VDC,24A,CUL,US,ATEX,FM'}
            #CCEECOMMBR-6976
            #parts_dict["5SY4210-7"] = {'Quantity' : qty, 'Description':  '10A, MCB for 230VAC'}
    except Exception,e:
        Trace.Write("Module: GS_SMPartsCalc.getPowerSupplyParts Error:".format(str(e)))
    return parts_dict

'''def getParts(Product, parts_dict):
    try:
        qty = getNoPowerSupplies(Product,parts_dict)
        if qty > 0:
            parts_dict["5SY4210-7"] = {'Quantity' : qty, 'Description':  '10A, MCB for 230VAC'}
    except Exception as e:
        Trace.Write("Module: GS_SMPartsCalc.getPowerSupplyParts Error:".format(str(e)))
    return parts_dict'''

def Get_Parts_Sic_length(Product,parts_dict):
    qty4 = 0 
    if Product.Name in ["SM Control Group", "R2Q SM Control Group"]:
        iota = Product.GetContainerByName("SM_CG_Common_Questions_Cont").Rows[0].GetColumnByName("SM_Universal_IOTA")
        marshaling = Product.GetContainerByName("SM_CG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Marshalling_Option")
        digout = Product.GetContainerByName("SM_IO_Count_Digital_Output_Cont")
        var1 = var2 = var3 = var4 = 0
        for row in digout.Rows:
            if row["Digital Output Type"] == "SDO(16) SIL 2/3 250Vac/Vdc UIO (0-5000)":
                var1 = row["Red (NIS)"] if row["Red (NIS)"] != "" else 0
                var2 = row["Non Red (NIS)"] if row["Non Red (NIS)"] != "" else 0
            elif row["Digital Output Type"] == "SDO(16) SIL 2/3 250Vac/Vdc COM UIO (0-5000)":
                var3 = row["Red (NIS)"] if row["Red (NIS)"] != "" else 0
                var4 = row["Non Red (NIS)"] if row["Non Red (NIS)"] != "" else 0
            qty4 = (2 *(D.Ceiling(float(var1)/16))) + (2*(D.Ceiling(float(var2)/16))) +(2*(D.Ceiling(float(var3)/16))) + (2*(D.Ceiling(float(var4)/16)))
    elif Product.Name == "SM Remote Group":
        iota = Product.Attr("SM_Universal_IOTA_Type").GetValue()
        marshaling = Product.GetContainerByName("SM_RG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Marshalling_Option")
        digout = Product.GetContainerByName("SM_RG_IO_Count_Digital_Output_Cont")
        var1 = var2 = var3 = var4 = 0
        for row in digout.Rows:
            if row["Digital_Output_Type"] == "SDO(16) SIL 2/3 250Vac/Vdc UIO   (0-5000)":
                var1 = row["Red_NIS"] if row["Red_NIS"] != "" else 0
                var2 = row["Non_Red_NIS"] if row["Non_Red_NIS"] != "" else 0
            elif row["Digital_Output_Type"] == "SDO(16) SIL 2/3 250Vac/Vdc COM UIO  (0-5000)":
                var3 = row["Red_NIS"] if row["Red_NIS"] != "" else 0
                var4 = row["Non_Red_NIS"] if row["Non_Red_NIS"] != "" else 0
            qty4 = (2 *(D.Ceiling(float(var1)/16))) + (2*(D.Ceiling(float(var2)/16))) +(2*(D.Ceiling(float(var3)/16))) + (2*(D.Ceiling(float(var4)/16)))
    if Product.Name in ["SM Control Group", "R2Q SM Control Group"]:
        iota = Product.GetContainerByName("SM_CG_Common_Questions_Cont").Rows[0].GetColumnByName("SM_Universal_IOTA").DisplayValue
        marshaling = Product.GetContainerByName("SM_CG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Marshalling_Option").DisplayValue 
        sic_length = Product.GetContainerByName("SM_CG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("SIC_Length").DisplayValue
        Trace.Write("sic "+str(sic_length))
        Trace.Write("marshaling "+str(marshaling))
        Trace.Write("iota "+str(iota))

        qty =D.Ceiling(int(qty4)/2)

        if iota == "RUSIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "2M":
            parts_dict["FS-SICC-2001/L3"] = {'Quantity' : int(qty),'Description': 'RUSIO SIC cable terminate on two FTA'}

        if iota == "RUSIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "3M":
            parts_dict["FS-SICC-2001/L3"] = {'Quantity' : int(qty),'Description': 'RUSIO SIC cable terminate on two FTA'}

        if iota == "RUSIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "5M":
            parts_dict["FS-SICC-2001/L5"] = {'Quantity' : int(qty),'Description': 'RUSIO SIC cable terminate on two FTA'}

        if iota == "RUSIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "6M":
            parts_dict["FS-SICC-2001/L6"] = {'Quantity' : int(qty),'Description': 'RUSIO SIC cable terminate on two FTA'}

        if iota == "RUSIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "10M":
            parts_dict["FS-SICC-2001/L10"] = {'Quantity' : int(qty),'Description': 'RUSIO SIC cable terminate on two FTA'}

        return parts_dict

    elif Product.Name == "SM Remote Group":
        iota = Product.Attr("SM_Universal_IOTA_Type").GetValue()
        marshaling = Product.GetContainerByName("SM_RG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Marshalling_Option").DisplayValue 
        sic_length = Product.GetContainerByName("SM_RG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("SIC_Length").DisplayValue
        EnclosureType= Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0]
        EnclosureTypeValue = EnclosureType.GetColumnByName('Enclosure_Type').DisplayValue
        Trace.Write("sic "+str(sic_length))
        Trace.Write("marshaling "+str(marshaling))
        Trace.Write("iota "+str(iota))

        qty =D.Ceiling(int(qty4)/2)

        if EnclosureTypeValue == "Cabinet" and iota == "RUSIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "2M":
            parts_dict["FS-SICC-2001/L3"] = {'Quantity' : int(qty),'Description': 'RUSIO SIC cable terminate on two FTA'}

        if EnclosureTypeValue == "Cabinet" and iota == "RUSIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "3M":
            parts_dict["FS-SICC-2001/L3"] = {'Quantity' : int(qty),'Description': 'RUSIO SIC cable terminate on two FTA'}

        if EnclosureTypeValue == "Cabinet" and iota == "RUSIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "5M":
            parts_dict["FS-SICC-2001/L5"] = {'Quantity' : int(qty),'Description': 'RUSIO SIC cable terminate on two FTA'}

        if EnclosureTypeValue == "Cabinet" and iota == "RUSIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "6M":
            parts_dict["FS-SICC-2001/L6"] = {'Quantity' : int(qty),'Description': 'RUSIO SIC cable terminate on two FTA'}

        if EnclosureTypeValue == "Cabinet" and iota == "RUSIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "10M":
            parts_dict["FS-SICC-2001/L10"] = {'Quantity' : int(qty),'Description': 'RUSIO SIC cable terminate on two FTA'}

        return parts_dict

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
def Get_Sic_length(Product,parts_dict):
    if Product.Name in ["SM Control Group", "R2Q SM Control Group"]:
        Trace.Write(Product.Name)
        TDIO52 =TUIO52= 0
        partsQty = []
        contParts = Product.GetContainerByName('SM_CG_PartSummary_Cont')
        partsQty = getPartsQty(contParts)
        TDIO52 = getQty(partsQty, 'FC-TDIO52')
        TUIO52 = getQty(partsQty, 'FC-TUIO52')
        Qnt = D.Ceiling(int(TDIO52) + int(TUIO52))
        Trace.Write("Qty"+str(Qnt))
        iota = Product.GetContainerByName("SM_CG_Common_Questions_Cont").Rows[0].GetColumnByName("SM_Universal_IOTA").DisplayValue
        marshaling = Product.GetContainerByName("SM_CG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Marshalling_Option").DisplayValue 
        sic_length = Product.GetContainerByName("SM_CG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("SIC_Length").DisplayValue
        Trace.Write("sic "+str(sic_length))
        Trace.Write("marshaling "+str(marshaling))
        Trace.Write("iota "+str(iota))

        qty1 =D.Ceiling(int(Qnt))

        if iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "25M":
            parts_dict["FC-SIC2250"] = {'Quantity' : int(qty1),'Description': 'SC SIC CABLE 2XCONNECTOR L25M / SIC2250'}

        if iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "20M":
            parts_dict["FC-SIC2200"] = {'Quantity' : int(qty1),'Description': 'SC SIC CABLE 2XCONNECTOR L20M/ SIC2200'}

        if iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "30M":
            parts_dict["FC-SIC2300"] = {'Quantity' : int(qty1),'Description': 'SC SIC CABLE 2XCONNECTOR L30M/ SIC2300'}

        if iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "3M":
            parts_dict["FC-SIC2030"] = {'Quantity' : int(qty1),'Description': 'SC SIC CABLE 2XCONNECTOR L3M / SIC2030'}

        if iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "2M":
            parts_dict["FC-SIC2020"] = {'Quantity' : int(qty1),'Description': 'SC SIC CABLE 2XCONNECTOR L2M / SIC2020'}

        if iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "6M":
            parts_dict["FC-SIC2060"] = {'Quantity' : int(qty1),'Description': 'SC SIC CABLE 2XCONNECTOR L6M / SIC2060'}

        if iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "5M":
            parts_dict["FC-SIC2050"] = {'Quantity' : int(qty1),'Description': 'SC SIC CABLE 2XCONNECTOR L5M/ SIC2050'}

        return parts_dict

    if Product.Name == "SM Remote Group":
        Trace.Write(Product.Name)
        TDIO52 =TUIO52= 0
        partsQty = []
        contParts = Product.GetContainerByName('SM_RG_PartSummary_Cont')
        partsQty = getPartsQty(contParts)
        TDIO52 = getQty(partsQty, 'FC-TDIO52')
        TUIO52 = getQty(partsQty, 'FC-TUIO52')
        Qnt = D.Ceiling(int(TDIO52) + int(TUIO52))
        Trace.Write("Qty"+str(Qnt))
        iota = Product.Attr("SM_Universal_IOTA_Type").GetValue()
        marshaling = Product.GetContainerByName("SM_RG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Marshalling_Option").DisplayValue 
        sic_length = Product.GetContainerByName("SM_RG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("SIC_Length").DisplayValue
        EnclosureType= Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0]
        EnclosureTypeValue = EnclosureType.GetColumnByName('Enclosure_Type').DisplayValue
        Trace.Write("sic "+str(sic_length))
        Trace.Write("marshaling "+str(marshaling))
        Trace.Write("iota "+str(iota))

        qty1 =D.Ceiling(int(Qnt))

        if EnclosureTypeValue == "Cabinet" and iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "25M":
            parts_dict["FC-SIC2250"] = {'Quantity' : int(qty1),'Description': 'SC SIC CABLE 2XCONNECTOR L25M / SIC2250'}

        if EnclosureTypeValue == "Cabinet" and iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "20M":
            parts_dict["FC-SIC2200"] = {'Quantity' : int(qty1),'Description': 'SC SIC CABLE 2XCONNECTOR L20M/ SIC2200'}

        if EnclosureTypeValue == "Cabinet" and iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "30M":
            parts_dict["FC-SIC2300"] = {'Quantity' : int(qty1),'Description': 'SC SIC CABLE 2XCONNECTOR L30M/ SIC2300'}

        if EnclosureTypeValue == "Cabinet" and iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "3M":
            parts_dict["FC-SIC2030"] = {'Quantity' : int(qty1),'Description': 'SC SIC CABLE 2XCONNECTOR L3M / SIC2030'}

        if EnclosureTypeValue == "Cabinet" and iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "2M":
            parts_dict["FC-SIC2020"] = {'Quantity' : int(qty1),'Description': 'SC SIC CABLE 2XCONNECTOR L2M / SIC2020'}

        if EnclosureTypeValue == "Cabinet" and iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "6M":
            parts_dict["FC-SIC2060"] = {'Quantity' : int(qty1),'Description': 'SC SIC CABLE 2XCONNECTOR L6M / SIC2060'}

        if EnclosureTypeValue == "Cabinet" and iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "5M":
            parts_dict["FC-SIC2050"] = {'Quantity' : int(qty1),'Description': 'SC SIC CABLE 2XCONNECTOR L5M/ SIC2050'}


        return parts_dict