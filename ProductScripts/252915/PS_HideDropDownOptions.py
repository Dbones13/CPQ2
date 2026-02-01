def getContainer(Name):
    return Product.GetContainerByName(Name)

country = Quote.GetCustomField('Account Address Country').Content
opmBasicInfoCon = getContainer('OPM_Basic_Information')
migrationPlatform = getContainer("OPM_Migration_platforms")
servicesCon = getContainer("OPM_Services")
msidcommon = getContainer("MSID_CommonQuestions")

for Row in opmBasicInfoCon.Rows:
    if Row["OPM_Is_the_Experion_System_LCN_Connected"] == "Yes":
        for row in migrationPlatform.Rows:
            attribute = row.GetColumnByName("OPM_Experion_Server_Hardware_Selection").ReferencingAttribute
            for value in attribute.Values:
                if value.Display in ('DELL T150 STD TPM','DELL R250XE STD TPM','DELL R450 STD TPM','DELL R450 STD','DELL R450 STD No TPM','Dell R350XE'):
                    value.Allowed = False
                if value.Display in ('DELL T550 STD TPM','DELL T550 STD No TPM','Dell R740XL','HP DL360 G10'):
                    value.Allowed = True
            break
    elif Row["OPM_Is_the_Experion_System_LCN_Connected"] == "No":
        for Row1 in msidcommon.Rows:
            if Row1["MSID_Future_Experion_Release"] in ('R501','R511','R510'):
                for row in migrationPlatform.Rows:
                    attribute = row.GetColumnByName("OPM_Experion_Server_Hardware_Selection").ReferencingAttribute
                    for value in attribute.Values:
                        if value.Display in ('DELL T150 STD TPM','DELL R250XE STD TPM','Dell R350XE'):
                            value.Allowed = False
                        if value.Display in ('Dell R740XL','HP DL360 G10','DELL T550 STD TPM','DELL T550 STD No TPM','DELL R450 STD TPM','DELL R450 STD No TPM') :
                            value.Allowed = True
                    break
            elif Row1["MSID_Future_Experion_Release"] == 'R520':
                for row in migrationPlatform.Rows:
                    attribute = row.GetColumnByName("OPM_Experion_Server_Hardware_Selection").ReferencingAttribute
                    for value in attribute.Values:
                        if value.Display in ('Dell R740XL','HP DL360 G10','DELL T550 STD TPM','DELL T150 STD TPM','DELL R250XE STD TPM','DELL T550 STD No TPM','DELL R450 STD TPM','DELL R450 STD No TPM','Dell R350XE') :
                            value.Allowed = True
                    break
    if Row["OPM_Is_this_is_a_Remote_Migration_Service_RMS"] == "Yes":
        for row in servicesCon.Rows:
            attribute = row.GetColumnByName("OPM_Acceptance_Test_Required").ReferencingAttribute
            for value in attribute.Values:
                if value.Display in ('HAT','FAT','FAT & SAT','No'):
                    value.Allowed = False
                if value.Display in ('HAT & SAT','SAT'):
                    value.Allowed = True
            break
    elif Row["OPM_Is_this_is_a_Remote_Migration_Service_RMS"] == "No":
        for row in servicesCon.Rows:
            attribute = row.GetColumnByName("OPM_Acceptance_Test_Required").ReferencingAttribute
            for value in attribute.Values:
                if value.Display in ('HAT','FAT','FAT & SAT','No','HAT','HAT & SAT','SAT'):
                    value.Allowed = True
    break

for Row1 in msidcommon.Rows:
    if Row1["MSID_Future_Experion_Release"] in ('R501','R511','R510'):
        for row1 in migrationPlatform.Rows:
            attr1 = row1.GetColumnByName("OPM_Select_RESS_platform_configuration").ReferencingAttribute
            for value in attr1.Values:
                if value.Display in ('DELL T150 STD TPM','DELL R250XE STD TPM'):
                    value.Allowed = False
                if value.Display in ('Dell R740XL','HP DL360 G10','DELL T550 STD TPM','DELL T550 STD No TPM','DELL R450 STD TPM','DELL R450 STD No TPM') :
                    value.Allowed = True
            attr2 = row1.GetColumnByName("OPM_Other_Servers_Hardware_Selection").ReferencingAttribute
            for value in attr2.Values:
                if value.Display in ('DELL T150 STD TPM','DELL R250XE STD TPM','Dell R350XE'):
                    value.Allowed = False
                if value.Display in ('HP DL360 G10','DELL T550 STD TPM','DELL T550 STD No TPM','DELL R450 STD TPM','DELL R450 STD No TPM'):
                    value.Allowed = True
            break
    elif Row1["MSID_Future_Experion_Release"] == 'R520':
        for row1 in migrationPlatform.Rows:
            attr1 = row1.GetColumnByName("OPM_Select_RESS_platform_configuration").ReferencingAttribute
            for value in attr1.Values:
                if value.Display in ('DELL T150 STD TPM','DELL R250XE STD TPM','HP DL360 G10','Dell R740XL','DELL T550 STD TPM','DELL T550 STD No TPM','DELL R450 STD TPM','DELL R450 STD No TPM') :
                    value.Allowed = True
            attr2 = row1.GetColumnByName("OPM_Other_Servers_Hardware_Selection").ReferencingAttribute
            for value in attr2.Values:
                Trace.Write("check18")
                if value.Display in ('DELL T150 STD TPM','DELL R250XE STD TPM','HP DL360 G10','DELL T550 STD TPM','DELL T550 STD No TPM','DELL R450 STD TPM','DELL R450 STD No TPM','Dell R350XE') :
                    Trace.Write("check19")
                    value.Allowed = True
            break

##EBR Product
ebrBasicInfo = getContainer('EBR_Basic_Information')
hwtohostebrphysical = getContainer('EBR_Hardware_to_Host_EBR_Physical_Node_Only')

for Row in ebrBasicInfo.Rows:
    Trace.Write('Value: '+Row['EBR_Future_EBR_Release'])
    if Row['EBR_Future_EBR_Release'] == 'R520':
        for row in hwtohostebrphysical.Rows:
            attributeebr = row.GetColumnByName('EBR_If_hardware_desired_select_host_type').ReferencingAttribute
            for value in attributeebr.Values:
                Trace.Write('Check point 3'+value.Display)
                if value.Display in ('None','DELL T150 STD TPM','DELL T550 STD TPM','DELL T550 STD No TPM','DELL R250XE STD TPM','DELL R450 STD TPM','Dell R740XL', 'HP DL360 G10','DELL R450 STD No TPM'):
                    value.Allowed = True
                #if value.Display in ('Dell R740XL', 'HP DL360 G10'):
                #    value.Allowed = False
            break
    break
for Row1 in hwtohostebrphysical.Rows:
    attributeebr = Row1.GetColumnByName('EBR_If_hardware_desired_select_host_type').ReferencingAttribute
    for values in attributeebr.Values:
        if country != 'china':
            Trace.Write("This is hi")
            if values.Display in ('DELL T550 STD No TPM','DELL R450 STD No TPM'):
                values.Allowed = False
                Trace.Write("Done")
    break
selectedProducts = list()
for row in getContainer("MSID_Product_Container").Rows:
    selectedProducts.append(row["Product Name"])

if 'ELCN' in selectedProducts:
    elcnNetworkGatewayUpgradeCon = getContainer('ELCN_Network_Gateway_Upgrade')
    elcnUpgradeNewElcnNodesCon =  getContainer('ELCN_Upgrade_New_ELCN_Nodes')
    totalQtyOfNetworkGateway = 0
    rowAssetDB = 2
    rowIndex = 0
    '''Sum of Upgrade Physical, Virtual, New Physical, and Virtual Quantities'''
    for row in elcnUpgradeNewElcnNodesCon.Rows:
        if rowIndex != rowAssetDB:
            for column in row.Columns:
                if row[column.Name] != '' and column.Name == "ELCN_Qty_of_Network_Gateways":
                    totalQtyOfNetworkGateway += int(row[column.Name])
        rowIndex += 1
    if totalQtyOfNetworkGateway < 2:
        row = elcnNetworkGatewayUpgradeCon.Rows[0]
        attribute = row.GetColumnByName("ELCN_Select_Switch_configuration_required").ReferencingAttribute
        for value in attribute.Values:
            if value.Display == 'Responsible - Alternate configuration':
                value.Allowed = False
    else:
        row = elcnNetworkGatewayUpgradeCon.Rows[0]
        attribute = row.GetColumnByName("ELCN_Select_Switch_configuration_required").ReferencingAttribute
        for value in attribute.Values:
            if value.Display == 'Responsible - Alternate configuration':
                value.Allowed = True

if "TPS to Experion" in selectedProducts:
    con = getContainer('TPS_EX_Additional_Stations')
    cont = getContainer('TPS_EX_General_Questions')
    r = cont.Rows[0]
    if(r["Additional_Server_ESV_Stations_ESF_ESC_ESF_Required"] == "Yes"):
        for row in con.Rows:
            if(row["TPS_EX_Additional_Stations_Type"] in ("Flex Station - Cabinet","Console Station - Cabinet","Console Extended Station - Cabinet","ES-T Station - Cabinet")):
                attribute = row.GetColumnByName("TPS_EX_Additional_Stations_Cabinat_Hardware").ReferencingAttribute
                for value in attribute.Values:
                    value.Allowed = False if value.Display in ("HP Z4 G4") else True


            elif(row["TPS_EX_Additional_Stations_Type"] in ("Console Station - Orion","Console Extended Station - Orion","Flex Station - Orion","ES-T Station - Orion")):
                attribute = row.GetColumnByName("TPS_EX_Additional_Stations_Cabinat_Hardware").ReferencingAttribute
                for value in attribute.Values:
                    value.Allowed = False if value.Display in ("Dell R7920XL RAID") else True

            elif(row["TPS_EX_Additional_Stations_Type"] == "ES-T Station - Desk"):
                attribute = row.GetColumnByName("TPS_EX_Additional_Stations_Desk_Hardware").ReferencingAttribute
                for value in attribute.Values:
                    value.Allowed = False if value.Display in ("Dell OptiPlex XE3") else True


if "TPS to Experion" in selectedProducts:
    con = getContainer('TPS_EX_Additional_Stations')
    cont = getContainer('TPS_EX_General_Questions')
    r = cont.Rows[0]
    if(r["Additional_Server_ESV_Stations_ESF_ESC_ESF_Required"] == "Yes"):
        for row in con.Rows:
            attribute = row.GetColumnByName("TPS_EX_Additional_Stations_RPS_Type").ReferencingAttribute
            for value in attribute.Values:
                value.Allowed = False if value.Display in ("WYSE 5070 - Thin Client","WYSE 5070 - Universal Thin Client") else True

if "TPS to Experion" in selectedProducts:
    con = getContainer('TPS_EX_Additional_Stations')
    cont = getContainer('TPS_EX_General_Questions')
    r = cont.Rows[0]
    if(r["Additional_Server_ESV_Stations_ESF_ESC_ESF_Required"] == "Yes"):
        for row in con.Rows:
            if(row["TPS_EX_Additional_Stations_Type"] in ("Flex Station - Cabinet","Console Station - Cabinet","Console Extended Station - Cabinet","ES-T Station - Cabinet")):
                attribute = row.GetColumnByName("TPS_EX_Additional_Stations_RPS_Mounting_Furniture").ReferencingAttribute
                if (row["TPS_EX_Additional_Stations_RPS_Type"] in ("P&F BTC12 – Dual Video Thin Client","P&F BTC14 – Quad Video Thin Client","WYSE 5070 - Thin Client for 5+ displays")):
                    for value in attribute.Values:
                        value.Allowed = False if value.Display not in ("NA") else True
                else:
                    for value in attribute.Values:
                        value.Allowed = True if value.Display not in ("NA") else False

if "TPS to Experion" in selectedProducts:
    con = getContainer('TPS_EX_Additional_Servers')
    msidCon= getContainer("MSID_CommonQuestions")
    ExRel = msidCon.Rows[0]["MSID_Future_Experion_Release"]
    if ExRel in ('R501','R511','R510'):
        for row in con.Rows:
            attribute_1 = row.GetColumnByName("TPS_EX_Additional_Server_Hardware").ReferencingAttribute
            for value in attribute_1.Values:
                if value.Display in ('Dell T340 Standard RAID','Dell T340 Performance','Dell R240XL','Dell R340XL','DELL T250XE STD TPM','DELL T150 STD TPM','DELL R250XE STD TPM'):
                    value.Allowed = False
                if value.Display in ('DELL T550 STD TPM','DELL T550 STD No TPM','DELL T450 STD TPM','DELL T450 STD No TPM','Dell R740XL','Dell XR11'):
                    value.Allowed = True
    elif ExRel == 'R520':
        for row in con.Rows:
            attribute_1 = row.GetColumnByName("TPS_EX_Additional_Server_Hardware").ReferencingAttribute
            for value in attribute_1.Values:
                if value.Display in ('Dell T340 Standard RAID','Dell T340 Performance','Dell R240XL','Dell R340XL'):
                    value.Allowed = False
                if value.Display in ('HP DL 320 G11','DELL T150 STD TPM','DELL T550 STD TPM','DELL T550 STD No TPM','DELL T250XE STD TPM','DELL T450 STD TPM','DELL T450 STD No TPM','Dell R740XL','Dell XR11','DELL R250XE STD TPM'):
                    value.Allowed = True
    for Row1 in con.Rows:
        attributeebr = Row1.GetColumnByName('TPS_EX_Additional_Server_Hardware').ReferencingAttribute
        for values in attributeebr.Values:
            if country != 'china':
                Trace.Write("This is TPS TO EXP:{0}".format(values.Display))
                if values.Display in ('DELL T550 STD No TPM','DELL R450 STD No TPM'):
                    values.Allowed = False
                    Trace.Write("Done")
        #break

if "TPS to Experion" in selectedProducts:
    con = getContainer('TPS_EX_Additional_Servers')
    cont = getContainer('TPS_EX_General_Questions')
    r = cont.Rows[0]
    if(r["Additional_Server_ESV_Stations_ESF_ESC_ESF_Required"] == "Yes"):
        for row in con.Rows:
            attribute_1 = row.GetColumnByName("TPS_EX_Addtional_Server_Additional_Hard_Drive").ReferencingAttribute
            attribute_2 = row.GetColumnByName("TPS_EX_Additional_Server_Additional_Memory").ReferencingAttribute
            if (row["TPS_EX_Additional_Server_Hardware"] in ("DELL T150 STD TPM","DELL T550 STD TPM","DELL T550 STD No TPM","DELL T250XE STD TPM","DELL T450 STD TPM","DELL T450 STD No TPM")):
                for value_1 in attribute_1.Values:
                    value_1.Allowed = False if value_1.Display not in ("NA") else True
                for value_2 in attribute_2.Values:
                    value_2.Allowed = False if value_2.Display not in ("NA") else True
                row.Product.Attr("TPS_EX_Additional_Server_Additional_Memory").SelectDisplayValue("NA")
                row.Product.Attr("TPS_EX_Additional_Hard_Drives").SelectDisplayValue("NA")
                row.ApplyProductChanges()
            else:
                for value_1 in attribute_1.Values:
                    value_1.Allowed = True if value_1.Display not in ("NA") else False
                for value_2 in attribute_2.Values:
                    value_2.Allowed = True if value_2.Display not in ("NA") else False
                if row['TPS_EX_Additional_Server_Additional_Memory'] == 'NA':
                    row.Product.Attr("TPS_EX_Additional_Server_Additional_Memory").SelectDisplayValue("None")
                if row['TPS_EX_Addtional_Server_Additional_Hard_Drive'] == 'NA':
                    row.Product.Attr("TPS_EX_Additional_Hard_Drives").SelectDisplayValue("No")
                row.ApplyProductChanges()

if "TPS to Experion" in selectedProducts:
    con = getContainer('TPS_EX_Conversion_ACET_EAPP')
    for row in con.Rows:
        if row["TPS_EX_Conversion_ACET_EAPP_Type"] == "APP to ACE-T":
            attribute = row.GetColumnByName("TPS_EX_Conversion_ACET_EAPP_Server_Hardware").ReferencingAttribute
            for value in attribute.Values:
                    value.Allowed = True if value.Display in ("HP DL 320 G11","DELL R740XL") else False

        elif row["TPS_EX_Conversion_ACET_EAPP_Type"] == "APP to EAPP":
            attribute = row.GetColumnByName("TPS_EX_Conversion_ACET_EAPP_Server_Hardware").ReferencingAttribute
            for value in attribute.Values:
                if value.Display in ("HP DL 320 G11","DELL T550 STD TPM","DELL T550 STD No TPM","DELL R740XL") and country in ('china','China'):
                    value.Allowed = True
                elif value.Display in ("HP DL 320 G11","DELL T550 STD TPM","DELL R740XL") and country not in ('china','China'):
                    value.Allowed = True
                else:
                    value.Allowed = False
                #value.Allowed = True if value.Display in ("HP DL360 G10","DELL T550 STD TPM","DELL T550 STD No TPM","DELL R740XL") else False

if 'EHPM/EHPMX/ C300PM' in selectedProducts:
    eNBMigrationConfigCont = getContainer('ENB_Migration_Config_Cont')
    xPMMigrationGeneralQnsCont = getContainer('xPM_Migration_General_Qns_Cont')
    row = xPMMigrationGeneralQnsCont.Rows[0]
    xPMMigratonScenarioCont = getContainer('xPM_Migration_Scenario_Cont')
    Row = xPMMigratonScenarioCont.Rows[0]
    if row["xPM_On_Process_Red_HPMs_or_Off_Process_Migration"] == "HPM to EHPM On Process" or row["xPM_On_Process_Red_HPMs_EHPMs_only"] == "HPM/EHPM to C300PM On Process":
        for rowENB in eNBMigrationConfigCont.Rows:
            attribute = rowENB.GetColumnByName("xPM_What_is_the_NIM_migration_scenario").ReferencingAttribute
            for value in attribute.Values:
                if value.Display == 'Non Redundant NIM to ENB':
                    value.Allowed = False
    else:
        for rowENB in eNBMigrationConfigCont.Rows:
            attribute = rowENB.GetColumnByName("xPM_What_is_the_NIM_migration_scenario").ReferencingAttribute
            for value in attribute.Values:
                if value.Display == 'Non Redundant NIM to ENB':
                    value.Allowed = True

    for row in xPMMigrationGeneralQnsCont.Rows:
        attribute1 = row.GetColumnByName("xPM_TPN_SW_Release_at_time_of_xPM_migration").ReferencingAttribute
        attribute2 = row.GetColumnByName("xPM_EPKS_SW_Release_at_time_of_xPM_migration").ReferencingAttribute
        attribute3 = row.GetColumnByName("xPM_On_Process_Red_HPMs_or_Off_Process_Migration").ReferencingAttribute
        attribute4 = row.GetColumnByName("xPM_On_Process_Red_HPMs_EHPMs_only").ReferencingAttribute
        attribute5 = row.GetColumnByName("xPM_On_Process_Red_HPMs_EHPMs_for_EHPMX_mig").ReferencingAttribute
        if Row["xPM_Select_the_migration_scenario"] == "xPM to EHPM":
            for value in attribute1.Values:
                value.Allowed = True if value.Display in ('TPN R684.2','TPN R685.1','TPN R685.2','TPN R685.3','TPN R686.2 or later','-') else False
            for value in attribute2.Values:
                value.Allowed = True if value.Display in ('None','EPKS R400/R410','EPKS R430','EPKS R431.1 / R431.2','EPKS R432.1 or later','EPKS R500 or later','-') else False
        if Row["xPM_Select_the_migration_scenario"] in ["xPM to C300PM",'xPM to EHPMX']:
            for value in attribute1.Values:
                value.Allowed = True if value.Display in ('TPN 690.2 or later','-') else False
            for value in attribute2.Values:
                value.Allowed = True if value.Display in ('EPKS R520.2 TCU1 or later','-') else False
        for value in attribute3.Values:
            if row["xPM_TPN_SW_Release_at_time_of_xPM_migration"] == "TPN R686.2 or later" and row["xPM_EPKS_SW_Release_at_time_of_xPM_migration"] == "EPKS R432.1 or later" and value.Display == "HPM to EHPM On Process":
                value.Allowed = True
            elif value.Display == "HPM to EHPM On Process":
                value.Allowed = False
        
        for value in attribute4.Values:
            if row["xPM_TPN_SW_Release_at_time_of_xPM_migration"] == "TPN 690.2 or later" and row["xPM_EPKS_SW_Release_at_time_of_xPM_migration"] == "EPKS R520.2 TCU1 or later" and value.Display == "HPM/EHPM/EHPMX to C300PM On Process":
                value.Allowed = True
            elif value.Display == "HPM/EHPM/EHPMX to C300PM On Process":
                value.Allowed = False
        for value in attribute5.Values:
            if row["xPM_TPN_SW_Release_at_time_of_xPM_migration"] == "TPN 690.2 or later" and row["xPM_EPKS_SW_Release_at_time_of_xPM_migration"] == "EPKS R520.2 TCU1 or later" and value.Display == "HPM/EHPM to EHPMX On Process":
                value.Allowed = True
            elif value.Display == "HPM/EHPM to EHPMX On Process":
                value.Allowed = False

        break

    listOfEHPMOptions = ['UPG PM/APM TO 7-SLOT EHPM Non RED With IOL','UPG PM/APM TO 15-SLOT EHPM Non RED With IOL','UPG PM/APM TO 7-SLOT EHPM RED With IOL','UPG PM/APM TO 15-SLOT EHPM RED With IOL','UPG HPM TO EHPM Non RED With IOL','UPG HPM TO EHPM RED With IOL','UPG HPM TO EHPM Non RED Without IOL','UPG HPM TO EHPM RED Without IOL']
    listOfC300PMOptions = ['Non-redundant PM/APM to C300PM in 7-slot chassis', 'Non-redundant PM/APM to C300PM in 15-slot chassis', 'Redundant PM/APM to C300PM in 7-slot chassis', 'Redundant PM/APM to C300PM in15-slot chassis', 'Non-redundant HPM to C300PM', 'Redundant HPM to C300PM', 'Non-redundant EHPM to C300PM', 'Redundant EHPM to C300PM','Non-redundant EHPMX to C300PM','Redundant EHPMX to C300PM']
    listOfEHPMXOptions = ["Non-redundant PM/APM to EHPMX in 7-slot chassis", "Non-redundant PM/APM to EHPMX in 15-slot chassis", "Redundant PM/APM to EHPMX in 7-slot chassis", "Redundant PM/APM to EHPMX in15-slot chassis", "Non-redundant HPM to EHPMX", "Redundant HPM to EHPMX", "Non-redundant EHPM to EHPMX", "Redundant EHPM to EHPMX"]
    C300list = ['Redundant HPM to C300PM','Redundant EHPM to C300PM','Redundant EHPMX to C300PM']
    EHPMXlist = ['Redundant HPM to EHPMX', 'Redundant EHPM to EHPMX']
    xPMMigrationConfigCont = getContainer('xPM_Migration_Config_Cont')
    xPMMigrationScenarioCont = getContainer('xPM_Migration_Scenario_Cont')
    rowMigrationScenario = xPMMigrationScenarioCont.Rows[0]

    if row['xPM_On_Process_Red_HPMs_EHPMs_only'] == 'HPM/EHPM/EHPMX to C300PM On Process':
        for row in xPMMigrationConfigCont.Rows:
            attribute = row.GetColumnByName("xPM_Migration_Scenario").ReferencingAttribute
            z =sum([listOfEHPMOptions,listOfC300PMOptions,listOfEHPMXOptions],[])
            for value in attribute.Values:
                if value.Display in C300list:
                    value.Allowed = True
                elif value.Display in z:
                    value.Allowed = False 
    elif row['xPM_On_Process_Red_HPMs_EHPMs_for_EHPMX_mig'] == 'HPM/EHPM to EHPMX On Process':
        for row in xPMMigrationConfigCont.Rows:
            attribute = row.GetColumnByName("xPM_Migration_Scenario").ReferencingAttribute
            z =sum([listOfEHPMOptions,listOfC300PMOptions,listOfEHPMXOptions],[])
            for value in attribute.Values:
                if value.Display in EHPMXlist:
                    value.Allowed = True
                elif value.Display in z:
                    value.Allowed = False 
    else:
        if rowMigrationScenario['xPM_Select_the_migration_scenario'] == 'xPM to C300PM':
            for row in xPMMigrationConfigCont.Rows:
                attribute = row.GetColumnByName("xPM_Migration_Scenario").ReferencingAttribute
                z =sum([listOfEHPMOptions,listOfEHPMXOptions],[])
                for value in attribute.Values:
                    if value.Display in listOfC300PMOptions:
                        value.Allowed = True
                    elif value.Display in z:
                        value.Allowed = False
                if row['xPM_Migration_Scenario'] not in listOfC300PMOptions or not row['xPM_Migration_Scenario']:
                    for col in row.Columns:
                        if col.Name == 'xPM_Migration_Scenario':
                            col.SetAttributeValue("Non-redundant PM/APM to C300PM in 7-slot chassis")
                            row['xPM_Migration_Scenario'] = "Non-redundant PM/APM to C300PM in 7-slot chassis"
                            break
        elif rowMigrationScenario['xPM_Select_the_migration_scenario'] == 'xPM to EHPM':
            for row in xPMMigrationConfigCont.Rows:
                attribute = row.GetColumnByName("xPM_Migration_Scenario").ReferencingAttribute
                z =sum([listOfC300PMOptions,listOfEHPMXOptions],[])
                for value in attribute.Values:
                    if value.Display in listOfEHPMOptions:
                        value.Allowed = True
                    elif value.Display in z:
                        value.Allowed = False
                if row['xPM_Migration_Scenario'] not in listOfEHPMOptions or not row['xPM_Migration_Scenario']:
                    for col in row.Columns:
                        if col.Name == 'xPM_Migration_Scenario':
                            col.SetAttributeValue("UPG PM/APM TO 7-SLOT EHPM Non RED With IOL")
                            row['xPM_Migration_Scenario'] = "UPG PM/APM TO 7-SLOT EHPM Non RED With IOL"
                            break
        elif rowMigrationScenario['xPM_Select_the_migration_scenario'] == 'xPM to EHPMX':
            for row in xPMMigrationConfigCont.Rows:
                attribute = row.GetColumnByName("xPM_Migration_Scenario").ReferencingAttribute
                z =sum([listOfC300PMOptions,listOfEHPMOptions],[])
                for value in attribute.Values:
                    if value.Display in listOfEHPMXOptions:
                        value.Allowed = True
                    elif value.Display in z:
                        value.Allowed = False
                if row['xPM_Migration_Scenario'] not in listOfEHPMXOptions or not row['xPM_Migration_Scenario']:
                    for col in row.Columns:
                        if col.Name == 'xPM_Migration_Scenario':
                            col.SetAttributeValue("Non-redundant PM/APM to EHPMX in 7-slot chassis")
                            row['xPM_Migration_Scenario'] = "Non-redundant PM/APM to EHPMX in 7-slot chassis"
                            break

if 'C200 Migration' in selectedProducts:
    C200MigrationGeneralQnsCon = getContainer('C200_Migration_General_Qns_Cont')
    C200MigrationScenario = getContainer('C200_Migration_Scenario_Cont')
    rowMigrationScenario = C200MigrationScenario.Rows[0]
    if rowMigrationScenario['C200_Select_the_Migration_Scenario'] == 'C200 to C300':
        for rowENB in C200MigrationGeneralQnsCon.Rows:
            attribute = rowENB.GetColumnByName("C200_Connection _to_Experion_Server").ReferencingAttribute
            for value in attribute.Values:
                #Trace.Write(value.Display)
                if value.Display == 'Dual Ethernet':
                    #Trace.Write(str(value.Display) + " (before: C300) = " + str(value.Allowed))
                    value.Allowed = False
                    #Trace.Write(str(value.Display) + " (after: C300) = " + str(value.Allowed))
            break
    elif rowMigrationScenario['C200_Select_the_Migration_Scenario'] == 'C200 to ControlEdge UOC':
        for rowENB in C200MigrationGeneralQnsCon.Rows:
            attribute = rowENB.GetColumnByName("C200_Connection _to_Experion_Server").ReferencingAttribute
            for value in attribute.Values:
                #Trace.Write(value.Display)
                x = value
                if value.Display == 'Dual Ethernet':
                    #Trace.Write(str(value.Display) + " (before: UOC) = " + str(value.Allowed))
                    value.Allowed = True
                    #Trace.Write(str(value.Display) + " (after: UOC) = " + str(value.Allowed))
            break

if 'C200 Migration' in selectedProducts:
    C200MigrationConfigCont = getContainer('C200_Migration_Config_Cont')
    C200MigrationScenario = getContainer('C200_Migration_Scenario_Cont')
    rowMigrationScenario = C200MigrationScenario.Rows[0]
    if rowMigrationScenario['C200_Select_the_Migration_Scenario'] == 'C200 to C300':
        for rowENB in C200MigrationConfigCont.Rows:
            attribute = rowENB.GetColumnByName("C200_peer_to_peer_communication").ReferencingAttribute
            for value in attribute.Values:
                #Trace.Write(value.Display)###################
                if value.Display in ('Allen Bradley PLC L2 connected','Allen Bradley PLC over ControlNet','C200 across cluster over ControlNet','C200 within same cluster'):
                    value.Allowed = False
                if value.Display in ('C200','Allen Bradley PLC'):
                    value.Allowed = True
    elif rowMigrationScenario['C200_Select_the_Migration_Scenario'] == 'C200 to ControlEdge UOC':
        for rowENB in C200MigrationConfigCont.Rows:
            attribute = rowENB.GetColumnByName("C200_peer_to_peer_communication").ReferencingAttribute
            for value in attribute.Values:
                if value.Display in ('Allen Bradley PLC L2 connected','Allen Bradley PLC over ControlNet','C200 across cluster over ControlNet','C200 within same cluster'):
                    value.Allowed = True
                if value.Display in ('C200','Allen Bradley PLC'):
                    value.Allowed = False


if 'C200 Migration' in selectedProducts:
    C200MigrationConfigCont = getContainer('C200_Migration_Config_Cont')
    C200MigrationScenario = getContainer('C200_Migration_Scenario_Cont')
    rowMigrationScenario = C200MigrationScenario.Rows[0]
    if rowMigrationScenario['C200_Select_the_Migration_Scenario'] == 'C200 to C300':
        for rowENB in C200MigrationConfigCont.Rows:
            attribute = rowENB.GetColumnByName("C200_Existing_PM_or_Non_Standard_Cabinet_Used").ReferencingAttribute
            if(rowENB["C200_Cabinet_type_customer_plans"] not in ("New Front & Rear Access Series C Cabinet","New Front Access Only Series C Cabinet")):
                for value in attribute.Values:
                    value.Allowed = False if value.Display == "NA" else True
                if rowENB.Product.Attr("C200_Existing_PM_or_Non_Standard_Cabinet_Used").GetValue() not in ("New Front Access Only Series C Cabinet"):
                    rowENB.Product.Attr("C200_Existing_PM_or_Non_Standard_Cabinet_Used").SelectDisplayValue("New Front & Rear Access Series C Cabinet")
                    rowENB.ApplyProductChanges()
            elif(rowENB["C200_Cabinet_type_customer_plans"] in ("New Front & Rear Access Series C Cabinet","New Front Access Only Series C Cabinet")):
                for value in attribute.Values:
                    value.Allowed = True if value.Display == "NA" else False
                rowENB.Product.Attr("C200_Existing_PM_or_Non_Standard_Cabinet_Used").SelectDisplayValue("NA")
                rowENB.ApplyProductChanges()


if 'C200 Migration' in selectedProducts:
    C200MigrationServicesCont1 = getContainer('C200_Services_1_Cont')
    C200MigrationScenario = getContainer('C200_Migration_Scenario_Cont')
    rowMigrationScenario = C200MigrationScenario.Rows[0]
    if rowMigrationScenario['C200_Select_the_Migration_Scenario'] == 'C200 to C300':
        for rowENB in C200MigrationServicesCont1.Rows:
            attribute = rowENB.GetColumnByName("C200_Documentation_Required").ReferencingAttribute
            for value in attribute.Values:
                if value.Display in ('DDS','DDS & Network Drawing'):
                    value.Allowed = False
                if value.Display in ('Yes'):
                    value.Allowed =True
            break
    elif rowMigrationScenario['C200_Select_the_Migration_Scenario'] == 'C200 to ControlEdge UOC':
        for rowENB in C200MigrationServicesCont1.Rows:
            attribute = rowENB.GetColumnByName("C200_Documentation_Required").ReferencingAttribute
            for value in attribute.Values:
                Trace.Write(value.Display)
                if value.Display in ('DDS','DDS & Network Drawing'):
                    value.Allowed = True
                if value.Display in ('Yes'):
                    value.Allowed =False
            break


if "LM to ELMM ControlEdge PLC" in selectedProducts:
    for row in getContainer('LM_to_ELMM_ControlEdge_PLC_Cont').Rows:
        attribute = row.GetColumnByName("LM_select_IO_network_topology").ReferencingAttribute
        if row["LM_are_the_IO_Racks_remotely_located"] in ["Yes - Local and Remote", "Yes - Only Remote"]:
            for value in attribute.Values:
                value.Allowed = False if value.Display == "Ring" else True
                row.Product.Attr("LM_select_IO_network_topology").SelectDisplayValue("Star")
            switch_attribute = row.GetColumnByName("LM_select_type_of_Switch_for_the_IO_network").ReferencingAttribute
            for val in switch_attribute.Values:
                val.Allowed = False if val.Display == "NA" else True
                if(row["LM_select_type_of_Switch_for_the_IO_network"] not in ("Single Mode Redundant","Single Mode Non-Redundant", "Multimode Non-Redundant")):
                    row.Product.Attr("LM_select_type_of_Switch_for_the_IO_network").SelectDisplayValue("Multimode Redundant")
                    row.ApplyProductChanges()
        else:
            for value in attribute.Values:
                value.Allowed = True
        attribute = row.GetColumnByName("LM_select_type_of_Switch_for_the_IO_network").ReferencingAttribute
        if row["LM_select_IO_network_topology"] in ["Ring"]:
            for value in attribute.Values:
                value.Allowed = True if value.Display == "NA" else False
                row.Product.Attr("LM_select_type_of_Switch_for_the_IO_network").SelectDisplayValue("NA")
        else:
            for value in attribute.Values:
                value.Allowed = False if value.Display == "NA" else True
                if(row["LM_select_type_of_Switch_for_the_IO_network"] not in ("Single Mode Redundant","Single Mode Non-Redundant", "Multimode Non-Redundant")):
                    row.Product.Attr("LM_select_type_of_Switch_for_the_IO_network").SelectDisplayValue("Multimode Redundant")
                    row.ApplyProductChanges()
        row.ApplyProductChanges()


if "Non - SESP FDM Upgrade" in selectedProducts:
    for row in getContainer('FDM_Upgrade_General_questions').Rows:
        attribute = row.GetColumnByName("FDM_Upgrade_Select_desired_FDM_release").ReferencingAttribute
        if row["FDM_Upgrade_What_is_the_current_release_of_the_system_to_be_upgraded"] == "FDM R501":
            for value in attribute.Values:
                value.Allowed = False if value.Display == "FDM R501" else True
        elif row["FDM_Upgrade_What_is_the_current_release_of_the_system_to_be_upgraded"] == "FDM R511":
            for value in attribute.Values:
                value.Allowed = True if value.Display == "FDM R520" else False
        else:
            for value in attribute.Values:
                value.Allowed = True

if "FDM Upgrade 1" in selectedProducts:
    fdmGenQues = getContainer("FDM_Upgrade_General_questions")
    for row in fdmGenQues.Rows:
        attr =  row.GetColumnByName("FDM_Upgrade_Select_desired_FDM_release").ReferencingAttribute
        if row["FDM_Upgrade_What_is_the_current_release_of_the_system_to_be_upgraded"] in ("FDM R440 or Lower",""):
            for value in attr.Values:
                Trace.Write(value.Display)
                if value.Display == "FDM R520":
                    value.Allowed = False
                if value.Display in ("FDM R501","FDM R511"):
                    value.Allowed = True
            row.ApplyProductChanges()
            break
        if row["FDM_Upgrade_What_is_the_current_release_of_the_system_to_be_upgraded"] in ("FDM R450","FDM R500","FDM R501","FDM R511"):
            for value in attr.Values:
                #Trace.Write(value.Display)
                if value.Display in ("FDM R520","FDM R501","FDM R511"):
                    value.Allowed = True
            row.ApplyProductChanges()
            break
if "FDM Upgrade 1" in selectedProducts:
    fdmGenQues1 = getContainer("FDM_Upgrade_General_questions")
    for row in fdmGenQues1.Rows:
        attr1 =  row.GetColumnByName("FDM_Upgrade_Select_desired_FDM_release").ReferencingAttribute
        Trace.Write(row["FDM_Upgrade_What_is_the_current_release_of_the_system_to_be_upgraded"])
        if row["FDM_Upgrade_What_is_the_current_release_of_the_system_to_be_upgraded"] in ("FDM R501"):
            for value in attr1.Values:
                Trace.Write(value.Display)
                if value.Display in ("FDM R520","FDM R511"):
                    value.Allowed = True
                #Trace.Write(value.Display)
                if value.Display == "FDM R501":
                    value.Allowed = False

            row.ApplyProductChanges()
            break
        if row["FDM_Upgrade_What_is_the_current_release_of_the_system_to_be_upgraded"] in ("FDM R511"):
            for value in attr1.Values:
                Trace.Write(value.Display)
                if value.Display in ("FDM R511","FDM R501"):
                    value.Allowed = False
                #Trace.Write(value.Display)
                if value.Display == "FDM R520":
                    value.Allowed = True 
            row.ApplyProductChanges()
            break
#Product.ApplyRules()