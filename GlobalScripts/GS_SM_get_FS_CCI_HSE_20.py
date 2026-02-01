#32667
def getNum(n):
    return 0 if n=="" or n==0 else int(n)
def get_FS_CCI_HSE_20(Product,parts_dict):
    enclosure = Product.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue
    identifier_modifier = Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").DisplayValue
    positional_key = Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").Value
    sc300=Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("S300").DisplayValue
    ft_puio=Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("Field_Termination_Assembly_for_PUIO").DisplayValue
    ft_pdio=Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("Field_Termination_Assembly_for_PDIO").DisplayValue
    puio=Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("PUIO_Count").DisplayValue
    pdio=Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("PDIO_Count").DisplayValue
    ioRed=Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("IO_Redundancy").DisplayValue
    cnm = Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("Number_of_Control_Network_Module_0-100").Value
    qty=getNum(Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Number_of_SM_SC_1.3M_Universal_Safety_Cabinets_(0-63)").Value)

    Trace.Write("enclosure "+str(enclosure))
    Trace.Write("identifier_modifier "+str(identifier_modifier))
    Trace.Write("positional_key "+str(enclosure))
    Trace.Write("sc300 "+str(sc300))
    Trace.Write("ft_puio "+str(ft_puio))
    Trace.Write("ft_pdio "+str(ft_pdio))
    Trace.Write("puio "+str(puio))
    Trace.Write("pdio "+str(pdio))
    Trace.Write("ioRed "+str(ioRed))

    if enclosure == "Universal Safety Cab-1.3M" and qty > 0:
        if identifier_modifier == "No":
            if (sc300=="Redundant S300" or sc300=="No S300") and (ioRed=="Redundant IO"):
                if (ft_pdio=="Default Marshalling FC-TDIO51/52") and (puio=="0") and (pdio=="32"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" : int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if (ft_pdio=="Default Marshalling FC-TDIO51/52") and (puio=="0") and (pdio=="64"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :2 * int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if (ft_puio=="Default Marshalling FC-TUIO51/52") and (puio=="32") and (pdio=="0"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" : int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if (ft_puio=="Default Marshalling FC-TUIO51/52") and (puio=="64") and (pdio=="0"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :2 * int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                ##
                if (ft_puio=="Default Marshalling FC-TUIO51/52") and (ft_pdio=="Default Marshalling FC-TDIO51/52") and (puio=="32") and (pdio=="32"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :2 * int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if (ft_puio=="Default Marshalling FC-TUIO51/52") and (ft_pdio=="Default Marshalling FC-TDIO51/52") and (puio=="32") and (pdio=="64"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3 * int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if (ft_puio=="Default Marshalling FC-TUIO51/52") and (ft_pdio=="Default Marshalling FC-TDIO51/52") and (puio=="64") and (pdio=="32"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3 * int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                #96
                if (ft_puio=="Default Marshalling FC-TUIO51/52") and (puio=="96") and (pdio=="0"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3 * int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if (ft_pdio=="Default Marshalling FC-TDIO51/52") and (puio=="0") and (pdio=="96"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3 * int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                #universal
                if (ft_puio=="Universal Marshalling, PTA" or ft_puio=="Intrinsically Safe") and (puio=="32") and (pdio=="0"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" : int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if (ft_puio=="Universal Marshalling, PTA" or ft_puio=="Intrinsically Safe" or ft_puio=="32 IS, 32 Non-IS") and (puio=="64") and (pdio=="0"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :2 * int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                ##
                if (ft_puio=="Universal Marshalling, PTA" or ft_puio=="Intrinsically Safe") and (ft_pdio=="Default Marshalling FC-TDIO51/52") and (puio=="32") and (pdio=="32"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :2 * int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if (ft_puio=="Universal Marshalling, PTA" or ft_puio=="Intrinsically Safe") and (ft_pdio=="Default Marshalling FC-TDIO51/52") and (puio=="32") and (pdio=="64"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if (ft_puio=="Universal Marshalling, PTA" or ft_puio=="Intrinsically Safe" or ft_puio=="32 IS, 32 Non-IS") and (ft_pdio=="Default Marshalling FC-TDIO51/52") and (puio=="64") and (pdio=="32"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                #96-pdio
                if (ft_pdio=="Universal Marshalling, PTA" or ft_pdio=="Intrinsically Safe" or ft_pdio=="32 IS, 64 Non-IS" or ft_pdio=="64 IS, 32 Non-IS") and (puio=="0") and (pdio=="96"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                ##
                if (ft_puio=="Universal Marshalling, PTA" or ft_puio=="Intrinsically Safe") and (ft_pdio=="Universal Marshalling, PTA" or ft_pdio=="Intrinsically Safe" or ft_pdio=="32 IS, 32 Non-IS") and (puio=="32") and (pdio=="64"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if (ft_puio=="Default Marshalling FC-TUIO51/52") and (ft_pdio=="Universal Marshalling, PTA" or ft_pdio=="Intrinsically Safe") and (puio=="64") and (pdio=="32"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if (ft_puio=="Universal Marshalling, PTA" or ft_puio=="Intrinsically Safe" or ft_puio=="32 IS, 32 Non-IS") and (ft_pdio=="Universal Marshalling, PTA" or ft_pdio=="Intrinsically Safe") and (puio=="64") and (pdio=="32"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" : 3*int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if (ft_puio=="Default Marshalling FC-TUIO51/52") and (ft_pdio=="Universal Marshalling, PTA" or ft_pdio=="Intrinsically Safe") and (puio=="32") and (pdio=="32"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :2* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                #universal-pdio
                if (ft_pdio=="Universal Marshalling, PTA" or ft_pdio=="Intrinsically Safe") and (puio=="0") and (pdio=="32"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if (ft_pdio=="Universal Marshalling, PTA" or ft_pdio=="Intrinsically Safe" or ft_pdio=="32 IS, 32 Non-IS") and (puio=="0") and (pdio=="64"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :2* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                ##
                if (ft_puio=="Universal Marshalling, PTA" or ft_puio=="Intrinsically Safe") and (ft_pdio=="Universal Marshalling, PTA" or ft_pdio=="Intrinsically Safe") and (puio=="32") and (pdio=="32"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :2* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if (ft_puio=="Default Marshalling FC-TUIO51/52") and (ft_pdio=="Universal Marshalling, PTA" or ft_pdio=="Intrinsically Safe" or ft_pdio=="32 IS, 32 Non-IS") and (puio=="32") and (pdio=="64"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                #96-puio
                if (ft_puio=="Universal Marshalling, PTA" or ft_puio=="Intrinsically Safe" or ft_puio=="32 IS, 64 Non-IS" or ft_puio=="64 IS, 32 Non-IS") and (puio=="96") and (pdio=="0"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
            elif (sc300=="Redundant S300" or sc300=="No S300") and (ioRed=="Non Redundant IO"):
                if (ft_pdio=="Default Marshalling FC-TDIO51/52") and (puio=="0") and (pdio=="32"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" : int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if (ft_pdio=="Default Marshalling FC-TDIO51/52") and (puio=="0") and (pdio=="64"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :2 * int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if (ft_puio=="Default Marshalling FC-TUIO51/52") and (puio=="32") and (pdio=="0"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" : int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if (ft_puio=="Default Marshalling FC-TUIO51/52") and (puio=="64") and (pdio=="0"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :2 * int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                ##
                if (ft_puio=="Default Marshalling FC-TUIO51/52") and (ft_pdio=="Default Marshalling FC-TDIO51/52") and (puio=="32") and (pdio=="32"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :2 * int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if (ft_puio=="Default Marshalling FC-TUIO51/52") and (ft_pdio=="Default Marshalling FC-TDIO51/52") and (puio=="32") and (pdio=="64"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3 * int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if (ft_puio=="Default Marshalling FC-TUIO51/52") and (ft_pdio=="Default Marshalling FC-TDIO51/52") and (puio=="64") and (pdio=="32"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3 * int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                #96
                if (ft_puio=="Default Marshalling FC-TUIO51/52") and (puio=="96") and (pdio=="0"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3 * int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if (ft_pdio=="Default Marshalling FC-TDIO51/52") and (puio=="0") and (pdio=="96"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3 * int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                #universal
                if (ft_puio=="Universal Marshalling, PTA" or ft_puio=="Intrinsically Safe") and (puio=="32") and (pdio=="0"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" : int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if (ft_puio=="Universal Marshalling, PTA" or ft_puio=="Intrinsically Safe" or ft_puio=="32 IS, 32 Non-IS") and (puio=="64") and (pdio=="0"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :2 * int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                ##
                if (ft_puio=="Universal Marshalling, PTA" or ft_puio=="Intrinsically Safe") and (ft_pdio=="Default Marshalling FC-TDIO51/52") and (puio=="32") and (pdio=="32"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :2 * int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if (ft_puio=="Universal Marshalling, PTA" or ft_puio=="Intrinsically Safe") and (ft_pdio=="Default Marshalling FC-TDIO51/52") and (puio=="32") and (pdio=="64"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if (ft_puio=="Universal Marshalling, PTA" or ft_puio=="Intrinsically Safe" or ft_puio=="32 IS, 32 Non-IS") and (ft_pdio=="Default Marshalling FC-TDIO51/52") and (puio=="64") and (pdio=="32"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                #96-pdio
                if (ft_pdio=="Universal Marshalling, PTA" or ft_pdio=="Intrinsically Safe" or ft_pdio=="32 IS, 64 Non-IS" or ft_pdio=="64 IS, 32 Non-IS") and (puio=="0") and (pdio=="96"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                ##
                if (ft_puio=="Universal Marshalling, PTA" or ft_puio=="Intrinsically Safe") and (ft_pdio=="Universal Marshalling, PTA" or ft_pdio=="Intrinsically Safe" or ft_pdio=="32 IS, 32 Non-IS") and (puio=="32") and (pdio=="64"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if (ft_puio=="Default Marshalling FC-TUIO51/52") and (ft_pdio=="Universal Marshalling, PTA" or ft_pdio=="Intrinsically Safe") and (puio=="64") and (pdio=="32"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if (ft_puio=="Universal Marshalling, PTA" or ft_puio=="Intrinsically Safe" or ft_puio=="32 IS, 32 Non-IS") and (ft_pdio=="Universal Marshalling, PTA" or ft_pdio=="Intrinsically Safe") and (puio=="64") and (pdio=="32"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" : int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if (ft_puio=="Default Marshalling FC-TUIO51/52") and (ft_pdio=="Universal Marshalling, PTA" or ft_pdio=="Intrinsically Safe") and (puio=="32") and (pdio=="32"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :2* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                #universal-pdio
                if (ft_pdio=="Universal Marshalling, PTA" or ft_pdio=="Intrinsically Safe") and (puio=="0") and (pdio=="32"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if (ft_pdio=="Universal Marshalling, PTA" or ft_pdio=="Intrinsically Safe" or ft_pdio=="32 IS, 32 Non-IS") and (puio=="0") and (pdio=="64"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :2* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                ##
                if (ft_puio=="Universal Marshalling, PTA" or ft_puio=="Intrinsically Safe") and (ft_pdio=="Universal Marshalling, PTA" or ft_pdio=="Intrinsically Safe") and (puio=="32") and (pdio=="32"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :2* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if (ft_puio=="Default Marshalling FC-TUIO51/52") and (ft_pdio=="Universal Marshalling, PTA" or ft_pdio=="Intrinsically Safe" or ft_pdio=="32 IS, 32 Non-IS") and (puio=="32") and (pdio=="64"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                #96-puio
                if (ft_puio=="Universal Marshalling, PTA" or ft_puio=="Intrinsically Safe" or ft_puio=="32 IS, 64 Non-IS" or ft_puio=="64 IS, 32 Non-IS") and (puio=="96") and (pdio=="0"):
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                    
            #CXCPQ-54547 - Start
            addon = parts_dict.get("FS-CCI-HSE-20",{"Quantity" : 0})["Quantity"]
            if sc300 == "Redundant S300" and cnm == "4":
                parts_dict["FS-CCI-HSE-20"] = {"Quantity" : int(qty) + int(addon), "Description" : "Ethernet cable, Red and Blue L 2 M"}
            if (sc300 == "No S300" and puio == "32" and pdio == "64" and cnm == "2") or (sc300 == "No S300" and puio == "64" and pdio == "32" and cnm == "2") or (sc300 == "No S300" and puio == "96" and pdio == "0" and cnm == "2") or (sc300 == "No S300" and puio == "0" and pdio == "96" and cnm == "2"):
                parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3 * int(qty) + int(addon), "Description" : "Ethernet cable, Red and Blue L 2 M"}
            #CXCPQ-54547 - End
            
        elif identifier_modifier == "Yes":
            Trace.Write("lvl 1-----")
            if (positional_key[3] == "S" or positional_key[3] == "X") and positional_key[13] == "R":
                if positional_key[6] == "M" and positional_key[8] == "X" and positional_key[9] == "A":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" : int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if positional_key[6] == "M" and positional_key[8] == "X" and positional_key[9] == "B":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :2 * int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if positional_key[5] == "M" and positional_key[8] == "A" and positional_key[9] == "X":
                    Trace.Write("lvl 2-----")
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" : int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if positional_key[5] == "M" and positional_key[8] == "B" and positional_key[9] == "X":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :2 * int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                ##
                if positional_key[5] == "M" and positional_key[6] == "M" and positional_key[8] == "A" and positional_key[9] == "A":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :2 * int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if positional_key[5] == "M" and positional_key[6] == "M" and positional_key[8] == "A" and positional_key[9] == "B":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3 * int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if positional_key[5] == "M" and positional_key[6] == "M" and positional_key[8] == "B" and positional_key[9] == "A":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3 * int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                #96
                if positional_key[5] == "M" and positional_key[8] == "C" and positional_key[9] == "X":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3 * int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if positional_key[6] == "M" and positional_key[8] == "X" and positional_key[9] == "C":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3 * int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                #universal
                if (positional_key[5] == "U" or positional_key[5] == "I") and positional_key[8] == "A" and positional_key[9] == "X":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" : int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if (positional_key[5] == "U" or positional_key[5] == "I" or positional_key[5] =="C") and positional_key[8] == "B" and positional_key[9] == "X":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :2 * int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                ##
                if (positional_key[5] == "U" or positional_key[5] == "I") and positional_key[6] == "M" and positional_key[8] == "A" and positional_key[9] == "A":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :2 * int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if (positional_key[5] == "U" or positional_key[5] == "I") and positional_key[6] == "M" and positional_key[8] == "A" and positional_key[9] == "B":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if (positional_key[5] == "U" or positional_key[5] == "I" or positional_key[5] =="C") and positional_key[6] == "M" and positional_key[8] == "B" and positional_key[9] == "A":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                #96-pdio
                if (positional_key[6] == "U" or positional_key[6] == "I" or positional_key[6] == "A" or positional_key[6] == "B") and positional_key[8] == "X" and positional_key[9] == "C":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                ##
                if (positional_key[5] == "U" or positional_key[5] == "I")  and (positional_key[6] == "U" or positional_key[6] == "I" or positional_key[6] == "C") and positional_key[8] == "A" and positional_key[9] == "B":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if positional_key[5] == "M" and (positional_key[6] == "U" or positional_key[6] == "I") and positional_key[8] == "B" and positional_key[9] == "A":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if (positional_key[5] == "U" or positional_key[5] == "I" or positional_key[5] =="C") and (positional_key[6] == "U" or positional_key[6] == "I") and positional_key[8] == "B" and positional_key[9] == "A":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" : 3*int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if positional_key[5] == "M" and (positional_key[6] == "U" or positional_key[6] == "I") and positional_key[8] == "A" and positional_key[9] == "A":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :2* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                #universal-pdio
                if (positional_key[6] == "U" or positional_key[6] == "I") and positional_key[8] == "X" and positional_key[9] == "A":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if (positional_key[6] == "U" or positional_key[6] == "I" or positional_key[6] == "C") and positional_key[8] == "X" and positional_key[9] == "B":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :2* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                ##
                if (positional_key[5] == "U" or positional_key[5] == "I") and (positional_key[6] == "U" or positional_key[6] == "I") and positional_key[8] == "A" and positional_key[9] == "A":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :2* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if positional_key[5] == "M" and (positional_key[6] == "U" or positional_key[6] == "I" or positional_key[6] == "C") and positional_key[8] == "A" and positional_key[9] == "B":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                #96-puio
                if (positional_key[5] == "U" or positional_key[5] == "I" or positional_key[5] == "A" or positional_key[5] == "B") and positional_key[8] == "C" and positional_key[9] == "X":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
            elif (positional_key[3] == "S" or positional_key[3] == "X") and positional_key[13] == "X":
                if positional_key[6] == "M" and positional_key[8] == "X" and positional_key[9] == "A":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" : int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if positional_key[6] == "M" and positional_key[8] == "X" and positional_key[9] == "B":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :2 * int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if positional_key[5] == "M" and positional_key[8] == "A" and positional_key[9] == "X":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" : int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if positional_key[5] == "M" and positional_key[8] == "B" and positional_key[9] == "X":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :2 * int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                ##
                if positional_key[5] == "M" and positional_key[6] == "M" and positional_key[8] == "A" and positional_key[9] == "A":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :2 * int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if positional_key[5] == "M" and positional_key[6] == "M" and positional_key[8] == "A" and positional_key[9] == "B":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3 * int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if positional_key[5] == "M" and positional_key[6] == "M" and positional_key[8] == "B" and positional_key[9] == "A":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3 * int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                #96
                if positional_key[5] == "M" and positional_key[8] == "C" and positional_key[9] == "X":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3 * int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if positional_key[6] == "M" and positional_key[8] == "X" and positional_key[9] == "C":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3 * int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                #universal
                if (positional_key[5] == "U" or positional_key[5] == "I") and positional_key[8] == "A" and positional_key[9] == "X":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" : int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if (positional_key[5] == "U" or positional_key[5] == "I" or positional_key[5] =="C") and positional_key[8] == "B" and positional_key[9] == "X":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :2 * int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                ##
                if (positional_key[5] == "U" or positional_key[5] == "I") and positional_key[6] == "M" and positional_key[8] == "A" and positional_key[9] == "A":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :2 * int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if (positional_key[5] == "U" or positional_key[5] == "I") and positional_key[6] == "M" and positional_key[8] == "A" and positional_key[9] == "B":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if (positional_key[5] == "U" or positional_key[5] == "I" or positional_key[5] =="C") and positional_key[6] == "M" and positional_key[8] == "B" and positional_key[9] == "A":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                #96-pdio
                if (positional_key[6] == "U" or positional_key[6] == "I" or positional_key[6] == "A" or positional_key[6] == "B") and positional_key[8] == "X" and positional_key[9] == "C":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                ##
                if (positional_key[5] == "U" or positional_key[5] == "I")  and (positional_key[6] == "U" or positional_key[6] == "I" or positional_key[6] == "C") and positional_key[8] == "A" and positional_key[9] == "B":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if positional_key[5] == "M" and (positional_key[6] == "U" or positional_key[6] == "I") and positional_key[8] == "B" and positional_key[9] == "A":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if (positional_key[5] == "U" or positional_key[5] == "I" or positional_key[5] =="C") and (positional_key[6] == "U" or positional_key[6] == "I") and positional_key[8] == "B" and positional_key[9] == "A":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" : int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if positional_key[5] == "M" and (positional_key[6] == "U" or positional_key[6] == "I") and positional_key[8] == "A" and positional_key[9] == "A":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :2* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                #universal-pdio
                if (positional_key[6] == "U" or positional_key[6] == "I") and positional_key[8] == "X" and positional_key[9] == "A":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if (positional_key[6] == "U" or positional_key[6] == "I" or positional_key[6] == "C") and positional_key[8] == "X" and positional_key[9] == "B":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :2* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                ##
                if (positional_key[5] == "U" or positional_key[5] == "I") and (positional_key[6] == "U" or positional_key[6] == "I") and positional_key[8] == "A" and positional_key[9] == "A":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :2* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                if positional_key[5] == "M" and (positional_key[6] == "U" or positional_key[6] == "I" or positional_key[6] == "C") and positional_key[8] == "A" and positional_key[9] == "B":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                #96-puio
                if (positional_key[5] == "U" or positional_key[5] == "I" or positional_key[5] == "A" or positional_key[5] == "B") and positional_key[8] == "C" and positional_key[9] == "X":
                    parts_dict["FS-CCI-HSE-20"] = {"Quantity" :3* int(qty), "Description" : "Ethernet cable, Red and Blue L 2 M"}
                    
            #CXCPQ-54547 - Start
            addon = parts_dict.get("FS-CCI-HSE-20",{"Quantity" : 0})["Quantity"]
            if positional_key[3] == "S" and positional_key[17] == "4":
                parts_dict["FS-CCI-HSE-20"] = {"Quantity" : int(qty) + int(addon), "Description" : "Ethernet cable, Red and Blue L 2 M"}
            if (positional_key[3] == "X" and positional_key[8] == "A" and positional_key[9] == "B" and positional_key[17] == "2") or (positional_key[3] == "X" and positional_key[8] == "B" and positional_key[9] == "A" and positional_key[17] == "2") or (positional_key[3] == "X"  and positional_key[8] == "C" and positional_key[9] == "X" and positional_key[17] == "2") or (positional_key[3] == "X" and positional_key[8] == "X" and positional_key[9] == "C" and positional_key[17] == "2"):
                parts_dict["FS-CCI-HSE-20"] = {"Quantity" : 3 * int(qty) + int(addon), "Description" : "Ethernet cable, Red and Blue L 2 M"}
            #CXCPQ-54547 - End
    return parts_dict
#test = get_FS_CCI_HSE_20(Product,{})
#Trace.Write(str(test))