#parts_dict={}
def getPartQuantity(parts_dict,part):
    try:
        return int(parts_dict[part]['Quantity'])
    except KeyError:
        return 0

def SM_RG_Licenses_Calcs(Product,parts_dict):
    sumrem=Product.Attr('Sum_Reminder').GetValue()
    if sumrem=="":
        sumrem=64

    SM_Red_select=Product.Attr('SM_Red_select').GetValue()
    if SM_Red_select=="":
        SM_Red_select="Redundant S300"
    if Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").DisplayValue=="No":
        Redselect=Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("S300").DisplayValue
    elif Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").DisplayValue=="Yes":
        code=Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").Value
        code=str(code)
        if code[3]=="S":
            Redselect="Redundant S300"
        if code[3]=="N":
            Redselect="Non Redundant S300"
    if SM_Red_select != Redselect :
        sumrem=0
    Product.Attr('SM_Red_select').AssignValue(str(Redselect))

    sumrem=int(sumrem)
    if Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").DisplayValue=="No":
        puio=int(Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("PUIO_Count").DisplayValue)
        pdio=int(Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("PDIO_Count").DisplayValue)
        sumup= puio+pdio
        if sumup>96:
            sumup=96
    elif Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").DisplayValue=="Yes":
        code=Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").Value
        code=str(code)
        Trace.Write(code)
        if len(code)>10:
            puio=code[8]
            pdio=code[9]
            if puio=='X':
                puiox=0
            elif puio=='A':
                puiox=32
            elif puio=='B':
                puiox=64
            elif puio=='C':
                puiox=96
            if pdio=='X':
                pdiox=0
            elif pdio=='A':
                pdiox=32
            elif pdio=='B':
                pdiox=64
            elif pdio=='C':
                pdiox=96
            else:
                puiox=0
                pdiox=0
            sumup= int(puiox)+int(pdiox)
            Trace.Write("Sumup"+str(sumup))
            if sumup>96:
                sumup=96
    addon=sumup-sumrem
    Product.Attr('Sum_Reminder').AssignValue(str(sumup))
    code='xxxxxxxxxxxxxxxxx'    
    if Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").DisplayValue=="Yes":
        code = str(Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").Value)
    attri=0
    FC_SCNTL_2 = getPartQuantity(parts_dict,'FC-TCNT11')
    #attri=Product.Attr('SM_RG_lic_SUM').GetValue()
    #attri=int(attri)
    Trace.Write(attri)
    val=Product.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue
    if Redselect=="Redundant S300":
        attri=int(Product.Attr('SM_RG_lic_SUM').GetValue())
    elif Redselect=="Non Redundant S300":
        attri=int(Product.Attr('SM_RG_lic_SUMNR').GetValue())
    attriR=int(Product.Attr('SM_RG_lic_SUM').GetValue())
    attriNR=int(Product.Attr('SM_RG_lic_SUMNR').GetValue())
    '''if attri==0:
        attri=1'''
    if val=="Universal Safety Cab-1.3M":
        puio=int(Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("PUIO_Count").DisplayValue)
        pdio=int(Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("PDIO_Count").DisplayValue)
        if Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").DisplayValue=="No" and puio + pdio > 0 :
            if Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("S300").DisplayValue=="Redundant S300":
                if attri+addon > 256:
                    parts_dict["FS-SCCNTL01"] = {'Quantity' : FC_SCNTL_2   , 'Description': 'SC S300 CONTROLLER LICENSE'}
                elif attri+addon >=97 and attri+addon <=256:
                    parts_dict["FS-SCCNTL03"] = {'Quantity' : FC_SCNTL_2  , 'Description': 'SC S300 RED CNTR LIC MEDIUM IO 97-256'}
                elif attri+addon >=1 and attri+addon <=96:
                    parts_dict["FS-SCCNTL05"] = {'Quantity' : FC_SCNTL_2  , 'Description': 'SC S300 RED CNTR LIC SMALL IO 1-96'}
                Product.Attr('SM_RG_lic_SUM').AssignValue(str(attri+addon))
                if sumrem==0:
                    Product.Attr('SM_RG_lic_SUMNR').AssignValue(str(attriNR-sumup))
            elif Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("S300").DisplayValue=="Non Redundant S300":
                if attri+addon > 256:
                    parts_dict["FS-SCCNTL02"] = {'Quantity' : FC_SCNTL_2   , 'Description': 'SC S300 NONRED CNTR LIC LARGE IO>256'}
                elif attri+addon >=97 and attri+addon <=256:
                    parts_dict["FS-SCCNTL04"] = {'Quantity' : FC_SCNTL_2  , 'Description': 'SC S300 NONRED CNTR LIC MEDIUM IO 97-256'}
                elif attri+addon >=1 and attri+addon <=96:
                    parts_dict["FS-SCCNTL06"] = {'Quantity' : FC_SCNTL_2  , 'Description': 'SC S300 NONRED CNTR LIC SMALL IO 1-96'}
                Product.Attr('SM_RG_lic_SUMNR').AssignValue(str(attri+addon))
                if sumrem==0:
                    Product.Attr('SM_RG_lic_SUM').AssignValue(str(attriR-sumup))
        elif Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").DisplayValue=="Yes":
            code = str(Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").Value)
            if not (code[8]=='X' and code[9]=='X'):
                if code[3]=="S":
                    if attri+addon > 256:
                        parts_dict["FS-SCCNTL01"] = {'Quantity' : FC_SCNTL_2   , 'Description': 'SC S300 CONTROLLER LICENSE'}
                    elif attri+addon >=97 and attri+addon <=256:
                        parts_dict["FS-SCCNTL03"] = {'Quantity' : FC_SCNTL_2  , 'Description': 'SC S300 RED CNTR LIC MEDIUM IO 97-256'}
                    elif attri+addon >=1 and attri+addon <=96:
                        parts_dict["FS-SCCNTL05"] = {'Quantity' : FC_SCNTL_2  , 'Description': 'SC S300 RED CNTR LIC SMALL IO 1-96'}
                    Product.Attr('SM_RG_lic_SUM').AssignValue(str(attri+addon))
                    if sumrem==0:
                        Product.Attr('SM_RG_lic_SUMNR').AssignValue(str(attriNR-sumup))
                elif code[3]=="N":
                    if attri+addon > 256:
                        parts_dict["FS-SCCNTL02"] = {'Quantity' : FC_SCNTL_2   , 'Description': 'SC S300 NONRED CNTR LIC LARGE IO>256'}
                    elif attri+addon >=97 and attri+addon <=256:
                        parts_dict["FS-SCCNTL04"] = {'Quantity' : FC_SCNTL_2  , 'Description': 'SC S300 NONRED CNTR LIC MEDIUM IO 97-256'}
                    elif attri+addon >=1 and attri+addon <=96:
                        parts_dict["FS-SCCNTL06"] = {'Quantity' : FC_SCNTL_2  , 'Description': 'SC S300 NONRED CNTR LIC SMALL IO 1-96'}
                    Product.Attr('SM_RG_lic_SUMNR').AssignValue(str(attri+addon))
                    if sumrem==0:
                        Product.Attr('SM_RG_lic_SUM').AssignValue(str(attriR-sumup))

    return parts_dict
#x=SM_RG_Licenses_Calcs(Product,parts_dict)
#Trace.Write(str(x))
#Trace.Write(attri)