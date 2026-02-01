import System.Decimal as D
import GS_SMPartsCalc
def addParts(parts, qty, desc, parts_dict):
    if parts != '' and qty > 0:
        parts_dict[parts] = {'Quantity' : qty, 'Description': desc}
    return parts_dict
#parts_dict={}

def getCGParts(FC_PDIO01,FC_PUIO01,TDOL,GPCS, Product, parts_dict):
    distance = switchIOLink = remoteLocation = extendedTemperature  =  conformallyCoated = ''
    if Product.Name in ["SM Control Group", "R2Q SM Control Group"]:
        try:
            Controller_Architecture = Product.GetContainerByName("SM_CG_Common_Questions_Cont").Rows[0].GetColumnByName("SM_SCController_Architecture").DisplayValue
        except Exception as e:
            Trace.Write("Module: sm_part_add_calcs Error:".format(str(e)))
        try:
            SIC_length= Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('SIC_Length').DisplayValue
        except Exception as e:
            Trace.Write("Module: sm_part_add_calcs Error:".format(str(e)))
        try:
            #UI question - Switch for Safety IO Link
            commonQnRow = Product.GetContainerByName('SM_CG_Common_Questions_Cont').Rows[0]
            switchIOLink = commonQnRow.GetColumnByName('SM_Switch_Safety_IO').DisplayValue
        except Exception as e:
            Trace.Write("Module: sm_part_add_calcs Error:".format(str(e)))

        #Total No of SM Remote group products added under the SM Control group product
        remoteLocation = Product.GetContainerByName('SM_RemoteGroup_Cont').Rows.Count
        if switchIOLink == 'Third Party MOXA':
            qty = 0
            #CXCPQ-31733
            parts = desc = ''
            qty = 1 if remoteLocation > 2 else 0
            if qty > 0:
                parts = 'FS-CCI-HSE-08'
                desc = 'SM RIO ETHERNET CABLE SET L=0.8M'
                parts_dict = addParts(parts, qty, desc, parts_dict)
            X=int(FC_PDIO01) + int(FC_PUIO01)
            Y = 0
            if Controller_Architecture =='Redundant':
                Y = 1
            if Controller_Architecture =='Redundant A.R.T+':
                Y = 2
            A = int(X) + int(Y)
            if A > 0 and parts_dict.get("FC-TCNT11") and float(parts_dict.get("FC-TCNT11")['Quantity']) > 0:
                qty = A
                parts = 'FS-CCI-HSE-30'
                desc = 'SM RIO ETHERNET CABLE SET L=3.0M'
                parts_dict = addParts(parts, qty, desc, parts_dict)

        if TDOL >0 or GPCS >0:
            Trace.Write("GPCS"+ str(GPCS))
            Trace.Write("TDOL"+ str(TDOL))
            TDOL1 = D.Ceiling(TDOL + GPCS)
            Trace.Write("TDOL1 : " + str(TDOL1))
            qty = TDOL1
            if SIC_length =="1M":
                parts="FC-SIC9010"
                desc ="SC SIC CABLE FTA OR THIRD PARTY L1M"
            elif SIC_length =="2M":
                parts="FC-SIC9020"
                desc ="SC SIC CABLE FTA OR THIRD PARTY L2M"
            elif SIC_length =="3M":
                parts="FC-SIC9030"
                desc ="SC SIC CABLE FTA OR THIRD PARTY L3M"
            elif SIC_length =="4M":
                parts="FC-SIC9040"
                desc ="SC SIC CABLE FTA OR THIRD PARTY L4M"
            elif SIC_length =="5M":
                parts="FC-SIC9050"
                desc ="SC SIC CABLE FTA OR THIRD PARTY L5M"
            elif SIC_length =="6M":
                parts="FC-SIC9060"
                desc ="SC SIC CABLE FTA OR THIRD PARTY L6M"
            elif SIC_length =="10M":
                parts="FC-SIC9100"
                desc ="SC SIC CABLE FTA OR THIRD PARTY L10M"
            elif SIC_length =="15M":
                parts="FC-SIC9150"
                desc ="SC SIC CABLE FTA OR THIRD PARTY L15M"
            elif SIC_length =="20M":
                parts="FC-SIC9200"
                desc ="SC SIC CABLE FTA OR THIRD PARTY L20M"
            elif SIC_length =="25M":
                parts="FC-SIC9250"
                desc ="SC SIC CABLE FTA OR THIRD PARTY L25M"
            elif SIC_length =="30M":
                parts="FC-SIC9300"
                desc ="SC SIC CABLE FTA OR THIRD PARTY L30M"
            parts_dict = addParts(parts, qty, desc, parts_dict)
    
    if Product.Name=="SM Remote Group":
        Enclosure_Type =Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0].GetColumnByName('Enclosure_Type').DisplayValue
        if Enclosure_Type== "Cabinet":
            if TDOL >0 or GPCS >0:
                TDOL1 = D.Ceiling(TDOL + GPCS)
                qty = TDOL1
                try:
                    SIC_length= Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('SIC_Length').DisplayValue
                except Exception as e:
                    Trace.Write("Module: sm_part_add_calcs Error:".format(str(e)))
                if SIC_length =="1M":
                    parts="FC-SIC9010"
                    desc ="SC SIC CABLE FTA OR THIRD PARTY L1M"
                elif SIC_length =="2M":
                    parts="FC-SIC9020"
                    desc ="SC SIC CABLE FTA OR THIRD PARTY L2M"
                elif SIC_length =="3M":
                    parts="FC-SIC9030"
                    desc ="SC SIC CABLE FTA OR THIRD PARTY L3M"
                elif SIC_length =="4M":
                    parts="FC-SIC9040"
                    desc ="SC SIC CABLE FTA OR THIRD PARTY L4M"
                elif SIC_length =="5M":
                    parts="FC-SIC9050"
                    desc ="SC SIC CABLE FTA OR THIRD PARTY L5M"
                elif SIC_length =="6M":
                    parts="FC-SIC9060"
                    desc ="SC SIC CABLE FTA OR THIRD PARTY L6M"
                elif SIC_length =="10M":
                    parts="FC-SIC9100"
                    desc ="SC SIC CABLE FTA OR THIRD PARTY L10M"
                elif SIC_length =="15M":
                    parts="FC-SIC9150"
                    desc ="SC SIC CABLE FTA OR THIRD PARTY L15M"
                elif SIC_length =="20M":
                    parts="FC-SIC9200"
                    desc ="SC SIC CABLE FTA OR THIRD PARTY L20M"
                elif SIC_length =="25M":
                    parts="FC-SIC9250"
                    desc ="SC SIC CABLE FTA OR THIRD PARTY L25M"
                elif SIC_length =="30M":
                    parts="FC-SIC9300"
                    desc ="SC SIC CABLE FTA OR THIRD PARTY L30M"
                parts_dict = addParts(parts, qty, desc, parts_dict)
    if GPCS >0:
         qty = GPCS
         #CXCPQ-31700
         parts = desc = ''
         parts = 'FC-GPCS-RIO16-PF'
         desc = 'P+F RUSIO universal term. board, 16ch'
         parts_dict = addParts(parts, qty, desc, parts_dict)
    return parts_dict

#CXCPQ-31855 added by Lahu
def get_parts3(Product,parts_dict):
    if Product.Name in ["SM Control Group", "R2Q SM Control Group"]:
        iota = Product.GetContainerByName("SM_CG_Common_Questions_Cont").Rows[0].GetColumnByName("SM_Universal_IOTA")
        marshaling = Product.GetContainerByName("SM_CG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Marshalling_Option")
        digout = Product.GetContainerByName("SM_IO_Count_Digital_Output_Cont")
        for row in digout.Rows:
            if row["Digital Output Type"] == "SDO(16) SIL 2/3 250Vac/Vdc COM UIO (0-5000)":
                var1 = row["Red (NIS)"] if row["Red (NIS)"] != "" else 0
                var2 = row["Non Red (NIS)"] if row["Non Red (NIS)"] != "" else 0
        if iota.Value == "RUSIO" and marshaling.Value == "Hardware_Marshalling_with_Other":
            var = 2 * (D.Ceiling(float(var1)/16)) + 2 * (D.Ceiling(float(var2)/16))
            if var >0:
                parts_dict["FC-TSRO-08UNI"] = {"Quantity" : int(var), "Description" : "DO(relay) FTA for SIL3 appl. 8ch CC"}
    elif Product.Name=="SM Remote Group":
        iota = Product.Attr("SM_Universal_IOTA_Type").GetValue()
        Enclosure_Type =Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0].GetColumnByName('Enclosure_Type').DisplayValue
        if Enclosure_Type== "Cabinet":
            marshaling = Product.GetContainerByName("SM_RG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Marshalling_Option")
            digout = Product.GetContainerByName("SM_RG_IO_Count_Digital_Output_Cont")
            for row in digout.Rows:
                if row["Digital_Output_Type"] == "SDO(16) SIL 2/3 250Vac/Vdc COM UIO  (0-5000)":
                    var1 = row["Red_NIS"] if row["Red_NIS"] != "" else 0
                    var2 = row["Non_Red_NIS"] if row["Non_Red_NIS"] != "" else 0
            if iota == "RUSIO" and marshaling.Value == "Hardware_Marshalling_with_Other":
                var = 2 * (D.Ceiling(float(var1)/16)) + 2 * (D.Ceiling(float(var2)/16))
                if var >0:
                    parts_dict["FC-TSRO-08UNI"] = {"Quantity" : int(var), "Description" : "DO(relay) FTA for SIL3 appl. 8ch CC"}
    return parts_dict
def FC_MCAR_02(FC_TUIO11,FC_TDIO11,TCNT11,Product,parts_dict):
    if Product.Name in ["SM Control Group", "R2Q SM Control Group"]:
        iota = Product.GetContainerByName("SM_CG_Common_Questions_Cont").Rows[0].GetColumnByName("SM_Universal_IOTA")
        Cabinet_Access = Product.GetContainerByName("SM_CG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Cabinet_Access")
        if iota.Value == "PUIO": #and Cabinet_Access.Value == "Dual_Access":
            var = (D.Ceiling((FC_TUIO11)/3.0)) + (D.Ceiling((FC_TDIO11)/3.0))+ (D.Ceiling((TCNT11)/2.0))
            if var >0:
                parts_dict["FC-MCAR-02"] = {"Quantity" : int(var), "Description" : "SM RIO 36 inch carrier"}
        return parts_dict
    elif Product.Name=="SM Remote Group":
        iota = Product.Attr("SM_Universal_IOTA_Type").GetValue()
        Cabinet_Access = Product.GetContainerByName("SM_RG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Cabinet_Access")
        Enclosure_Type =Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0].GetColumnByName('Enclosure_Type').DisplayValue
        if Enclosure_Type== "Cabinet":
            if iota == "PUIO": #and Cabinet_Access.Value == "Dual_Access":
                var = (D.Ceiling((FC_TUIO11)/3.0)) + (D.Ceiling((FC_TDIO11)/3.0))
                if var >0:
                    parts_dict["FC-MCAR-02"] = {"Quantity" : int(var), "Description" : "SM RIO 36 inch carrier"}
        return parts_dict
def cabinet_part(Product,parts_dict):
    if Product.Name in ["SM Control Group", "R2Q SM Control Group"]:
        iota = Product.GetContainerByName("SM_CG_Common_Questions_Cont").Rows[0].GetColumnByName("SM_Universal_IOTA")
        Cabinet_Access = Product.GetContainerByName("SM_CG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Cabinet_Access")
        Cabinet_Light = Product.GetContainerByName("SM_CG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Cabinet_Light")
        cab_qnt,powerSupply,switches=GS_SMPartsCalc.getNumberOfCGCabinet(Product)
        var = cab_qnt
        Trace.Write(cab_qnt)
        Trace.Write(powerSupply)
        Trace.Write(switches)
        if iota.Value == "PUIO" and Cabinet_Access.Value == "Dual_Access":
            if var >0:
                # CXCPQ-32300 and CXCPQ-32329 and CXCPQ-32166
                parts_dict["FS-MB-0002"] = {"Quantity" : int(var), "Description" : "Power busbar max.200A 24/48/110Vdc, 60cm"}
                parts_dict["FS-PDC-MB24-1P"] = {"Quantity" : int(var), "Description" : "POWER DISTR.CABLE MB-0001 TO PDB-0824 LS"}
                parts_dict["FS-BCU-0036"] = {"Quantity" : int(var), "Description" : "Rittal TS8808211 fdl/rdr/pl RAL7035"}
                #CXCPQ-32326
                if powerSupply >0 or switches >0:
                    var1 = D.Ceiling(switches/6.0)
                    var2 =D.Ceiling(powerSupply/4.0)
                    var= max(var1,var2)
                    parts_dict["FC-PDB-0824P"] = {"Quantity" : int(var), "Description" : "Power distr.board 8ch.24Vdc 2A CC"}
        # CXCPQ-32352 
        var = cab_qnt
        if iota.Value == "RUSIO" and Cabinet_Access.Value != "Dual_Access" and var >0:
            parts_dict["FS-BCU-0038"] = {"Quantity" : int(var), "Description" : "Rittal TS8804210 FDR/PL RAL7035"}
        #Shivani
        if iota.Value == "RUSIO" and Cabinet_Access.Value != "Dual_Access" and var >0:
            parts_dict["FC-FANWR-24R"] = {"Quantity" : int(var), "Description" : "24Vdc fan unit with readback CC"}
            #parts_dict["SZ 4155.110"] = {"Quantity" : 2*(int(var)), "Description" : "RITTAL CAB. LIGHT 110/240V+SENSOR+OUTLET"}
        if iota.Value == "RUSIO" and Cabinet_Access.Value == "Dual_Access" and var >0:
            parts_dict["FS-BCU-0036"] = {"Quantity" : int(var), "Description" : "Rittal TS8808211 fdl/rdr/pl RAL7035"}
            parts_dict["FC-FANWR-24R"] = {"Quantity" : int(var), "Description" : "24Vdc fan unit with readback CC"}
        if iota.Value == "RUSIO" and Cabinet_Access.Value == "Dual_Access" and Cabinet_Light.Value == "Yes" and var >0:
            parts_dict["SZ 4155.110"] = {"Quantity" : 2*(int(var)), "Description" : "RITTAL CAB. LIGHT 110/240V+SENSOR+OUTLET"}

        if iota.Value == "RUSIO" and Cabinet_Access.Value == "Dual_Access" and var >0:
            #  CXCPQ-32229
            parts_dict["FS-PDC-MB24-1P"] = {"Quantity" : int(var), "Description" : "POWER DISTR.CABLE MB-0001 TO PDB-0824 LS"}
            #CXCPQ-33228
            if powerSupply >0 or switches >0:
                var1 = D.Ceiling(switches/6.0)
                var2 =D.Ceiling(powerSupply/4.0)
                var= max(var1,var2)
                parts_dict["FC-PDB-0824P"] = {"Quantity" : int(var), "Description" : "Power distr.board 8ch.24Vdc 2A CC"}
        #Trace.Write(parts_dict)
    elif Product.Name=="SM Remote Group":
        iota = Product.Attr("SM_Universal_IOTA_Type").GetValue()
        Cabinet_Access = Product.GetContainerByName("SM_RG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Cabinet_Access")
        Cabinet_Light = Product.GetContainerByName("SM_RG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Cabinet_Light")
        cab_qnt, powerSupply, switches = GS_SMPartsCalc.getNumberOfRGCabinet(Product)
        var = cab_qnt
        Enclosure_Type =Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0].GetColumnByName('Enclosure_Type').DisplayValue
        if Enclosure_Type== "Cabinet":
            if iota == "PUIO" and Cabinet_Access.Value == "Dual_Access":
                if var >0:
                    # CXCPQ-32300 and CXCPQ-32329
                    Trace.Write("cab_qnt : "+str(cab_qnt))
                    parts_dict["FS-MB-0002"] = {"Quantity" : int(var), "Description" : "Power busbar max.200A 24/48/110Vdc, 60cm"}
                    parts_dict["FS-PDC-MB24-1P"] = {"Quantity" : int(var), "Description" : "POWER DISTR.CABLE MB-0001 TO PDB-0824 LS"}
                    parts_dict["FS-BCU-0036"] = {"Quantity" : int(var), "Description" : "Rittal TS8808211 fdl/rdr/pl RAL7035"}
                    #CXCPQ-32326
                    if powerSupply >0 or switches >0 or var>0:
                        var1 = D.Ceiling(switches/6.0)
                        var2 =D.Ceiling(powerSupply/4.0)
                        var= max(var1,var2)
                        parts_dict["FC-PDB-0824P"] = {"Quantity" : int(var), "Description" : "Power distr.board 8ch.24Vdc 2A CC"}
            var = cab_qnt
            if iota == "RUSIO" and Cabinet_Access.Value != "Dual_Access" and var >0:
                parts_dict["FS-BCU-0038"] = {"Quantity" : int(var), "Description" : "Rittal TS8804210 FDR/PL RAL7035"}
            #Shivani
            if iota == "RUSIO" and Cabinet_Access.Value != "Dual_Access" and var >0:
                parts_dict["FC-FANWR-24R"] = {"Quantity" : int(var), "Description" : "24Vdc fan unit with readback CC"}
                #parts_dict["SZ 4155.110"] = {"Quantity" : 2*(int(var)), "Description" : "RITTAL CAB. LIGHT 110/240V+SENSOR+OUTLET"}
            if iota == "RUSIO" and Cabinet_Access.Value == "Dual_Access" and var >0:
                parts_dict["FS-BCU-0036"] = {"Quantity" : int(var), "Description" : "Rittal TS8808211 fdl/rdr/pl RAL7035"}
                parts_dict["FC-FANWR-24R"] = {"Quantity" : int(var), "Description" : "24Vdc fan unit with readback CC"}
            if iota == "RUSIO" and Cabinet_Access.Value == "Dual_Access" and Cabinet_Light.Value == "Yes" and var >0:
                parts_dict["SZ 4155.110"] = {"Quantity" : 2*(int(var)), "Description" : "RITTAL CAB. LIGHT 110/240V+SENSOR+OUTLET"}

            if iota == "RUSIO" and Cabinet_Access.Value == "Dual_Access" and var >0:
                # CXCPQ-32352 and CXCPQ-32229
                parts_dict["FS-PDC-MB24-1P"] = {"Quantity" : int(var), "Description" : "POWER DISTR.CABLE MB-0001 TO PDB-0824 LS"}
                #CXCPQ-33228
                if powerSupply >0 or switches >0:
                    var1 = D.Ceiling(switches/6.0)
                    var2 =D.Ceiling(powerSupply/4.0)
                    var= max(var1,var2)
                    parts_dict["FC-PDB-0824P"] = {"Quantity" : int(var), "Description" : "Power distr.board 8ch.24Vdc 2A CC"}
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

def filler_plate(Product,parts_dict):
    if Product.Name in ["SM Control Group", "R2Q SM Control Group"]:
        PUIO=MCAR=S300=switch=PDIO=RUSIO_iotaNR= 0
        partsQty = []
        contParts = Product.GetContainerByName('SM_CG_PartSummary_Cont')
        iota = Product.GetContainerByName("SM_CG_Common_Questions_Cont").Rows[0].GetColumnByName("SM_Universal_IOTA")
        Cabinet_Access = Product.GetContainerByName("SM_CG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Cabinet_Access")
        MCAR_Filler=Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName('MCAR_Blank_Filler').DisplayValue
        partsQty = getPartsQty(contParts)
        PUIO = getQty(partsQty, 'FC-TUIO11')
        PDIO = getQty(partsQty, 'FC-TDIO11')
        RUSIO_iotaNR =getQty(partsQty, 'FC-IOTA-NR24')
        RUSIO_iotaR =getQty(partsQty, 'FC-IOTA-R24')
        MCAR = getQty(partsQty, 'FC-MCAR-02')
        S300 = getQty(partsQty, 'FC-TCNT11')
        switch = getQty(partsQty, 'FC-SSWM01')
        if iota.Value == "PUIO" and Cabinet_Access.Value == "Dual_Access" and MCAR_Filler=="Yes":
            Qnt = (MCAR *36)-((S300 *18)+(PUIO * 12)+(PDIO * 12)+(switch * 3))
            Qnt = D.Ceiling(Qnt/3.0)
            if Qnt >0:
                parts_dict["CC-MCC003"] = {"Quantity" : int(Qnt), "Description" : "CARRIER COVER, IOTA"}
        elif iota.Value == "RUSIO" and Cabinet_Access.Value == "Dual_Access" and MCAR_Filler=="Yes":
            Qnt = (MCAR *36)-((S300 *18)+(PUIO * 12)+(switch * 3)+(PDIO *12)+(RUSIO_iotaNR * 12)+(RUSIO_iotaR * 18))
            Qnt = D.Ceiling(Qnt/3.0)
            if Qnt >0:
                parts_dict["CC-MCC003"] = {"Quantity" : int(Qnt), "Description" : "CARRIER COVER, IOTA"}
        elif iota.Value == "PUIO" and Cabinet_Access.Value != "Dual_Access" and MCAR_Filler=="Yes":
            Qnt = (MCAR *36)-((S300 *18)+(PUIO * 12)+(PDIO * 12)+(switch * 3))
            Qnt = D.Ceiling(Qnt/3.0)
            if Qnt >0:
                parts_dict["CC-MCC003"] = {"Quantity" : int(Qnt), "Description" : "CARRIER COVER, IOTA"}
        elif iota.Value == "RUSIO" and Cabinet_Access.Value != "Dual_Access" and MCAR_Filler=="Yes":
            Qnt = (MCAR *36)-((S300 *18)+(PUIO * 12)+(switch * 3)+(PDIO *12)+(RUSIO_iotaNR * 12)+(RUSIO_iotaR * 18))
            Qnt = D.Ceiling(Qnt/3.0)
            if Qnt >0:
                parts_dict["CC-MCC003"] = {"Quantity" : int(Qnt), "Description" : "CARRIER COVER, IOTA"}

    elif Product.Name=="SM Remote Group":
        PUIO=MCAR=S300=switch= 0
        partsQty = []
        contParts = Product.GetContainerByName('SM_RG_PartSummary_Cont')
        iota = Product.Attr("SM_Universal_IOTA_Type").GetValue()
        partsQty = getPartsQty(contParts)
        PUIO = getQty(partsQty, 'FC-TUIO11')
        PDIO = getQty(partsQty, 'FC-TDIO11')
        RUSIO_iotaNR =getQty(partsQty, 'FC-IOTA-NR24')
        RUSIO_iotaR =getQty(partsQty, 'FC-IOTA-R24')
        MCAR = getQty(partsQty, 'FC-MCAR-02')
        S300 = getQty(partsQty, 'FC-TCNT11')
        switch = getQty(partsQty, 'FC-SSWM01')
        Cabinet_Access = Product.GetContainerByName("SM_RG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Cabinet_Access")
        Enclosure_Type =Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0].GetColumnByName('Enclosure_Type').DisplayValue
        MCAR_Filler=Product.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName('SM_MCAR_Blank_Filler').DisplayValue
        if Enclosure_Type== "Cabinet":
            if iota == "PUIO" and Cabinet_Access.Value == "Dual_Access" and MCAR_Filler=="Yes":
                Qnt = (MCAR *36)-((S300 *18)+(PUIO * 12)+(PDIO * 12)+(switch * 3))
                Qnt = D.Ceiling(Qnt/3.0)
                if Qnt >0:
                    parts_dict["CC-MCC003"] = {"Quantity" : int(Qnt), "Description" : "CARRIER COVER, IOTA"}
            elif iota == "RUSIO" and Cabinet_Access.Value == "Dual_Access" and MCAR_Filler=="Yes":
                Qnt = (MCAR *36)-((S300 *18)+(PUIO * 12)+(switch * 3)+(PDIO *12)+(RUSIO_iotaNR * 12)+(RUSIO_iotaR * 18))
                Qnt = D.Ceiling(Qnt/3.0)
                if Qnt >0:
                    parts_dict["CC-MCC003"] = {"Quantity" : int(Qnt), "Description" : "CARRIER COVER, IOTA"}
            elif iota == "PUIO" and Cabinet_Access.Value != "Dual_Access" and MCAR_Filler=="Yes":
                Qnt =  (MCAR *36)-((S300 *18)+(PUIO * 12)+(PDIO * 12)+(switch * 3))
                Qnt = D.Ceiling(Qnt/3.0)
                if Qnt >0:
                    parts_dict["CC-MCC003"] = {"Quantity" : int(Qnt), "Description" : "CARRIER COVER, IOTA"}
            elif iota == "RUSIO" and Cabinet_Access.Value != "Dual_Access" and MCAR_Filler=="Yes":
                Qnt = (MCAR *36)-((S300 *18)+(PUIO * 12)+(switch * 3)+(PDIO *12)+(RUSIO_iotaNR * 12)+(RUSIO_iotaR * 18))
                Qnt = D.Ceiling(Qnt/3.0)
                if Qnt >0:
                    parts_dict["CC-MCC003"] = {"Quantity" : int(Qnt), "Description" : "CARRIER COVER, IOTA"}
    return parts_dict
#Trace.Write(cabinet_part(Product,parts_dict))