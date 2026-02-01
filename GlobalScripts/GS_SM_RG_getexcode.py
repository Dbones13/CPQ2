def getexcode(Product,parts_dict):
    if Product.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue=="Universal Safety Cab-1.3M":
        if Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").DisplayValue=="No":
            red=Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("S300").DisplayValue
            ftpuio=Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("Field_Termination_Assembly_for_PUIO").DisplayValue
            ftpdio=Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("Field_Termination_Assembly_for_PDIO").DisplayValue
            puio=Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("PUIO_Count").DisplayValue
            pdio=Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("PDIO_Count").DisplayValue
            iored=Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("IO_Redundancy").DisplayValue
            qty=Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Number_of_SM_SC_1.3M_Universal_Safety_Cabinets_(0-63)").Value
            if qty=="":
                qty=0


            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="Universal Marshalling, PTA")	 and (puio=="32")and (pdio=="0") and (iored=="Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="Universal Marshalling, PTA")	 and (puio=="32")and (pdio=="0") and (iored=="Non Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="Universal Marshalling, PTA")	 and (puio=="64")and (pdio=="0") and (iored=="Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*4  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="32 IS, 32 Non-IS")	 and (puio=="64")and (pdio=="0") and (iored=="Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="Universal Marshalling, PTA")	 and (puio=="64")and (pdio=="0") and (iored=="Non Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*4  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="32 IS, 32 Non-IS")	 and (puio=="64")and (pdio=="0") and (iored=="Non Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*4  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="Universal Marshalling, PTA") and (ftpdio=="Default Marshalling FC-TDIO51/52") and (puio=="32") and (pdio=="32") and (iored=="Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="Universal Marshalling, PTA") and (ftpdio=="Default Marshalling FC-TDIO51/52") and (puio=="32") and (pdio=="32") and (iored=="Non Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="Universal Marshalling, PTA") and (ftpdio=="Default Marshalling FC-TDIO51/52") and (puio=="32") and (pdio=="64") and (iored=="Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="Universal Marshalling, PTA") and (ftpdio=="Default Marshalling FC-TDIO51/52") and (puio=="32") and (pdio=="64") and (iored=="Non Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="Universal Marshalling, PTA") and (ftpdio=="Default Marshalling FC-TDIO51/52") and (puio=="64") and (pdio=="32") and (iored=="Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*4  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="32 IS, 32 Non-IS") and (ftpdio=="Default Marshalling FC-TDIO51/52") and (puio=="64") and (pdio=="32") and (iored=="Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="Universal Marshalling, PTA") and (ftpdio=="Default Marshalling FC-TDIO51/52") and (puio=="64") and (pdio=="32") and (iored=="Non Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*4  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="32 IS, 32 Non-IS") and (ftpdio=="Default Marshalling FC-TDIO51/52") and (puio=="64") and (pdio=="32") and (iored=="Non Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpdio=="Universal Marshalling, PTA")and (puio=="0") and (pdio=="96") and (iored=="Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*6  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpdio=="32 IS, 64 Non-IS")and (puio=="0") and (pdio=="96") and (iored=="Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*4  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpdio=="64 IS, 32 Non-IS")and (puio=="0") and (pdio=="96") and (iored=="Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpdio=="Universal Marshalling, PTA")and (puio=="0") and (pdio=="96") and (iored=="Non Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*6  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpdio=="32 IS, 64 Non-IS")and (puio=="0") and (pdio=="96") and (iored=="Non Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*4  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpdio=="64 IS, 32 Non-IS")and (puio=="0") and (pdio=="96") and (iored=="Non Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="Universal Marshalling, PTA") and (ftpdio=="Universal Marshalling, PTA") and (puio=="32") and (pdio=="64") and (iored=="Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*6  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="Intrinsically Safe") and (ftpdio=="Universal Marshalling, PTA") and (puio=="32") and (pdio=="64") and (iored=="Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*4  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="Universal Marshalling, PTA") and (ftpdio=="Intrinsically Safe") and (puio=="32") and (pdio=="64") and (iored=="Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="Universal Marshalling, PTA") and (ftpdio=="Universal Marshalling, PTA") and (puio=="32") and (pdio=="64") and (iored=="Non Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*6  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="Intrinsically Safe") and (ftpdio=="Universal Marshalling, PTA") and (puio=="32") and (pdio=="64") and (iored=="Non Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*4  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="Universal Marshalling, PTA") and (ftpdio=="Intrinsically Safe") and (puio=="32") and (pdio=="64") and (iored=="Non Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="Default Marshalling FC-TUIO51/52") and (ftpdio=="Universal Marshalling, PTA") and (puio=="64") and (pdio=="32") and (iored=="Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="Default Marshalling FC-TUIO51/52") and (ftpdio=="Universal Marshalling, PTA") and (puio=="64") and (pdio=="32") and (iored=="Non Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="Universal Marshalling, PTA") and (ftpdio=="Universal Marshalling, PTA") and (puio=="64") and (pdio=="32") and (iored=="Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*6  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="Universal Marshalling, PTA") and (ftpdio=="Intrinsically Safe") and (puio=="64") and (pdio=="32") and (iored=="Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*4  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="32 IS, 32 Non-IS") and (ftpdio=="Universal Marshalling, PTA") and (puio=="64") and (pdio=="32") and (iored=="Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="Intrinsically Safe") and (ftpdio=="Universal Marshalling, PTA") and (puio=="64") and (pdio=="32") and (iored=="Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="Universal Marshalling, PTA") and (ftpdio=="Universal Marshalling, PTA") and (puio=="64") and (pdio=="32") and (iored=="Non Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*6  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="Universal Marshalling, PTA") and (ftpdio=="Intrinsically Safe") and (puio=="64") and (pdio=="32") and (iored=="Non Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*4  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="32 IS, 32 Non-IS") and (ftpdio=="Universal Marshalling, PTA") and (puio=="64") and (pdio=="32") and (iored=="Non Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="Intrinsically Safe") and (ftpdio=="Universal Marshalling, PTA") and (puio=="64") and (pdio=="32") and (iored=="Non Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="Default Marshalling FC-TUIO51/52") and (ftpdio=="Universal Marshalling, PTA") and (puio=="32") and (pdio=="32") and (iored=="Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="Default Marshalling FC-TUIO51/52") and (ftpdio=="Universal Marshalling, PTA") and (puio=="32") and (pdio=="32") and (iored=="Non Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpdio=="Universal Marshalling, PTA")and (puio=="0") and (pdio=="32") and (iored=="Redundant IO")	:
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpdio=="Universal Marshalling, PTA")and (puio=="0") and (pdio=="32") and (iored=="Non Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpdio=="Universal Marshalling, PTA")and (puio=="0") and (pdio=="64") and (iored=="Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*4  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpdio=="32 IS, 32 Non-IS")and (puio=="0") and (pdio=="64") and (iored=="Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpdio=="Universal Marshalling, PTA")and (puio=="0") and (pdio=="64") and (iored=="Non Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*4  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpdio=="32 IS, 32 Non-IS")and (puio=="0") and (pdio=="64") and (iored=="Non Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="Universal Marshalling, PTA") and (ftpdio=="Universal Marshalling, PTA") and (puio=="32") and (pdio=="32") and (iored=="Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*4  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="Intrinsically Safe") and (ftpdio=="Universal Marshalling, PTA") and (puio=="32") and (pdio=="32") and (iored=="Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="Universal Marshalling, PTA") and (ftpdio=="Intrinsically Safe") and (puio=="32") and (pdio=="32") and (iored=="Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="Universal Marshalling, PTA") and (ftpdio=="Universal Marshalling, PTA") and (puio=="32") and (pdio=="32") and (iored=="Non Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*4  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="Intrinsically Safe") and (ftpdio=="Universal Marshalling, PTA") and (puio=="32") and (pdio=="32") and (iored=="Non Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="Universal Marshalling, PTA") and (ftpdio=="Intrinsically Safe") and (puio=="32") and (pdio=="32") and (iored=="Non Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="Default Marshalling FC-TUIO51/52") and (ftpdio=="Universal Marshalling, PTA") and (puio=="32") and (pdio=="64") and (iored=="Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*4  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="Default Marshalling FC-TUIO51/52") and (ftpdio=="32 IS, 32 Non-IS") and (puio=="32") and (pdio=="64") and (iored=="Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="Default Marshalling FC-TUIO51/52") and (ftpdio=="Universal Marshalling, PTA") and (puio=="32") and (pdio=="64") and (iored=="Non Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*4  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="Default Marshalling FC-TUIO51/52") and (ftpdio=="32 IS, 32 Non-IS") and (puio=="32") and (pdio=="64") and (iored=="Non Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="Universal Marshalling, PTA")	 and (puio=="96")and (pdio=="0") and (iored=="Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*6  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="32 IS, 64 Non-IS")	 and (puio=="96")and (pdio=="0") and (iored=="Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*4  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="64 IS, 32 Non-IS")	 and (puio=="96")and (pdio=="0") and (iored=="Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="Universal Marshalling, PTA")	 and (puio=="96")and (pdio=="0") and (iored=="Non Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*6  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="32 IS, 64 Non-IS")	 and (puio=="96")and (pdio=="0") and (iored=="Non Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*4  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="Redundant S300" or red=="No S300") and (ftpuio=="64 IS, 32 Non-IS")	 and (puio=="96")and (pdio=="0") and (iored=="Non Redundant IO"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
        
        elif Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").DisplayValue=="Yes":
            code=str(Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").Value)
            red=code[3]
            ftpuio=code[5]
            ftpdio=code[6]
            puio=code[8]
            pdio=code[9]
            iored=code[13]
            qty=Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Number_of_SM_SC_1.3M_Universal_Safety_Cabinets_(0-63)").Value
            if qty=="":
                qty=0


            if (red=="S" or red=="X") and (ftpuio=="U")	 and (puio=="A")and (pdio=="X") and (iored=="R"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="U")	 and (puio=="A")and (pdio=="X") and (iored=="X"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="U")	 and (puio=="B")and (pdio=="X") and (iored=="R"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*4  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="C")	 and (puio=="B")and (pdio=="X") and (iored=="R"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="U")	 and (puio=="B")and (pdio=="X") and (iored=="X"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*4  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="C")	 and (puio=="B")and (pdio=="X") and (iored=="X"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*4  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="U") and (ftpdio=="M") and (puio=="A") and (pdio=="A") and (iored=="R"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="U") and (ftpdio=="M") and (puio=="A") and (pdio=="A") and (iored=="X"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="U") and (ftpdio=="M") and (puio=="A") and (pdio=="B") and (iored=="R"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="U") and (ftpdio=="M") and (puio=="A") and (pdio=="B") and (iored=="X"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="U") and (ftpdio=="M") and (puio=="B") and (pdio=="A") and (iored=="R"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*4  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="U") and (ftpdio=="C") and (puio=="B") and (pdio=="A") and (iored=="R"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="U") and (ftpdio=="M") and (puio=="B") and (pdio=="A") and (iored=="X"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*4  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="C") and (ftpdio=="M") and (puio=="B") and (pdio=="A") and (iored=="X"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpdio=="U")and (puio=="X") and (pdio=="C") and (iored=="R"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*6  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpdio=="A")and (puio=="X") and (pdio=="C") and (iored=="R"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*4  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpdio=="B")and (puio=="X") and (pdio=="C") and (iored=="R"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpdio=="U")and (puio=="X") and (pdio=="C") and (iored=="X"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*6  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpdio=="A")and (puio=="X") and (pdio=="C") and (iored=="X"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*4  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpdio=="B")and (puio=="X") and (pdio=="C") and (iored=="X"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="U") and (ftpdio=="U") and (puio=="A") and (pdio=="B") and (iored=="R"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*6  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="I") and (ftpdio=="U") and (puio=="A") and (pdio=="B") and (iored=="R"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*4  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="U") and (ftpdio=="I") and (puio=="A") and (pdio=="B") and (iored=="R"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="U") and (ftpdio=="U") and (puio=="A") and (pdio=="B") and (iored=="X"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*6  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="I") and (ftpdio=="U") and (puio=="A") and (pdio=="B") and (iored=="X"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*4  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="U") and (ftpdio=="I") and (puio=="A") and (pdio=="B") and (iored=="X"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="M") and (ftpdio=="U") and (puio=="B") and (pdio=="A") and (iored=="R"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="M") and (ftpdio=="U") and (puio=="B") and (pdio=="A") and (iored=="X"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="U") and (ftpdio=="U") and (puio=="B") and (pdio=="A") and (iored=="R"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*6  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="U") and (ftpdio=="I") and (puio=="B") and (pdio=="A") and (iored=="R"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*4  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="C") and (ftpdio=="U") and (puio=="B") and (pdio=="A") and (iored=="R"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="I") and (ftpdio=="U") and (puio=="B") and (pdio=="A") and (iored=="R"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="U") and (ftpdio=="U") and (puio=="B") and (pdio=="A") and (iored=="X"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*6  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="U") and (ftpdio=="I") and (puio=="B") and (pdio=="A") and (iored=="X"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*4  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="C") and (ftpdio=="U") and (puio=="B") and (pdio=="A") and (iored=="X"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="I") and (ftpdio=="U") and (puio=="B") and (pdio=="A") and (iored=="X"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="M") and (ftpdio=="U") and (puio=="A") and (pdio=="A") and (iored=="R"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="M") and (ftpdio=="U") and (puio=="A") and (pdio=="A") and (iored=="X"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpdio=="U")and (puio=="X") and (pdio=="A") and (iored=="R")	:
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpdio=="U")and (puio=="X") and (pdio=="A") and (iored=="X"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpdio=="U")and (puio=="X") and (pdio=="B") and (iored=="R"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*4  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpdio=="C")and (puio=="X") and (pdio=="B") and (iored=="R"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpdio=="U")and (puio=="X") and (pdio=="B") and (iored=="X"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*4  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpdio=="C")and (puio=="X") and (pdio=="B") and (iored=="X"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="U") and (ftpdio=="U") and (puio=="A") and (pdio=="A") and (iored=="R"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*4  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="I") and (ftpdio=="U") and (puio=="A") and (pdio=="A") and (iored=="R"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="U") and (ftpdio=="I") and (puio=="A") and (pdio=="A") and (iored=="R"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="U") and (ftpdio=="U") and (puio=="A") and (pdio=="A") and (iored=="X"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*4  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="I") and (ftpdio=="U") and (puio=="A") and (pdio=="A") and (iored=="X"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="U") and (ftpdio=="I") and (puio=="A") and (pdio=="A") and (iored=="X"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="M") and (ftpdio=="U") and (puio=="A") and (pdio=="B") and (iored=="R"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*4  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="M") and (ftpdio=="C") and (puio=="A") and (pdio=="B") and (iored=="R"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="M") and (ftpdio=="U") and (puio=="A") and (pdio=="B") and (iored=="X"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*4  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="M") and (ftpdio=="C") and (puio=="A") and (pdio=="B") and (iored=="X"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="U")	 and (puio=="C")and (pdio=="X") and (iored=="R"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*6  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="A")	 and (puio=="C")and (pdio=="X") and (iored=="R"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*4  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="B")	 and (puio=="C")and (pdio=="X") and (iored=="R"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="U")	 and (puio=="C")and (pdio=="X") and (iored=="X"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*6  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="A")	 and (puio=="C")and (pdio=="X") and (iored=="X"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*4  , 'Description': 'SCA-Signal Condition Assembly 24V'}
            if (red=="S" or red=="X") and (ftpuio=="B")	 and (puio=="C")and (pdio=="X") and (iored=="X"):
                parts_dict["FC-USCA01"] = {'Quantity' : int(qty)*2  , 'Description': 'SCA-Signal Condition Assembly 24V'}
    return parts_dict