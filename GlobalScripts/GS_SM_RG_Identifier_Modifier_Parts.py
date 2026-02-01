#parts_dict={}

def get_identifier_Modifier(Product,parts_dict):
    Enclosure_Type=Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0].GetColumnByName('Enclosure_Type').DisplayValue   
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
    Trace.Write("S300"+str(S300))
    Trace.Write("PUIO_Count= "+str(PUIO_Count))
    Trace.Write("PDIO_Count= "+str(PDIO_Count))
    Trace.Write("IO_Redundancy= "+str(IO_Redundancy))
    Trace.Write("Power_Supply_Type= "+str(Power_Supply_Type))
    Trace.Write("Power_Supply_Redundancy ="+str(Power_Supply_Type))
    Trace.Write("Field_for_PUIO ="+str(Field_for_PUIO))
    Trace.Write("Field_for_PDIO= "+str(Field_for_PDIO))

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
    if Enclosure_Type == "Universal Safety Cab-1.3M":
        if len(Identifier_Modifier)>20 and Specify_Identifier=="Yes" and Safety_Cabinets_qnt >0:
            if (Identifier_Modifier[3]=="S" or Identifier_Modifier[3]=="X") and Identifier_Modifier[13]=="R":
                var=0
                if (Identifier_Modifier[5]=="M") and (Identifier_Modifier[6]=="M") and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="B": #1
                    var= 2 * Safety_Cabinets_qnt
                if (Identifier_Modifier[5]=="M") and (Identifier_Modifier[6]=="M") and Identifier_Modifier[8]=="B" and Identifier_Modifier[9]=="A": #3
                    var= 2 * Safety_Cabinets_qnt
                if (Identifier_Modifier[6]=="M") and Identifier_Modifier[8]=="X" and Identifier_Modifier[9]=="C": #5
                    var= 2 * Safety_Cabinets_qnt
                if (Identifier_Modifier[5]=="U") and (Identifier_Modifier[6]=="M") and Identifier_Modifier[8]=="B" and Identifier_Modifier[9]=="A": #7
                    var= 2 * Safety_Cabinets_qnt
                parts_dict["FC-TDIO52"] = {"Quantity" : int(var), "Description" : "SC SAFETY FTA KNIFE, EOL, 24VDC, 16CH, R"}

            if (Identifier_Modifier[3]=="S" or Identifier_Modifier[3]=="X") and Identifier_Modifier[13]=="X":
            	var=0
                if (Identifier_Modifier[5]=="M") and (Identifier_Modifier[6]=="M") and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="B": #2
                    var= 2 * Safety_Cabinets_qnt
                if (Identifier_Modifier[5]=="M") and (Identifier_Modifier[6]=="M") and Identifier_Modifier[8]=="B" and Identifier_Modifier[9]=="A": #4
                    var= 2 * Safety_Cabinets_qnt
                if (Identifier_Modifier[6]=="M") and Identifier_Modifier[8]=="X" and Identifier_Modifier[9]=="C": #6
                    var= 2 * Safety_Cabinets_qnt
                if (Identifier_Modifier[5]=="U") and (Identifier_Modifier[6]=="M") and Identifier_Modifier[8]=="B" and Identifier_Modifier[9]=="A": #8
                    var= 2 * Safety_Cabinets_qnt
                parts_dict["FC-TDIO52"] = {"Quantity" : int(var), "Description" : "SC SAFETY FTA KNIFE, EOL, 24VDC, 16CH, R"}

        elif Specify_Identifier=="No" and (S300=="Redundant S300" or S300 == "No S300") and IO_Redundancy=="Redundant IO" and Safety_Cabinets_qnt >0:
            var=0
            if Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO_Count=="32" and PDIO_Count=="64": #1
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO_Count=="64" and PDIO_Count=="32": #3
                var= 2 * Safety_Cabinets_qnt 
            elif Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and (PUIO_Count=="0" or '') and PDIO_Count=="96": #5
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PUIO=="Universal Marshalling, PTA" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO_Count=="64" and PDIO_Count=="32": #7
                var= 2 * Safety_Cabinets_qnt
            parts_dict["FC-TDIO52"] = {"Quantity" : int(var), "Description" : "SC SAFETY FTA KNIFE, EOL, 24VDC, 16CH, R"}

        elif Specify_Identifier=="No" and (S300=="Redundant S300" or S300=="No S300") and IO_Redundancy=="Non Redundant IO" and Safety_Cabinets_qnt !='' and Safety_Cabinets_qnt >0:
            var=0
            if Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO_Count=="32" and PDIO_Count=="64": #2
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO_Count=="64" and PDIO_Count=="32": #4
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and (PUIO_Count=="0" or '') and PDIO_Count=="96": #6
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PUIO=="Universal Marshalling, PTA" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO_Count=="64" and PDIO_Count=="32": #8
                var= 2 * Safety_Cabinets_qnt
            parts_dict["FC-TDIO52"] = {"Quantity" : int(var), "Description" : "SC SAFETY FTA KNIFE, EOL, 24VDC, 16CH, R"}
    return parts_dict
#fun= get_identifier_Modifier(Product,parts_dict)
#Trace.Write("fun= "+str(fun))
#CXCPQ-33990 added by Lahu
def get_identifier_UGIA01(Product,parts_dict):
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
            if (Identifier_Modifier[3]=="S" or Identifier_Modifier[3]=="X") and Identifier_Modifier[13]=="R":
                var=0
                if (Identifier_Modifier[6]=="C") and (Identifier_Modifier[8]=="X") and Identifier_Modifier[9]=="B": #15
                    var= Safety_Cabinets_qnt * 2
                if (Identifier_Modifier[6]=="I") and (Identifier_Modifier[8]=="X") and Identifier_Modifier[9]=="B": #43
                    var= Safety_Cabinets_qnt * 4
                if (Identifier_Modifier[6]=="I") and (Identifier_Modifier[8]=="X") and Identifier_Modifier[9]=="A": #41
                    var= Safety_Cabinets_qnt * 2
                if (Identifier_Modifier[6]=="B") and (Identifier_Modifier[8]=="X") and Identifier_Modifier[9]=="C": #17
                    var= Safety_Cabinets_qnt * 4
                if (Identifier_Modifier[6]=="A") and (Identifier_Modifier[8]=="X") and Identifier_Modifier[9]=="C": #16
                    var= Safety_Cabinets_qnt * 2
                if (Identifier_Modifier[6]=="I") and (Identifier_Modifier[8]=="X") and Identifier_Modifier[9]=="C": #15
                    var= Safety_Cabinets_qnt * 6
                if (Identifier_Modifier[5]=="B") and (Identifier_Modifier[8]=="C") and Identifier_Modifier[9]=="X": #59
                    var= Safety_Cabinets_qnt * 4
                if (Identifier_Modifier[5]=="A") and (Identifier_Modifier[8]=="C") and Identifier_Modifier[9]=="X": #58
                    var= Safety_Cabinets_qnt * 2
                if (Identifier_Modifier[5]=="I") and (Identifier_Modifier[8]=="C") and Identifier_Modifier[9]=="X": #57
                    var= Safety_Cabinets_qnt * 6
                if Identifier_Modifier[5]=="C" and Identifier_Modifier[8]=="B" and Identifier_Modifier[9]=="X": #4
                    var= Safety_Cabinets_qnt * 2
                if (Identifier_Modifier[5]=="I") and (Identifier_Modifier[8]=="A") and Identifier_Modifier[9]=="X": #1
                    var= Safety_Cabinets_qnt * 2
                if Identifier_Modifier[5]=="I" and Identifier_Modifier[8]=="B" and Identifier_Modifier[9]=="X": #3
                    var= Safety_Cabinets_qnt * 4
                if Identifier_Modifier[5]=="M" and Identifier_Modifier[6]=="C" and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="B": #54
                    var= Safety_Cabinets_qnt * 2
                if Identifier_Modifier[5]=="M" and Identifier_Modifier[6]=="I" and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="B": #53
                    var= Safety_Cabinets_qnt * 4
                if Identifier_Modifier[5]=="U" and Identifier_Modifier[6]=="I" and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="A": #49
                    var= Safety_Cabinets_qnt * 2
                if Identifier_Modifier[5]=="I" and Identifier_Modifier[6]=="U" and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="A": #48
                    var= Safety_Cabinets_qnt * 2
                if Identifier_Modifier[5]=="I" and Identifier_Modifier[6]=="I" and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="A": #47
                    var= Safety_Cabinets_qnt * 4
                if Identifier_Modifier[5]=="M" and Identifier_Modifier[6]=="I" and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="A": #39
                    var= Safety_Cabinets_qnt * 2
                if (Identifier_Modifier[5]=="C" or Identifier_Modifier[5]=="I") and Identifier_Modifier[6]=="U" and Identifier_Modifier[8]=="B" and Identifier_Modifier[9]=="A": #33/34
                    var= Safety_Cabinets_qnt * 4
                if Identifier_Modifier[5]=="U" and Identifier_Modifier[6]=="I" and Identifier_Modifier[8]=="B" and Identifier_Modifier[9]=="A": #32
                    var= Safety_Cabinets_qnt * 2
                if Identifier_Modifier[5]=="I" and Identifier_Modifier[6]=="I" and Identifier_Modifier[8]=="B" and Identifier_Modifier[9]=="A": #31
                    var= Safety_Cabinets_qnt * 6
                if Identifier_Modifier[5]=="M" and Identifier_Modifier[6]=="I" and Identifier_Modifier[8]=="B" and Identifier_Modifier[9]=="A": #29
                    var= Safety_Cabinets_qnt * 2
                if Identifier_Modifier[5]=="I" and Identifier_Modifier[6]=="U" and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="B": #23
                    var= Safety_Cabinets_qnt * 2
                if Identifier_Modifier[5]=="U" and Identifier_Modifier[6]=="I" and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="B": #24
                    var= Safety_Cabinets_qnt * 4
                if Identifier_Modifier[5]=="U" and Identifier_Modifier[6]=="C" and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="B": #22
                    var= Safety_Cabinets_qnt * 2
                if Identifier_Modifier[5]=="I" and Identifier_Modifier[6]=="I" and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="B": #21
                    var= Safety_Cabinets_qnt * 6
                if Identifier_Modifier[5]=="C" and Identifier_Modifier[6]=="M" and Identifier_Modifier[8]=="B" and Identifier_Modifier[9]=="A": #12
                    var= Safety_Cabinets_qnt * 2
                if Identifier_Modifier[5]=="I" and Identifier_Modifier[6]=="M" and Identifier_Modifier[8]=="A" and (Identifier_Modifier[9]=="X" or Identifier_Modifier[9]=="B"): #7/9
                    var= Safety_Cabinets_qnt * 2
                if Identifier_Modifier[5]=="I" and Identifier_Modifier[6]=="M" and Identifier_Modifier[8]=="B" and Identifier_Modifier[9]=="A": #11
                    var= Safety_Cabinets_qnt * 4
                parts_dict["CC-UGIA01"] = {"Quantity" : int(var), "Description" : "IS SCA-Signal Condition Assembly 24V"}
            elif (Identifier_Modifier[3]=="S" or "X") and Identifier_Modifier[13]=="X":
                var=0
                if (Identifier_Modifier[6]=="C") and (Identifier_Modifier[8]=="X") and Identifier_Modifier[9]=="B": #18
                    var= Safety_Cabinets_qnt * 2
                elif (Identifier_Modifier[6]=="I") and (Identifier_Modifier[8]=="X") and Identifier_Modifier[9]=="B": #45
                    var= Safety_Cabinets_qnt * 4
                elif (Identifier_Modifier[6]=="I") and (Identifier_Modifier[8]=="X") and Identifier_Modifier[9]=="A": #42
                    var= Safety_Cabinets_qnt * 2
                elif (Identifier_Modifier[6]=="B") and (Identifier_Modifier[8]=="X") and Identifier_Modifier[9]=="C": #20
                    var= Safety_Cabinets_qnt * 4
                elif (Identifier_Modifier[6]=="A") and (Identifier_Modifier[8]=="X") and Identifier_Modifier[9]=="C": #19
                    var= Safety_Cabinets_qnt * 2
                elif (Identifier_Modifier[6]=="I") and (Identifier_Modifier[8]=="X") and Identifier_Modifier[9]=="C": #18
                    var= Safety_Cabinets_qnt * 6
                elif (Identifier_Modifier[5]=="B") and (Identifier_Modifier[8]=="C") and Identifier_Modifier[9]=="X": #62
                    var= Safety_Cabinets_qnt * 4
                elif (Identifier_Modifier[5]=="A") and (Identifier_Modifier[8]=="C") and Identifier_Modifier[9]=="X": #61
                    var= Safety_Cabinets_qnt * 2
                elif (Identifier_Modifier[5]=="I") and (Identifier_Modifier[8]=="C") and Identifier_Modifier[9]=="X": #60
                    var= Safety_Cabinets_qnt * 6
                elif Identifier_Modifier[5]=="C" and Identifier_Modifier[8]=="B" and Identifier_Modifier[9]=="X": #6
                    var= Safety_Cabinets_qnt * 2
                elif (Identifier_Modifier[5]=="I") and (Identifier_Modifier[8]=="A") and Identifier_Modifier[9]=="X": #2
                    var= Safety_Cabinets_qnt * 2
                elif Identifier_Modifier[5]=="I" and Identifier_Modifier[8]=="B" and Identifier_Modifier[9]=="X": #5
                    var= Safety_Cabinets_qnt * 4
                elif Identifier_Modifier[5]=="M" and Identifier_Modifier[6]=="C" and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="B": #56
                    var= Safety_Cabinets_qnt * 2
                elif Identifier_Modifier[5]=="M" and Identifier_Modifier[6]=="I" and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="B": #55
                    var= Safety_Cabinets_qnt * 4
                elif Identifier_Modifier[5]=="U" and Identifier_Modifier[6]=="I" and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="A": #52
                    var= Safety_Cabinets_qnt * 2
                elif Identifier_Modifier[5]=="I" and Identifier_Modifier[6]=="U" and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="A": #51
                    var= Safety_Cabinets_qnt * 2
                elif Identifier_Modifier[5]=="I" and Identifier_Modifier[6]=="I" and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="A": #50
                    var= Safety_Cabinets_qnt * 4
                elif Identifier_Modifier[5]=="M" and Identifier_Modifier[6]=="I" and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="A": #40
                    var= Safety_Cabinets_qnt * 2
                elif (Identifier_Modifier[5]=="C" or Identifier_Modifier[5]=="I") and Identifier_Modifier[6]=="U" and Identifier_Modifier[8]=="B" and Identifier_Modifier[9]=="A": #37/38
                    var= Safety_Cabinets_qnt * 4
                elif Identifier_Modifier[5]=="U" and Identifier_Modifier[6]=="I" and Identifier_Modifier[8]=="B" and Identifier_Modifier[9]=="A": #36
                    var= Safety_Cabinets_qnt * 2
                elif Identifier_Modifier[5]=="I" and Identifier_Modifier[6]=="I" and Identifier_Modifier[8]=="B" and Identifier_Modifier[9]=="A": #35
                    var= Safety_Cabinets_qnt * 6
                elif Identifier_Modifier[5]=="M" and Identifier_Modifier[6]=="I" and Identifier_Modifier[8]=="B" and Identifier_Modifier[9]=="A": #30
                    var= Safety_Cabinets_qnt * 2
                elif Identifier_Modifier[5]=="I" and Identifier_Modifier[6]=="U" and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="B": #27
                    var= Safety_Cabinets_qnt * 2
                elif Identifier_Modifier[5]=="U" and Identifier_Modifier[6]=="I" and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="B": #28
                    var= Safety_Cabinets_qnt * 4
                elif Identifier_Modifier[5]=="U" and Identifier_Modifier[6]=="C" and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="B": #26
                    var= Safety_Cabinets_qnt * 2
                elif Identifier_Modifier[5]=="I" and Identifier_Modifier[6]=="I" and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="B": #25
                    var= Safety_Cabinets_qnt * 6
                elif Identifier_Modifier[5]=="C" and Identifier_Modifier[6]=="M" and Identifier_Modifier[8]=="B" and Identifier_Modifier[9]=="A": #14
                    var= Safety_Cabinets_qnt * 2
                elif Identifier_Modifier[5]=="I" and Identifier_Modifier[6]=="M" and Identifier_Modifier[8]=="A" and (Identifier_Modifier[9]=="A" or Identifier_Modifier[9]=="B"): #8/10
                    var= Safety_Cabinets_qnt * 2
                elif Identifier_Modifier[5]=="I" and Identifier_Modifier[6]=="M" and Identifier_Modifier[8]=="B" and Identifier_Modifier[9]=="A": #13
                    var= Safety_Cabinets_qnt * 4
                parts_dict["CC-UGIA01"] = {"Quantity" : int(var), "Description" : "IS SCA-Signal Condition Assembly 24V"}

        elif Specify_Identifier=="No" and S300!="Non Redundant S300" and IO_Redundancy=="Redundant IO" and Safety_Cabinets_qnt >0:
            var=0
            if Field_for_PUIO=="32 IS, 32 Non-IS" and (PUIO_Count=="64")and PDIO_Count=="0": #4
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PUIO=="Intrinsically Safe" and (PDIO_Count=="0")and PUIO_Count=="64": #3
                var= 4 * Safety_Cabinets_qnt
            elif Field_for_PUIO=="Intrinsically Safe" and (PDIO_Count=="0")and PUIO_Count=="32": #1
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PUIO=="64 IS, 32 Non-IS" and (PDIO_Count=="0")and PUIO_Count=="96": #59
                var= 4 * Safety_Cabinets_qnt
            elif Field_for_PUIO=="32 IS, 64 Non-IS" and (PDIO_Count=="0")and PUIO_Count=="96": #58
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PUIO=="Intrinsically Safe" and (PDIO_Count=="0")and PUIO_Count=="96": #57
                var= 6 * Safety_Cabinets_qnt
            elif Field_for_PDIO=="32 IS, 32 Non-IS" and (PUIO_Count=="0")and PDIO_Count=="64": #44
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PDIO=="Intrinsically Safe" and (PUIO_Count=="0")and PDIO_Count=="64": #43
                var= 4 * Safety_Cabinets_qnt
            elif Field_for_PDIO=="Intrinsically Safe" and (PUIO_Count=="0")and PDIO_Count=="32": #41
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PDIO=="64 IS, 32 Non-IS" and (PUIO_Count=="0")and PDIO_Count=="96": #17
                var= 4 * Safety_Cabinets_qnt
            elif Field_for_PDIO=="32 IS, 64 Non-IS" and (PUIO_Count=="0")and PDIO_Count=="96": #16
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PDIO=="Intrinsically Safe" and (PUIO_Count=="0")and PDIO_Count=="96": #15
                var= 6 * Safety_Cabinets_qnt
            elif Field_for_PUIO =="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="32 IS, 32 Non-IS" and PUIO_Count=="32" and PDIO_Count=="64": #54
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PUIO =="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Intrinsically Safe" and PUIO_Count=="32" and PDIO_Count=="64": #53
                var= 4 * Safety_Cabinets_qnt
            elif Field_for_PUIO =="Universal Marshalling, PTA" and Field_for_PDIO=="Intrinsically Safe" and PUIO_Count=="32" and PDIO_Count=="32": #49
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PUIO =="Intrinsically Safe" and Field_for_PDIO=="Universal Marshalling, PTA" and PUIO_Count=="32" and PDIO_Count=="32": #48
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PUIO =="Intrinsically Safe" and Field_for_PDIO=="Intrinsically Safe" and PUIO_Count=="32" and PDIO_Count=="32": #47
                var= 4 * Safety_Cabinets_qnt
            elif Field_for_PUIO =="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Intrinsically Safe" and PUIO_Count=="32" and PDIO_Count=="32": #39
                var= 2 * Safety_Cabinets_qnt
            elif (Field_for_PUIO =="32 IS, 32 Non-IS" or Field_for_PUIO =="Intrinsically Safe") and Field_for_PDIO=="Universal Marshalling, PTA" and PUIO_Count=="64" and PDIO_Count=="32": #33/34
                var= 4 * Safety_Cabinets_qnt
            elif Field_for_PUIO =="Universal Marshalling, PTA" and Field_for_PDIO=="Intrinsically Safe" and PUIO_Count=="64" and PDIO_Count=="32": #32
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PUIO =="Intrinsically Safe" and Field_for_PDIO=="Intrinsically Safe" and PUIO_Count=="64" and PDIO_Count=="32": #31
                var= 6 * Safety_Cabinets_qnt
            elif Field_for_PUIO =="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Intrinsically Safe" and PUIO_Count=="64" and PDIO_Count=="32": #29
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PUIO =="Universal Marshalling, PTA" and Field_for_PDIO=="Intrinsically Safe" and PUIO_Count=="32" and PDIO_Count=="64": #24
                var= 4 * Safety_Cabinets_qnt
            elif Field_for_PUIO =="Intrinsically Safe" and Field_for_PDIO=="Universal Marshalling, PTA" and PUIO_Count=="32" and PDIO_Count=="64": #23
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PUIO =="Universal Marshalling, PTA" and Field_for_PDIO=="32 IS, 32 Non-IS" and PUIO_Count=="32" and PDIO_Count=="64": #22
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PUIO =="Intrinsically Safe" and Field_for_PDIO=="Intrinsically Safe" and PUIO_Count=="32" and PDIO_Count=="64": #21
                var= 6 * Safety_Cabinets_qnt
            elif Field_for_PUIO =="32 IS, 32 Non-IS" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO_Count=="64" and PDIO_Count=="32": #12
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PUIO =="Intrinsically Safe" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO_Count=="64" and PDIO_Count=="32": #11
                var= 4 * Safety_Cabinets_qnt
            elif Field_for_PUIO =="Intrinsically Safe" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO_Count=="32" and (PDIO_Count=="0" or PDIO_Count=="64"): #7/9
                var= 2 * Safety_Cabinets_qnt
            parts_dict["CC-UGIA01"] = {"Quantity" : int(var), "Description" : "IS SCA-Signal Condition Assembly 24V"}
        elif Specify_Identifier=="No" and (S300=="Redundant S300" or "No S300") and IO_Redundancy=="Non Redundant IO" and Safety_Cabinets_qnt !='' and Safety_Cabinets_qnt >0:
            var=0
            if Field_for_PUIO=="32 IS, 32 Non-IS" and (PUIO_Count=="64"or '' )and PDIO_Count=="0": #6
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PUIO=="Intrinsically Safe" and (PDIO_Count=="0"or '' )and PUIO_Count=="64": #5
                var= 4 * Safety_Cabinets_qnt
            elif Field_for_PUIO=="Intrinsically Safe" and (PDIO_Count=="0"or '' )and PUIO_Count=="32": #2
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PUIO=="64 IS, 32 Non-IS" and (PDIO_Count=="0"or '' )and PUIO_Count=="96": #62
                var= 4 * Safety_Cabinets_qnt
            elif Field_for_PUIO=="32 IS, 64 Non-IS" and (PDIO_Count=="0"or '' )and PUIO_Count=="96": #61
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PUIO=="Intrinsically Safe" and (PDIO_Count=="0"or '' )and PUIO_Count=="96": #60
                var= 6 * Safety_Cabinets_qnt
            elif Field_for_PDIO=="32 IS, 32 Non-IS" and (PUIO_Count=="0"or '' )and PDIO_Count=="64": #46
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PDIO=="Intrinsically Safe" and (PUIO_Count=="0"or '' )and PDIO_Count=="64": #45
                var= 4 * Safety_Cabinets_qnt
            elif Field_for_PDIO=="Intrinsically Safe" and (PUIO_Count=="0"or '' )and PDIO_Count=="32": #42
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PDIO=="64 IS, 32 Non-IS" and (PUIO_Count=="0"or '' )and PDIO_Count=="96": #20
                var= 4 * Safety_Cabinets_qnt
            elif Field_for_PDIO=="32 IS, 64 Non-IS" and (PUIO_Count=="0"or '' )and PDIO_Count=="96": #19
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PDIO=="Intrinsically Safe" and (PUIO_Count=="0"or '' )and PDIO_Count=="96": #18
                var= 6 * Safety_Cabinets_qnt
            elif Field_for_PUIO =="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="32 IS, 32 Non-IS" and PUIO_Count=="32" and PDIO_Count=="64": #56
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PUIO =="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Intrinsically Safe" and PUIO_Count=="32" and PDIO_Count=="64": #55
                var= 4 * Safety_Cabinets_qnt
            elif Field_for_PUIO =="Universal Marshalling, PTA" and Field_for_PDIO=="Intrinsically Safe" and PUIO_Count=="32" and PDIO_Count=="32": #52
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PUIO =="Intrinsically Safe" and Field_for_PDIO=="Universal Marshalling, PTA" and PUIO_Count=="32" and PDIO_Count=="32": #51
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PUIO =="Intrinsically Safe" and Field_for_PDIO=="Intrinsically Safe" and PUIO_Count=="32" and PDIO_Count=="32": #50
                var= 4 * Safety_Cabinets_qnt
            elif Field_for_PUIO =="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Intrinsically Safe" and PUIO_Count=="32" and PDIO_Count=="32": #40
                var= 2 * Safety_Cabinets_qnt
            elif (Field_for_PUIO =="32 IS, 32 Non-IS" or Field_for_PUIO =="Intrinsically Safe") and Field_for_PDIO=="Universal Marshalling, PTA" and PUIO_Count=="64" and PDIO_Count=="32": #37/38
                var= 4 * Safety_Cabinets_qnt
            elif Field_for_PUIO =="Universal Marshalling, PTA" and Field_for_PDIO=="Intrinsically Safe" and PUIO_Count=="64" and PDIO_Count=="32": #36
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PUIO =="Intrinsically Safe" and Field_for_PDIO=="Intrinsically Safe" and PUIO_Count=="64" and PDIO_Count=="32": #35
                var= 6 * Safety_Cabinets_qnt
            elif Field_for_PUIO =="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Intrinsically Safe" and PUIO_Count=="64" and PDIO_Count=="32": #30
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PUIO =="Universal Marshalling, PTA" and Field_for_PDIO=="Intrinsically Safe" and PUIO_Count=="32" and PDIO_Count=="64": #28
                var= 4 * Safety_Cabinets_qnt
            elif Field_for_PUIO =="Intrinsically Safe" and Field_for_PDIO=="Universal Marshalling, PTA" and PUIO_Count=="32" and PDIO_Count=="64": #27
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PUIO =="Universal Marshalling, PTA" and Field_for_PDIO=="32 IS, 32 Non-IS" and PUIO_Count=="32" and PDIO_Count=="64": #26
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PUIO =="Intrinsically Safe" and Field_for_PDIO=="Intrinsically Safe" and PUIO_Count=="32" and PDIO_Count=="64": #25
                var= 6 * Safety_Cabinets_qnt
            elif Field_for_PUIO =="32 IS, 32 Non-IS" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO_Count=="64" and PDIO_Count=="32": #14
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PUIO =="Intrinsically Safe" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO_Count=="64" and PDIO_Count=="32": #13
                var= 4 * Safety_Cabinets_qnt
            elif Field_for_PUIO =="Intrinsically Safe" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO_Count=="32" and (PDIO_Count=="32" or PDIO_Count=="64"): #8/10
                var= 2 * Safety_Cabinets_qnt
            parts_dict["CC-UGIA01"] = {"Quantity" : int(var), "Description" : "IS SCA-Signal Condition Assembly 24V"}
    return parts_dict