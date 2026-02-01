def getContainer(Name):
    return Product.GetContainerByName(Name)

selectedProducts = list()
for row in getContainer("MSID_Product_Container").Rows:
    selectedProducts.append(row["Product Name"])

if 'C200 Migration' in selectedProducts:
    con = getContainer("C200_Third_Party_Items_Cont")
    check = Product.ParseString('<*CTX( Container(C200_Migration_Scenario_Cont).Row(1).Column(C200_Select_the_Migration_Scenario).GetDisplayValue )*>')
    if(check == "C200 to C300"):
        count = con.Rows.Count
        if count == 4:
            while count > 0:
                con.DeleteRow(count-1)
                count-=1
        if con.Rows.Count == 0:
            row = con.AddNewRow()
    elif(con.Rows.Count == 1 and check == "C200 to ControlEdge UOC"):
        con.DeleteRow(0)
        i = 4
        while i>0:
            row = con.AddNewRow()
            i-=1
    con.Calculate()

if "FDM Upgrade" in selectedProducts:
    con = getContainer("FDM_Upgrade_Additional_Configuration")
    check = Product.ParseString('<*CTX( Container(FDM_Upgrade_General_questions).Row(1).Column(FDM_Upgrade_Additional_Components_to_be_offered_for_number_of_FDMs_?).GetDisplayValue )*>')
    if(check =="Yes"):
        if con.Rows.Count == 0:
            for i in range(3):
                con.AddNewRow()
            colValuesDict = {"FDM_Upgrade_Are_additional_components_required_for_this_FDM":"No","FDM_Upgrade_Audit_trail_file_required": "No","FDM_Upgrade_HART_Devices_Offline_Configuration_required": "No","FDM_Upgrade_Is_Experion_Server_redundant_for_FDM_Multiplexer_Monitoring" : "Yes","FDM_Upgrade_Asset_Sentinel_integration_required": "No"}
            for row in con.Rows:
                for col in row.Columns:
                    defaultVal = colValuesDict.get(col.Name)
                    if defaultVal:
                        col.SetAttributeValue(defaultVal)
                        row.SetColumnValue(col.Name,defaultVal)
    else:
        if con.Rows.Count >0:
            con.Rows.Clear()
    con.Calculate()