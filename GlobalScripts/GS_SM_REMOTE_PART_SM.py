import math as m
#parts_dict={}
def get_int(val):
    if val:
        return int(val)
    return 0
def get_parts(Product,parts_dict):
    Enclosure_Type = Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0].GetColumnByName('Enclosure_Type').DisplayValue
    #Trace.Write(Enclosure_Type)
    SM_RT_SPY_MOD_SMSC_USC = Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont').Rows[0].GetColumnByName('Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet').DisplayValue
    #Trace.Write(SM_RT_SPY_MOD_SMSC_USC)
    SM_RT_ID_MOD_SMSC_USC = Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont').Rows[0].GetColumnByName('Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet').Value
    #Trace.Write(SM_RT_ID_MOD_SMSC_USC)
    SM_RT_NO_SMSC_USC = Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont').Rows[0].GetColumnByName('Number_of_SM_SC_1.3M_Universal_Safety_Cabinets_(0-63)').Value
    #Trace.Write(SM_RT_NO_SMSC_USC)
    if Enclosure_Type == "Universal Safety Cab-1.3M":
        if str(SM_RT_SPY_MOD_SMSC_USC) =="Yes":
            #CXCPQ-32148
            if SM_RT_ID_MOD_SMSC_USC[3] == "S":
                parts_dict["FC-SCNT02"] = {"Quantity" : 2 *get_int(SM_RT_NO_SMSC_USC), "Description": 'SC S300 SAFETY CONTROLLER SIL3'}
            #elif SM_RT_ID_MOD_SMSC_USC[3] == "N":
                #parts_dict["FC-SCNT02"] = {"Quantity" : 1 *get_int(SM_RT_NO_SMSC_USC), "Description": 'SC S300 SAFETY CONTROLLER SIL3'}
            elif SM_RT_ID_MOD_SMSC_USC[3] == "X":
                parts_dict["FC-SCNT02"] = {"Quantity" : 0 *get_int(SM_RT_NO_SMSC_USC), "Description": 'SC S300 SAFETY CONTROLLER SIL3'}
            Trace.Write("SM_RT_ID_MOD_SMSC_USC[3] : "+str(SM_RT_ID_MOD_SMSC_USC[3]))
            #CXCPQ-31674
            if SM_RT_ID_MOD_SMSC_USC[1] == "S":
                if SM_RT_ID_MOD_SMSC_USC[2] == "A":
                    if SM_RT_ID_MOD_SMSC_USC[5] == "M" or SM_RT_ID_MOD_SMSC_USC[5] =="U":
                        if SM_RT_ID_MOD_SMSC_USC[6] == "M" or SM_RT_ID_MOD_SMSC_USC[6] =="U":
                            if SM_RT_ID_MOD_SMSC_USC[10] == "E":
                                if SM_RT_ID_MOD_SMSC_USC[11] == "R":
                                    if SM_RT_ID_MOD_SMSC_USC[16] == "X":
                                        parts_dict["50159996-302"] = {"Quantity" : get_int(SM_RT_NO_SMSC_USC), "Description": "USC SYSTEM LABEL, SS CABINET"}
            #CXCPQ-31675
            if SM_RT_ID_MOD_SMSC_USC[1] == "S":
                if SM_RT_ID_MOD_SMSC_USC[2] == "B":
                    if SM_RT_ID_MOD_SMSC_USC[5] == "M" or SM_RT_ID_MOD_SMSC_USC[5] =="U":
                        if SM_RT_ID_MOD_SMSC_USC[6] == "M" or SM_RT_ID_MOD_SMSC_USC[6] =="U":
                            if SM_RT_ID_MOD_SMSC_USC[10] == "E":
                                if SM_RT_ID_MOD_SMSC_USC[11] == "R":
                                    if SM_RT_ID_MOD_SMSC_USC[16] == "X":
                                        parts_dict["50159996-303"] = {"Quantity" : get_int(SM_RT_NO_SMSC_USC), "Description": "USC SYSTEM LABEL, SS CABINET WITH FANS"}
            #CXCPQ-31676
            if SM_RT_ID_MOD_SMSC_USC[1] == "S":
                if SM_RT_ID_MOD_SMSC_USC[2] == "A":
                    if SM_RT_ID_MOD_SMSC_USC[5] == "M" or SM_RT_ID_MOD_SMSC_USC[5] =="U":
                        if SM_RT_ID_MOD_SMSC_USC[6] == "M" or SM_RT_ID_MOD_SMSC_USC[6] =="U":
                            if SM_RT_ID_MOD_SMSC_USC[10] == "Q":
                                if SM_RT_ID_MOD_SMSC_USC[11] == "R":
                                    if SM_RT_ID_MOD_SMSC_USC[16] == "X":
                                        parts_dict["50159996-304"] = {"Quantity" : get_int(SM_RT_NO_SMSC_USC), "Description": "USC SYSTEM LABEL, SS CABINET"}
            #CXCPQ-31704
            if SM_RT_ID_MOD_SMSC_USC[1] == "S":
                if SM_RT_ID_MOD_SMSC_USC[2] == "A":
                    if SM_RT_ID_MOD_SMSC_USC[5] == "M" or SM_RT_ID_MOD_SMSC_USC[5] == "U":
                        if SM_RT_ID_MOD_SMSC_USC[6] == "M" or SM_RT_ID_MOD_SMSC_USC[6] =="U":
                            if SM_RT_ID_MOD_SMSC_USC[10] == "D":
                                if SM_RT_ID_MOD_SMSC_USC[11] == "R":
                                    if SM_RT_ID_MOD_SMSC_USC[16] == "Y":
                                        parts_dict["50159996-322"] = {"Quantity" : get_int(SM_RT_NO_SMSC_USC), "Description": "USC SYSTEM LABEL, SS CABINET, ABU DHABI"}
            #CXCPQ-31702
            if SM_RT_ID_MOD_SMSC_USC[1] == "S":
                if SM_RT_ID_MOD_SMSC_USC[2] == "B":
                    if SM_RT_ID_MOD_SMSC_USC[5] == "M" or SM_RT_ID_MOD_SMSC_USC[5] =="U":
                        if SM_RT_ID_MOD_SMSC_USC[6] == "M" or SM_RT_ID_MOD_SMSC_USC[6] =="U":
                            if SM_RT_ID_MOD_SMSC_USC[10] == "Q":
                                if SM_RT_ID_MOD_SMSC_USC[11] == "R":
                                    if SM_RT_ID_MOD_SMSC_USC[16] == "Y":
                                        parts_dict["50159996-321"] = {"Quantity" : get_int(SM_RT_NO_SMSC_USC), "Description": "USC SYSTEM LABEL, SS CABINET WITH FANS, ABU DHABI"}
            #CXCPQ-31694
            if SM_RT_ID_MOD_SMSC_USC[1] == "S":
                if SM_RT_ID_MOD_SMSC_USC[2] == "A":
                    if SM_RT_ID_MOD_SMSC_USC[5] == "M" or SM_RT_ID_MOD_SMSC_USC[5] =="U":
                        if SM_RT_ID_MOD_SMSC_USC[6] == "M" or SM_RT_ID_MOD_SMSC_USC[6] =="U":
                            if SM_RT_ID_MOD_SMSC_USC[10] == "Q":
                                if SM_RT_ID_MOD_SMSC_USC[11] == "R":
                                    if SM_RT_ID_MOD_SMSC_USC[16] == "Y":
                                        parts_dict["50159996-320"] = {"Quantity" : get_int(SM_RT_NO_SMSC_USC), "Description": "USC SYSTEM LABEL, SS CABINET, ABU DHABI"}
            #Trace.Write("SM_RT_ID_MOD_SMSC_USC[1] : "+str(SM_RT_ID_MOD_SMSC_USC[1]))
            #Trace.Write("SM_RT_ID_MOD_SMSC_USC[2] : "+str(SM_RT_ID_MOD_SMSC_USC[2]))
            #Trace.Write("SM_RT_ID_MOD_SMSC_USC[5] : "+str(SM_RT_ID_MOD_SMSC_USC[5]))
            #Trace.Write("SM_RT_ID_MOD_SMSC_USC[6] : "+str(SM_RT_ID_MOD_SMSC_USC[6]))
            #Trace.Write("SM_RT_ID_MOD_SMSC_USC[10] : "+str(SM_RT_ID_MOD_SMSC_USC[10]))
            #Trace.Write("SM_RT_ID_MOD_SMSC_USC[11] : "+str(SM_RT_ID_MOD_SMSC_USC[11]))
            #Trace.Write("SM_RT_ID_MOD_SMSC_USC[16] : "+str(SM_RT_ID_MOD_SMSC_USC[16]))
        elif str(SM_RT_SPY_MOD_SMSC_USC) =="No":
            SM_RT_S300 = Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('S300').DisplayValue
            #Trace.Write(SM_RT_S300)
            SM_RT_Cab_MtrlType = Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('Cabinet_Material_Type_Ingress_Protection').DisplayValue
            SM_RT_Amb_Temp = Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('Ambient_Temperature_Range').DisplayValue
            SM_RT_TerAsmly_PUIO = Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('Field_Termination_Assembly_for_PUIO').DisplayValue
            SM_RT_TerAsmly_PDIO = Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('Field_Termination_Assembly_for_PDIO').DisplayValue
            SM_RT_Pwr_Sply = Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('Power_Supply_Type').DisplayValue
            SM_RT_Pwr_Sply_Red = Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('Power_Supply_Redundancy').DisplayValue
            SM_RT_Abu_Dhabi = Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('Abu_Dhabi_Build_Loc').DisplayValue
            #CXCPQ-32148
            if SM_RT_S300 == "Redundant S300":
                parts_dict["FC-SCNT02"] = {'Quantity' : 2 *get_int(SM_RT_NO_SMSC_USC), 'Description': 'SC S300 SAFETY CONTROLLER SIL3'}
            #elif SM_RT_S300 == "Non Redundant S300":
                #parts_dict["FC-SCNT02"] = {'Quantity' : 1 *get_int(SM_RT_NO_SMSC_USC), 'Description': 'SC S300 SAFETY CONTROLLER SIL3'}
            elif SM_RT_S300 == "No S300":
                parts_dict["FC-SCNT02"] = {'Quantity' : 0 *get_int(SM_RT_NO_SMSC_USC), 'Description': 'SC S300 SAFETY CONTROLLER SIL3'}
            Trace.Write("SM_RT_S300 :"+str(SM_RT_S300))
            #CXCPQ-31674
            if SM_RT_Cab_MtrlType == "316L Stainless 1.3M, IP66":   
                if SM_RT_Amb_Temp == "Without Fan, Max Ambient +40°C":
                    if SM_RT_TerAsmly_PUIO == "Default Marshalling FC-TUIO51/52" or SM_RT_TerAsmly_PUIO == "Universal Marshalling, PTA":
                        if SM_RT_TerAsmly_PDIO == "Default Marshalling FC-TDIO51/52" or SM_RT_TerAsmly_PDIO =="Universal Marshalling, PTA":
                            if SM_RT_Pwr_Sply_Red == "Redundant":
                                if SM_RT_Pwr_Sply == "48A FC-PSU-UNI2450U":
                                    if SM_RT_Abu_Dhabi == "No":
                                        parts_dict["50159996-302"] = {"Quantity" : get_int(SM_RT_NO_SMSC_USC), "Description": "USC SYSTEM LABEL, SS CABINET"}
            #CXCPQ-31675
            if SM_RT_Cab_MtrlType == "316L Stainless 1.3M, IP66":
                if SM_RT_Amb_Temp == "With Fan, Max Ambient +55°C":
                    if SM_RT_TerAsmly_PUIO == "Default Marshalling FC-TUIO51/52" or SM_RT_TerAsmly_PUIO == "Universal Marshalling, PTA":
                        if SM_RT_TerAsmly_PDIO == "Default Marshalling FC-TDIO51/52" or SM_RT_TerAsmly_PDIO =="Universal Marshalling, PTA":
                            if SM_RT_Pwr_Sply_Red == "Redundant":
                                if SM_RT_Pwr_Sply == "48A FC-PSU-UNI2450U":
                                    if SM_RT_Abu_Dhabi == "No":
                                        parts_dict["50159996-303"] = {"Quantity" : get_int(SM_RT_NO_SMSC_USC), "Description": "USC SYSTEM LABEL, SS CABINET WITH FANS"}
            #CXCPQ-31676
            if SM_RT_Cab_MtrlType == "316L Stainless 1.3M, IP66":
                if SM_RT_Amb_Temp == "Without Fan, Max Ambient +40°C":
                    if SM_RT_TerAsmly_PUIO == "Default Marshalling FC-TUIO51/52" or SM_RT_TerAsmly_PUIO =="Universal Marshalling, PTA":
                        if SM_RT_TerAsmly_PDIO == "Default Marshalling FC-TDIO51/52" or SM_RT_TerAsmly_PDIO =="Universal Marshalling, PTA":
                            if SM_RT_Pwr_Sply_Red == "Redundant":
                                if SM_RT_Pwr_Sply == "20A AC/DC QUINT 4+ PS":
                                    if SM_RT_Abu_Dhabi == "No":
                                        parts_dict["50159996-304"] = {"Quantity" : get_int(SM_RT_NO_SMSC_USC), "Description": "USC SYSTEM LABEL, SS CABINET"}
            #CXCPQ-31704
            if SM_RT_Cab_MtrlType == "316L Stainless 1.3M, IP66":   
                if SM_RT_Amb_Temp == "Without Fan, Max Ambient +40°C":
                    if SM_RT_TerAsmly_PUIO == "Default Marshalling FC-TUIO51/52" or SM_RT_TerAsmly_PUIO =="Universal Marshalling, PTA":
                        if SM_RT_TerAsmly_PDIO == "Default Marshalling FC-TDIO51/52" or SM_RT_TerAsmly_PDIO =="Universal Marshalling, PTA":
                            if SM_RT_Pwr_Sply_Red == "Redundant":
                                if SM_RT_Pwr_Sply == "24 VDC/DC QUINT 4+ Supply":
                                    if SM_RT_Abu_Dhabi == "Yes":
                                        parts_dict["50159996-322"] = {"Quantity" : get_int(SM_RT_NO_SMSC_USC), "Description": "USC SYSTEM LABEL, SS CABINET, ABU DHABI"}
            #CXCPQ-31702
            if SM_RT_Cab_MtrlType == "316L Stainless 1.3M, IP66":
                if SM_RT_Amb_Temp == "With Fan, Max Ambient +55°C":
                    if SM_RT_TerAsmly_PUIO == "Default Marshalling FC-TUIO51/52" or SM_RT_TerAsmly_PUIO == "Universal Marshalling, PTA":
                        if SM_RT_TerAsmly_PDIO == "Default Marshalling FC-TDIO51/52" or SM_RT_TerAsmly_PDIO =="Universal Marshalling, PTA":
                            if SM_RT_Pwr_Sply_Red == "Redundant":
                                if SM_RT_Pwr_Sply == "20A AC/DC QUINT 4+ PS":
                                    if SM_RT_Abu_Dhabi == "Yes":
                                        parts_dict["50159996-321"] = {"Quantity" : get_int(SM_RT_NO_SMSC_USC), "Description": "USC SYSTEM LABEL, SS CABINET WITH FANS, ABU DHABI"}
            #CXCPQ-31694
            if SM_RT_Cab_MtrlType == "316L Stainless 1.3M, IP66":
                if SM_RT_Amb_Temp == "Without Fan, Max Ambient +40°C":
                    if SM_RT_TerAsmly_PUIO == "Default Marshalling FC-TUIO51/52" or SM_RT_TerAsmly_PUIO =="Universal Marshalling, PTA":
                        if SM_RT_TerAsmly_PDIO == "Default Marshalling FC-TDIO51/52" or SM_RT_TerAsmly_PDIO =="Universal Marshalling, PTA":
                            if SM_RT_Pwr_Sply_Red == "Redundant":
                                if SM_RT_Pwr_Sply == "20A AC/DC QUINT 4+ PS":
                                    if SM_RT_Abu_Dhabi == "Yes":
                                        parts_dict["50159996-320"] = {"Quantity" : get_int(SM_RT_NO_SMSC_USC), "Description": "USC SYSTEM LABEL, SS CABINET, ABU DHABI"}
            #Trace.Write("Cabinet Material Type : "+str(SM_RT_Cab_MtrlType))
            #Trace.Write("Ambient_Temp : "+(SM_RT_Amb_Temp))
            #Trace.Write("TerAsmly_PUIO : "+str(SM_RT_TerAsmly_PUIO))
            #Trace.Write("TerAsmly_PDIO : "+str(SM_RT_TerAsmly_PDIO))
            #Trace.Write("Pwr_Sply_Red : "+str(SM_RT_Pwr_Sply_Red))
            #Trace.Write("Pwr_Sply Type : "+str(SM_RT_Pwr_Sply))
            #Trace.Write("Abu_Dhabi location : "+str(SM_RT_Abu_Dhabi))
    return parts_dict
#func1= get_parts(Product,parts_dict)
#Trace.Write(str(func1))