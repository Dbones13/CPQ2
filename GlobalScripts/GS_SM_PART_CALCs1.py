#from GS_SMPartsCalc import getHardwiredMarshallingParts
#from GS_SMPartsCalc1 import get_parts
import System.Decimal as D
#parts_dict={}
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
def Get_Sic_length(Product):
    qty1 =0
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
        Trace.Write("Prabhat "+str(qty1))
    
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
        Trace.Write("qty1rg"+str(qty1))
    return qty1
def Get_Parts(Product,parts_dict):
    qty5 =Get_Sic_length(Product)
    Trace.Write("qty5 "+str(qty5))
    qty4 =qty3= 0 
    if Product.Name in ["SM Control Group", "R2Q SM Control Group"]:
        iota = Product.GetContainerByName("SM_CG_Common_Questions_Cont").Rows[0].GetColumnByName("SM_Universal_IOTA")
        marshaling = Product.GetContainerByName("SM_CG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Marshalling_Option")
        digout = Product.GetContainerByName("SM_IO_Count_Digital_Output_Cont")
        var1 = var2 = var3 = var4 = 0
        for row in digout.Rows:
            if row["Digital Output Type"] == "SDO(16) SIL 2/3 250Vac/Vdc COM UIO (0-5000)":
                var1 = row["Red (NIS)"] if row["Red (NIS)"] != "" else 0
                var2 = row["Non Red (NIS)"] if row["Non Red (NIS)"] != "" else 0
            elif row["Digital Output Type"] == "SDO(16) SIL 2/3 250Vac/Vdc COM DIO (0-5000)":
                var3 = row["Red (NIS)"] if row["Red (NIS)"] != "" else 0
                var4 = row["Non Red (NIS)"] if row["Non Red (NIS)"] != "" else 0
            qty4 = (2 *(D.Ceiling(float(var1)/16))) + (2*(D.Ceiling(float(var2)/16))) +(2*(D.Ceiling(float(var3)/16))) + (2*(D.Ceiling(float(var4)/16)))
            if row["Digital Output Type"] == "SDO(16) SIL 2/3 250Vac/Vdc UIO (0-5000)":
                var5 = row["Red (NIS)"] if row["Red (NIS)"] != "" else 0
                var6 = row["Non Red (NIS)"] if row["Non Red (NIS)"] != "" else 0
            elif row["Digital Output Type"] == "SDO(16) SIL 2/3 250Vac/Vdc DIO (0-5000)":
                var7 = row["Red (NIS)"] if row["Red (NIS)"] != "" else 0
                var8 = row["Non Red (NIS)"] if row["Non Red (NIS)"] != "" else 0
                qty3= (2*D.Ceiling(float(var5)/16)) + (2*D.Ceiling(float(var6)/16)) + (2*D.Ceiling(float(var7)/16)) +(2*D.Ceiling(float(var8)/16))
    elif Product.Name == "SM Remote Group":
        iota = Product.Attr("SM_Universal_IOTA_Type").GetValue()
        marshaling = Product.GetContainerByName("SM_RG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Marshalling_Option")
        digout = Product.GetContainerByName("SM_RG_IO_Count_Digital_Output_Cont")
        var1 = var2 = var3 = var4 = 0
        for row in digout.Rows:
            if row["Digital_Output_Type"] == "SDO(16) SIL 2/3 250Vac/Vdc COM UIO  (0-5000)":
                var1 = row["Red_NIS"] if row["Red_NIS"] != "" else 0
                var2 = row["Non_Red_NIS"] if row["Non_Red_NIS"] != "" else 0
            elif row["Digital_Output_Type"] == "SDO(16) SIL 2/3 250Vac/Vdc COM DIO  (0-5000)":
                var3 = row["Red_NIS"] if row["Red_NIS"] != "" else 0
                var4 = row["Non_Red_NIS"] if row["Non_Red_NIS"] != "" else 0
            qty4 = (2 *(D.Ceiling(float(var1)/16))) + (2*(D.Ceiling(float(var2)/16))) +(2*(D.Ceiling(float(var3)/16))) + (2*(D.Ceiling(float(var4)/16)))
            if row["Digital_Output_Type"] == "SDO(16) SIL 2/3 250Vac/Vdc UIO   (0-5000)":
                var5 = row["Red_NIS"] if row["Red_NIS"] != "" else 0
                var6 = row["Non_Red_NIS"] if row["Non_Red_NIS"] != "" else 0
            elif row["Digital_Output_Type"] == "SDO(16) SIL 2/3 250Vac/Vdc DIO  (0-5000)":
                var7 = row["Red_NIS"] if row["Red_NIS"] != "" else 0
                var8 = row["Non_Red_NIS"] if row["Non_Red_NIS"] != "" else 0
                qty3= (2*D.Ceiling(float(var5)/16)) + (2*D.Ceiling(float(var6)/16)) + (2*D.Ceiling(float(var7)/16)) +(2*D.Ceiling(float(var8)/16))
    if Product.Name in ["SM Control Group", "R2Q SM Control Group"]:
        iota = Product.GetContainerByName("SM_CG_Common_Questions_Cont").Rows[0].GetColumnByName("SM_Universal_IOTA").DisplayValue
        marshaling = Product.GetContainerByName("SM_CG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Marshalling_Option").DisplayValue 
        sic_length = Product.GetContainerByName("SM_CG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("SIC_Length").DisplayValue
        Trace.Write("sic "+str(sic_length))
        Trace.Write("marshaling "+str(marshaling))
        Trace.Write("iota "+str(iota))

        qty =D.Ceiling((int(qty3)/2)+(int(qty4)/2))
        Trace.Write("qty "+str(qty))
        Total= qty+qty5
        Trace.Write("Total "+str(Total))

        if iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "1M":
            parts_dict["FC-SIC2010"] = {'Quantity' : int(Total),'Description': 'SC SIC CABLE 2XCONNECTOR L1M / SIC2010'}

        if iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "2M":
            parts_dict["FC-SIC2020"] = {'Quantity' : int(Total),'Description': 'SC SIC CABLE 2XCONNECTOR L2M / SIC2020'}

        if iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "3M":
            parts_dict["FC-SIC2030"] = {'Quantity' : int(Total),'Description': 'SC SIC CABLE 2XCONNECTOR L3M / SIC2030'}

        if iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "5M":
            parts_dict["FC-SIC2050"] = {'Quantity' : int(Total),'Description': 'SC SIC CABLE 2XCONNECTOR L5M / SIC2050'}

        if iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "6M":
            parts_dict["FC-SIC2060"] = {'Quantity' : int(Total),'Description': 'SC SIC CABLE 2XCONNECTOR L6M / SIC2060'}

        if iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "10M":
            parts_dict["FC-SIC2100"] = {'Quantity' : int(Total),'Description': 'SC SIC CABLE 2XCONNECTOR L10M / SIC2100'}

        if iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "15M":
            parts_dict["FC-SIC2150"] = {'Quantity' : int(Total),'Description': 'SC SIC CABLE 2XCONNECTOR L15M / SIC2150'}

        if iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "20M":
            parts_dict["FC-SIC2200"] = {'Quantity' : int(Total),'Description': 'SC SIC CABLE 2XCONNECTOR L20M / SIC2200'}

        if iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "25M":
            parts_dict["FC-SIC2250"] = {'Quantity' : int(Total),'Description': 'SC SIC CABLE 2XCONNECTOR L25M / SIC2250'}

        if iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "30M":
            parts_dict["FC-SIC2300"] = {'Quantity' : int(Total),'Description': 'SC SIC CABLE 2XCONNECTOR L30M / SIC2300'}


        return parts_dict

    elif Product.Name == "SM Remote Group":
        
        iota = Product.Attr("SM_Universal_IOTA_Type").GetValue()
        Enclosure_type = Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0].GetColumnByName('Enclosure_Type').DisplayValue
        marshaling = Product.GetContainerByName("SM_RG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Marshalling_Option").DisplayValue 
        sic_length = Product.GetContainerByName("SM_RG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("SIC_Length").DisplayValue
        Trace.Write("Enclosure_type "+str(Enclosure_type))
        Trace.Write("sic "+str(sic_length))
        Trace.Write("marshaling "+str(marshaling))
        Trace.Write("iota "+str(iota))

        qty =D.Ceiling((int(qty3)/2)+(int(qty4)/2))
        Trace.Write("qty "+str(qty))
        Total= qty+qty5
        Trace.Write("Total "+str(Total))

        if Enclosure_type == "Cabinet":
            if iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "1M":
                parts_dict["FC-SIC2010"] = {'Quantity' : int(Total),'Description': 'SC SIC CABLE 2XCONNECTOR L1M / SIC2010'}

            if iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "2M":
                parts_dict["FC-SIC2020"] = {'Quantity' : int(Total),'Description': 'SC SIC CABLE 2XCONNECTOR L2M / SIC2020'}

            if iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "3M":
                parts_dict["FC-SIC2030"] = {'Quantity' : int(Total),'Description': 'SC SIC CABLE 2XCONNECTOR L3M / SIC2030'}

            if iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "5M":
                parts_dict["FC-SIC2050"] = {'Quantity' : int(Total),'Description': 'SC SIC CABLE 2XCONNECTOR L5M / SIC2050'}

            if iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "6M":
                parts_dict["FC-SIC2060"] = {'Quantity' : int(Total),'Description': 'SC SIC CABLE 2XCONNECTOR L6M / SIC2060'}

            if iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "10M":
                parts_dict["FC-SIC2100"] = {'Quantity' : int(Total),'Description': 'SC SIC CABLE 2XCONNECTOR L10M / SIC2100'}

            if iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "15M":
                parts_dict["FC-SIC2150"] = {'Quantity' : int(Total),'Description': 'SC SIC CABLE 2XCONNECTOR L15M / SIC2150'}

            if iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "20M":
                parts_dict["FC-SIC2200"] = {'Quantity' : int(Total),'Description': 'SC SIC CABLE 2XCONNECTOR L20M / SIC2200'}

            if iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "25M":
                parts_dict["FC-SIC2250"] = {'Quantity' : int(Total),'Description': 'SC SIC CABLE 2XCONNECTOR L25M / SIC2250'}

            if iota == "PUIO" and marshaling == "Hardware Marshalling with Other" and sic_length == "30M":
                parts_dict["FC-SIC2300"] = {'Quantity' : int(Total),'Description': 'SC SIC CABLE 2XCONNECTOR L30M / SIC2300'}


        return parts_dict

#var=Get_Parts(Product,parts_dict)
#Trace.Write("parts1="+str(var))