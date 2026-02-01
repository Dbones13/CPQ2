#parts_dict={}
def getPartQuantity(parts_dict,part):
    try:
        return int(parts_dict[part]['Quantity'])
    except KeyError:
        return 0


def SM_Licenses_Calcs(Product,parts_dict,TCSNT11):
    FC_SCNTL_2 = TCSNT11
    total = 0
    totalrg = 0
    totalrgp = 0
    sumup = 0
    totalsum = 0
    totalsumnred= 0
    totalsumall= 0
    totalnons= 0
    code='xxxxxxxxxxxxxxxxx'
    containers = ['SM_IO_Count_Analog_Input_Cont', 'SM_IO_Count_Analog_Output_Cont', 'SM_IO_Count_Digital_Input_Cont', 'SM_IO_Count_Digital_Output_Cont','SM_CG_DI_RLY_NMR_Cont','SM_CG_DO_RLY_NMR_Cont']

    for container in containers:
        cont = Product.GetContainerByName(container)
        for row in cont.Rows:
            for col in row.Columns:
                #Trace.Write(col.Name)
                if col.Name not in ['Digital Input Type','Digital Output Type','Analog Input Type','Analog Output Type', 'Rank'] and col.Value.strip() !='':
                    total  += float(col.Value)
    Trace.Write("total:{}".format(int(total)))


    #RG
    for row in Product.GetContainerByName("SM_RemoteGroup_Cont").Rows:
        Redselect=""
        y=row.Product
        val=y.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue
        if val=="Cabinet":
            containers = ['SM_RG_IO_Count_Digital_Input_Cont', 'SM_RG_IO_Count_Digital_Output_Cont', 'SM_RG_IO_Count_Analog_Input_Cont', 'SM_RG_IO_Count_Analog_Output_Cont','SM_RG_DI_RLY_NMR_Cont','SM_RG_DO_RLY_NMR_Cont']

            for container in containers:
                cont = y.GetContainerByName(container)
                for row in cont.Rows:
                    for col in row.Columns:
                        #Trace.Write(col.Name)
                        if col.Name not in ['Digital_Input_Type','Digital_Output_Type','Analog_Input_Type','Analog_Output_Type','Digital Input Type','Digital Output Type', 'Rank','Total_DI_Points','Total_DO_Points','Total_AI_Points','Total_AO_Point'] and col.Value.strip() !='':
                            totalrg  += float(col.Value)
            Trace.Write("totalrg--:{}".format(int(totalrg)))
        elif val=="Universal Safety Cab-1.3M":
            if 1:
                if y.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").DisplayValue=="No":
                    puio=int(y.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("PUIO_Count").DisplayValue)
                    pdio=int(y.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("PDIO_Count").DisplayValue)
                    sumup= puio+pdio
                    if sumup>96:
                        sumup=96
                elif y.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").DisplayValue=="Yes":
                    code=y.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").Value
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
            if y.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").DisplayValue=="No":
                Redselect=y.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("S300").DisplayValue
            elif y.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").DisplayValue=="Yes":
                code=y.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").Value
                code=str(code)
                if code[3]=="S":
                    Redselect="Redundant S300"
                #CXCPQ-54877 - Start
                '''if code[3]=="N":
                    Redselect="Non Redundant S300"'''
                #CXCPQ-54877 - End
                if code[3]=="X":
                    Redselect="Non S300"

        if val=="Cabinet":
            totalrgp=totalrg+totalrgp
        if Redselect=="Redundant S300":
            totalsum=totalsum+sumup
        elif Redselect=="Non Redundant S300":
            totalsumnred=totalsumnred+sumup
        elif Redselect=="No S300":
            Trace.Write("t"+str(totalrg))
            totalnons=totalnons+sumup
        Trace.Write("totalrgp "+ str(totalrgp))
        Trace.Write(totalsum)
    
    for row in Product.GetContainerByName("SM_RemoteGroup_Cont").Rows:
        y=row.Product
        y.Attr('SM_RG_lic_SUM').AssignValue(str(totalsum))
        y.Attr('SM_RG_lic_SUMNR').AssignValue(str(totalsumnred))


    totalsumall=total+totalrgp
    Trace.Write("total================================>"+ str(totalsumall))
    if Product.GetContainerByName("SM_RemoteGroup_Cont").Rows.Count ==0 or totalrgp > 0:
        if totalsumall > 256:
            parts_dict["FS-SCCNTL01"] = {'Quantity' : FC_SCNTL_2   , 'Description': 'SC S300 CONTROLLER LICENSE'}
        elif totalsumall >=97 and totalsumall <=256:
            parts_dict["FS-SCCNTL03"] = {'Quantity' : FC_SCNTL_2  , 'Description': 'SC S300 RED CNTR LIC MEDIUM IO 97-256'}
        elif totalsumall >=1 and totalsumall <=96:
            parts_dict["FS-SCCNTL05"] = {'Quantity' : FC_SCNTL_2  , 'Description': 'SC S300 RED CNTR LIC SMALL IO 1-96'}
    
    Trace.Write(code[4])
    #totalsumall=total+totalnons
    Trace.Write(totalsumall+totalnons)
    for row in Product.GetContainerByName("SM_RemoteGroup_Cont").Rows:
        y=row.Product
        val2=y.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue
        if val2=="Universal Safety Cab-1.3M":
            if y.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").DisplayValue=="No":
                if y.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("S300").DisplayValue=="No S300" :
                    if total+totalnons > 256:
                        parts_dict["FS-SCCNTL01"] = {'Quantity' : FC_SCNTL_2   , 'Description': 'SC S300 CONTROLLER LICENSE'}
                    elif total+totalnons >=97 and total+totalnons <=256:
                        Trace.Write("True136")
                        parts_dict["FS-SCCNTL03"] = {'Quantity' : FC_SCNTL_2  , 'Description': 'SC S300 RED CNTR LIC MEDIUM IO 97-256'}
                    elif total+totalnons >=1 and total+totalnons <=96:
                        Trace.Write("True138")
                        parts_dict["FS-SCCNTL05"] = {'Quantity' : FC_SCNTL_2  , 'Description': 'SC S300 RED CNTR LIC SMALL IO 1-96'}
            elif y.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").DisplayValue=="Yes":
                code = str(y.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").Value)
                if code[3]=="X":
                    if total+totalnons > 256:
                        parts_dict["FS-SCCNTL01"] = {'Quantity' : FC_SCNTL_2   , 'Description': 'SC S300 CONTROLLER LICENSE'}
                    elif total+totalnons >=97 and total+totalnons <=256:
                        parts_dict["FS-SCCNTL03"] = {'Quantity' : FC_SCNTL_2  , 'Description': 'SC S300 RED CNTR LIC MEDIUM IO 97-256'}
                    elif total+totalnons >=1 and total+totalnons <=96:
                        parts_dict["FS-SCCNTL05"] = {'Quantity' : FC_SCNTL_2  , 'Description': 'SC S300 RED CNTR LIC SMALL IO 1-96'}
                    
                
                    
    for row in Product.GetContainerByName("SM_RemoteGroup_Cont").Rows:
        y=row.Product
        val2=y.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue
        if val2=="Universal Safety Cab-1.3M":
            if y.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").DisplayValue=="No":
                if y.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("S300").DisplayValue=="Redundant S300" :
                    if total > 256:
                        parts_dict["FS-SCCNTL01"] = {'Quantity' : FC_SCNTL_2   , 'Description': 'SC S300 CONTROLLER LICENSE'}
                    elif total >=97 and total <=256:
                        parts_dict["FS-SCCNTL03"] = {'Quantity' : FC_SCNTL_2  , 'Description': 'SC S300 RED CNTR LIC MEDIUM IO 97-256'}
                    elif total >=1 and total <=96:
                        parts_dict["FS-SCCNTL05"] = {'Quantity' : FC_SCNTL_2  , 'Description': 'SC S300 RED CNTR LIC SMALL IO 1-96'}
            elif y.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").DisplayValue=="Yes":
                code = str(y.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").Value)
                if code[3]=="S":
                    if total > 256:
                        parts_dict["FS-SCCNTL01"] = {'Quantity' : FC_SCNTL_2   , 'Description': 'SC S300 CONTROLLER LICENSE'}
                    elif total >=97 and total <=256:
                        parts_dict["FS-SCCNTL03"] = {'Quantity' : FC_SCNTL_2  , 'Description': 'SC S300 RED CNTR LIC MEDIUM IO 97-256'}
                    elif total >=1 and total <=96:
                        parts_dict["FS-SCCNTL05"] = {'Quantity' : FC_SCNTL_2  , 'Description': 'SC S300 RED CNTR LIC SMALL IO 1-96'}
                    
    
    for row in Product.GetContainerByName("SM_RemoteGroup_Cont").Rows:
        y2=row.Product
        val2=y2.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue
        if val2=="Universal Safety Cab-1.3M":
            if y2.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").DisplayValue=="No":
                if y2.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("S300").DisplayValue=="Non Redundant S300" :
                    if total > 256:
                        parts_dict["FS-SCCNTL02"] = {'Quantity' : FC_SCNTL_2   , 'Description': 'SC S300 NONRED CNTR LIC LARGE IO>256'}
                    elif total >=97 and total <=256:
                        parts_dict["FS-SCCNTL04"] = {'Quantity' : FC_SCNTL_2  , 'Description': 'SC S300 NONRED CNTR LIC MEDIUM IO 97-256'}
                    elif total >=1 and total <=96:
                        parts_dict["FS-SCCNTL06"] = {'Quantity' : FC_SCNTL_2  , 'Description': 'SC S300 NONRED CNTR LIC SMALL IO 1-96'}
            elif y2.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").DisplayValue=="Yes":
                code = str(y2.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").Value)
                if code[3]=="N":
                    if total > 256:
                        parts_dict["FS-SCCNTL02"] = {'Quantity' : FC_SCNTL_2   , 'Description': 'SC S300 NONRED CNTR LIC LARGE IO>256'}
                    elif total >=97 and total <=256:
                        parts_dict["FS-SCCNTL04"] = {'Quantity' : FC_SCNTL_2  , 'Description': 'SC S300 NONRED CNTR LIC MEDIUM IO 97-256'}
                    elif total >=1 and total <=96:
                        parts_dict["FS-SCCNTL06"] = {'Quantity' : FC_SCNTL_2  , 'Description': 'SC S300 NONRED CNTR LIC SMALL IO 1-96'}
                    
    return parts_dict
#ss=SM_Licenses_Calcs(Product,parts_dict,4)
#Trace.Write(str(ss))