#32662 (ADDED BY SHIVANI)
#parts_dict={}
def get_identifier_Positions(Product,parts_dict):
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
            if Identifier_Modifier[9]=="X" and Identifier_Modifier[8]=="A":  #1
                var1= Safety_Cabinets_qnt * 1
            elif (Identifier_Modifier[9]=="X") and Identifier_Modifier[8]=="B": #2
                var1= Safety_Cabinets_qnt * 2
            elif (Identifier_Modifier[9]=="X") and Identifier_Modifier[8]=="C": #3
                var1= Safety_Cabinets_qnt * 3
            elif (Identifier_Modifier[9]=="A") and Identifier_Modifier[8]=="X": #4
                var1= Safety_Cabinets_qnt * 1
            elif (Identifier_Modifier[9]=="B") and Identifier_Modifier[8]=="X": #5
                var1= Safety_Cabinets_qnt * 2
            elif (Identifier_Modifier[9]=="C") and Identifier_Modifier[8]=="X": #6
                var1= Safety_Cabinets_qnt * 3
            elif (Identifier_Modifier[9]=="A") and Identifier_Modifier[8]=="A": #7
                var1= Safety_Cabinets_qnt * 2
            elif (Identifier_Modifier[9]=="B") and Identifier_Modifier[8]=="A": #8
                var1= Safety_Cabinets_qnt * 3
            elif (Identifier_Modifier[9]=="A") and Identifier_Modifier[8]=="B": #9
                var1= Safety_Cabinets_qnt * 3
            if var1>0:
                parts_dict["51121566-102"] = {"Quantity" : int(var1), "Description" : "Shield Ground Bar"}
        elif Specify_Identifier=="No":
            
            if PUIO_Count=="32" and PDIO_Count=="0":
                Trace.Write(PUIO_Count)
                Trace.Write(PDIO_Count)
                var1= Safety_Cabinets_qnt * 1
            elif PUIO_Count=="64" and PDIO_Count=="0":
                var1= Safety_Cabinets_qnt * 2
            elif PUIO_Count=="96" and PDIO_Count=="0":
                var1= Safety_Cabinets_qnt * 3
            elif PUIO_Count=="0" and PDIO_Count=="32":
                var1= Safety_Cabinets_qnt * 1
            elif PUIO_Count=="0" and PDIO_Count=="64":
                var1= Safety_Cabinets_qnt * 2
            elif PUIO_Count=="0" and PDIO_Count=="96":
                var1= Safety_Cabinets_qnt * 3
            elif PUIO_Count=="32" and PDIO_Count=="32":
                var1= Safety_Cabinets_qnt * 2
            elif PUIO_Count=="32" and PDIO_Count=="64":
                var1= Safety_Cabinets_qnt * 3
            elif PUIO_Count=="64" and PDIO_Count=="32":
                var1= Safety_Cabinets_qnt * 3
            if var1>0:
                parts_dict["51121566-102"]={'Quantity':int(var1),'Description':'Shield Ground Bar'}
    return parts_dict
#Trace.Write(str(get_identifier_Positions(Product,parts_dict)))