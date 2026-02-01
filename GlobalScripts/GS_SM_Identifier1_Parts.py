parts_dict={}
def getPartsQty(container):
    partsQty = dict()
    if container.Rows.Count > 0:
        for cont_row in container.Rows:
            partName = cont_row.GetColumnByName('CE_Part_Number').Value
            qty = int(cont_row.GetColumnByName('CE_Final_Quantity').Value) if cont_row.GetColumnByName('CE_Final_Quantity').Value.strip() != '' else 0
            partsQty[partName] = qty
    return partsQty
def getPartQuantity(parts_dict,part):
    try:
        return int(parts_dict[part]['Quantity'])
    except KeyError:
        return 0
#parts qty
def getQty(partsQty, partName):
    qty = 0
    if partName in partsQty:
        qty = partsQty[partName]
    return qty
def identifier_Modifier1(Product,parts_dict):
    Enclosure_Type=Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0].GetColumnByName('Enclosure_Type').DisplayValue
    if Enclosure_Type == "Universal Safety Cab-1.3M":
        Specify_Identifier=Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont').Rows[0].GetColumnByName('Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet').DisplayValue
        Material_Type_Ingress=Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('Cabinet_Material_Type_Ingress_Protection').DisplayValue
        Power_Supply_Type=Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('Power_Supply_Type').DisplayValue
        Power_Supply_Redundancy=Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('Power_Supply_Redundancy').DisplayValue
        Ambient_Temperature_Range=Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('Ambient_Temperature_Range').DisplayValue
        Field_for_PUIO=Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('Field_Termination_Assembly_for_PUIO').DisplayValue
        Field_for_PDIO=Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('Field_Termination_Assembly_for_PDIO').DisplayValue
        Abu_Dhabi=Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('Abu_Dhabi_Build_Loc').DisplayValue
        S300=Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('S300').DisplayValue
        PUIO=Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('PUIO_Count').DisplayValue
        PDIO=Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('PDIO_Count').DisplayValue
        IO_Redundancy=Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('IO_Redundancy').DisplayValue
        SCCNTL05=attri= 0
        partsQty = []
        contParts = Product.GetContainerByName('SM_RG_PartSummary_Cont')
        partsQty = getPartsQty(contParts)
        SCCNTL05 = getQty(partsQty, 'FC-SCNT02')
        SCCNTL05= int(SCCNTL05)
        attri=Product.Attr('SM_RG_lic_SUM').GetValue() if Product.Attr('SM_RG_lic_SUM').GetValue()!='' else 0
        attri=int(attri)
        try:
            Identifier_Modifier=Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont').Rows[0].GetColumnByName('Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet').Value
            Trace.Write(Identifier_Modifier)
        except:
            Identifier_Modifier=0
        Safety_Cabinets_qnt=Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont').Rows[0].GetColumnByName('Number_of_SM_SC_1.3M_Universal_Safety_Cabinets_(0-63)').Value
        if Safety_Cabinets_qnt!='':
            Safety_Cabinets_qnt=int(Safety_Cabinets_qnt)
        else:
            Safety_Cabinets_qnt=0
        Trace.Write(Identifier_Modifier)
        strL=list(Identifier_Modifier)
        lenght_str=len(list(Identifier_Modifier))
        Trace.Write(str(strL))
        if lenght_str>20:
            str0=strL[0]
            str1=strL[1]
            str2=strL[2]
            str3=strL[3]
            str4=strL[4]
            str5=strL[5]
            str6=strL[6]
            str7=strL[7]
            str8=strL[8]
            str9=strL[9]
            str10=strL[10]
            str11=strL[11]
            str12=strL[12]
            str13=strL[13]
            str14=strL[14]
            str15=strL[15]
            str16=strL[16]
            str17=strL[17]
            str18=strL[18]
            str19=strL[19]
            str20=strL[20]
        #CXCPQ-34245
        var=0
        var1=0
        if Specify_Identifier=="No" and (S300=="Redundant S300" or S300=="No S300") and IO_Redundancy=="Redundant IO":
            if Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO=="64" and PDIO=="32":#1
                #Trace.Write("part1")
                var= 3 * int(Safety_Cabinets_qnt)
            elif Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO=="0" and PDIO=="64":#3
                #Trace.Write("part3")
                var= 3 * int(Safety_Cabinets_qnt) 
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and PUIO=="64" and PDIO=="0":#5
                #Trace.Write("part5")
                var= 3 * int(Safety_Cabinets_qnt)
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO=="32" and PDIO=="32":#7
                #Trace.Write("part7")
                var= 3 * int(Safety_Cabinets_qnt)
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO=="32" and PDIO=="64":#9
                #Trace.Write("part9")
                var= 3 * int(Safety_Cabinets_qnt) 
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and PUIO=="96" and PDIO=="0":#11
                #Trace.Write("part11")
                var= 3 * int(Safety_Cabinets_qnt) 
            elif Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO=="0" and PDIO=="96":#13
                #Trace.Write("part13")
                var= 3 * int(Safety_Cabinets_qnt) 
            elif Field_for_PUIO=="Universal Marshalling, PTA" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO=="32" and PDIO=="64":#15
                #Trace.Write("part15")
                var= 3 * int(Safety_Cabinets_qnt) 
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Intrinsically Safe"  and PUIO=="64" and PDIO=="32":#17
                #Trace.Write("part17")
                var= 2 * int(Safety_Cabinets_qnt)
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Universal Marshalling, PTA" and PUIO=="64" and PDIO=="32":
                var= int(Safety_Cabinets_qnt)
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and (Field_for_PDIO=="Universal Marshalling, PTA" or Field_for_PDIO=="Intrinsically Safe") and PUIO=="32" and PDIO=="32":
                var= int(Safety_Cabinets_qnt)
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and (Field_for_PDIO=="Universal Marshalling, PTA" or Field_for_PDIO=="Intrinsically Safe" or Field_for_PDIO=="32 IS, 32 Non-IS") and PUIO=="32" and PDIO=="64":
                var= int(Safety_Cabinets_qnt)
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and PUIO=="32" and PDIO=="0":
                var= int(Safety_Cabinets_qnt)
            elif Field_for_PUIO=="Universal Marshalling, PTA" and Field_for_PDIO=="M" and PUIO=="32" and PDIO=="32":
                var= int(Safety_Cabinets_qnt)
            elif Field_for_PDIO=="Default Marshalling FC-TUIO51/52" and PUIO=="0" and PDIO=="32":
                var= int(Safety_Cabinets_qnt)
            elif Field_for_PDIO=="Default Marshalling FC-TUIO51/52" and PUIO=="0" and PDIO=="96":
                var= int(Safety_Cabinets_qnt)
            if var>0:
                parts_dict["FC-SIC2010"] = {"Quantity" : int(var), "Description" : "SC SIC CABLE 2XCONNECTOR L 1M"}
        #CXCPQ-34245(2)
        if Specify_Identifier=="No" and (S300=="Redundant S300" or S300=="No S300") and IO_Redundancy=="Non Redundant IO":
            if Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO=="64" and PDIO=="32":#2
                #Trace.Write("part2")
                var= 3 * int(Safety_Cabinets_qnt)
            elif Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO=="0" and PDIO=="64":#4
                #Trace.Write("part4")
                var= 3 * int(Safety_Cabinets_qnt) 
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and PUIO=="64" and PDIO=="0":#6
                #Trace.Write("part6")
                var= 3 * int(Safety_Cabinets_qnt) 
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO=="32" and PDIO=="32":#8
                #Trace.Write("part8")
                var= 3 * int(Safety_Cabinets_qnt) 
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO=="32" and PDIO=="64":#10
                #Trace.Write("part10")
                var= 3 * int(Safety_Cabinets_qnt) 
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and PUIO=="96" and PDIO=="0":#12
                #Trace.Write("part12")
                var= 3 * int(Safety_Cabinets_qnt) 
            elif Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO=="0" and PDIO=="96":#14
                #Trace.Write("part14")
                var= 3 * int(Safety_Cabinets_qnt) 
            elif Field_for_PUIO=="Universal Marshalling, PTA" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO=="32" and PDIO=="64":#16
                #Trace.Write("part16")
                var= 3 * int(Safety_Cabinets_qnt) 
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Intrinsically Safe" and PUIO=="64" and PDIO=="32":#18
                #Trace.Write("part18")
                var= 2 * int(Safety_Cabinets_qnt)
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Universal Marshalling, PTA" and PUIO=="64" and PDIO=="32":
                var= int(Safety_Cabinets_qnt)
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and (Field_for_PDIO=="Universal Marshalling, PTA" or Field_for_PDIO=="Intrinsically Safe") and PUIO=="32" and PDIO=="32":
                var= int(Safety_Cabinets_qnt)
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and (Field_for_PDIO=="Universal Marshalling, PTA" or Field_for_PDIO=="Intrinsically Safe" or Field_for_PDIO=="32 IS, 32 Non-IS") and PUIO=="32" and PDIO=="64":
                var= int(Safety_Cabinets_qnt)
            elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and PUIO=="32" and PDIO=="0":
                var= int(Safety_Cabinets_qnt)
            elif Field_for_PUIO=="Universal Marshalling, PTA" and Field_for_PDIO=="M" and PUIO=="32" and PDIO=="32":
                var= int(Safety_Cabinets_qnt)
            elif Field_for_PDIO=="Default Marshalling FC-TUIO51/52" and PUIO=="0" and PDIO=="32":
                var= int(Safety_Cabinets_qnt)
            elif Field_for_PDIO=="Default Marshalling FC-TUIO51/52" and PUIO=="0" and PDIO=="96":
                var= int(Safety_Cabinets_qnt)
            if var>0:
                parts_dict["FC-SIC2010"] = {"Quantity" : int(var), "Description" : "SC SIC CABLE 2XCONNECTOR L 1M"}
        #CXCPQ-34240
        if Specify_Identifier=="No" and (S300=="Redundant S300" or S300=="No S300") and IO_Redundancy=="Redundant IO":
            if Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Universal Marshalling, PTA" and PUIO=="64" and PDIO=="32":#1
                #Trace.Write("part1")
                var1= 2* int(Safety_Cabinets_qnt)
            elif (Field_for_PUIO=="Universal Marshalling, PTA" or Field_for_PUIO=="Intrinsically Safe") and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO=="32" and PDIO=="64":#3
                #Trace.Write("part3")
                var1= 2* int(Safety_Cabinets_qnt)
            elif (Field_for_PDIO=="Universal Marshalling, PTA" or Field_for_PDIO=="Intrinsically Safe" or Field_for_PDIO=="64 IS, 32 Non-IS" or Field_for_PDIO=="32 IS, 64 Non-IS")  and PUIO=="0" and PDIO=="96":#5
                #Trace.Write("part5.5")
                var1= 2* int(Safety_Cabinets_qnt)
            elif (Field_for_PUIO=="Universal Marshalling, PTA" or Field_for_PUIO=="Intrinsically Safe") and (Field_for_PDIO=="Universal Marshalling, PTA" or Field_for_PDIO=="Intrinsically Safe" or Field_for_PDIO=="32 IS, 32 Non-IS") and PUIO=="32" and PDIO=="64":#7
                #Trace.Write("part7")
                var1= 2* int(Safety_Cabinets_qnt)
            elif (Field_for_PUIO=="Universal Marshalling, PTA" or Field_for_PUIO=="Intrinsically Safe" or Field_for_PUIO=="32 IS, 32 Non-IS") and (Field_for_PDIO=="Universal Marshalling, PTA" or Field_for_PDIO=="Intrinsically Safe") and PUIO=="64" and PDIO=="32":#9
                #Trace.Write("part9")
                var1= 2* int(Safety_Cabinets_qnt)
            elif (Field_for_PUIO=="Default Marshalling FC-TUIO51/52") and (Field_for_PDIO=="Universal Marshalling, PTA" or Field_for_PDIO=="Intrinsically Safe" or Field_for_PDIO=="32 IS, 32 Non-IS") and PUIO=="32" and PDIO=="64":#11
                #Trace.Write("part11")
                var1= 2* int(Safety_Cabinets_qnt)
            elif (Field_for_PUIO=="Universal Marshalling, PTA" or Field_for_PUIO=="Intrinsically Safe" or Field_for_PUIO=="64 IS, 32 Non-IS" or Field_for_PUIO=="32 IS, 64 Non-IS") and PUIO=="96" and PDIO=="0":#13
                #Trace.Write("part13")
                var1= 2* int(Safety_Cabinets_qnt)
            if var1>0:
                parts_dict["FC-SIC5020"] = {"Quantity" : int(var1), "Description" : "Ethernet cable, Red and Blue L 2M"}
        #CXCPQ-34240(2)
        elif Specify_Identifier=="No" and (S300=="Redundant S300" or S300=="No S300" or S300=="Non Redundant S300") and IO_Redundancy=="Non Redundant IO":
            if Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Universal Marshalling, PTA" and PUIO=="64" and PDIO=="32":#2
                #Trace.Write("part2")
                var1= 2* int(Safety_Cabinets_qnt)
            elif (Field_for_PUIO=="Universal Marshalling, PTA" or Field_for_PUIO=="Intrinsically Safe") and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and PUIO=="32" and PDIO=="64":#4
                #Trace.Write("part4")
                var1= 2* int(Safety_Cabinets_qnt)
            elif (Field_for_PDIO=="Universal Marshalling, PTA" or Field_for_PDIO=="Intrinsically Safe" or Field_for_PDIO=="64 IS, 32 Non-IS" or Field_for_PDIO=="32 IS, 64 Non-IS")  and PUIO=="0" and PDIO=="96":#6
                #Trace.Write("part6")
                var1= 2* int(Safety_Cabinets_qnt)
            elif (Field_for_PUIO=="Universal Marshalling, PTA" or Field_for_PUIO=="Intrinsically Safe") and (Field_for_PDIO=="Universal Marshalling, PTA" or Field_for_PDIO=="Intrinsically Safe" or Field_for_PDIO=="32 IS, 32 Non-IS") and PUIO=="32" and PDIO=="64":#8
                #Trace.Write("part8")
                var1= 2* int(Safety_Cabinets_qnt)
            elif (Field_for_PUIO=="Universal Marshalling, PTA" or Field_for_PUIO=="Intrinsically Safe" or Field_for_PUIO=="32 IS, 32 Non-IS") and (Field_for_PDIO=="Universal Marshalling, PTA" or Field_for_PDIO=="Intrinsically Safe") and PUIO=="64" and PDIO=="32":#10
                #Trace.Write("part10")
                var1= 2* int(Safety_Cabinets_qnt)
            elif (Field_for_PUIO=="Default Marshalling FC-TUIO51/52") and (Field_for_PDIO=="Universal Marshalling, PTA" or Field_for_PDIO=="Intrinsically Safe" or Field_for_PDIO=="32 IS, 32 Non-IS") and PUIO=="32" and PDIO=="64":#12
                #Trace.Write("part12")
                var1= 2* int(Safety_Cabinets_qnt)
            elif (Field_for_PUIO=="Universal Marshalling, PTA" or Field_for_PUIO=="Intrinsically Safe" or Field_for_PUIO=="32 IS, 64 Non-IS" or Field_for_PUIO=="64 IS, 32 Non-IS") and PUIO=="96" and PDIO=="0":#14
                #Trace.Write("part14")
                var1= 2* int(Safety_Cabinets_qnt)
            if var1>0:
                parts_dict["FC-SIC5020"] = {"Quantity" : int(var1), "Description" :"Ethernet cable, Red and Blue L 2M"}
        if lenght_str>20:
            #CXCPQ-34245
            if (str3=="S" or str3=="X") and str13=="R" and Specify_Identifier=="Yes" and lenght_str>20:
                if str5=="M" and str6=="M" and str8=="B" and str9=="A":#1
                    #Trace.Write("part1")
                    var= 3 * int(Safety_Cabinets_qnt)
                elif str6=="M" and str8=="X" and str9=="B":#3
                    #Trace.Write("part3")
                    var= 3 * int(Safety_Cabinets_qnt) 
                elif str5=="M" and str8=="B" and str9=="X":#5
                    #Trace.Write("part4")
                    var= 3 * int(Safety_Cabinets_qnt) 
                elif str5=="M" and str6=="M" and str8=="A" and str9=="A":#7
                    #Trace.Write("Part7")
                    var= 3 * int(Safety_Cabinets_qnt)
                elif str5=="M" and str6=="M" and str8=="A" and str9=="B":#9
                    #Trace.Write("Part9")
                    var= 3 * int(Safety_Cabinets_qnt) 
                elif str5=="M" and str8=="C" and str9=="X":#11
                    #Trace.Write("part11")
                    var= 3 * int(Safety_Cabinets_qnt) 
                elif str6=="M" and str8=="X" and str9=="C":#13
                    #Trace.Write("part13")
                    var= 3 * int(Safety_Cabinets_qnt)
                elif str5=="U" and str6=="M" and str8=="A" and str9=="B":#15
                    #Trace.Write("part15")
                    var= 3 * int(Safety_Cabinets_qnt)
                elif str5=="M" and str6=="I" and str8=="B" and str9=="A":#17
                    #Trace.Write("part17")
                    var= 2 * int(Safety_Cabinets_qnt)
                elif str5=="M" and str6=="U" and str8=="B" and str9=="A":
                    var= int(Safety_Cabinets_qnt)
                elif str5=="M" and (str6=="U" or str6=="I") and str8=="A" and str9=="A":
                    var= int(Safety_Cabinets_qnt)
                elif str5=="M" and (str6=="U" or str6=="I" or str6=="C") and str8=="A" and str9=="B":
                    var= int(Safety_Cabinets_qnt)
                elif str5=="M" and str8=="A" and str9=="X":
                    var= int(Safety_Cabinets_qnt)
                elif str5=="U" and str6=="M" and str8=="A" and str9=="A":
                    var= int(Safety_Cabinets_qnt)
                elif str6=="M" and str8=="X" and str9=="A":
                    var= int(Safety_Cabinets_qnt)
                elif str6=="M" and str8=="X" and str9=="C":
                    var= int(Safety_Cabinets_qnt)
                if var>0:
                    parts_dict["FC-SIC2010"] = {"Quantity" : int(var), "Description" : "SC SIC CABLE 2XCONNECTOR L 1M"}
            if (str3=="S" or str3=="X") and str13=="X" and Specify_Identifier=="Yes" and lenght_str>20:
                if str5=="M" and str6=="M" and str8=="B" and str9=="A":#2
                    #Trace.Write("Part2")
                    var= 3 * int(Safety_Cabinets_qnt)
                elif str6=="M" and str8=="X" and str9=="B":#4
                    #Trace.Write("Part4")
                    var= 3 * int(Safety_Cabinets_qnt)
                elif str5=="M" and str8=="B" and str9=="X":#6
                    #Trace.Write("Part6")
                    var= 3 * int(Safety_Cabinets_qnt)
                elif str5=="M" and str6=="M" and str8=="A" and str9=="A":#8
                    #Trace.Write("Part8")
                    var= 3 * int(Safety_Cabinets_qnt)
                elif str5=="M" and str6=="M" and str8=="A" and str9=="B":#10
                    #Trace.Write("part10")
                    var= 3 * int(Safety_Cabinets_qnt)
                elif str5=="M" and str8=="C" and str9=="X":#12
                    #Trace.Write("part12")
                    var= 3 * int(Safety_Cabinets_qnt)
                elif str6=="M" and str8=="X" and str9=="C":#14
                    #Trace.Write("part14")
                    var= 3 * int(Safety_Cabinets_qnt)
                elif str5=="U" and str6=="M" and str8=="A" and str9=="B":#16
                    #Trace.Write("part16")
                    var= 3 * int(Safety_Cabinets_qnt)
                elif str5=="M" and str6=="I" and str8=="B" and str9=="A":
                    #Trace.Write("part18")
                    var= 2 * int(Safety_Cabinets_qnt)
                elif str5=="M" and str6=="U" and str8=="B" and str9=="A":
                    var= int(Safety_Cabinets_qnt)
                elif str5=="M" and (str6=="U" or str6=="I") and str8=="A" and str9=="A":
                    var= int(Safety_Cabinets_qnt)
                elif str5=="M" and (str6=="U" or str6=="I" or str6=="C") and str8=="A" and str9=="B":
                    var= int(Safety_Cabinets_qnt)
                elif str5=="M" and str8=="A" and str9=="X":
                    var= int(Safety_Cabinets_qnt)
                elif str5=="U" and str6=="M" and str8=="A" and str9=="A":
                    var= int(Safety_Cabinets_qnt)
                elif str6=="M" and str8=="X" and str9=="A":
                    var= int(Safety_Cabinets_qnt)
                elif str6=="M" and str8=="X" and str9=="C":
                    var= int(Safety_Cabinets_qnt)
                if var>0:
                	parts_dict["FC-SIC2010"] = {"Quantity" : int(var), "Description" : "SC SIC CABLE 2XCONNECTOR L 1M"}
            #CXCPQ-34240
            if (str3=="S" or str3=="X") and Specify_Identifier=="Yes" and lenght_str>20 :
                if str5=="M" and str6=="U" and str8=="B" and str9=="A" and str13=="R":#1
                    #Trace.Write("part1.1")
                    var1= 2 * int(Safety_Cabinets_qnt)
                elif (str5=="U" or str5=="I") and str6=="M" and str8=="A" and str9=="B"  and str13=="R" :#3
                    #Trace.Write("Part3.3")
                    var1= 2 * int(Safety_Cabinets_qnt)
                elif (str6=="U" or str6=="I" or str6=="A" or str6=="B") and str8=="X" and str9=="C"  and str13=="R":#5
                    #Trace.Write("Part5.5")
                    var1= 2 * int(Safety_Cabinets_qnt)
                elif (str5=="U" or str5=="I") and (str6=="U" or str6=="I" or str6=="C") and str8=="A" and str9=="B" and str13=="R":#7
                    #Trace.Write("Part7.7")
                    var1= 2 * int(Safety_Cabinets_qnt)
                elif (str5=="U" or str5=="I" or str5=="C") and (str6=="U" or str6=="I") and str8=="B" and str9=="A" and str13=="R":#9
                    #Trace.Write("Part9.9")
                    var1= 2 * int(Safety_Cabinets_qnt)
                elif (str5=="M") and (str6=="U" or str6=="I"or str6=="C") and str8=="A" and str9=="B" and str13=="R":#11
                    #Trace.Write("Part11.11")
                    var1= 2 * int(Safety_Cabinets_qnt)
                elif (str5=="U" or str5=="I" or str5=="A" or str5=="B") and str8=="C" and str9=="X" and str13=="R":#13
                    #Trace.Write("Part13.13")
                    var1= 2 * int(Safety_Cabinets_qnt)
                if var1>0:
                    parts_dict["FC-SIC5020"] = {"Quantity" : int(var1), "Description" : "Ethernet cable, Red and Blue L 2M"}
            if (str3=="S" or str3=="X" or str3=="N") and Specify_Identifier=="Yes" and lenght_str>20 :
                if str5=="M" and str6=="U" and str8=="B" and str9=="A" and str13=="X":#2
                    #Trace.Write("Part2.2")
                    var1= 2 * int(Safety_Cabinets_qnt)
                elif (str5=="U" or str5=="I") and str6=="M" and str8=="A" and str9=="B" and str13=="X":#4
                    #Trace.Write("Part4.4")
                    var1= 2 * int(Safety_Cabinets_qnt)
                elif (str6=="U" or str6=="I" or str6=="A" or str6=="B") and str8=="X" and str9=="C" and str13=="X":#6
                    #Trace.Write("Part6.6")
                    var1= 2 * int(Safety_Cabinets_qnt) 
                elif (str5=="U" or str5=="I") and (str6=="U" or str6=="I" or str6=="C") and str8=="A" and str9=="B" and str13=="X":#8
                    #Trace.Write("Part8.8")
                    var1= 2 * int(Safety_Cabinets_qnt)
                elif (str5=="U" or str5=="I" or str5=="C") and (str6=="U" or str6=="I") and str8=="B" and str9=="A" and str13=="X":#10
                    #Trace.Write("Part10.10")
                    var1= 2 * int(Safety_Cabinets_qnt)
                elif (str5=="M") and (str6=="U" or str6=="I"or str6=="C") and str8=="A" and str9=="B" and str13=="X":#12
                    #Trace.Write("Part12.12")
                    var1= 2 * int(Safety_Cabinets_qnt)
                elif (str5=="U" or str5=="I" or str5=="A" or str5=="B") and str8=="C" and str9=="X" and str13=="X":#14
                    #Trace.Write("Part14.14")
                    var1= 2 * int(Safety_Cabinets_qnt)
                if var1>0:
                    parts_dict["FC-SIC5020"] = {"Quantity" : int(var1), "Description" : "Ethernet cable, Red and Blue L 2M"} 
    return parts_dict
#X=identifier_Modifier1(Product,parts_dict)
#Trace.Write(str(X))