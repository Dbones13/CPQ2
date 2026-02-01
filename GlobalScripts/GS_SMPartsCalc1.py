import System.Decimal as D
from math import ceil
from GS_SMPartsCalc import getNumberOfCGCabinet,getNumberOfRGCabinet



def get_parts(Product,parts_dict):
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

    if iota.Value == "PUIO" and marshaling.Value == "Hardware_Marshalling_with_Other":
    #if marshaling.Value == "Hardware_Marshalling_with_Other":
        var = 2 * (D.Ceiling(float(var1)/16) + D.Ceiling(float(var2)/16) + D.Ceiling(float(var3)/16) + D.Ceiling(float(var4)/16))
        if var>0:
            parts_dict["FC-TSRO-08UNI"] = {"Quantity" : int(var), "Description" : "DO(relay) FTA SIL3 common power 8ch CC / TSROUNI"}

    return parts_dict

def get_parts1(Product,parts_dict):
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

    if iota == "PUIO" and marshaling.Value == "Hardware_Marshalling_with_Other":
    #if marshaling.Value == "Hardware_Marshalling_with_Other":
        var = 2 * (D.Ceiling(float(var1)/16) + D.Ceiling(float(var2)/16) + D.Ceiling(float(var3)/16) + D.Ceiling(float(var4)/16))
        if var>0:
            parts_dict["FC-TSRO-08UNI"] = {"Quantity" : int(var), "Description" : "DO(relay) FTA SIL3 common power 8ch CC / TSROUNI"}

    return parts_dict

def cg_cabinet_access(Product,parts_dict):
    cabinet = powersupply = switches = 0
    iota = Product.GetContainerByName("SM_CG_Common_Questions_Cont").Rows[0].GetColumnByName("SM_Universal_IOTA").DisplayValue
    cab_acc = Product.GetContainerByName("SM_CG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Cabinet_Access").DisplayValue
    cab_light = Product.GetContainerByName("SM_CG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Cabinet_Light").DisplayValue

    cabinet, powersupply, switches = getNumberOfCGCabinet(Product)
    qty1 = cabinet
    if qty1 > 0:
        #CXCPQ 33064
        if iota == "PUIO" and cab_acc == "Single Access":
            parts_dict["FS-BCU-0038"] = {"Quantity" : int(qty1), "Description" : "Rittal TS8804210 FDR/PL RAL7035"}
        #CXCPQ 33068
        if iota == "PUIO" and cab_acc == "Single Access" and cab_light == "Yes":
            parts_dict["4140252"] = {"Quantity" : int(qty1), "Description" : "ABL SURSUM BREAKER 8A 2D8UM"}
        #CXCPQ 33069
        if iota == "PUIO" and cab_acc == "Single Access" and cab_light == "Yes":
            parts_dict["SZ 4315.150"] = {"Quantity" : int(qty1), "Description" : "RITTAL POWER CABLE 3M GREY"}
        #CXCPQ 33065
        if iota == "PUIO" and cab_acc == "Single Access":
            parts_dict["FC-FANWR-24R"] = {"Quantity" : int(qty1), "Description" : "24Vdc fan unit with readback CC"}
        #CXCPQ 33066
        if iota == "PUIO" and cab_acc == "Single Access" and cab_light == "Yes":
            parts_dict["SZ 4155.110"] = {"Quantity" : int(qty1), "Description" : "RITTAL CAB. LIGHT 110/240V+SENSOR+OUTLET"}
        #CXCPQ 33356
        if iota == "RUSIO" and cab_acc == "Single Access":
            parts_dict["FC-FANWR-24R"] = {"Quantity" : int(qty1), "Description" : "24Vdc fan unit with readback CC"}
        #CXCPQ 33362
        if iota == "RUSIO" and cab_acc == "Single Access" and cab_light == "Yes":
            parts_dict["4140252"] = {"Quantity" : int(qty1), "Description" : "ABL SURSUM BREAKER 8A 2D8UM"}
        #CXCPQ 33359
        if iota == "RUSIO" and cab_acc == "Single Access" and cab_light == "Yes":
            parts_dict["SZ 4155.110"] = {"Quantity" : int(qty1), "Description" : "RITTAL CAB. LIGHT 110/240V+SENSOR+OUTLET"}

        #CXCPQ-33223
        if iota == "RUSIO" and cab_acc != "Single Access" and cab_light == "Yes":
            parts_dict["SZ 4315.150"] = {"Quantity" : int(qty1) * 2, "Description" : "RITTAL POWER CABLE 3M GREY"}


        #CXCPQ-33222
        if iota == "RUSIO" and cab_acc != "Single Access" and cab_light == "Yes":
            parts_dict["4140252"] = {"Quantity" : int(qty1) * 2, "Description" : "ABL SURSUM BREAKER 8A 2D8UM"}
    return parts_dict


def rg_cabinet_access(Product,parts_dict):
    cabinet = powersupply = switches = 0
    enclosure = Product.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue
    iota = Product.Attr("SM_Universal_IOTA_Type").GetValue()
    cab_acc = Product.GetContainerByName("SM_RG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Cabinet_Access").DisplayValue
    cab_light = Product.GetContainerByName("SM_RG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Cabinet_Light").DisplayValue

    cabinet, powersupply, switches = getNumberOfRGCabinet(Product)
    Trace.Write("cabinetforRGsystems------>"+str(cabinet))
    qty1 = cabinet
    if enclosure == "Cabinet":
        if qty1 > 0:
            #CXCPQ 33064
            if iota == "PUIO" and cab_acc == "Single Access":
                parts_dict["FS-BCU-0038"] = {"Quantity" : int(qty1), "Description" : "Rittal TS8804210 FDR/PL RAL7035"}
            #CXCPQ 33068
            if iota == "PUIO" and cab_acc == "Single Access" and cab_light == "Yes":
                parts_dict["4140252"] = {"Quantity" : int(qty1), "Description" : "ABL SURSUM BREAKER 8A 2D8UM"}
            #CXCPQ 33069
            if iota == "PUIO" and cab_acc == "Single Access" and cab_light == "Yes":
                parts_dict["SZ 4315.150"] = {"Quantity" : int(qty1), "Description" : "RITTAL POWER CABLE 3M GREY"}
            #CXCPQ 33065
            if iota == "PUIO" and cab_acc == "Single Access":
                parts_dict["FC-FANWR-24R"] = {"Quantity" : int(qty1), "Description" : "24Vdc fan unit with readback CC"}
            #CXCPQ 33066
            if iota == "PUIO" and cab_acc == "Single Access" and cab_light == "Yes":
                parts_dict["SZ 4155.110"] = {"Quantity" : int(qty1), "Description" : "RITTAL CAB. LIGHT 110/240V+SENSOR+OUTLET"}
            #CXCPQ 33356
            if iota == "RUSIO" and cab_acc == "Single Access":
                parts_dict["FC-FANWR-24R"] = {"Quantity" : int(qty1), "Description" : "24Vdc fan unit with readback CC"}
            #CXCPQ 33362
            if iota == "RUSIO" and cab_acc == "Single Access" and cab_light == "Yes":
                parts_dict["4140252"] = {"Quantity" : int(qty1), "Description" : "ABL SURSUM BREAKER 8A 2D8UM"}
            #CXCPQ 33359
            if iota == "RUSIO" and cab_acc == "Single Access" and cab_light == "Yes":
                parts_dict["SZ 4155.110"] = {"Quantity" : int(qty1), "Description" : "RITTAL CAB. LIGHT 110/240V+SENSOR+OUTLET"}

            #CXCPQ-33223
            if iota == "RUSIO" and cab_acc != "Single Access" and cab_light == "Yes":
                parts_dict["SZ 4315.150"] = {"Quantity" : int(qty1) * 2, "Description" : "RITTAL POWER CABLE 3M GREY"}
            #CXCPQ-33222
            if iota == "RUSIO" and cab_acc != "Single Access" and cab_light == "Yes":
                parts_dict["4140252"] = {"Quantity" : int(qty1) * 2, "Description" : "ABL SURSUM BREAKER 8A 2D8UM"}
    return parts_dict


def sm_parts(Product,parts_dict):
    enclosure = Product.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue
    identifier_modifier = Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").DisplayValue
    positional_key = Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").Value
    qty = Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Number_of_SM_SC_1.3M_Universal_Safety_Cabinets_(0-63)").Value
    cab_material_type = Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("Cabinet_Material_Type_Ingress_Protection").DisplayValue
    amb_temp = Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("Ambient_Temperature_Range").DisplayValue
    PUIO = Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("PUIO_Count").DisplayValue
    PDIO = Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("PDIO_Count").DisplayValue
    field_PUIO = Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("Field_Termination_Assembly_for_PUIO").DisplayValue
    field_PDIO = Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("Field_Termination_Assembly_for_PDIO").DisplayValue
    power_supply = Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("Power_Supply_Type").DisplayValue
    ps_redundancy = Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("Power_Supply_Redundancy").DisplayValue
    abu_dhabi = Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("Abu_Dhabi_Build_Loc").DisplayValue
    s_300 = Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("S300").DisplayValue
    temp_monitoring = Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("Temperature_Monitoring").DisplayValue
    external_block = Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("External _24VDC_Terminal_Block").DisplayValue
    fibre_optics = Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("Fiber_Optic_Extender").DisplayValue
    CNM = Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("Number_of_Control_Network_Module_0-100").Value
    cnm_sfp = Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("CNM_SFP_Type").DisplayValue
    if qty == "":
        qty = 0
    if enclosure == "Universal Safety Cab-1.3M" and qty > 0:

        if identifier_modifier == "No":

            #CXCPQ-31688
            if cab_material_type == "316L Stainless 1.3M, IP66" and amb_temp == "With Fan, Max Ambient +55°C" and field_PUIO == "Intrinsically Safe" and field_PDIO == "Intrinsically Safe" and power_supply == "20A AC/DC QUINT 4+ PS" and ps_redundancy == "Redundant" and abu_dhabi == "No":
                parts_dict["50159996-313"] = {"Quantity" : int(qty), "Description" : "USC SYSTEM LABEL, SS CABINET WITH FANS, IS"}

            #CXCPQ-31689
            if cab_material_type == "316L Stainless 1.3M, IP66" and amb_temp == "With Fan, Max Ambient +55°C" and field_PUIO == "Intrinsically Safe" and field_PDIO == "Intrinsically Safe" and power_supply == "24 VDC/DC QUINT 4+ Supply" and ps_redundancy == "Redundant" and abu_dhabi == "No":
                parts_dict["50159996-315"] = {"Quantity" : int(qty), "Description" : "USC SYSTEM LABEL, SS CABINET WITH FANS, IS"}

            #CXCPQ-31690
            if cab_material_type == "316L Stainless 1.3M, IP66" and amb_temp == "Without Fan, Max Ambient +40°C" and (field_PUIO == "Default Marshalling FC-TUIO51/52" or field_PUIO == "Universal Marshalling, PTA") and (field_PDIO == "Default Marshalling FC-TDIO51/52" or field_PDIO == "Universal Marshalling, PTA") and power_supply == "24A AC/DC FC-PSUNI2424" and ps_redundancy == "Redundant" and abu_dhabi == "Yes":
                parts_dict["50159996-316"] = {"Quantity" : int(qty), "Description" : "USC SYSTEM LABEL, SS CABINET, ABU DHABI"}

            #CXCPQ-32668 #CXCPQ-118187
            if s_300 == "No S300" and (external_block == "External TB 4A or less" or external_block == "External TB w/6A Fuse"):
                parts_dict["50159943-004"] = {"Quantity" : int(qty), "Description" : "External Terminal Block"}

            #CXCPQ-32669
            if s_300 == "No S300" and (temp_monitoring == "No STT650" or temp_monitoring == "STT650") and external_block == "External TB 4A or less":
                parts_dict["51202677-039"] = {"Quantity" : int(qty), "Description" : "Din Rail, 39 INCH"}

            #CXCPQ-32670
            if (s_300 == "No S300" or s_300 == "Redundant S300" or s_300 == "Non Redundant S300") and temp_monitoring == "STT650":
                parts_dict["50143176-100"] = {"Quantity" : int(qty), "Description" : "STT650"}

            #CXCPQ-32152,32154,32156
            #if s_300 == "Redundant S300" or s_300 == "Non Redundant S300":
                #CXCPQ-54369 - Start
                #addon = parts_dict.get("FC-MCC003",{"Quantity" : 0})["Quantity"]
                #parts_dict["FC-MCC003"] = {"Quantity" : int(qty) + int(addon), "Description" : "Filler panel"}
                #CXCPQ-54369 - End
                #CXCPQ-54115 - Start
                #parts_dict["FC-MCAR-01"] = {"Quantity" : int(qty), "Description" : "Carrier Assembly Panel Mounted"}
                #CXCPQ-54115 - End
                #CXCPQ-54745 - Start
                #parts_dict["FS-CCI-HSE-08"] = {"Quantity" : int(qty), "Description" : "Ethernet cable, Red and Blue 0.8 M"}
                #CXCPQ-54745 - End
            #CXCPQ-34328
            if s_300 == "No S300" and fibre_optics == "Single Mode x2 EDS-408A":
                parts_dict["4600154"] = {"Quantity" : 2*int(qty), "Description" : "EDS-408A-SS-SC-T"}
            if (s_300 == "Redundant S300") and fibre_optics == "Single Mode x4 EDS-408A":
                parts_dict["4600154"] = {"Quantity" : 4*int(qty), "Description" : "EDS-408A-SS-SC-T"}
            #CXCPQ-34329
            if s_300 == "No S300" and fibre_optics == "Multi Mode x2 EDS-408A":
                parts_dict["4600156"] = {"Quantity" : 2*int(qty), "Description" : "EDS-408A-MM-SC-T"}
            if (s_300 == "Redundant S300") and fibre_optics == "Multi Mode x4 EDS-408A":
                parts_dict["4600156"] = {"Quantity" : 4*int(qty), "Description" : "EDS-408A-MM-SC-T"}

            #CXCPQ-54745 - Start
            if (s_300 == "Redundant S300" and CNM == "0") or (PUIO == "32" and PDIO == "0" and CNM == "2") or (PUIO == "0" and PDIO == "32" and CNM == "2") or (PUIO == "32" and PDIO == "0" and CNM == "4") or (PUIO == "0" and PDIO == "32" and CNM == "4"):
                parts_dict["FS-CCI-HSE-08"] = {"Quantity" : int(qty), "Description" : "Ethernet cable, Red and Blue 0.8 M"}

            if (PUIO == "64" and PDIO == "0" and CNM == "2") or (PUIO == "0" and PDIO == "64" and CNM == "2") or (PUIO == "32" and PDIO == "32" and CNM == "2") or (PUIO == "64" and PDIO == "0" and CNM == "4") or (PUIO == "0" and PDIO == "64" and CNM == "4") or (PUIO == "32" and PDIO == "32" and CNM == "4"):
                parts_dict["FS-CCI-HSE-08"] = {"Quantity" : 2*int(qty), "Description" : "Ethernet cable, Red and Blue 0.8 M"}
            #CXCPQ-54745 - End

            #CXCPQ-54115 - Start
            if (s_300 == "Redundant S300" and CNM in ["0","4"]) or (s_300 == "No S300" and PUIO == "32" and PDIO in ["32","64"] and CNM == "2") or (s_300 == "No S300" and PUIO == "64" and PDIO == "32" and CNM == "2") or (s_300 == "No S300" and PUIO in ["32","64","96"] and PDIO == "0" and CNM == "2") or (s_300 == "No S300" and PUIO == "0" and PDIO in ["32","96","64"] and CNM == "2"):
                parts_dict["FC-MCAR-01"] = {"Quantity" : int(qty), "Description" : "Carrier Assembly Panel Mounted"}
            #CXCPQ-54115 - End
            
            #CXCPQ-54369 - Start
            #addon = parts_dict.get("FC-MCC003",{"Quantity" : 0})["Quantity"]
            if s_300 == "Redundant S300" and CNM == "0":
                parts_dict["FC-MCC003"] = {"Quantity" : int(qty), "Description" : "Filler panel"}
            if (s_300 == "No S300" and PUIO == "32" and PDIO == "64" and CNM == "2") or (s_300 == "No S300" and PUIO == "64" and PDIO == "32" and CNM == "2") or (s_300 == "No S300" and PUIO == "96" and PDIO == "0" and CNM == "2") or (s_300 == "No S300" and PUIO == "0" and PDIO == "96" and CNM == "2"):
                parts_dict["FC-MCC003"] = {"Quantity" : 2*(int(qty)), "Description" : "Filler panel"}
            if s_300 == "Redundant S300" and CNM == "4":
                parts_dict["FC-MCC003"] = {"Quantity" : 3*(int(qty)), "Description" : "Filler panel"}
            if (PUIO == "32" and PDIO == "0" and CNM == "0") or (PUIO == "0" and PDIO == "32" and CNM == "0"):
                parts_dict["FC-MCC003"] = {"Quantity" : 8*(int(qty)), "Description" : "Filler panel"}
            if (PUIO == "64" and PDIO == "0" and CNM == "0") or (PUIO == "0" and PDIO == "64" and CNM == "0") or (PUIO == "32" and PDIO == "32" and CNM == "0"):
                parts_dict["FC-MCC003"] = {"Quantity" : 4*(int(qty)), "Description" : "Filler panel"}
        
                
            #CXCPQ-54369 - End
            
            #CXCPQ-54528 - Start
            if s_300 == "Redundant S300" and CNM == "4":
                parts_dict["FC-MCAR-03"] = {"Quantity" : int(qty), "Description" : "SM USIO 36 INCH CARRIER FLAT"}
                parts_dict["CC-INWM01"] = {"Quantity" : 4*(int(qty)), "Description" : "NETWORK MODULE - MAIN"}
                parts_dict["CC-TNWC01"] = {"Quantity" : 4*(int(qty)), "Description" : "NETWORK MODULE IOTA"}
            if s_300 == "No S300" and CNM == "2":
                parts_dict["CC-INWM01"] = {"Quantity" : 2*(int(qty)), "Description" : "NETWORK MODULE - MAIN"}
                parts_dict["CC-TNWC01"] = {"Quantity" : 2*(int(qty)), "Description" : "NETWORK MODULE IOTA"}
            if CNM == "2" or CNM == "4":
                if cnm_sfp == "15km Single Mode SFP":
                    parts_dict["50154761-001"] = {"Quantity" : 2*(int(qty)), "Description" : "SFP-SINGLE MODE 20KM"}
                if cnm_sfp == "2Km Multi Mode SFP":
                    parts_dict["50154762-002"] = {"Quantity" : 2*(int(qty)), "Description" : "TXRX OPT SFP 125 MB/S 1310NM"}
                if cnm_sfp == "10km Single Mode SFP":
                    parts_dict["50182312-001"] = {"Quantity" : 2*(int(qty)), "Description" : "SFP - Single Mode 10KM 1 GBPS"}
                if cnm_sfp == "550m Multi Mode SFP":
                    parts_dict["50185149-001"] = {"Quantity" : 2*(int(qty)), "Description" : "SFP - MM 1 GBPS 50/125 & 62.5/125 uM"}
            #CXCPQ-54528 - End

        elif len(positional_key) >= 17:

            #CXCPQ-31688
            if positional_key[1] == "S" and positional_key[2] == "B" and positional_key[5] == "I" and positional_key[6] == "I" and positional_key[10] == "Q" and positional_key[11] == "R" and positional_key[16] == "X":
                parts_dict["50159996-313"] = {"Quantity" : int(qty), "Description" : "USC SYSTEM LABEL, SS CABINET WITH FANS, IS"}

            #CXCPQ-31689
            if positional_key[1] == "S" and positional_key[2] == "B" and positional_key[5] == "I" and positional_key[6] == "I" and positional_key[10] == "D" and positional_key[11] == "R" and positional_key[16] == "X":
                parts_dict["50159996-315"] = {"Quantity" : int(qty), "Description" : "USC SYSTEM LABEL, SS CABINET WITH FANS, IS"}

            #CXCPQ-31690
            if positional_key[1] == "S" and positional_key[2] == "A" and (positional_key[5] == "M" or positional_key[5] == "U") and (positional_key[6] == "M" or positional_key[6] == "U") and positional_key[10] == "A" and positional_key[11] == "R" and positional_key[16] == "Y":
                parts_dict["50159996-316"] = {"Quantity" : int(qty), "Description" : "USC SYSTEM LABEL, SS CABINET, ABU DHABI"}

            #CXCPQ-32668 #CXCPQ-118187
            if positional_key[3] == "X" and (positional_key[15] == "Y" or positional_key[15] == "V"):
                parts_dict["50159943-004"] = {"Quantity" : int(qty), "Description" : "External Terminal Block"}

            #CXCPQ-32669
            if positional_key[3] == "X" and (positional_key[14] == "X" or positional_key[14] == "Y") and positional_key[15] == "Y":
                parts_dict["51202677-039"] = {"Quantity" : int(qty), "Description" : "Din Rail, 39 INCH"}

            #CXCPQ-32670
            if (positional_key[3] == "X" or positional_key[3] == "S" or positional_key[3] == "N") and positional_key[14] == "Y" :
                parts_dict["50143176-100"] = {"Quantity" : int(qty), "Description" : "STT650"}

            #CXCPQ-32152,32154,32156
            #if positional_key[3] == "S" or positional_key[3] == "N":
                #CXCPQ-54369 - Start
                #addon = parts_dict.get("FC-MCC003",{"Quantity" : 0})["Quantity"]
                #parts_dict["FC-MCC003"] = {"Quantity" : int(qty) + int(addon), "Description" : "Filler panel"}
                #CXCPQ-54369 - End
                #CXCPQ-54115 - Start
                #parts_dict["FC-MCAR-01"] = {"Quantity" : int(qty), "Description" : "Carrier Assembly Panel Mounted"}
                #CXCPQ-54115 - End
                #CXCPQ-54745 - Start
                #parts_dict["FS-CCI-HSE-08"] = {"Quantity" : int(qty), "Description" : "Ethernet cable, Red and Blue 0.8 M"}
                #CXCPQ-54745 - End
            #CXCPQ-34328
            if positional_key[3] == "X" and positional_key[4] == "U":
                parts_dict["4600154"] = {"Quantity" : 2*int(qty), "Description" : "EDS-408A-SS-SC-T"}
            if (positional_key[3] == "S") and positional_key[4] == "S":
                parts_dict["4600154"] = {"Quantity" : 4*int(qty), "Description" : "EDS-408A-SS-SC-T"}

            #CXCPQ-34329
            if positional_key[3] == "X" and positional_key[4] == "W":
                parts_dict["4600156"] = {"Quantity" : 2*int(qty), "Description" : "EDS-408A-MM-SC-T"}
            if (positional_key[3] == "S") and positional_key[4] == "M":
                parts_dict["4600156"] = {"Quantity" : 4*int(qty), "Description" : "EDS-408A-MM-SC-T"}

            #CXCPQ-54745 - Start
            if (positional_key[3] == "S" and positional_key[17] == "0") or (positional_key[8] == "A" and positional_key[9] == "X" and positional_key[17] == "2") or (positional_key[8] == "X" and positional_key[9] == "A" and positional_key[17] == "2") or (positional_key[8] == "A" and positional_key[9] == "X" and positional_key[17] == "4") or (positional_key[8] == "X" and positional_key[9] == "A" and positional_key[17] == "4"):
                parts_dict["FS-CCI-HSE-08"] = {"Quantity" : int(qty), "Description" : "Ethernet cable, Red and Blue 0.8 M"}

            if (positional_key[8] == "B" and positional_key[9] == "X" and positional_key[17] == "2") or (positional_key[8] == "X" and positional_key[9] == "B" and positional_key[17] == "2") or (positional_key[8] == "A" and positional_key[9] == "A" and positional_key[17] == "2") or (positional_key[8] == "B" and positional_key[9] == "X" and positional_key[17] == "4") or (positional_key[8] == "X" and positional_key[9] == "B" and positional_key[17] == "4") or (positional_key[8] == "A" and positional_key[9] == "A" and positional_key[17] == "4"):
                parts_dict["FS-CCI-HSE-08"] = {"Quantity" : 2*int(qty), "Description" : "Ethernet cable, Red and Blue 0.8 M"}
            #CXCPQ-54745 - End

            #CXCPQ-54115 - Start
            '''Log.Info("ghhkjkhkk")
            Log.Info(str(positional_key[3] == "X" and positional_key[8] == "A" and positional_key[9] == "A" and positional_key[17] == "2"))
            if (positional_key[3] == "S" and positional_key[17] in ['0','4']) or (positional_key[3] == "X" and positional_key[8] == "A" and positional_key[9] == "B" and positional_key[17] == "2") or (positional_key[3] == "X" and positional_key[8] == "A" and positional_key[9] == "A" and positional_key[17] == "2") or (positional_key[3] == "X" and positional_key[8] == "B" and positional_key[9] == "A" and positional_key[17] == "2") or (positional_key[3] == "X" and positional_key[8] in ["C","B","A"] and positional_key[9] == "X" and positional_key[17] == "2") or (positional_key[3] == "X" and positional_key[8] == "X" and positional_key[9] in ["C","B","A"] and positional_key[17] == "2"):
                Log.Info("Inside MCAR")
                parts_dict["FC-MCAR-01"] = {"Quantity" : int(qty), "Description" : "Carrier Assembly Panel Mounted"}'''

            #CXCPQ-54115 - End
            
            '''#CXCPQ-54369 - Start
            #addon = parts_dict.get("FC-MCC003",{"Quantity" : 0})["Quantity"]
            if positional_key[3] == "S" and positional_key[17] == "0":
                Log.Write("A")
                parts_dict["FC-MCC003"] = {"Quantity" : int(qty), "Description" : "Filler panel"}
            if (positional_key[3] == "X" and positional_key[8] == "A" and positional_key[9] == "B" and positional_key[17] == "2") or (positional_key[3] == "X" and positional_key[8] == "B" and positional_key[9] == "A" and positional_key[17] == "2") or (positional_key[3] == "X" and positional_key[8] == "C" and positional_key[9] == "X" and positional_key[17] == "2") or (positional_key[3] == "X" and positional_key[8] == "X" and positional_key[9] == "C" and positional_key[17] == "2"):
                parts_dict["FC-MCC003"] = {"Quantity" : 2*(int(qty)), "Description" : "Filler panel"}
                Log.Write("b")
            if positional_key[3] == "S" and positional_key[17] == "4":
                Log.Write("c")
                parts_dict["FC-MCC003"] = {"Quantity" : 3*(int(qty)), "Description" : "Filler panel"}
            if (positional_key[8] == "A" and positional_key[9] == "X" and positional_key[17] == "0") or (positional_key[8] == "X" and positional_key[9] == "A" and positional_key[17] == "0"):
                parts_dict["FC-MCC003"] = {"Quantity" : 8*(int(qty)), "Description" : "Filler panel"}
                Log.Write("d")
            if (positional_key[8] == "B" and positional_key[9] == "X" and positional_key[17] == "0") or (positional_key[8] == "X" and positional_key[9] == "B" and positional_key[17] == "0") or (positional_key[8] == "A" and positional_key[9] == "A" and positional_key[17] == "0"):
                parts_dict["FC-MCC003"] = {"Quantity" : 4*(int(qty)), "Description" : "Filler panel"}
                Log.Write("e")
            #CXCPQ-54369 - End'''
            
            #CXCPQ-54528 - Start
            if positional_key[3] == "S" and positional_key[17] == "4":
                parts_dict["FC-MCAR-03"] = {"Quantity" : int(qty), "Description" : "SM USIO 36 INCH CARRIER FLAT"}
                parts_dict["CC-INWM01"] = {"Quantity" : 4*(int(qty)), "Description" : "NETWORK MODULE - MAIN"}
                parts_dict["CC-TNWC01"] = {"Quantity" : 4*(int(qty)), "Description" : "NETWORK MODULE IOTA"}
            if positional_key[3] == "X" and positional_key[17] == "2":
                parts_dict["CC-INWM01"] = {"Quantity" : 2*(int(qty)), "Description" : "NETWORK MODULE - MAIN"}
                parts_dict["CC-TNWC01"] = {"Quantity" : 2*(int(qty)), "Description" : "NETWORK MODULE IOTA"}
            if positional_key[17] == "2" or positional_key[17] == "4":
                if positional_key[18] == "B":
                    parts_dict["50154761-001"] = {"Quantity" : 2*(int(qty)), "Description" : "SFP-SINGLE MODE 20KM"}
                if positional_key[18] == "C":
                    parts_dict["50154762-002"] = {"Quantity" : 2*(int(qty)), "Description" : "TXRX OPT SFP 125 MB/S 1310NM"}
                if positional_key[18] == "D":
                    parts_dict["50182312-001"] = {"Quantity" : 2*(int(qty)), "Description" : "SFP - Single Mode 10KM 1 GBPS"}
                if positional_key[18] == "E":
                    parts_dict["50185149-001"] = {"Quantity" : 2*(int(qty)), "Description" : "SFP - MM 1 GBPS 50/125 & 62.5/125 uM"}
            #CXCPQ-54528 - End
    return parts_dict