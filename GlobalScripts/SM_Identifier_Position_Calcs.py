#CXCPQ-34197
#parts_dict={}
def identifier_FC_TUIO51(Product,parts_dict):
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
            if (Identifier_Modifier[3]=="S" or Identifier_Modifier[3]== "X") and Identifier_Modifier[13]=="R":
                var=0
                if (Identifier_Modifier[5]=="M") and (Identifier_Modifier[8]=="A") and Identifier_Modifier[9]=="X": #1
                    var= Safety_Cabinets_qnt * 2
                elif (Identifier_Modifier[5]=="M") and (Identifier_Modifier[8]=="B") and Identifier_Modifier[9]=="X": #3
                    var= Safety_Cabinets_qnt * 4
                elif (Identifier_Modifier[5]=="M") and (Identifier_Modifier[6]=="M") and Identifier_Modifier[8]=="A" and (Identifier_Modifier[9]=="A"): #5
                    var= Safety_Cabinets_qnt * 2
                elif (Identifier_Modifier[5]=="M") and (Identifier_Modifier[6]=="M") and Identifier_Modifier[8]=="A" and (Identifier_Modifier[9]=="B"): #7
                    var= Safety_Cabinets_qnt * 2
                elif (Identifier_Modifier[5]=="M") and (Identifier_Modifier[6]=="M") and Identifier_Modifier[8]=="B" and (Identifier_Modifier[9]=="A"): #9
                    var= Safety_Cabinets_qnt * 4
                elif (Identifier_Modifier[5]=="M") and Identifier_Modifier[8]=="C" and (Identifier_Modifier[9]=="X"): #11
                    var= Safety_Cabinets_qnt * 4
                elif (Identifier_Modifier[5]=="M") and (Identifier_Modifier[6]=="U") and Identifier_Modifier[8]=="B" and (Identifier_Modifier[9]=="A"): #13
                    var= Safety_Cabinets_qnt * 2
                elif (Identifier_Modifier[5]=="M") and (Identifier_Modifier[6]=="U") and Identifier_Modifier[8]=="A" and (Identifier_Modifier[9]=="A"): #15
                    var= Safety_Cabinets_qnt * 2
                elif (Identifier_Modifier[5]=="M") and (Identifier_Modifier[6]=="U" or Identifier_Modifier[6]== "I" or Identifier_Modifier[6]== "C") and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="B": #17
                    var= Safety_Cabinets_qnt * 2
                parts_dict["FC-TUIO51"] = {"Quantity" : int(var), "Description" : "SC FTA FC-PUIO01 KNIFE, EOL, 24VDC, 16CH, L"}

            elif (Identifier_Modifier[3]=="S" or Identifier_Modifier[3]== "X" or Identifier_Modifier[3]== "N") and Identifier_Modifier[13]=="X":
                var=0
                if (Identifier_Modifier[5]=="M") and (Identifier_Modifier[8]=="A") and Identifier_Modifier[9]=="X": #2
                    var= Safety_Cabinets_qnt * 2
                elif (Identifier_Modifier[5]=="M") and (Identifier_Modifier[8]=="B") and Identifier_Modifier[9]=="X": #4
                    var= Safety_Cabinets_qnt * 4
                elif (Identifier_Modifier[5]=="M") and (Identifier_Modifier[6]=="M") and Identifier_Modifier[8]=="A" and (Identifier_Modifier[9]=="A"): #6
                    var= Safety_Cabinets_qnt * 2
                elif (Identifier_Modifier[5]=="M") and (Identifier_Modifier[6]=="M") and Identifier_Modifier[8]=="A" and (Identifier_Modifier[9]=="B"): #8
                    var= Safety_Cabinets_qnt * 2
                elif (Identifier_Modifier[5]=="M") and (Identifier_Modifier[6]=="M") and Identifier_Modifier[8]=="B" and (Identifier_Modifier[9]=="A"): #10
                    var= Safety_Cabinets_qnt * 4
                elif (Identifier_Modifier[5]=="M") and Identifier_Modifier[8]=="C" and (Identifier_Modifier[9]=="X"): #12
                    var= Safety_Cabinets_qnt * 4
                elif (Identifier_Modifier[5]=="M") and (Identifier_Modifier[6]=="U") and Identifier_Modifier[8]=="B" and (Identifier_Modifier[9]=="A"): #14
                    var= Safety_Cabinets_qnt * 2
                elif (Identifier_Modifier[5]=="M") and (Identifier_Modifier[6]=="U") and Identifier_Modifier[8]=="A" and (Identifier_Modifier[9]=="A"): #16
                    var= Safety_Cabinets_qnt * 2
                elif (Identifier_Modifier[5]=="M") and (Identifier_Modifier[6]=="U" or Identifier_Modifier[6]== "I" or Identifier_Modifier[6]=="C") and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="B": #18
                    var= Safety_Cabinets_qnt * 2
                parts_dict["FC-TUIO51"] = {"Quantity" : int(var), "Description" : "SC FTA FC-PUIO01 KNIFE, EOL, 24VDC, 16CH, L"}

        elif Specify_Identifier=="No" and (S300=="Redundant S300" or S300 == "No S300") and IO_Redundancy=="Redundant IO" and Safety_Cabinets_qnt >0:
            var=0
            if Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and (PUIO_Count=="32"or '' )and (PDIO_Count=="0" or ''): #1
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and (PUIO_Count=="64"or '' )and (PDIO_Count=="0" or ''): #3
                var= 4 * Safety_Cabinets_qnt
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO_Count=="32" and PDIO_Count=="32": #5
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO_Count=="32" and PDIO_Count=="64": #7
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO_Count=="64" and PDIO_Count=="32": #9
                var= 4 * Safety_Cabinets_qnt
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and PUIO_Count=="96" and PDIO_Count=="0": #11
                var= 4 * Safety_Cabinets_qnt
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Universal Marshalling, PTA" and PUIO_Count=="64" and PDIO_Count=="32": #13
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Universal Marshalling, PTA" and PUIO_Count=="32" and PDIO_Count=="32": #15
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and (Field_for_PDIO=="Universal Marshalling, PTA" or Field_for_PDIO=="Intrinsically Safe" or Field_for_PDIO=="32 IS, 32 Non-IS") and PUIO_Count=="32" and PDIO_Count=="64": #15
                var= 2 * Safety_Cabinets_qnt
            parts_dict["FC-TUIO51"] = {"Quantity" : int(var), "Description" : "SC FTA FC-PUIO01 KNIFE, EOL, 24VDC, 16CH, L"}

        elif Specify_Identifier=="No" and (S300=="Redundant S300" or S300== "No S300" or S300== "Non Redundant S300") and IO_Redundancy=="Non Redundant IO" and Safety_Cabinets_qnt !='' and Safety_Cabinets_qnt >0:
            var=0
            if Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and (PUIO_Count=="32"or '' ) and (PDIO_Count=="0" or ''): #2
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and (PUIO_Count=="64"or '' )and (PDIO_Count=="0" or ''): #4
                var= 4 * Safety_Cabinets_qnt
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO_Count=="32" and PDIO_Count=="32": #6
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO_Count=="32" and PDIO_Count=="64": #8
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO_Count=="64" and PDIO_Count=="32": #10
                var= 4 * Safety_Cabinets_qnt
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and PUIO_Count=="96" and (PDIO_Count=="0" or ''): #12
                var= 4 * Safety_Cabinets_qnt
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Universal Marshalling, PTA" and PUIO_Count=="64" and PDIO_Count=="32": #14
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Universal Marshalling, PTA" and PUIO_Count=="32" and PDIO_Count=="32": #16
                var= 2 * Safety_Cabinets_qnt
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and (Field_for_PDIO=="Universal Marshalling, PTA" or Field_for_PDIO=="Intrinsically Safe" or Field_for_PDIO=="32 IS, 32 Non-IS") and PUIO_Count=="32" and PDIO_Count=="64": #15
                var= 2 * Safety_Cabinets_qnt
            parts_dict["FC-TUIO51"] = {"Quantity" : int(var), "Description" : "SC FTA FC-PUIO01 KNIFE, EOL, 24VDC, 16CH, L"}

    return parts_dict
#part=identifier_FC_TUIO51(Product,parts_dict)
#Trace.Write("Parts= "+str(part))

#CXCPQ-34238
def get_identifier_SIC2005(Product,parts_dict):
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
                    var= Safety_Cabinets_qnt
                elif (Identifier_Modifier[6]=="M") and Identifier_Modifier[8]=="X" and Identifier_Modifier[9]=="A": #3
                    var= Safety_Cabinets_qnt
                elif (Identifier_Modifier[6]=="M") and Identifier_Modifier[8]=="X" and Identifier_Modifier[9]=="B": #5
                    var= Safety_Cabinets_qnt
                elif (Identifier_Modifier[5]=="M") and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="X": #7
                    var= Safety_Cabinets_qnt
                elif (Identifier_Modifier[5]=="M") and Identifier_Modifier[8]=="B" and Identifier_Modifier[9]=="X": #9
                    var= Safety_Cabinets_qnt
                elif (Identifier_Modifier[5]=="M") and (Identifier_Modifier[6]=="M") and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="A": #11
                    var= Safety_Cabinets_qnt
                elif (Identifier_Modifier[5]=="M") and (Identifier_Modifier[6]=="M") and Identifier_Modifier[8]=="B" and Identifier_Modifier[9]=="A": #13
                    var= Safety_Cabinets_qnt
                elif (Identifier_Modifier[5]=="M") and Identifier_Modifier[8]=="C" and Identifier_Modifier[9]=="X": #15
                    var= Safety_Cabinets_qnt
                elif (Identifier_Modifier[6]=="M") and Identifier_Modifier[8]=="X" and Identifier_Modifier[9]=="C": #17
                    var= Safety_Cabinets_qnt
                elif (Identifier_Modifier[5]=="U") and (Identifier_Modifier[6]=="M") and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="A": #19
                    var= Safety_Cabinets_qnt
                elif (Identifier_Modifier[5]=="U") and (Identifier_Modifier[6]=="M") and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="B": #21
                    var= Safety_Cabinets_qnt
                elif (Identifier_Modifier[5]=="M") and (Identifier_Modifier[6]=="U") and Identifier_Modifier[8]=="B" and Identifier_Modifier[9]=="A": #23
                    var= Safety_Cabinets_qnt
                elif (Identifier_Modifier[5]=="M") and (Identifier_Modifier[6]=="U" or Identifier_Modifier[6]=="I") and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="A": #25
                    var= Safety_Cabinets_qnt
                elif (Identifier_Modifier[5]=="M") and (Identifier_Modifier[6]=="U" or Identifier_Modifier[6]=="I" or Identifier_Modifier[6]=="C") and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="B": #27
                    var= Safety_Cabinets_qnt
                parts_dict["FC-SIC2005"] = {"Quantity" : int(var), "Description" : "SC SIC CABLE 2XCONNECTOR L 0.5M"}

            elif (Identifier_Modifier[3]=="S" or Identifier_Modifier[3]== "X") and Identifier_Modifier[13]=="X":
                var=0
                if (Identifier_Modifier[5]=="M") and (Identifier_Modifier[6]=="M") and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="B": #2
                    var= Safety_Cabinets_qnt
                elif (Identifier_Modifier[6]=="M") and Identifier_Modifier[8]=="X" and Identifier_Modifier[9]=="A": #4
                    var= Safety_Cabinets_qnt
                elif (Identifier_Modifier[6]=="M") and Identifier_Modifier[8]=="X" and Identifier_Modifier[9]=="B": #6
                    var= Safety_Cabinets_qnt
                elif (Identifier_Modifier[5]=="M") and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="X": #8
                    var= Safety_Cabinets_qnt
                elif (Identifier_Modifier[5]=="M") and Identifier_Modifier[8]=="B" and Identifier_Modifier[9]=="X": #10
                    var= Safety_Cabinets_qnt
                elif (Identifier_Modifier[5]=="M") and (Identifier_Modifier[6]=="M") and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="A": #12
                    var= Safety_Cabinets_qnt
                elif (Identifier_Modifier[5]=="M") and (Identifier_Modifier[6]=="M") and Identifier_Modifier[8]=="B" and Identifier_Modifier[9]=="A": #14
                    var= Safety_Cabinets_qnt
                elif (Identifier_Modifier[5]=="M") and Identifier_Modifier[8]=="C" and Identifier_Modifier[9]=="X": #16
                    var= Safety_Cabinets_qnt
                elif (Identifier_Modifier[6]=="M") and Identifier_Modifier[8]=="X" and Identifier_Modifier[9]=="C": #18
                    var= Safety_Cabinets_qnt
                elif (Identifier_Modifier[5]=="U") and (Identifier_Modifier[6]=="M") and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="A": #20
                    var= Safety_Cabinets_qnt
                elif (Identifier_Modifier[5]=="U") and (Identifier_Modifier[6]=="M") and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="B": #22
                    var= Safety_Cabinets_qnt
                elif (Identifier_Modifier[5]=="M") and (Identifier_Modifier[6]=="U") and Identifier_Modifier[8]=="B" and Identifier_Modifier[9]=="A": #24
                    var= Safety_Cabinets_qnt
                elif (Identifier_Modifier[5]=="M") and (Identifier_Modifier[6]=="U" or Identifier_Modifier[6]=="I") and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="A": #26
                    var= Safety_Cabinets_qnt
                elif (Identifier_Modifier[5]=="M") and (Identifier_Modifier[6]=="U" or Identifier_Modifier[6]=="I" or Identifier_Modifier[6]=="C") and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="B": #28
                    var= Safety_Cabinets_qnt
                parts_dict["FC-SIC2005"] = {"Quantity" : int(var), "Description" : "SC SIC CABLE 2XCONNECTOR L 0.5M"}

        elif Specify_Identifier=="No" and (S300=="Redundant S300" or S300 == "No S300") and IO_Redundancy=="Redundant IO" and Safety_Cabinets_qnt >0:
            var=0
            if Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO_Count=="32" and PDIO_Count=="64": #1
                var= Safety_Cabinets_qnt
            elif Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO_Count=="0" and PDIO_Count=="32": #3
                var= Safety_Cabinets_qnt
            elif Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO_Count=="0" and PDIO_Count=="64": #5
                var= Safety_Cabinets_qnt
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and PUIO_Count=="32" and PDIO_Count=="0": #7
                var= Safety_Cabinets_qnt
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and PUIO_Count=="64" and PDIO_Count=="0": #9
                var= Safety_Cabinets_qnt
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO_Count=="32" and PDIO_Count=="32": #11
                var= Safety_Cabinets_qnt
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO_Count=="64" and PDIO_Count=="32": #13
                var= Safety_Cabinets_qnt
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and PUIO_Count=="96" and PDIO_Count=="0": #15
                var= Safety_Cabinets_qnt
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and PUIO_Count=="0" and PDIO_Count=="96": #17
                var= Safety_Cabinets_qnt
            elif Field_for_PUIO=="Universal Marshalling, PTA" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO_Count=="32" and PDIO_Count=="32": #19
                var= Safety_Cabinets_qnt
            elif Field_for_PUIO=="Universal Marshalling, PTA" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO_Count=="32" and PDIO_Count=="64": #21
                var= Safety_Cabinets_qnt
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Universal Marshalling, PTA" and PUIO_Count=="64" and PDIO_Count=="32": #23
                var= Safety_Cabinets_qnt
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and (Field_for_PDIO=="Universal Marshalling, PTA" or Field_for_PDIO=="Intrinsically Safe") and PUIO_Count=="32" and PDIO_Count=="32": #25
                var= Safety_Cabinets_qnt
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and (Field_for_PDIO=="Universal Marshalling, PTA" or Field_for_PDIO=="Intrinsically Safe" or Field_for_PDIO=="32 IS, 32 Non-IS") and PUIO_Count=="32" and PDIO_Count=="64": #27
                var= Safety_Cabinets_qnt
            parts_dict["FC-SIC2005"] = {"Quantity" : int(var), "Description" : "SC SIC CABLE 2XCONNECTOR L 0.5M"}

        elif Specify_Identifier=="No" and (S300=="Redundant S300" or S300=="No S300") and IO_Redundancy=="Non Redundant IO" and Safety_Cabinets_qnt !='' and Safety_Cabinets_qnt >0:
            var=0
            if Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO_Count=="32" and PDIO_Count=="64": #2
                var= Safety_Cabinets_qnt
            elif Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO_Count=="0" and PDIO_Count=="32": #4
                var= Safety_Cabinets_qnt
            elif Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO_Count=="0" and PDIO_Count=="64": #6
                var= Safety_Cabinets_qnt
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and PUIO_Count=="32" and PDIO_Count=="0": #8
                var= Safety_Cabinets_qnt
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and PUIO_Count=="64" and PDIO_Count=="0": #10
                var= Safety_Cabinets_qnt
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO_Count=="32" and PDIO_Count=="32": #12
                var= Safety_Cabinets_qnt
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO_Count=="64" and PDIO_Count=="32": #14
                var= Safety_Cabinets_qnt
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and PUIO_Count=="96" and PDIO_Count=="0": #16
                var= Safety_Cabinets_qnt
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and PUIO_Count=="0" and PDIO_Count=="96": #18
                var= Safety_Cabinets_qnt
            elif Field_for_PUIO=="Universal Marshalling, PTA" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO_Count=="32" and PDIO_Count=="32": #20
                var= Safety_Cabinets_qnt
            elif Field_for_PUIO=="Universal Marshalling, PTA" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO_Count=="32" and PDIO_Count=="64": #22
                var= Safety_Cabinets_qnt
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Universal Marshalling, PTA" and PUIO_Count=="64" and PDIO_Count=="32": #24
                var= Safety_Cabinets_qnt
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and (Field_for_PDIO=="Universal Marshalling, PTA" or Field_for_PDIO=="Intrinsically Safe") and PUIO_Count=="32" and PDIO_Count=="32": #26
                var= Safety_Cabinets_qnt
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and (Field_for_PDIO=="Universal Marshalling, PTA" or Field_for_PDIO=="Intrinsically Safe" or Field_for_PDIO=="32 IS, 32 Non-IS") and PUIO_Count=="32" and PDIO_Count=="64": #28
                var= Safety_Cabinets_qnt
            parts_dict["FC-SIC2005"] = {"Quantity" : int(var), "Description" : "SC SIC CABLE 2XCONNECTOR L 0.5M"}



    return parts_dict
#fun= get_identifier_SIC2005(Product,parts_dict)
#Trace.Write("fun= "+str(fun))