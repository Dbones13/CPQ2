def getFloat(v):
    if v:
        return float(v)
    return 0

def getContainer(prod, conName):
    return prod.GetContainerByName(conName)

def getServiceProduct(product,Quote):
    sespTypeSP = ''
    accountName = Quote.GetCustomField("Account Name").Content if Quote and Quote.GetCustomField("Account Name").Content else " "
    getMSID = product.Attr('Migration_MSID_Choices').GetValue()
    sespCurr = SqlHelper.GetFirst("Select * from MSID where SFDCIdentifier IS NOT NULL and Service_Product !=''  and MSID = '{}' and Account_Name='{}'" .format(getMSID,accountName))
    if sespCurr is not None:
        sespTypeSP= sespCurr.Service_Product
        if sespTypeSP == 'SESP Software Flex':
            return 'Yes'
        elif sespTypeSP == 'SESP Support Flex':
            return 'No'
    return 'Yes'

def checkSESP(product,Quote):
    sespType = ''
    sesp = Quote.GetCustomField("Entitlement").Content if Quote and Quote.GetCustomField("Entitlement").Content else ""
    if sesp in ['K&E Pricing Plus', 'Non-SESP MSID with new SESP Plus']:
        sespType = 'Yes'
    elif sesp in ['', 'Non-SESP MSID with new SESP Flex']:
        sespType = 'No'
    elif sesp in ['K&E Pricing Flex']:
        sespType = getServiceProduct(product,Quote)
    return sespType

def updateAttrDictWithCustomXpm(product, attrValDict,Quote):
    con = getContainer(product, "ENB_Migration_Config_Cont")
    ENB_K4_processor_boards_Non_Redundant_config = 0
    ENB_K4_processor_boards_Redundant_config = 0
    for row in con.Rows:
        if row["xPM_Does_the_customer_have_K4_processor_boards"] == "No" and row["xPM_What_is_the_NIM_migration_scenario"] == "Non Redundant NIM to ENB":
            ENB_K4_processor_boards_Non_Redundant_config += getFloat(row["xPM_Number_of_NIMs_in_this_config"])
        if row["xPM_Does_the_customer_have_K4_processor_boards"] == "No" and row["xPM_What_is_the_NIM_migration_scenario"] == "Redundant NIM to ENB":
            ENB_K4_processor_boards_Redundant_config += getFloat(row["xPM_Number_of_NIMs_in_this_config"]) * 2
    attrValDict["ENB_K4_processor_boards_Non_Redundant_config"] = ENB_K4_processor_boards_Non_Redundant_config
    attrValDict["ENB_K4_processor_boards_Redundant_config"] = ENB_K4_processor_boards_Redundant_config

    isC300Mig = getContainer(product, "xPM_Migration_Scenario_Cont").Rows[0]["xPM_Select_the_migration_scenario"] == "xPM to C300PM"
    total_xpm_points = 0
    total_exp_conn = 0
    sespType = checkSESP(product,Quote)
    migCon = getContainer(product, "xPM_Migration_Config_Cont")
    if isC300Mig and sespType in ("No", ""):
        for row in migCon.Rows:
            xPM_config = getFloat(row["xPM_Number_of_xPMs_in_this_config"])
            total_xpm_points += (getFloat(row["xPM_Number_of_xPM_Points_including_SI"]) * xPM_config)
    if isC300Mig and sespType in ("Yes") :
        scenarioList = ['HPM', 'EHPM']
        for row in migCon.Rows:
            xPM_config = getFloat(row["xPM_Number_of_xPMs_in_this_config"])
            multiplier = 2200 if any(scenario in row["xPM_Migration_Scenario"] for scenario in scenarioList) else 1000
            if ((getFloat(row["xPM_Number_of_xPM_Points_including_SI"] ) * xPM_config) - (xPM_config * multiplier)) > 0:
                total_xpm_points += ((getFloat(row["xPM_Number_of_xPM_Points_including_SI"] ) * xPM_config) - (xPM_config * multiplier))
    if not isC300Mig:
        for row in migCon.Rows:
            total_exp_conn += getFloat(row["xPM_How_many_EHPMs_will_require_Exp_conn"])
    attrValDict["xPM_Total_xPM_require_exp_conn"] = total_exp_conn
    attrValDict["xPM_Total_xPM_Points_Including_SI"] = total_xpm_points
    attrValDict["SESP_TYPE"] = sespType

    con = getContainer(product, "xPM_Network_Upgrade_Cont")
    res = 0
    for row in con.Rows:
        res += getFloat(row["xPM_Qty_of_Red_pair_of_CF9_firewalls"])
        res += getFloat(row["xPM_Qty_Additional_Red_pair_of_CF9_firewalls"])
    attrValDict["xpm_Optic_Extender_needed"] = "true" if res > 0 else "false"

def populateWriteInsTPAPMD(product):
    writeInData = dict()
    msid= product.Attr('Migration_MSID_Choices').GetValue()
    sysNumber= product.Attr('Migration_MSID_System_Number').GetValue()
    area = msid +" - "+ sysNumber
    third_party =getContainer(product,'TPA_Third_Party_Items_Cont')
    for x in third_party.Rows:
        if x["WriteIn"] not in ['Extended warranty for servers']:
        	if x["Display_Flag"]  in [0, "0"] and getFloat(x["Unit_Price"]) >0 and getFloat(x["Unit_Cost"])>0 and getFloat(x["Final_Qty"])>0:
                 writeInData[x["WriteIn"]] = [x["Unit_Price"],x["Unit_Cost"],x["WriteIn_Type"],x["Final_Qty"], area]
        else:
            if getFloat(x["Final_Qty"])>0:
                    writeInData[x["WriteIn"]] = [x["Unit_Price"],x["Unit_Cost"],x["WriteIn_Type"],x["Final_Qty"], area]

    if product.Attr("MIgration_Scope_Choices").GetValue() not in ["LABOR"]:
        productContainer = product.GetContainerByName("MSID_Product_Container")
        productRow = productContainer.Rows.GetByColumnName("Product Name", "TPA/PMD Migration")
        prod = productRow.Product
        con = prod.GetContainerByName("WriteInProduct")
        if con.Rows.Count > 0:
            con.Clear()
        for wi, wiData in writeInData.items():
            row = con.AddNewRow()
            row.Product.Attr("Selected_WriteIn").AssignValue(wiData[2])
            row.Product.Attr("Price").AssignValue(str(wiData[0]))
            row.Product.Attr("Cost").AssignValue(str(wiData[1]))
            row.Product.Attr("QI_Area").AssignValue(wiData[4])
            row.Product.Attr("ItemQuantity").AssignValue(wiData[3])
            row.Product.Attr("Extended Description").AssignValue(str(wi))
            row.Product.ApplyRules()
            row.ApplyProductChanges()
            row.Calculate()
    else:
        productContainer = product.GetContainerByName("MSID_Product_Container")
        productRow = productContainer.Rows.GetByColumnName("Product Name", "TPA/PMD Migration")
        prod = productRow.Product
        con = prod.GetContainerByName("WriteInProduct")
        if con.Rows.Count > 0:
            con.Clear()
    con.Calculate()

def populateCBECwritein(product):
    writeInData = dict()
    msid= product.Attr('Migration_MSID_Choices').GetValue()
    sysNumber= product.Attr('Migration_MSID_System_Number').GetValue()
    area = msid +" - "+ sysNumber
    thirdPartyCost = '0'
    thirdPartyPrice = '0'
    ext_des=''
    con = getContainer(product, "CB_EC_Third_party_items_Cont")
    for row in con.Rows:
        thirdPartyCost=row["CB_EC_Cost"] if row["CB_EC_Cost"] is None or str(row["CB_EC_Cost"]) != '' else '0'
        thirdPartyPrice=row["CB_EC_Price"] if row["CB_EC_Price"] is None or str(row["CB_EC_Price"]) != '' else '0'
        ext_des=row["CB_EC_Extended_Description"]
        break

    writeInData["Write-in Third Party Hardware Misc"]=[thirdPartyPrice,thirdPartyCost,ext_des, area]
    if float(thirdPartyPrice) > 0  and float(thirdPartyCost)> 0:
        productContainer = product.GetContainerByName("MSID_Product_Container")

        productRow = productContainer.Rows.GetByColumnName("Product Name", "CB-EC Upgrade to C300-UHIO")

        prod = productRow.Product
        con1 = prod.GetContainerByName("WriteInProduct")
        Trace.Write(con1)
        con1.Rows.Clear()
        for wi, wiData in writeInData.items():
            if con1.Rows.Count == 0:
            	row = con1.AddNewRow()
            row.Product.Attr("Selected_WriteIn").AssignValue(wi)
            row.Product.Attr("Price").AssignValue(wiData[0])
            row.Product.Attr("Cost").AssignValue(wiData[1])
            row.Product.Attr("QI_Area").AssignValue(wiData[3])
            row.Product.Attr("ItemQuantity").AssignValue("1")
            row.Product.Attr("Extended Description").AssignValue(wiData[2])
            row.Product.ApplyRules()
            row.ApplyProductChanges()
            row.Calculate()
        con1.Calculate()