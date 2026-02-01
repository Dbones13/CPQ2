def getContainer(Name):
    return Product.GetContainerByName(Name)
selectedProducts = list()
for row in getContainer("MSID_Product_Container").Rows:
    selectedProducts.append(row["Product Name"])
if "xPM to C300 Migration" in selectedProducts:
    xpm_cont1 = getContainer("xPM_C300_Series_ C_Cabinet_Configuration")
    xpm_cont2 = getContainer("xPM_C300_Series_C_Cabinet_Configuration_FAOnly")
    for row1 in xpm_cont1.Rows:
        #attr1 = row1.GetColumnByName("xPM_C300_Power_System_Vendor").ReferencingAttribute
        attr2 = row1.GetColumnByName("xPM_C300_Power_System_Type").ReferencingAttribute
        if row1["xPM_C300_Power_System_Vendor"] == 'Meanwell' or row1["xPM_C300_Power_System_Vendor"] == 'Phoenix Contact':
            for value in attr2.Values:
                #Trace.Write("Hello:{0},{1}".format(value.Display,row1["xPM_C300_Power_System_Vendor"]))
                if value.Display in ('Redundant with BBU 20A','Redundant 40A','Non Redundant 40A'):
                    value.Allowed = False
                if value.Display in ('Redundant 20A','Non Redundant 20A'):
                    value.Allowed = True
            row1.ApplyProductChanges()
            break
        if row1["xPM_C300_Power_System_Vendor"] == 'TDI':
            for value in attr2.Values:
                #Trace.Write("Hello:{0}".format(value.Display))
                if value.Display in ('Redundant with BBU 20A','Redundant 40A','Non Redundant 40A','Redundant 20A','Non Redundant 20A'):
                    value.Allowed = True
            row1.ApplyProductChanges()
            break
    for row2 in xpm_cont2.Rows:
        attr2 = row2.GetColumnByName("xPM_C300_Power_System_Type").ReferencingAttribute
        if row2["xPM_C300_Power_System_Vendor"] == 'Meanwell' or row1["xPM_C300_Power_System_Vendor"] == 'Phoenix Contact':
            for value in attr2.Values:
                #Trace.Write("Hello:{0}".format(value.Display))
                if value.Display in ('Redundant with BBU 20A','Redundant 40A','Non Redundant 40A'):
                    value.Allowed = False
                if value.Display in ('Redundant 20A','Non Redundant 20A'):
                    value.Allowed = True
            row2.ApplyProductChanges()
            break
        if row2["xPM_C300_Power_System_Vendor"] == 'TDI':
            for value in attr2.Values:
                #Trace.Write("Hello:{0}".format(value.Display))
                if value.Display in ('Redundant with BBU 20A','Redundant 40A','Non Redundant 40A','Redundant 20A','Non Redundant 20A'):
                    value.Allowed = True
            row2.ApplyProductChanges()
            break
if "C200 Migration" in selectedProducts:
    c200_cont1 = getContainer("C200_C300_Series_C_Cabinet_Config_Cont")
    c200_cont2 = getContainer("C200_C300_Series_C_Cabinet_Config_Cont_FAOnly")
    for row1 in c200_cont1.Rows:
        #attr1 = row1.GetColumnByName("xPM_C300_Power_System_Vendor").ReferencingAttribute
        attr2 = row1.GetColumnByName("C200_C300_Power_System_Type").ReferencingAttribute
        if row1["C200_C300_Power_System_Vendor"] == 'Meanwell' or row1["C200_C300_Power_System_Vendor"] == 'Phoenix Contact':
            for value in attr2.Values:
                #Trace.Write("Hello:{0},{1}".format(value.Display,row1["C200_C300_Power_System_Vendor"]))
                if value.Display in ('Redundant with BBU 20A','Redundant 40A','Non Redundant 40A'):
                    value.Allowed = False
                if value.Display in ('Redundant 20A','Non Redundant 20A'):
                    value.Allowed = True
            row1.ApplyProductChanges()
            break
        if row1["C200_C300_Power_System_Vendor"] == 'TDI':
            for value in attr2.Values:
                #Trace.Write("Hello:{0}".format(value.Display))
                if value.Display in ('Redundant with BBU 20A','Redundant 40A','Non Redundant 40A','Redundant 20A','Non Redundant 20A'):
                    value.Allowed = True
            row1.ApplyProductChanges()
            break
    for row2 in c200_cont2.Rows:
        attr2 = row2.GetColumnByName("C200_C300_Power_System_Type").ReferencingAttribute
        if row2["C200_C300_Power_System_Vendor"] == 'Meanwell' or row1["C200_C300_Power_System_Vendor"] == 'Phoenix Contact':
            for value in attr2.Values:
                #Trace.Write("Hello:{0}".format(value.Display))
                if value.Display in ('Redundant with BBU 20A','Redundant 40A','Non Redundant 40A'):
                    value.Allowed = False
                if value.Display in ('Redundant 20A','Non Redundant 20A'):
                    value.Allowed = True
            row2.ApplyProductChanges()
            break
        if row2["C200_C300_Power_System_Vendor"] == 'TDI':
            for value in attr2.Values:
                #Trace.Write("Hello:{0}".format(value.Display))
                if value.Display in ('Redundant with BBU 20A','Redundant 40A','Non Redundant 40A','Redundant 20A','Non Redundant 20A'):
                    value.Allowed = True
            row2.ApplyProductChanges()
            break

if "OPM" in selectedProducts:
    con1 = getContainer('MSID_CommonQuestions')
    for row in con1.Rows:
        fut_rel = row["MSID_Future_Experion_Release"]
        break

    con2 = getContainer('OPM_Basic_Information')
    for row in con2.Rows:
        lcn = row["OPM_Is_the_Experion_System_LCN_Connected"]
        sshw = row["OPM_Servers_and_Stations_HW_replace_needed"]
        ress = row["OPM_RESS_Migration_in_scope"]
        break
    platform_con = getContainer('OPM_Migration_platforms')
    if lcn == 'Yes' or sshw == 'Yes' or ress == 'Yes' :
        
        for row in platform_con.Rows:
                attr1 = row.GetColumnByName("OPM_ACET_EAPP_Server_Hardware_Selection").ReferencingAttribute
                attr2 = row.GetColumnByName("OPM_Other_Servers_Hardware_Selection").ReferencingAttribute
                attr3 = row.GetColumnByName("OPM_Experion_Server_Hardware_Selection").ReferencingAttribute
                attr4 = row.GetColumnByName("OPM_Select_RESS_platform_configuration").ReferencingAttribute
                if fut_rel in ('R520','R530','R511','R510'):
                    for value in attr1.Values:
                        if fut_rel in ('R510','R511') and value.Display in('HP DL 320 G11'):
                            value.Allowed=False
                    for value in attr2.Values:
                        if fut_rel in ('R510','R511') and value.Display in('HP DL 320 G11'):
                            value.Allowed=False
                    for value in attr3.Values:
                        if fut_rel in ('R510','R511') and value.Display in('HP DL 320 G11'):
                            value.Allowed=False
                    for value in attr4.Values:
                        if fut_rel in ('R510','R511') and value.Display in('HP DL 320 G11'):
                            value.Allowed=False
                attr5 = row.GetColumnByName("OPM_EST_Tower_Hardware_Selection").ReferencingAttribute
                attr6 = row.GetColumnByName("OPM_ESC_ESF_or_ESCE_Tower_Hardware_Selection").ReferencingAttribute
                flag=True if lcn=="Yes" and sshw=="Yes" else False
                if fut_rel not in ('R520','R530'):
                    for value in attr5.Values:
                        if value.Display in ('HP Z4 G5','Dell T5860XL'):
                            value.Allowed = False
                        else:
                            if value.Display=="HP Z4 G4 MLK" and flag:
                                value.Allowed=False
                            else:
                                value.Allowed = True
                    for value in attr6.Values:
                        if value.Display in ('HP Z4 G5','Dell T5860XL'):
                            value.Allowed = False
                        else:
                            if value.Display=="HP Z4 G4 MLK" and flag:
                                value.Allowed=False
                            else:
                                value.Allowed = True
                elif fut_rel == 'R530':
                    for value in attr5.Values:
                        if value.Display in ('HP Z4 G5','Dell T5860XL'):
                            value.Allowed = True
                        else:
                            value.Allowed = False
                    for value in attr6.Values:
                        if value.Display in ('HP Z4 G5','Dell T5860XL'):
                            value.Allowed = True
                        else:
                            value.Allowed = False
                else:
                    for value in attr5.Values:
                        if value.Display in ('HP Z4 G4 MLK','Dell T5820XL'):
                            value.Allowed = True
                        else:
                            value.Allowed = False
                    for value in attr6.Values:
                        if value.Display in ('HP Z4 G4 MLK','Dell T5820XL'):
                            value.Allowed = True
                        else:
                            value.Allowed = False
                row.ApplyProductChanges()
                break
        if fut_rel in ('R520','R530','R511','R510'):
            for row in platform_con.Rows:
                attr1 = row.GetColumnByName("OPM_ACET_EAPP_Server_Hardware_Selection").ReferencingAttribute
                attr3 = row.GetColumnByName("OPM_Experion_Server_Hardware_Selection").ReferencingAttribute
                for value in attr1.Values:
                    if value.Display in ('Dell R740XL'):
                        value.Allowed = False
                for value in attr3.Values:
                    if value.Display in ('Dell R740XL'):
                        value.Allowed = False
                row.ApplyProductChanges()
                break
    if ress == 'Yes' and fut_rel in ('R520','R530','R511','R510'):
        for row in platform_con.Rows:
            attr4 = row.GetColumnByName("OPM_Select_RESS_platform_configuration").ReferencingAttribute
            for value in attr4.Values:
                if value.Display in ('Dell R740XL'):
                    value.Allowed = False
            row.ApplyProductChanges()
            break
if "TPS to Experion" in selectedProducts:
    con1 = getContainer('MSID_CommonQuestions')
    for row in con1.Rows:
        fut_rel = row["MSID_Future_Experion_Release"]
        break
    genQueCon = getContainer('TPS_EX_General_Questions')
    for row in genQueCon.Rows:
        addServer = row['Additional_Server_ESV_Stations_ESF_ESC_ESF_Required']
        break
    estCon = getContainer('TPS_EX_Station_Conversion_EST')
    esvtCon = getContainer('TPS_EX_Conversion_ESVT_Server')
    acetCon = getContainer('TPS_EX_Conversion_ACET_EAPP')
    bundleCon = getContainer('TPS_EX_Bundle_Conversion_Server_Stations')
    addSerCon = getContainer('TPS_EX_Additional_Servers')
    addStn = getContainer('TPS_EX_Additional_Stations')
    for row in estCon.Rows:
        #Trace.Write(row['TPS_EX_Future_Mounting_Furniture'])
        con_type = row['TPS_EX_Station_Conversion_Type']
        #Trace.Write(str(con_type))
        attr1 = row.GetColumnByName("TPS_EX_Hardware").ReferencingAttribute
        if fut_rel not in('R520','R530'):
            for value in attr1.Values:
                #Trace.Write(value.Display)
                if value.Display in ('HP Z4 G4 MLK','HP Z4 G5','Dell T5860XL','Dell R7960XL'):
                    value.Allowed = False
                else:
                    value.Allowed = True
        elif fut_rel == 'R530':
            if con_type == 'UGUS to ES-T':
                for value in attr1.Values :
                    if value.Display in ('Dell T5860XL','HP Z4 G5'):
                        value.Allowed = True
                    else:
                        value.Allowed = False
            else:
                for value in attr1.Values :
                    if value.Display in ('Dell T5860XL','HP Z4 G5','Dell R7960XL'):
                        value.Allowed = True
                    else:
                        value.Allowed = False
        else:
            for value in attr1.Values:
                if value.Display in ('HP Z4 G4 MLK','DELL R7920XL RAID','DELL T5820XL'):
                    value.Allowed = True
                else:
                    value.Allowed = False
    row.ApplyProductChanges()
    hardwareValues=['Dell Optiplex XE4','Dell R7960XL','HP Z4 G5','Dell T5860XL']
    for row in addStn.Rows:
        flag = True if fut_rel == 'R530'and addServer == "Yes" else False
        if(row["TPS_EX_Additional_Stations_Type"] in ("Flex Station - Cabinet","Console Station - Cabinet","Console Extended Station - Cabinet","ES-T Station - Cabinet","Console Station - Orion","Console Extended Station - Orion","Flex Station - Orion","ES-T Station - Orion")):
            attr1 = row.GetColumnByName("TPS_EX_Additional_Stations_Cabinat_Hardware").ReferencingAttribute
            for value in attr1.Values:
                value.Allowed = True if value.Display in hardwareValues and flag else True if value.Display not in hardwareValues and flag==False else False

        elif(row["TPS_EX_Additional_Stations_Type"] in ("Console Station - Desk","Console Extended Station - Desk","Flex Station - Desk","ES-T Station - Desk")):
            attr2 = row.GetColumnByName("TPS_EX_Additional_Stations_Desk_Hardware").ReferencingAttribute
            for value in attr2.Values:
                value.Allowed = True if value.Display in hardwareValues and flag else True if value.Display not in hardwareValues and flag==False else False
        
    row.ApplyProductChanges()
        
    containerList=[esvtCon,acetCon,addSerCon,bundleCon]
    containerAttrMap={
        "TPS_EX_Conversion_ESVT_Server":"TPS_EX_ESVT_Server_Hardware",
        "TPS_EX_Conversion_ACET_EAPP":"TPS_EX_Conversion_ACET_EAPP_Server_Hardware",
        "TPS_EX_Additional_Servers":"TPS_EX_Additional_Server_Hardware",
        "TPS_EX_Bundle_Conversion_Server_Stations":"TPS_EX_Bundle_Conversion_ESVT_Server_Hardware"
    }
    flag=True
    for container in containerList:
        columName=containerAttrMap[container.Name]
        flag=False if( columName=="TPS_EX_Additional_Server_Hardware" and addServer!="Yes") else True
        for row in container.Rows:
            attr1 = row.GetColumnByName(columName).ReferencingAttribute
            if fut_rel in ('R520','R530','R511','R510') and flag:
                for value in attr1.Values:
                    if fut_rel in ('R510','R511') and value.Display in('HP DL 320 G11'):
                        value.Allowed=False
                    Log.Info("ContainerName:{0} ColumnName: {1} value display: {2} allowed or not: {3}".format(container.Name,columName,value.Display,value.Allowed))
        row.ApplyProductChanges()
    
    for row in bundleCon.Rows:
        attr2 = row.GetColumnByName("TPS_EX_Bundle_Conversion_EST_Station_Hardware").ReferencingAttribute
        if fut_rel not in('R520','R530'):
            for value in attr2.Values:
                #Trace.Write(value.Display)
                if value.Display in ('HP Z4 G4 MLK','HP Z4 G5','Dell T5860XL','Dell R7960XL'):
                    value.Allowed = False
                else:
                    value.Allowed = True
        elif fut_rel =='R530':
            for value in attr2.Values:
                #Trace.Write(value.Display)
                if value.Display in ('Dell T5860XL','HP Z4 G5','Dell R7960XL'):
                    value.Allowed = True
                else:
                    value.Allowed = False
        else:
            for value in attr2.Values:
                if value.Display == 'HP Z4 G4 MLK':
                    value.Allowed = True
                else:
                    value.Allowed = False
        row.ApplyProductChanges()

    
if "OPM" in selectedProducts or "Non - SESP FDM Upgrade" in selectedProducts or "TPS to Experion":
    con1 = getContainer('MSID_CommonQuestions')
    for row in con1.Rows:
        fut_rel = row["MSID_Future_Experion_Release"]
        curr_rel = row["MSID_Current_Experion_Release"]
        curr_attr = row.GetColumnByName("MSID_Current_Experion_Release").ReferencingAttribute
        fut_attr = row.GetColumnByName("MSID_Future_Experion_Release").ReferencingAttribute
        break
    if curr_rel == 'R511.x':
        for value in fut_attr.Values:
            if value.Display in ('R510','R511'):
                value.Allowed = False
            else:
                value.Allowed = True

    elif curr_rel == 'R520.x':
        for value in fut_attr.Values:
            if value.Display in ('R510','R511','R520'):
                value.Allowed = False
            else:
                value.Allowed = True

    elif curr_rel == 'R510.x':
        for value in fut_attr.Values:
            if value.Display in ('R510'):
                value.Allowed = False
            else:
                value.Allowed = True
    else:
        for value in fut_attr.Values:
            value.Allowed = True

for i in selectedProducts:
    if i in ["ELCN","TPS to Experion","EHPM/EHPMX/ C300PM","C200 Migration","Non - SESP FDM Upgrade","OPM","FDM Upgrade 1","xPM to C300 Migration","LM to ELMM ControlEdge PLC"]:
        Product.ApplyRules()
        break
country = Quote.GetCustomField('Account Address Country').Content
opmBasicInfoCon = getContainer('OPM_Basic_Information')
migrationPlatform = getContainer("OPM_Migration_platforms")
servicesCon = getContainer("OPM_Services")
msidcommon = getContainer("MSID_CommonQuestions")
if "OPM" in selectedProducts:
    for row in opmBasicInfoCon.Rows:
        #Trace.Write(row["OPM_Is_the_Experion_System_LCN_Connected"])
        if row["OPM_Is_the_Experion_System_LCN_Connected"] == "No":
            for row1 in migrationPlatform.Rows:
                attr_lcn = row1.GetColumnByName("OPM_Experion_Server_Hardware_Selection").ReferencingAttribute
                for value in attr_lcn.Values:
                    if value.Display in ('Dell R740XL'):
                        #Trace.Write("check5")
                        value.Allowed = False
        row.ApplyProductChanges()
        break
    for Row2 in migrationPlatform.Rows:
        attr1 = Row2.GetColumnByName("OPM_Experion_Server_Hardware_Selection").ReferencingAttribute
        attr2 = Row2.GetColumnByName("OPM_Other_Servers_Hardware_Selection").ReferencingAttribute
        attr3 = Row2.GetColumnByName("OPM_Select_RESS_platform_configuration").ReferencingAttribute
        attr4 = Row2.GetColumnByName("OPM_ACET_EAPP_Server_Hardware_Selection").ReferencingAttribute
        #Trace.Write("Country:{0}".format(country))
        for values in attr1.Values:
            if country not in ('china','China'):
                #Trace.Write("This is hi2.2.0:{0}".format(values.Display))
                if values.Display in ('DELL T550 STD No TPM','DELL R450 STD No TPM','HP DL360 G10'):
                    values.Allowed = False
                
                    #Trace.Write("Done1")
            Row2.ApplyProductChanges()
            #break
        for values in attr2.Values:
            if country not in ('china','China'):
                if values.Display in ('DELL T550 STD No TPM','DELL R450 STD No TPM','HP DL360 G10'):
                    values.Allowed = False
                    #Trace.Write("Done2")
            Row2.ApplyProductChanges()
        for values in attr3.Values:
            if country not in ('china','China'):
                if values.Display in ('DELL T550 STD No TPM','DELL R450 STD No TPM','HP DL360 G10'):
                    values.Allowed = False
                    #Trace.Write("Done3")
            Row2.ApplyProductChanges()
        for values in attr4.Values:
            if country not in ('china','China'):
                if values.Display in ('DELL T550 STD No TPM','DELL R450 STD No TPM','HP DL360 G10'):
                    values.Allowed = False
                    #Trace.Write("Done3")
            Row2.ApplyProductChanges()
#Product.ApplyRules()