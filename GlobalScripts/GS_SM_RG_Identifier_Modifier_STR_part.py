#CXCPQ-34319 ADDED BY LAHU
def get_identifier_Boot(Product,parts_dict):
    Enclosure_Type=Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0].GetColumnByName('Enclosure_Type').DisplayValue
    if Enclosure_Type == "Universal Safety Cab-1.3M":
        Specify_Identifier=Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont').Rows[0].GetColumnByName('Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet').DisplayValue
        Material_Type_Ingress=Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('Cabinet_Material_Type_Ingress_Protection').DisplayValue
        S300=Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('S300').DisplayValue
        PUIO_Count=Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('PUIO_Count').DisplayValue
        PDIO_Count=Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('PDIO_Count').DisplayValue
        IO_Redundancy=Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('IO_Redundancy').DisplayValue
        Power_Supply_Type=Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('Power_Supply_Type').DisplayValue
        Power_Supply_Redundancy=Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('Power_Supply_Redundancy').DisplayValue
        Ambient_Temperature_Range=Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('Ambient_Temperature_Range').DisplayValue
        Field_for_PUIO=Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('Field_Termination_Assembly_for_PUIO').DisplayValue
        Field_for_PDIO=Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('Field_Termination_Assembly_for_PDIO').DisplayValue
        Abu_Dhabi=Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('Abu_Dhabi_Build_Loc').DisplayValue
        try:
            Identifier_Modifier=Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont').Rows[0].GetColumnByName('Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet').Value
            Trace.Write(Identifier_Modifier)
        except:
            Identifier_Modifier=0
        Safety_Cabinets_qnt=Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont').Rows[0].GetColumnByName('Number_of_SM_SC_1.3M_Universal_Safety_Cabinets_(0-63)').Value
        if Safety_Cabinets_qnt !='':
            Safety_Cabinets_qnt=int(Safety_Cabinets_qnt)
        else:
            Safety_Cabinets_qnt=0
        if len(Identifier_Modifier)>20 and Specify_Identifier=="Yes" and Safety_Cabinets_qnt >0:
            var1=0
            if (Identifier_Modifier[3]=="S" or Identifier_Modifier[3]=="X") and Identifier_Modifier[13]=="X":
                if Identifier_Modifier[5]=="M" and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="X": #1
                    var1= Safety_Cabinets_qnt * 1
                elif (Identifier_Modifier[5]=="M") and Identifier_Modifier[8]=="B" and Identifier_Modifier[9]=="X": #2
                    var1= Safety_Cabinets_qnt * 2
                elif Identifier_Modifier[5]=="M" and Identifier_Modifier[6]=="M" and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="A": #3
                    var1= Safety_Cabinets_qnt * 1
                elif Identifier_Modifier[5]=="M" and Identifier_Modifier[6]=="M" and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="B": #4
                    var1= Safety_Cabinets_qnt * 1
                elif Identifier_Modifier[5]=="M" and Identifier_Modifier[6]=="M" and Identifier_Modifier[8]=="B" and Identifier_Modifier[9]=="A": #5
                    var1= Safety_Cabinets_qnt * 2
                elif Identifier_Modifier[5]=="M" and Identifier_Modifier[8]=="C" and Identifier_Modifier[9]=="X": #6
                    var1= Safety_Cabinets_qnt * 3
                if (Identifier_Modifier[5]=="U" or Identifier_Modifier[5]=="I") and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="X": #7
                    var1= Safety_Cabinets_qnt * 1
                if (Identifier_Modifier[5]=="U" or Identifier_Modifier[5]=="I" or Identifier_Modifier[5]=="C") and Identifier_Modifier[8]=="B" and Identifier_Modifier[9]=="X": #8
                    var1= Safety_Cabinets_qnt * 2
                if (Identifier_Modifier[5]=="U" or Identifier_Modifier[5]=="I") and Identifier_Modifier[6]=="M" and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="A": #9
                    var1= Safety_Cabinets_qnt * 1
                if (Identifier_Modifier[5]=="U" or Identifier_Modifier[5]=="I") and Identifier_Modifier[6]=="M" and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="B": #10
                    var1= Safety_Cabinets_qnt * 1
                if (Identifier_Modifier[5]=="U" or Identifier_Modifier[5]=="I" or Identifier_Modifier[5]=="C") and Identifier_Modifier[6]=="M" and Identifier_Modifier[8]=="B" and (Identifier_Modifier[9]=="A"): #10
                    var1= Safety_Cabinets_qnt * 2
                if (Identifier_Modifier[6]=="U" or Identifier_Modifier[6]=="I" or Identifier_Modifier[6]=="A" or Identifier_Modifier[6]=="B")  and Identifier_Modifier[8]=="X" and Identifier_Modifier[9]=="C": #12
                    var1= Safety_Cabinets_qnt * 3
                if var1>0:
                    parts_dict["50159655-001"] = {"Quantity" : int(var1), "Description" : "Boot connector for PUIO IOTA"}
        elif Specify_Identifier=="No" and (S300=="Redundant S300" or "No S300") and IO_Redundancy=="Non Redundant IO" and Safety_Cabinets_qnt !='' and Safety_Cabinets_qnt >0:
            var1=0
            Trace.Write(PDIO_Count)
            if Field_for_PUIO =="Default Marshalling FC-TUIO51/52" and PUIO_Count=="32" and PDIO_Count=="0": #1
                var1= 1 * Safety_Cabinets_qnt
            elif  Field_for_PUIO =="Default Marshalling FC-TUIO51/52" and PUIO_Count=="64" and PDIO_Count=="0": #2
                var1= 2 * Safety_Cabinets_qnt
            elif Field_for_PUIO =="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO_Count=="32" and PDIO_Count=="32": #3
                var1= 1 * Safety_Cabinets_qnt
            elif Field_for_PUIO =="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO_Count=="32" and PDIO_Count=="64": #4
                var1= 1 * Safety_Cabinets_qnt
            elif Field_for_PUIO =="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO_Count=="64" and PDIO_Count=="32": #5
                var1= 2 * Safety_Cabinets_qnt
            elif Field_for_PUIO =="Default Marshalling FC-TUIO51/52" and PUIO_Count=="96" and PDIO_Count=="0": #6
                var1= 3 * Safety_Cabinets_qnt
            elif (Field_for_PUIO =="Intrinsically Safe" or Field_for_PUIO =="Universal Marshalling, PTA") and PUIO_Count=="32" and PDIO_Count=="0": #7
                var1= 1 * Safety_Cabinets_qnt
            elif (Field_for_PUIO =="Intrinsically Safe" or Field_for_PUIO =="Universal Marshalling, PTA" or Field_for_PUIO =="32 IS, 32 Non-IS") and PUIO_Count=="64" and PDIO_Count=="0": #8
                var1= 2 * Safety_Cabinets_qnt
            elif (Field_for_PUIO =="Intrinsically Safe" or Field_for_PUIO =="Universal Marshalling, PTA") and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO_Count=="32" and PDIO_Count=="32": #9
                var1= 1 * Safety_Cabinets_qnt
            elif (Field_for_PUIO =="Intrinsically Safe" or Field_for_PUIO =="Universal Marshalling, PTA")  and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO_Count=="32" and PDIO_Count=="64": #10
                var1= 1 * Safety_Cabinets_qnt
            elif (Field_for_PUIO =="Intrinsically Safe" or Field_for_PUIO =="Universal Marshalling, PTA" or Field_for_PUIO =="32 IS, 32 Non-IS") and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO_Count=="64" and PDIO_Count=="32": #11
                var1= 2 * Safety_Cabinets_qnt
            elif(Field_for_PDIO =="Intrinsically Safe" or Field_for_PDIO =="Universal Marshalling, PTA" or Field_for_PDIO =="32 IS, 64 Non-IS" or Field_for_PDIO =="64 IS, 32 Non-IS") and PUIO_Count=="0" and PDIO_Count=="96": #12
                var1= 3 * Safety_Cabinets_qnt
            if var1>0:
                parts_dict["50159655-001"] = {"Quantity" : int(var1), "Description" : "Boot connector for PUIO IOTA"}
    return parts_dict