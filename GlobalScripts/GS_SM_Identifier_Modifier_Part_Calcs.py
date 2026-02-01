#parts_dict={}
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
def identifier_Modifier(Product,parts_dict):
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
        Fiber_Optic=Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('Fiber_Optic_Extender').DisplayValue
        CNM = Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("Number_of_Control_Network_Module_0-100").Value
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
        #CXCPQ-32149,CXCPQ-32150 and CXCPQ-32151
        var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
        if Specify_Identifier=="No" and S300!="No S300" and var >0:
            parts_dict["FC-TCNT11"] = {"Quantity" : int(var), "Description" : "SC S300 IOTA CNTRL REDUNDANT"}
            '''if SCCNTL05 >0 and attri >=1 and attri <=96 and S300!="Non Redundant S300":
                var1= var + SCCNTL05
            else:
                var1=var
            parts_dict["FS-SCCNTL05"] = {"Quantity" : int(var1), "Description" : "SC S300 CNTRL LIC SMALL RED IO 1-96"}'''
        #CXCPQ-54746 - Start
        '''if Specify_Identifier=="No" and S300=="Non Redundant S300" and var >0:
            parts_dict["FS-CCI-HSE-01"] = {"Quantity" : int(var), "Description" : "Ethernet cable, Yellow and Green L 1.0 M"}
        elif Specify_Identifier=="No" and S300=="Redundant S300" and var >0:
            parts_dict["FS-CCI-HSE-01"] = {"Quantity" : int(2*var), "Description" : "Ethernet cable, Yellow and Green L 1.0 M"}'''
        #CXCPQ-54746 - End
        #CXCPQ-31618 AND 31666
        if Specify_Identifier=="No" and Ambient_Temperature_Range=="With Fan, Max Ambient +55°C":
            var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
            Trace.Write("var"+str(var))
            if var>0:
                parts_dict["51454248-100"] = {"Quantity" : int(var), "Description" : "Fan Assembly"}
         #CXCPQ-31671
        if Specify_Identifier=="No" and  Power_Supply_Type=="48A FC-PSU-UNI2450U" and Power_Supply_Redundancy == "Redundant" :
            var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
            if var>0:
                parts_dict["50159474-006"] = {"Quantity" : int(var), "Description" : "Power Back Plate Assy- Eplax Power supply"}
        #CXCPQ-31678
        if Specify_Identifier=="No" and Material_Type_Ingress=="316L Stainless 1.3M, IP66" and Ambient_Temperature_Range=="Without Fan, Max Ambient +40°C" and Power_Supply_Type=="24 VDC/DC QUINT 4+ Supply" and (Field_for_PUIO =="Default Marshalling FC-TUIO51/52" or Field_for_PUIO == "Universal Marshalling, PTA") and (Field_for_PDIO =="Default Marshalling FC-TDIO51/52" or Field_for_PDIO == "Universal Marshalling, PTA") and Power_Supply_Redundancy == "Redundant" and Abu_Dhabi == "No":
            var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
            if var>0:
                parts_dict["50159996-306"] = {"Quantity" : int(var), "Description" : "USC SYSTEM LABEL, SS CABINET"}
        #CXCPQ-31672
        if Specify_Identifier=="No" and Material_Type_Ingress=="316L Stainless 1.3M, IP66" and Ambient_Temperature_Range=="Without Fan, Max Ambient +40°C" and Power_Supply_Type=="24A AC/DC FC-PSUNI2424" and (Field_for_PUIO =="Default Marshalling FC-TUIO51/52" or Field_for_PUIO == "Universal Marshalling, PTA") and (Field_for_PDIO =="Default Marshalling FC-TDIO51/52" or Field_for_PDIO == "Universal Marshalling, PTA") and Power_Supply_Redundancy == "Redundant" and Abu_Dhabi == "No":
            var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
            if var>0:
                parts_dict["50159996-300"] = {"Quantity" : int(var), "Description" : "USC SYSTEM LABEL, SS CABINET"}
        #CXCPQ-31671
        if Specify_Identifier=="No" and Material_Type_Ingress=="316L Stainless 1.3M, IP66" and Ambient_Temperature_Range=="With Fan, Max Ambient +55°C" and Power_Supply_Type=="20A AC/DC QUINT 4+ PS" and (Field_for_PUIO =="Default Marshalling FC-TUIO51/52" or Field_for_PUIO == "Universal Marshalling, PTA") and (Field_for_PDIO =="Default Marshalling FC-TDIO51/52" or Field_for_PDIO =="Universal Marshalling, PTA") and Power_Supply_Redundancy == "Redundant" and Abu_Dhabi == "No":
            var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
            if var>0:
                parts_dict["50159996-305"] = {"Quantity" : int(var), "Description" : "USC SYSTEM LABEL, SS CABINET WITH FANS"}
        #CXCPQ-31673
        if Specify_Identifier=="No" and Material_Type_Ingress=="316L Stainless 1.3M, IP66" and Ambient_Temperature_Range=="With Fan, Max Ambient +55°C" and Power_Supply_Type=="24A AC/DC FC-PSUNI2424" and (Field_for_PUIO =="Default Marshalling FC-TUIO51/52" or Field_for_PUIO == "Universal Marshalling, PTA") and (Field_for_PDIO =="Default Marshalling FC-TDIO51/52" or Field_for_PDIO == "Universal Marshalling, PTA") and Power_Supply_Redundancy == "Redundant" and Abu_Dhabi == "No":
            var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
            if var>0:
                parts_dict["50159996-301"] = {"Quantity" : int(var), "Description" : "USC SYSTEM LABEL, SS CABINET WITH FANS"}
        #CXCPQ-31707
        if Specify_Identifier=="No" and Material_Type_Ingress=="316L Stainless 1.3M, IP66" and Ambient_Temperature_Range=="With Fan, Max Ambient +55°C" and Power_Supply_Type=="24 VDC/DC QUINT 4+ Supply" and (Field_for_PUIO =="Default Marshalling FC-TUIO51/52" or Field_for_PUIO =="Universal Marshalling, PTA") and (Field_for_PDIO =="Default Marshalling FC-TDIO51/52" or Field_for_PDIO == "Universal Marshalling, PTA") and Power_Supply_Redundancy == "Redundant" and Abu_Dhabi == "Yes":
            var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
            if var>0:
                parts_dict["50159996-323"] = {"Quantity" : int(var), "Description" : "USC SYSTEM LABEL, SS CABINET WITH FANS, ABU DHABI"}
        #CXCPQ-31708
        if Specify_Identifier=="No" and Material_Type_Ingress=="316L Stainless 1.3M, IP66" and Ambient_Temperature_Range=="With Fan, Max Ambient +55°C" and Power_Supply_Type=="24A AC/DC FC-PSUNI2424" and Field_for_PUIO =="Intrinsically Safe" and Field_for_PDIO =="Intrinsically Safe" and Power_Supply_Redundancy == "Redundant" and Abu_Dhabi == "Yes":
            var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
            if var>0:
                parts_dict["50159996-325"] = {"Quantity" : int(var), "Description" : "USC SYSTEM LABEL, SS CABINET WITH FANS, IS"}
        #CXCPQ-31711
        if Specify_Identifier=="No" and Material_Type_Ingress=="316L Stainless 1.3M, IP66" and Ambient_Temperature_Range=="With Fan, Max Ambient +55°C" and Power_Supply_Type=="48A FC-PSU-UNI2450U" and Field_for_PUIO =="Intrinsically Safe" and Field_for_PDIO =="Intrinsically Safe" and Power_Supply_Redundancy == "Redundant" and Abu_Dhabi == "Yes":
            var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
            if var>0:
                parts_dict["50159996-327"] = {"Quantity" : int(var), "Description" : "USC SYSTEM LABEL, SS CABINET WITH FANS, IS"}
        #Cxcpq-31666
        if Specify_Identifier=="No" and Material_Type_Ingress=="316L Stainless 1.3M, IP66":
            var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
            Trace.Write("var"+str(var))
            if var>0:
                parts_dict["50154983-001"] = {"Quantity" : int(var), "Description" : "1.3M, 316L Stainless IP66 Cabinet "}
        #CXCPQ-31668
        if Specify_Identifier=="No" and Power_Supply_Type=="24A AC/DC FC-PSUNI2424" and Power_Supply_Redundancy=="Redundant":
                var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
                if var>0:
                    parts_dict["50159474-002"] = {"Quantity" : int(var), "Description" : "Power Back Plate Assy - ATDI 600W Redundant"}
        #CXCPQ-31669
        if Specify_Identifier=="No" and Power_Supply_Type=="24 VDC/DC QUINT 4+ Supply" and Power_Supply_Redundancy=="Redundant":
                var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
                if var>0:
                    parts_dict["50159474-004"] = {"Quantity" : int(var), "Description" : "Power Back Plate Assy - DC Quint 4+ Redundant"}

        #CXCPQ-31731
		#commented CCEECOMMBR-6977
        """if Specify_Identifier=="No" and Power_Supply_Type=="24 VDC/DC QUINT 4+ Supply":
            var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
            Trace.Write("var"+str(var))
            if var>0:
                parts_dict["50159998-200"] = {"Quantity" : int(var), "Description" : "USC FUSE REFERENCE GUIDE, FOR DC MAINS"}"""
        #CXCPQ-31682
        if Specify_Identifier=="No" and Material_Type_Ingress=="316L Stainless 1.3M, IP66" and Ambient_Temperature_Range=="With Fan, Max Ambient +55°C" and Power_Supply_Type=="24 VDC/DC QUINT 4+ Supply" and (Field_for_PUIO =="Default Marshalling FC-TUIO51/52" or Field_for_PUIO == "Universal Marshalling, PTA") and (Field_for_PDIO =="Default Marshalling FC-TDIO51/52" or Field_for_PDIO =="Universal Marshalling, PTA") and Power_Supply_Redundancy == "Redundant" and Abu_Dhabi == "No":
            var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
            if var>0:
                parts_dict["50159996-307"] = {"Quantity" : int(var), "Description" : "USC SYSTEM LABEL, SS CABINET WITH FANS"}
        #CXCPQ-31683
        if Specify_Identifier=="No" and Material_Type_Ingress=="316L Stainless 1.3M, IP66" and Ambient_Temperature_Range=="With Fan, Max Ambient +55°C" and Power_Supply_Type=="24A AC/DC FC-PSUNI2424" and (Field_for_PUIO =="Intrinsically Safe") and (Field_for_PDIO =="Intrinsically Safe") and Power_Supply_Redundancy == "Redundant" and Abu_Dhabi == "No":
            var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
            if var>0:
                parts_dict["50159996-309"] = {"Quantity" : int(var), "Description" : "USC SYSTEM LABEL, SS CABINET WITH FANS,"}
        #CXCPQ-31685
        if Specify_Identifier=="No" and Material_Type_Ingress=="316L Stainless 1.3M, IP66" and Ambient_Temperature_Range=="With Fan, Max Ambient +55°C" and Power_Supply_Type=="48A FC-PSU-UNI2450U" and (Field_for_PUIO =="Intrinsically Safe") and (Field_for_PDIO =="Intrinsically Safe") and Power_Supply_Redundancy == "Redundant" and Abu_Dhabi == "No":
            var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
            if var>0:
                parts_dict["50159996-311"] = {"Quantity" : int(var), "Description" : "USC SYSTEM LABEL, SS CABINET WITH FANS,"}
        #CXCPQ-31691
        if Specify_Identifier=="No" and Material_Type_Ingress=="316L Stainless 1.3M, IP66" and Ambient_Temperature_Range=="With Fan, Max Ambient +55°C" and Power_Supply_Type=="24A AC/DC FC-PSUNI2424" and (Field_for_PUIO =="Default Marshalling FC-TUIO51/52" or Field_for_PUIO =="Universal Marshalling, PTA") and (Field_for_PDIO =="Default Marshalling FC-TDIO51/52" or Field_for_PDIO == "Universal Marshalling, PTA") and Abu_Dhabi == "Yes":
            var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
            if var>0:
                parts_dict["50159996-317"] = {"Quantity" : int(var), "Description" : "USC SYSTEM LABEL, SS CABINET WITH FANS, ABU DHABI"}
        #CXCPQ-31692
        if Specify_Identifier=="No" and Material_Type_Ingress=="316L Stainless 1.3M, IP66" and Ambient_Temperature_Range=="Without Fan, Max Ambient +40°C" and Power_Supply_Type=="48A FC-PSU-UNI2450U" and (Field_for_PUIO =="Default Marshalling FC-TUIO51/52" or Field_for_PUIO =="Universal Marshalling, PTA") and (Field_for_PDIO =="Default Marshalling FC-TDIO51/52" or Field_for_PDIO =="Universal Marshalling, PTA") and Power_Supply_Redundancy == "Redundant" and Abu_Dhabi == "Yes":
            var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
            if var>0:
                parts_dict["50159996-318"] = {"Quantity" : int(var), "Description" : "USC SYSTEM LABEL, SS CABINET, ABU DHABI"}
        #CXCPQ-31693
        if Specify_Identifier=="No" and Material_Type_Ingress=="316L Stainless 1.3M, IP66" and Ambient_Temperature_Range=="With Fan, Max Ambient +55°C" and Power_Supply_Type=="48A FC-PSU-UNI2450U" and (Field_for_PUIO =="Default Marshalling FC-TUIO51/52" or Field_for_PUIO =="Universal Marshalling, PTA") and (Field_for_PDIO =="Default Marshalling FC-TDIO51/52" or Field_for_PDIO =="Universal Marshalling, PTA") and Power_Supply_Redundancy == "Redundant" and Abu_Dhabi == "Yes":
            var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
            if var>0:
                parts_dict["50159996-319"] = {"Quantity" : int(var), "Description" : "USC SYSTEM LABEL, SS CABINET WITH FANS, ABU DHABI"}
        #CXCPQ-32665
        if Specify_Identifier=="No" and (S300=="Redundant S300" or S300=="No S300")  and Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and PUIO=="96" and PDIO=="0" and IO_Redundancy=="Redundant IO":
            Trace.Write(PUIO)
            if var>0:
                parts_dict["FC-TUIO52"] = {"Quantity" : (2*int(var)), "Description" : "SC FTA FC-PUIO01 KNIFE, EOL, 24VDC, 16CH, R"}
        if Specify_Identifier=="No" and (S300=="Redundant S300" or S300=="No S300" or S300=="Non Redundant S300") and Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and PUIO=="96" and PDIO=="0" and IO_Redundancy=="Non Redundant IO":
            if var>0:
                parts_dict["FC-TUIO52"] = {"Quantity" : (2*int(var)), "Description" : "SC FTA FC-PUIO01 KNIFE, EOL, 24VDC, 16CH, R"}
        #CXCPQ-34330 Prabhat
        if Specify_Identifier=="No" and  S300=="No S300" and Fiber_Optic=="Single Mode x2 EDS-305":
            if var>0:
                parts_dict["4600135"] = {"Quantity" : (2*int(var)), "Description" : "EDS-305-S-SC-T"}
        if Specify_Identifier=="No" and (S300=="Redundant S300") and Fiber_Optic=="Single Mode x4 EDS-305":
            if var>0:
                parts_dict["4600135"] = {"Quantity" : (4*int(var)), "Description" : "EDS-305-S-SC-T"}
        #CXCPQ-34331 Prabhat
        if Specify_Identifier=="No" and  S300=="No S300" and Fiber_Optic=="Multi Mode x2 EDS-305":
            if var>0:
                parts_dict["4600120"] = {"Quantity" : (2*int(var)), "Description" : "EDS-305-M-SC-T"}
        if Specify_Identifier=="No" and (S300=="Redundant S300") and Fiber_Optic=="Multi Mode x4 EDS-305":
            if var>0:
                parts_dict["4600120"] = {"Quantity" : (4*int(var)), "Description" : "EDS-305-M-SC-T"}
        #CXCPQ-32661,31667
        if Specify_Identifier=="No" and (PUIO=="32" or PUIO=="64" or PUIO=="96"):
            if var>0:
                parts_dict["FC-TALARM01"] = {"Quantity" : int(var), "Description" : "Alarm"}
        if Specify_Identifier=="No" and (PUIO=="32" or PUIO=="64" or PUIO=="96") and Field_for_PUIO=="Intrinsically Safe":
            if var>0:
                parts_dict["50171803-001"] = {"Quantity" : int(var), "Description" : "SCA IS Partition"}
        #CXCPQ-31670
        if Specify_Identifier=="No" and Power_Supply_Type=="20A AC/DC QUINT 4+ PS" and Power_Supply_Redundancy=="Redundant":
                if var>0:
                    parts_dict["50159474-008"] = {"Quantity" : int(var), "Description" : "Power Back Plate Assy - Quint 4+ Redundant"}
        #CXCPQ-31723
        if Specify_Identifier=="No" and Ambient_Temperature_Range=="With Fan, Max Ambient +55°C" and Field_for_PUIO=="Intrinsically Safe" and Field_for_PDIO=="Intrinsically Safe" and Power_Supply_Type=="20A AC/DC QUINT 4+ PS" and Power_Supply_Redundancy=="Redundant" and Abu_Dhabi=="Yes":
                if var>0:
                    parts_dict["50159996-329"] = {"Quantity" : int(var), "Description" : "USC SYSTEM LABEL, SS CABINET WITH FANS, IS"}
        #CXCPQ-31725
        if Specify_Identifier=="No" and Material_Type_Ingress=="316L Stainless 1.3M, IP66" and Ambient_Temperature_Range=="With Fan, Max Ambient +55°C" and Field_for_PUIO=="Intrinsically Safe" and Field_for_PDIO=="Intrinsically Safe" and Power_Supply_Type=="24 VDC/DC QUINT 4+ Supply" and Power_Supply_Redundancy=="Redundant" and Abu_Dhabi=="Yes":
                if var>0:
                    parts_dict["50159996-331"] = {"Quantity" : int(var), "Description" : "USC SYSTEM LABEL, SS CABINET WITH FANS, IS"}
        #CXCPQ-31730
		#commented CCEECOMMBR-6977
        """if Specify_Identifier=="No" and (Power_Supply_Type=="20A AC/DC QUINT 4+ PS" or Power_Supply_Type=="24A AC/DC FC-PSUNI2424" or Power_Supply_Type=="48A FC-PSU-UNI2450U"):
            if var>0:
                parts_dict["50159998-100"] = {"Quantity" : int(var), "Description" : "USC FUSE REFERENCE GUIDE, FOR AC MAINS"}"""
        if lenght_str>20:
            #CXCPQ-32149,CXCPQ-32150 and CXCPQ-32151
            var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
            if (str3=="S") and Specify_Identifier=="Yes" and var >0:
                parts_dict["FC-TCNT11"] = {"Quantity" : int(var), "Description" : "SC S300 IOTA CNTRL REDUNDANT"}
                '''if SCCNTL05 >0 and attri >=1 and attri <=96 and S300!="Non Redundant S300":
                    var1= var + SCCNTL05
                else:
                    var1=var
                parts_dict["FS-SCCNTL05"] = {"Quantity" : int(var1), "Description" : "SC S300 CNTRL LIC SMALL RED IO 1-96"}'''
            #CXCPQ-54746 - Start
            '''if str3=="N"and Specify_Identifier=="Yes" and var >0:
                parts_dict["FS-CCI-HSE-01"] = {"Quantity" : int(var), "Description" : "Ethernet cable, Yellow and Green L 1.0 M"}
            elif str3=="S"and Specify_Identifier=="Yes" and var >0:
                parts_dict["FS-CCI-HSE-01"] = {"Quantity" : int(2*var), "Description" : "Ethernet cable, Yellow and Green L 1.0 M"}'''
            #CXCPQ-54746 - End

            #CXCPQ-31731
			#commented CCEECOMMBR-6977
            """if str10=="D" and Specify_Identifier=="Yes" and lenght_str>20 :
                var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
                if var>0:
                    parts_dict["50159998-200"] = {"Quantity" : int(var), "Description" : "USC FUSE REFERENCE GUIDE, FOR DC MAINS"}"""
            #CXCPQ-31678
            if str1=="S" and str2=="A" and (str5=="M" or str5=="U") and (str6=="M" or str6=="U") and str10=="D"and str11=="R" and str16 == "X" and Specify_Identifier=="Yes" and lenght_str>20 :
                var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
                if var >0:
                    parts_dict["50159996-306"] = {"Quantity" : int(var), "Description" : "USC SYSTEM LABEL, SS CABINET"}
            #CXCPQ-31672
            if str1=="S" and str2=="A" and (str5=="M" or str5=="U") and (str6=="M" or str6=="U") and str10=="A"and str11=="R" and str16 == "X" and Specify_Identifier=="Yes" and lenght_str>20 :
                var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
                if var >0:
                    parts_dict["50159996-300"] = {"Quantity" : int(var), "Description" : "USC SYSTEM LABEL, SS CABINET"}
            #CXCPQ-31671
            if str10=="E" and str11=="R" and Specify_Identifier=="Yes" and lenght_str>20 :
                var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
                if var>0:
                    parts_dict["50159474-006"] = {"Quantity" : int(var), "Description" : "Power Back Plate Assy- Eplax Power supply"}
            #CXCPQ-31673
            if str1=="S" and str2=="B" and (str5=="M" or str5=="U") and (str6=="M" or str6=="U") and str10=="A"and str11=="R" and str16 == "X" and Specify_Identifier=="Yes" and lenght_str>20 :
                var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
                if var>0:
                    parts_dict["50159996-301"] = {"Quantity" : int(var), "Description" : "USC SYSTEM LABEL, SS CABINET WITH FANS"}
            #CXCPQ-31707
            if str1=="S" and str2=="B" and (str5=="M" or str5=="U") and (str6=="M" or str6=="U") and str10=="D"and str11=="R" and str16 == "Y" and Specify_Identifier=="Yes" and lenght_str>20 :
                var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
                if var>0:
                    parts_dict["50159996-323"] = {"Quantity" : int(var), "Description" : "USC SYSTEM LABEL, SS CABINET WITH FANS, ABU DHABI"}
            #CXCPQ-31708
            if str1=="S" and str2=="B" and str5=="I" and str6=="I" and str10=="A"and str11=="R" and str16 == "Y" and Specify_Identifier=="Yes" and lenght_str>20 :
                var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
                if var>0:
                    parts_dict["50159996-325"] = {"Quantity" : int(var), "Description" : "USC SYSTEM LABEL, SS CABINET WITH FANS, IS"}
            #CXCPQ-31711
            if str1=="S" and str2=="B" and str5=="I" and str6=="I" and str10=="E"and str11=="R" and str16 == "Y" and Specify_Identifier=="Yes" and lenght_str>20 :
                var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
                if var>0:
                    parts_dict["50159996-327"] = {"Quantity" : int(var), "Description" : "USC SYSTEM LABEL, SS CABINET WITH FANS, IS"}
            if (str1 =="S" and Specify_Identifier=="Yes" and lenght_str>20):
                var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
                if var>0:
                     parts_dict["50154983-001"] = {"Quantity" : int(var), "Description" : "1.3M, 316L Stainless IP66 Cabinet "}
            #CXCPQ-31677
            if str1=="S" and str2=="B" and (str5=="M" or str5=="U") and (str6=="M" or str6=="U") and str10=="Q"and str11=="R" and str16 == "X" and Specify_Identifier=="Yes" and lenght_str>20 :
                var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
                if var>0:
                    parts_dict["50159996-305"] = {"Quantity" : int(var), "Description" : "USC SYSTEM LABEL, SS CABINET WITH FANS"}
            if (str2 =="B" and Specify_Identifier=="Yes" and lenght_str>20):
                var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
                if var>0:
                     parts_dict["51454248-100"] = {"Quantity" : int(var), "Description" : "Fan Assembly "}
            #CXCPQ-31668
            if str10=="A" and str11=="R" and Specify_Identifier=="Yes":
                var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
                if var>0:
                    parts_dict["50159474-002"] = {"Quantity" : int(var), "Description" : "Power Back Plate Assy - ATDI 600W Redundant"}
            #CXCPQ-31699
            if str10=="D" and str11=="R" and Specify_Identifier=="Yes":
                var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
                if var>0:
                    parts_dict["50159474-004"] = {"Quantity" : int(var), "Description" : "Power Back Plate Assy - DC Quint 4+ Redundant"}
            #CXCPQ-31682
            if str1=="S" and str2=="B" and (str5=="M" or str5=="U") and (str6=="M" or str6=="U") and str10=="D"and str11=="R" and str16 == "X" and Specify_Identifier=="Yes" and lenght_str>20 :
                var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
                if var >0:
                    parts_dict["50159996-307"] = {"Quantity" : int(var), "Description" : "USC SYSTEM LABEL, SS CABINET WITH FANS"}
            #CXCPQ-31683
            if str1=="S" and str2=="B" and str5=="I" and str6=="I" and str10=="A"and str11=="R" and str16 == "X" and Specify_Identifier=="Yes" and lenght_str>20 :
                var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
                if var>0:
                    parts_dict["50159996-309"] = {"Quantity" : int(var), "Description" : "USC SYSTEM LABEL, SS CABINET WITH FANS,"}
            #CXCPQ-31685
            if str1=="S" and str2=="B" and str5=="I" and str6=="I" and str10=="E"and str11=="R" and str16 == "X" and Specify_Identifier=="Yes" and lenght_str>20 :
                var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
                if var>0:
                    parts_dict["50159996-311"] = {"Quantity" : int(var), "Description" : "USC SYSTEM LABEL, SS CABINET WITH FANS,"}
            #CXCPQ-31691
            if str1=="S" and str2=="B" and (str5=="M" or str5=="U") and (str6=="M" or str6=="U") and str10=="A"and str11=="R" and str16 == "Y" and Specify_Identifier=="Yes" and lenght_str>20 :
                var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
                if var >0:
                    parts_dict["50159996-317"] = {"Quantity" : int(var), "Description" : "USC SYSTEM LABEL, SS CABINET WITH FANS, ABU DHABI"}
            #CXCPQ-31692
            if str1=="S" and str2=="A" and (str5=="M" or str5=="U") and (str6=="M" or str6=="U") and str10=="E"and str11=="R" and str16 == "Y" and Specify_Identifier=="Yes" and lenght_str>20 :
                var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
                if var >0:
                    parts_dict["50159996-318"] = {"Quantity" : int(var), "Description" : "USC SYSTEM LABEL, SS CABINET, ABU DHABI"}
            #CXCPQ-31693
            if str1=="S" and str2=="B" and (str5=="M" or str5=="U") and (str6=="M" or str6=="U") and str10=="E"and str11=="R" and str16 == "Y" and Specify_Identifier=="Yes" and lenght_str>20 :
                var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
                if var >0:
                    parts_dict["50159996-319"] = {"Quantity" : int(var), "Description" : "USC SYSTEM LABEL, SS CABINET WITH FANS, ABU DHABI"}
            #CXCPQ-32665
            if (str3=="S" or str3=="X") and str5=="M" and str8=="C" and str9=="X" and str13=="R":
                var= 2 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
                if var >0:
                    parts_dict["FC-TUIO52"] = {"Quantity" : int(var), "Description" : "SC FTA FC-PUIO01 KNIFE, EOL, 24VDC, 16CH, R"}
            if (str3=="S" or str3=="X" or str3=="N") and str5=="M" and str8=="C" and str9=="X" and str13=="X":
                var= 2 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
                if var >0:
                    parts_dict["FC-TUIO52"] = {"Quantity" : int(var), "Description" : "SC FTA FC-PUIO01 KNIFE, EOL, 24VDC, 16CH, R"}
            #CXCPQ-34330 Prabhat
            if (str3=="X") and str4=="V":
                var= 2 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
                if var >0:
                    parts_dict["4600135"] = {"Quantity" : int(var), "Description" : "EDS-305-S-SC-T"}
            if (str3=="S") and str4 == "T":
                var= 4 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
                if var >0:
                    parts_dict["4600135"] = {"Quantity" : int(var), "Description" : "EDS-305-S-SC-T"}
            #CXCPQ-34331 Prabhat
            if (str3=="X") and str4=="Y":
                var= 2 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
                if var >0:
                    parts_dict["4600120"] = {"Quantity" : int(var), "Description" : "EDS-305-S-SC-T"}
            if (str3=="S") and str4 == "N":
                var= 4 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
                if var >0:
                    parts_dict["4600120"] = {"Quantity" : int(var), "Description" : "EDS-305-S-SC-T"}
            #CXCPQ-32661
            if (str8=="A" or str8=="B" or str8=="C") :
                var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
                if var >0:
                    parts_dict["FC-TALARM01"] = {"Quantity" : int(var), "Description" : "Alarm"}
            #CXCPQ-31667
            if (str8=="A" or str8=="B" or str8=="C") and str5=="I" :
                var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
                if var >0:
                    parts_dict["50171803-001"] = {"Quantity" : int(var), "Description" : "SCA IS Partition"}
            #CXCPQ-31670
            if str10=="Q" and str11=="R" and  Specify_Identifier=="Yes" and lenght_str>20 :
                    var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
                    if var>0:
                        parts_dict["50159474-008"] = {"Quantity" : int(var), "Description" : "Power Back Plate Assy - Quint 4+ Redundant"}
            #CXCPQ-31723
            if str1=="S" and str2=="B" and str5=="I" and str6=="I" and str10=="Q"  and str11=="R" and str16=="Y" and  Specify_Identifier=="Yes" and lenght_str>20 :
                    var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
                    if var>0:
                        parts_dict["50159996-329"] = {"Quantity" : int(var), "Description" : "USC SYSTEM LABEL, SS CABINET WITH FANS, IS"}
            #CXCPQ-31725
            if str1=="S" and str2=="B" and str5=="I" and str6=="I" and str10=="D"  and str11=="R" and str16=="Y" and  Specify_Identifier=="Yes" and lenght_str>20 :
                    var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
                    if var>0:
                        parts_dict["50159996-331"] = {"Quantity" : int(var), "Description" : "USC SYSTEM LABEL, SS CABINET WITH FANS, IS"}
            #CXCPQ-31730
			#commented CCEECOMMBR-6977
            """if (str10=="Q" or str10=="A" or str10=="E") and Specify_Identifier=="Yes" and lenght_str>20 :
                var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
                if var>0:
                    parts_dict["50159998-100"] = {"Quantity" : int(var), "Description" : "USC FUSE REFERENCE GUIDE, FOR AC MAINS"}"""

        #CXCPQ-54746 - Start
        var= 1 * int(Safety_Cabinets_qnt) if Safety_Cabinets_qnt != "" else 0
        if Specify_Identifier=="No" and var >0:
            if S300 == "Redundant S300" and (CNM == "0" or CNM == "4"):
                parts_dict["FS-CCI-HSE-01"] = {"Quantity" : int(2*var), "Description" : "Ethernet cable, Yellow and Green L 1.0 M"}

        if Specify_Identifier=="Yes" and var >0 and lenght_str>20:
            if str3 == "S"and (str17 == "0" or str17 == "4"):
                parts_dict["FS-CCI-HSE-01"] = {"Quantity" : int(2*var), "Description" : "Ethernet cable, Yellow and Green L 1.0 M"}

        #CXCPQ-54746 - End
    return parts_dict
#part=identifier_Modifier(Product,parts_dict)
#Trace.Write(str(part))