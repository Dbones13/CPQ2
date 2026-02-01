import math as m
#parts_dict={}
def get_int(val):
    if val:
        return int(val)
    return 0
def get_MODID(Product,parts_dict):
    if Product.Name == "SM Remote Group":
        Enclosure_Type = Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0].GetColumnByName('Enclosure_Type').DisplayValue
        if Enclosure_Type == "Universal Safety Cab-1.3M":
            Enclosure_Type = Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0].GetColumnByName('Enclosure_Type').DisplayValue
            #Trace.Write(Enclosure_Type)
            SM_RT_SPY_MOD_SMSC_USC = Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont').Rows[0].GetColumnByName('Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet').DisplayValue
            #Trace.Write(SM_RT_SPY_MOD_SMSC_USC)
            SM_RT_ID_MOD_SMSC_USC = Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont').Rows[0].GetColumnByName('Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet').Value
            #Trace.Write(SM_RT_ID_MOD_SMSC_USC)
            SM_RT_NO_SMSC_USC = Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont').Rows[0].GetColumnByName('Number_of_SM_SC_1.3M_Universal_Safety_Cabinets_(0-63)').Value
            #Trace.Write(SM_RT_NO_SMSC_USC)
            if str(SM_RT_SPY_MOD_SMSC_USC) =="Yes":
                #CXCPQ-34295
                #No.1
                if SM_RT_ID_MOD_SMSC_USC[3] == "S" or SM_RT_ID_MOD_SMSC_USC[3] == "X" or SM_RT_ID_MOD_SMSC_USC[3] == "N":
                    if SM_RT_ID_MOD_SMSC_USC[5] == "U" or SM_RT_ID_MOD_SMSC_USC[5] == "I" or SM_RT_ID_MOD_SMSC_USC[5] == "C":
                        if SM_RT_ID_MOD_SMSC_USC[6] == "M":
                            if SM_RT_ID_MOD_SMSC_USC[8] == "B":
                                if SM_RT_ID_MOD_SMSC_USC[9] == "A":
                                    if SM_RT_ID_MOD_SMSC_USC[13] == "X":
                                        parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #No.2
                if SM_RT_ID_MOD_SMSC_USC[3] == "S" or SM_RT_ID_MOD_SMSC_USC[3] == "X":
                    if SM_RT_ID_MOD_SMSC_USC[5] == "U" or SM_RT_ID_MOD_SMSC_USC[5] == "I" or SM_RT_ID_MOD_SMSC_USC[5] == "C":
                        if SM_RT_ID_MOD_SMSC_USC[8] == "B":
                            if SM_RT_ID_MOD_SMSC_USC[9] == "X":
                                if SM_RT_ID_MOD_SMSC_USC[13] == "R":
                                    parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #No.3
                if SM_RT_ID_MOD_SMSC_USC[3] == "S" or SM_RT_ID_MOD_SMSC_USC[3] == "X" or SM_RT_ID_MOD_SMSC_USC[3] == "N":
                    if SM_RT_ID_MOD_SMSC_USC[5] == "U" or SM_RT_ID_MOD_SMSC_USC[5] == "I" or SM_RT_ID_MOD_SMSC_USC[5] == "C":
                        if SM_RT_ID_MOD_SMSC_USC[8] == "B":
                            if SM_RT_ID_MOD_SMSC_USC[9] == "X":
                                if SM_RT_ID_MOD_SMSC_USC[13] == "X":
                                    parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #No.4
                if SM_RT_ID_MOD_SMSC_USC[3] == "S" or SM_RT_ID_MOD_SMSC_USC[3] == "X":
                    if SM_RT_ID_MOD_SMSC_USC[5] == "U" or SM_RT_ID_MOD_SMSC_USC[5] == "I":
                        if SM_RT_ID_MOD_SMSC_USC[6] == "M":
                            if SM_RT_ID_MOD_SMSC_USC[8] == "A":
                                if SM_RT_ID_MOD_SMSC_USC[9] == "A":
                                    if SM_RT_ID_MOD_SMSC_USC[13] == "R":
                                        parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #No.5
                if SM_RT_ID_MOD_SMSC_USC[3] == "S" or SM_RT_ID_MOD_SMSC_USC[3] == "X" or SM_RT_ID_MOD_SMSC_USC[3] == "N":
                    if SM_RT_ID_MOD_SMSC_USC[5] == "U" or SM_RT_ID_MOD_SMSC_USC[5] == "I":
                        if SM_RT_ID_MOD_SMSC_USC[6] == "M":
                            if SM_RT_ID_MOD_SMSC_USC[8] == "A":
                                if SM_RT_ID_MOD_SMSC_USC[9] == "A":
                                    if SM_RT_ID_MOD_SMSC_USC[13] == "X":
                                        parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #No.6
                if SM_RT_ID_MOD_SMSC_USC[3] == "S" or SM_RT_ID_MOD_SMSC_USC[3] == "X":
                    if SM_RT_ID_MOD_SMSC_USC[5] == "U" or SM_RT_ID_MOD_SMSC_USC[5] == "I" or SM_RT_ID_MOD_SMSC_USC[5] == "C":
                        if SM_RT_ID_MOD_SMSC_USC[6] == "M":
                            if SM_RT_ID_MOD_SMSC_USC[8] == "B":
                                if SM_RT_ID_MOD_SMSC_USC[9] == "A":
                                    if SM_RT_ID_MOD_SMSC_USC[13] == "R":
                                        parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #No.7
                if SM_RT_ID_MOD_SMSC_USC[3] == "S" or SM_RT_ID_MOD_SMSC_USC[3] == "X":
                    if SM_RT_ID_MOD_SMSC_USC[6] == "U" or SM_RT_ID_MOD_SMSC_USC[6] == "I" or SM_RT_ID_MOD_SMSC_USC[6] == "A" or SM_RT_ID_MOD_SMSC_USC[6] == "B":
                        if SM_RT_ID_MOD_SMSC_USC[8] == "X":
                            if SM_RT_ID_MOD_SMSC_USC[9] == "C":
                                if SM_RT_ID_MOD_SMSC_USC[13] == "R":
                                    parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #No.8
                if SM_RT_ID_MOD_SMSC_USC[3] == "S" or SM_RT_ID_MOD_SMSC_USC[3] == "X" or SM_RT_ID_MOD_SMSC_USC[3] == "N":
                    if SM_RT_ID_MOD_SMSC_USC[6] == "U" or SM_RT_ID_MOD_SMSC_USC[6] == "I" or SM_RT_ID_MOD_SMSC_USC[6] == "A" or SM_RT_ID_MOD_SMSC_USC[6] == "B":
                        if SM_RT_ID_MOD_SMSC_USC[8] == "X":
                            if SM_RT_ID_MOD_SMSC_USC[9] == "C":
                                if SM_RT_ID_MOD_SMSC_USC[13] == "X":
                                    parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #No.9
                if SM_RT_ID_MOD_SMSC_USC[3] == "S" or SM_RT_ID_MOD_SMSC_USC[3] == "X":
                    if SM_RT_ID_MOD_SMSC_USC[5] == "U" or SM_RT_ID_MOD_SMSC_USC[5] == "I":
                        if SM_RT_ID_MOD_SMSC_USC[6] == "U" or SM_RT_ID_MOD_SMSC_USC[6] == "I" or SM_RT_ID_MOD_SMSC_USC[6] == "C":
                            if SM_RT_ID_MOD_SMSC_USC[8] == "A":
                                if SM_RT_ID_MOD_SMSC_USC[9] == "B":
                                    if SM_RT_ID_MOD_SMSC_USC[13] == "R":
                                        parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #No.10
                if SM_RT_ID_MOD_SMSC_USC[3] == "S" or SM_RT_ID_MOD_SMSC_USC[3] == "X" or SM_RT_ID_MOD_SMSC_USC[3] == "N":
                    if SM_RT_ID_MOD_SMSC_USC[5] == "U" or SM_RT_ID_MOD_SMSC_USC[5] == "I":
                        if SM_RT_ID_MOD_SMSC_USC[6] == "U" or SM_RT_ID_MOD_SMSC_USC[6] == "I" or SM_RT_ID_MOD_SMSC_USC[6] == "C":
                            if SM_RT_ID_MOD_SMSC_USC[8] == "A":
                                if SM_RT_ID_MOD_SMSC_USC[9] == "B":
                                    if SM_RT_ID_MOD_SMSC_USC[13] == "X":
                                        parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #No.11
                if SM_RT_ID_MOD_SMSC_USC[3] == "S" or SM_RT_ID_MOD_SMSC_USC[3] == "X" :
                    if SM_RT_ID_MOD_SMSC_USC[5] == "U" or SM_RT_ID_MOD_SMSC_USC[5] == "I" or SM_RT_ID_MOD_SMSC_USC[5] == "C":
                        if SM_RT_ID_MOD_SMSC_USC[6] == "U" or SM_RT_ID_MOD_SMSC_USC[6] == "I":
                            if SM_RT_ID_MOD_SMSC_USC[8] == "B":
                                if SM_RT_ID_MOD_SMSC_USC[9] == "A":
                                    if SM_RT_ID_MOD_SMSC_USC[13] == "R":
                                        parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #No.12
                if SM_RT_ID_MOD_SMSC_USC[3] == "S" or SM_RT_ID_MOD_SMSC_USC[3] == "X" or SM_RT_ID_MOD_SMSC_USC[3] == "N" :
                    if SM_RT_ID_MOD_SMSC_USC[5] == "U" or SM_RT_ID_MOD_SMSC_USC[5] == "I" or SM_RT_ID_MOD_SMSC_USC[5] == "C":
                        if SM_RT_ID_MOD_SMSC_USC[6] == "U" or SM_RT_ID_MOD_SMSC_USC[6] == "I":
                            if SM_RT_ID_MOD_SMSC_USC[8] == "B":
                                if SM_RT_ID_MOD_SMSC_USC[9] == "A":
                                    if SM_RT_ID_MOD_SMSC_USC[13] == "X":
                                        parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #No.13
                if SM_RT_ID_MOD_SMSC_USC[3] == "S" or SM_RT_ID_MOD_SMSC_USC[3] == "X":
                    if SM_RT_ID_MOD_SMSC_USC[5] == "M":
                        if SM_RT_ID_MOD_SMSC_USC[6] == "U":
                            if SM_RT_ID_MOD_SMSC_USC[8] == "A":
                                if SM_RT_ID_MOD_SMSC_USC[9] == "A":
                                    if SM_RT_ID_MOD_SMSC_USC[13] == "R":
                                        parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #No.14
                if SM_RT_ID_MOD_SMSC_USC[3] == "S" or SM_RT_ID_MOD_SMSC_USC[3] == "X" or SM_RT_ID_MOD_SMSC_USC[3] == "N" :
                    if SM_RT_ID_MOD_SMSC_USC[5] == "M":
                        if SM_RT_ID_MOD_SMSC_USC[6] == "U":
                            if SM_RT_ID_MOD_SMSC_USC[8] == "A":
                                if SM_RT_ID_MOD_SMSC_USC[9] == "A":
                                    if SM_RT_ID_MOD_SMSC_USC[13] == "X":
                                        parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #No.15
                if SM_RT_ID_MOD_SMSC_USC[3] == "S" or SM_RT_ID_MOD_SMSC_USC[3] == "X":
                    if SM_RT_ID_MOD_SMSC_USC[6] == "U" or SM_RT_ID_MOD_SMSC_USC[6] == "I" or SM_RT_ID_MOD_SMSC_USC[6] == "C":
                        if SM_RT_ID_MOD_SMSC_USC[8] == "X":
                            if SM_RT_ID_MOD_SMSC_USC[9] == "B":
                                if SM_RT_ID_MOD_SMSC_USC[13] == "R":
                                    parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #No.16
                if SM_RT_ID_MOD_SMSC_USC[3] == "S" or SM_RT_ID_MOD_SMSC_USC[3] == "X" or SM_RT_ID_MOD_SMSC_USC[3] == "N" :
                    if SM_RT_ID_MOD_SMSC_USC[6] == "U" or SM_RT_ID_MOD_SMSC_USC[6] == "I" or SM_RT_ID_MOD_SMSC_USC[6] == "C":
                        if SM_RT_ID_MOD_SMSC_USC[8] == "X":
                            if SM_RT_ID_MOD_SMSC_USC[9] == "B":
                                if SM_RT_ID_MOD_SMSC_USC[13] == "X":
                                    parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #No.17
                if SM_RT_ID_MOD_SMSC_USC[3] == "S" or SM_RT_ID_MOD_SMSC_USC[3] == "X":
                    if SM_RT_ID_MOD_SMSC_USC[5] == "U" or SM_RT_ID_MOD_SMSC_USC[5] == "I":
                        if SM_RT_ID_MOD_SMSC_USC[6] == "U" or SM_RT_ID_MOD_SMSC_USC[6] == "I":
                            if SM_RT_ID_MOD_SMSC_USC[8] == "A":
                                if SM_RT_ID_MOD_SMSC_USC[9] == "A":
                                    if SM_RT_ID_MOD_SMSC_USC[13] == "R":
                                        parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #No.18
                if SM_RT_ID_MOD_SMSC_USC[3] == "S" or SM_RT_ID_MOD_SMSC_USC[3] == "X" or SM_RT_ID_MOD_SMSC_USC[3] == "N" :
                    if SM_RT_ID_MOD_SMSC_USC[5] == "U" or SM_RT_ID_MOD_SMSC_USC[5] == "I":
                        if SM_RT_ID_MOD_SMSC_USC[6] == "U" or SM_RT_ID_MOD_SMSC_USC[6] == "I":
                            if SM_RT_ID_MOD_SMSC_USC[8] == "A":
                                if SM_RT_ID_MOD_SMSC_USC[9] == "A":
                                    if SM_RT_ID_MOD_SMSC_USC[13] == "X":
                                        parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #No.19
                if SM_RT_ID_MOD_SMSC_USC[3] == "S" or SM_RT_ID_MOD_SMSC_USC[3] == "X":
                    if SM_RT_ID_MOD_SMSC_USC[5] == "M":
                        if SM_RT_ID_MOD_SMSC_USC[6] == "U" or SM_RT_ID_MOD_SMSC_USC[6] == "I" or SM_RT_ID_MOD_SMSC_USC[6] == "C":
                            if SM_RT_ID_MOD_SMSC_USC[8] == "A":
                                if SM_RT_ID_MOD_SMSC_USC[9] == "B":
                                    if SM_RT_ID_MOD_SMSC_USC[13] == "R":
                                        parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #No.20
                if SM_RT_ID_MOD_SMSC_USC[3] == "S" or SM_RT_ID_MOD_SMSC_USC[3] == "X" or SM_RT_ID_MOD_SMSC_USC[3] == "N":
                    if SM_RT_ID_MOD_SMSC_USC[5] == "M":
                        if SM_RT_ID_MOD_SMSC_USC[6] == "U" or SM_RT_ID_MOD_SMSC_USC[6] == "I" or SM_RT_ID_MOD_SMSC_USC[6] == "C":
                            if SM_RT_ID_MOD_SMSC_USC[8] == "A":
                                if SM_RT_ID_MOD_SMSC_USC[9] == "B":
                                    if SM_RT_ID_MOD_SMSC_USC[13] == "X":
                                        parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #No.21
                if SM_RT_ID_MOD_SMSC_USC[3] == "S" or SM_RT_ID_MOD_SMSC_USC[3] == "X":
                    if SM_RT_ID_MOD_SMSC_USC[5] == "U" or SM_RT_ID_MOD_SMSC_USC[5] == "I" or SM_RT_ID_MOD_SMSC_USC[5] == "A" or SM_RT_ID_MOD_SMSC_USC[5] == "B":
                        if SM_RT_ID_MOD_SMSC_USC[8] == "C":
                            if SM_RT_ID_MOD_SMSC_USC[9] == "X":
                                if SM_RT_ID_MOD_SMSC_USC[13] == "R":
                                    parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #No.22
                if SM_RT_ID_MOD_SMSC_USC[3] == "S" or SM_RT_ID_MOD_SMSC_USC[3] == "X" or SM_RT_ID_MOD_SMSC_USC[3] == "N":
                    if SM_RT_ID_MOD_SMSC_USC[5] == "U" or SM_RT_ID_MOD_SMSC_USC[5] == "I" or SM_RT_ID_MOD_SMSC_USC[5] == "A" or SM_RT_ID_MOD_SMSC_USC[5] == "B":
                        if SM_RT_ID_MOD_SMSC_USC[8] == "C":
                            if SM_RT_ID_MOD_SMSC_USC[9] == "X":
                                if SM_RT_ID_MOD_SMSC_USC[13] == "X":
                                    parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
            elif str(SM_RT_SPY_MOD_SMSC_USC) =="No":
                SM_RT_S300 = Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('S300').DisplayValue
                SM_RT_TerAsmly_PUIO = Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('Field_Termination_Assembly_for_PUIO').DisplayValue
                SM_RT_TerAsmly_PDIO = Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('Field_Termination_Assembly_for_PDIO').DisplayValue
                SM_RT_PUIO = Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('PUIO_Count').DisplayValue
                SM_RT_PDIO = Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('PDIO_Count').DisplayValue
                SM_RT_IORed = Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('IO_Redundancy').DisplayValue
                #CXCPQ-34293
                #No.1
                if SM_RT_S300 == "Redundant S300" or SM_RT_S300 == "No S300" or SM_RT_S300 == "Non Redundant S300":
                    if SM_RT_TerAsmly_PUIO == "Universal Marshalling, PTA" or SM_RT_TerAsmly_PUIO == "Intrinsically Safe" or SM_RT_TerAsmly_PUIO == "32 IS, 32 Non-IS":
                        if SM_RT_TerAsmly_PDIO == "Default Marshalling FC-TDIO51/52":
                            if SM_RT_PUIO == "64":
                                if SM_RT_PDIO == "32":
                                    if SM_RT_IORed == "Non Redundant IO":
                                        parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #No.2
                if SM_RT_S300 == "Redundant S300" or SM_RT_S300 == "No S300":
                    if SM_RT_TerAsmly_PUIO == "Universal Marshalling, PTA" or SM_RT_TerAsmly_PUIO == "Intrinsically Safe" or SM_RT_TerAsmly_PUIO == "32 IS, 32 Non-IS":
                        if SM_RT_PUIO == "64":
                            if SM_RT_PDIO == "0":
                                if SM_RT_IORed == "Redundant IO":
                                    parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #No.3
                if SM_RT_S300 == "Redundant S300" or SM_RT_S300 == "No S300" or SM_RT_S300 == "Non Redundant S300":
                    if SM_RT_TerAsmly_PUIO == "Universal Marshalling, PTA" or SM_RT_TerAsmly_PUIO == "Intrinsically Safe" or SM_RT_TerAsmly_PUIO == "32 IS, 32 Non-IS":
                        if SM_RT_PUIO == "64":
                            if SM_RT_PDIO == "0":
                                if SM_RT_IORed == "Non Redundant IO":
                                    parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #No.4
                if SM_RT_S300 == "Redundant S300" or SM_RT_S300 == "No S300":
                    if SM_RT_TerAsmly_PUIO == "Universal Marshalling, PTA" or SM_RT_TerAsmly_PUIO == "Intrinsically Safe":
                        if SM_RT_TerAsmly_PDIO == "Default Marshalling FC-TDIO51/52":
                            if SM_RT_PUIO == "32":
                                if SM_RT_PDIO == "32":
                                    if SM_RT_IORed == "Redundant IO":
                                        parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #No.5
                if SM_RT_S300 == "Redundant S300" or SM_RT_S300 == "No S300" or SM_RT_S300 == "Non Redundant S300":
                    if SM_RT_TerAsmly_PUIO == "Universal Marshalling, PTA" or SM_RT_TerAsmly_PUIO == "Intrinsically Safe":
                        if SM_RT_TerAsmly_PDIO == "Default Marshalling FC-TDIO51/52":
                            if SM_RT_PUIO == "32":
                                if SM_RT_PDIO == "32":
                                    if SM_RT_IORed == "Non Redundant IO":
                                        parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #No.6
                if SM_RT_S300 == "Redundant S300" or SM_RT_S300 == "No S300":
                    if SM_RT_TerAsmly_PUIO == "Universal Marshalling, PTA" or SM_RT_TerAsmly_PUIO == "Intrinsically Safe" or SM_RT_TerAsmly_PUIO == "32 IS, 32 Non-IS":
                        if SM_RT_TerAsmly_PDIO == "Default Marshalling FC-TDIO51/52":
                            if SM_RT_PUIO == "64":
                                if SM_RT_PDIO == "32":
                                    if SM_RT_IORed == "Redundant IO":
                                        parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #No.7
                if SM_RT_S300 == "Redundant S300" or SM_RT_S300 == "No S300":
                    if SM_RT_TerAsmly_PDIO == "Universal Marshalling, PTA" or SM_RT_TerAsmly_PDIO == "Intrinsically Safe" or SM_RT_TerAsmly_PDIO == "32 IS, 64 Non-IS" or SM_RT_TerAsmly_PDIO == "64 IS, 32 Non-IS":
                        if SM_RT_PUIO == "0":
                            if SM_RT_PDIO == "96":
                                if SM_RT_IORed == "Redundant IO":
                                    parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #No.8
                if SM_RT_S300 == "Redundant S300" or SM_RT_S300 == "No S300" or SM_RT_S300 == "Non Redundant S300":
                    if SM_RT_TerAsmly_PDIO == "Universal Marshalling, PTA" or SM_RT_TerAsmly_PDIO == "Intrinsically Safe" or SM_RT_TerAsmly_PDIO == "32 IS, 64 Non-IS" or SM_RT_TerAsmly_PDIO == "64 IS, 32 Non-IS":
                        if SM_RT_PUIO == "0":
                            if SM_RT_PDIO == "96":
                                if SM_RT_IORed == "Non Redundant IO":
                                    parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #No.9
                if SM_RT_S300 == "Redundant S300" or SM_RT_S300 == "No S300":
                    if SM_RT_TerAsmly_PUIO == "Universal Marshalling, PTA" or SM_RT_TerAsmly_PUIO == "Intrinsically Safe":
                        if SM_RT_TerAsmly_PDIO == "Universal Marshalling, PTA" or SM_RT_TerAsmly_PDIO == "Intrinsically Safe" or SM_RT_TerAsmly_PDIO == "32 IS, 32 Non-IS":
                            if SM_RT_PUIO == "32":
                                if SM_RT_PDIO == "64":
                                    if SM_RT_IORed == "Redundant IO":
                                        parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #No.10
                if SM_RT_S300 == "Redundant S300" or SM_RT_S300 == "No S300" or SM_RT_S300 == "Non Redundant S300":
                    if SM_RT_TerAsmly_PUIO == "Universal Marshalling, PTA" or SM_RT_TerAsmly_PUIO == "Intrinsically Safe":
                        if SM_RT_TerAsmly_PDIO == "Universal Marshalling, PTA" or SM_RT_TerAsmly_PDIO == "Intrinsically Safe" or SM_RT_TerAsmly_PDIO == "32 IS, 32 Non-IS":
                            if SM_RT_PUIO == "32":
                                if SM_RT_PDIO == "64":
                                    if SM_RT_IORed == "Non Redundant IO":
                                        parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #No.11
                if SM_RT_S300 == "Redundant S300" or SM_RT_S300 == "No S300":
                    if SM_RT_TerAsmly_PUIO == "Universal Marshalling, PTA" or SM_RT_TerAsmly_PUIO == "Intrinsically Safe" or SM_RT_TerAsmly_PUIO == "32 IS, 32 Non-IS":
                        if SM_RT_TerAsmly_PDIO == "Universal Marshalling, PTA" or SM_RT_TerAsmly_PDIO == "Intrinsically Safe":
                            if SM_RT_PUIO == "64":
                                if SM_RT_PDIO == "32":
                                    if SM_RT_IORed == "Redundant IO":
                                        parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #No.12
                if SM_RT_S300 == "Redundant S300" or SM_RT_S300 == "No S300" or SM_RT_S300 == "Non Redundant S300":
                    if SM_RT_TerAsmly_PUIO == "Universal Marshalling, PTA" or SM_RT_TerAsmly_PUIO == "Intrinsically Safe" or SM_RT_TerAsmly_PUIO == "32 IS, 32 Non-IS":
                        if SM_RT_TerAsmly_PDIO == "Universal Marshalling, PTA" or SM_RT_TerAsmly_PDIO == "Intrinsically Safe":
                            if SM_RT_PUIO == "64":
                                if SM_RT_PDIO == "32":
                                    if SM_RT_IORed == "Non Redundant IO":
                                        parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                 #No.13
                if SM_RT_S300 == "Redundant S300" or SM_RT_S300 == "No S300":
                    if SM_RT_TerAsmly_PUIO == "Default Marshalling FC-TUIO51/52":
                        if SM_RT_TerAsmly_PDIO == "Universal Marshalling, PTA":
                            if SM_RT_PUIO == "32":
                                if SM_RT_PDIO == "32":
                                    if SM_RT_IORed == "Redundant IO":
                                        parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                 #No.14
                if SM_RT_S300 == "Redundant S300" or SM_RT_S300 == "No S300" or SM_RT_S300 == "Non Redundant S300":
                    if SM_RT_TerAsmly_PUIO == "Default Marshalling FC-TUIO51/52":
                        if SM_RT_TerAsmly_PDIO == "Universal Marshalling, PTA":
                            if SM_RT_PUIO == "32":
                                if SM_RT_PDIO == "32":
                                    if SM_RT_IORed == "Non Redundant IO":
                                        parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                 #No.15
                if SM_RT_S300 == "Redundant S300" or SM_RT_S300 == "No S300":
                    if SM_RT_TerAsmly_PDIO == "Universal Marshalling, PTA" or SM_RT_TerAsmly_PDIO == "Intrinsically Safe" or SM_RT_TerAsmly_PDIO == "32 IS, 32 Non-IS" :
                        if SM_RT_PUIO == "0":
                            if SM_RT_PDIO == "64":
                                if SM_RT_IORed == "Redundant IO":
                                    parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                 #No.16
                if SM_RT_S300 == "Redundant S300" or SM_RT_S300 == "No S300" or SM_RT_S300 == "Non Redundant S300":
                    if SM_RT_TerAsmly_PDIO == "Universal Marshalling, PTA" or SM_RT_TerAsmly_PDIO == "Intrinsically Safe" or SM_RT_TerAsmly_PDIO == "32 IS, 32 Non-IS":
                        if SM_RT_PUIO == "0":
                            if SM_RT_PDIO == "64":
                                if SM_RT_IORed == "Non Redundant IO":
                                    parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #No.17
                if SM_RT_S300 == "Redundant S300" or SM_RT_S300 == "No S300":
                    if SM_RT_TerAsmly_PUIO == "Universal Marshalling, PTA" or SM_RT_TerAsmly_PUIO == "Intrinsically Safe":
                        if SM_RT_TerAsmly_PDIO == "Universal Marshalling, PTA" or SM_RT_TerAsmly_PDIO == "Intrinsically Safe":
                            if SM_RT_PUIO == "32":
                                if SM_RT_PDIO == "32":
                                    if SM_RT_IORed == "Redundant IO":
                                        parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #No.18
                if SM_RT_S300 == "Redundant S300" or SM_RT_S300 == "No S300" or SM_RT_S300 == "Non Redundant S300":
                    if SM_RT_TerAsmly_PUIO == "Universal Marshalling, PTA" or SM_RT_TerAsmly_PUIO == "Intrinsically Safe":
                        if SM_RT_TerAsmly_PDIO == "Universal Marshalling, PTA" or SM_RT_TerAsmly_PDIO == "Intrinsically Safe":
                            if SM_RT_PUIO == "32":
                                if SM_RT_PDIO == "32":
                                    if SM_RT_IORed == "Non Redundant IO":
                                        parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #No.19
                if SM_RT_S300 == "Redundant S300" or SM_RT_S300 == "No S300":
                    if SM_RT_TerAsmly_PUIO == "Default Marshalling FC-TUIO51/52":
                        if SM_RT_TerAsmly_PDIO == "Universal Marshalling, PTA" or SM_RT_TerAsmly_PDIO == "Intrinsically Safe" or SM_RT_TerAsmly_PDIO == "32 IS, 32 Non-IS":
                           if SM_RT_PUIO == "32":
                                if SM_RT_PDIO == "64":
                                    if SM_RT_IORed == "Redundant IO":
                                        parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #No.20
                if SM_RT_S300 == "Redundant S300" or SM_RT_S300 == "No S300" or SM_RT_S300 == "Non Redundant S300":
                    if SM_RT_TerAsmly_PUIO == "Default Marshalling FC-TUIO51/52":
                        if SM_RT_TerAsmly_PDIO == "Universal Marshalling, PTA" or SM_RT_TerAsmly_PDIO == "Intrinsically Safe" or SM_RT_TerAsmly_PDIO == "32 IS, 32 Non-IS":
                            if SM_RT_PUIO == "32":
                                if SM_RT_PDIO == "64":
                                    if SM_RT_IORed == "Non Redundant IO":
                                        parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #No.21
                if SM_RT_S300 == "Redundant S300" or SM_RT_S300 == "No S300":
                    if SM_RT_TerAsmly_PUIO == "Universal Marshalling, PTA" or SM_RT_TerAsmly_PUIO == "Intrinsically Safe" or SM_RT_TerAsmly_PUIO == "32 IS, 64 Non-IS" or SM_RT_TerAsmly_PUIO == "64 IS, 32 Non-IS":
                        if SM_RT_PUIO == "96":
                            if SM_RT_PDIO == "0":
                                if SM_RT_IORed == "Redundant IO":
                                    parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #No.22
                if SM_RT_S300 == "Redundant S300" or SM_RT_S300 == "No S300" or SM_RT_S300 == "Non Redundant S300":
                    if SM_RT_TerAsmly_PUIO == "Universal Marshalling, PTA" or SM_RT_TerAsmly_PUIO == "Intrinsically Safe" or SM_RT_TerAsmly_PUIO == "32 IS, 64 Non-IS" or SM_RT_TerAsmly_PUIO == "64 IS, 32 Non-IS":
                        if SM_RT_PUIO == "96":
                            if SM_RT_PDIO == "0":
                                if SM_RT_IORed == "Non Redundant IO":
                                    parts_dict["FC-SIC5010"] = {"Quantity" : 2 * get_int(SM_RT_NO_SMSC_USC), "Description": "SCA 37 POS. SUB-D SIC CABLE, L 1.0M / SC SIC CABLE 2XCONNECTOR L1.0M"}
                #Trace.Write(SM_RT_S300)
                #Trace.Write(SM_RT_TerAsmly_PUIO)
                #Trace.Write(SM_RT_TerAsmly_PDIO)
                #Trace.Write(SM_RT_PUIO)
                #Trace.Write(SM_RT_PDIO)
                #Trace.Write(SM_RT_IORed)
    return parts_dict
#fun = get_MODID(Product,parts_dict)
#Trace.Write ("Final Value :"+str(fun))