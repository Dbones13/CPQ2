def getAttributeValue(Name):
    return Product.Attr(Name).GetValue()

def getContainer(Name):
    return Product.GetContainerByName(Name)

def resetFDMColumn(container, index):
    row = container.Rows[index]
    for column in row.Columns:
        if column.Name != "FDM_Upgrade_Do_you_want_to_upgrade_this_FDM":
            row[column.Name] = "0"
        row.Calculate()

def resetAddFDMColumn(container, index):
    row = container.Rows[index]
    for column in row.Columns:
        if column.Name not in  ("FDM_Upgrade_Are_additional_components_required_for_this_FDM","FDM_Upgrade_Audit_trail_file_required","FDM_Upgrade_HART_Devices_Offline_Configuration_required","FDM_Upgrade_Is_Experion_Server_redundant_for_FDM_Multiplexer_Monitoring","FDM_Upgrade_Asset_Sentinel_integration_required"):
            row[column.Name] = "0"
        if column.Name in ("FDM_Upgrade_Audit_trail_file_required","FDM_Upgrade_HART_Devices_Offline_Configuration_required","FDM_Upgrade_Asset_Sentinel_integration_required"):
            column.SetAttributeValue("No")
        if column.Name in ("FDM_Upgrade_Is_Experion_Server_redundant_for_FDM_Multiplexer_Monitoring"):
            column.SetAttributeValue("Yes")
        row.Calculate()

def resetHostFDMColumn(container, index):
    row = container.Rows[index]
    for column in row.Columns:
        if column.Name not in  ("FDM_Upgrade_Is_HW_required_for_this_FDM","FDM_Upgrade_Will_Honeywell_provide_the_FDM_server","FDM_Upgrade_FDM_Gateway_PC_Hardware_Selection"):
            row[column.Name] = "0"
        if column.Name in ("FDM_Upgrade_Will_Honeywell_provide_the_FDM_server"):
            column.SetAttributeValue("No")
        if column.Name in ("FDM_Upgrade_FDM_Gateway_PC_Hardware_Selection"):
            column.SetAttributeValue("Tower")  
        row.Calculate()

selectedProducts = list()

for row in getContainer("MSID_Product_Container").Rows:
    selectedProducts.append(row["Product Name"])

if "FDM Upgrade" in selectedProducts:
    fdmcon = getContainer('FDM_Upgrade_Configuration')
    for row in fdmcon.Rows:
        if row["FDM_Upgrade_Do_you_want_to_upgrade_this_FDM"] != "Yes":
            resetFDMColumn(fdmcon, row.RowIndex)
    fdmcon.Calculate()
    
    check = Product.ParseString('<*CTX( Container(FDM_Upgrade_General_questions).Row(1).Column(FDM_Upgrade_Additional_Components_to_be_offered_for_number_of_FDMs_?).GetDisplayValue )*>')
    if check == "Yes":
        fdmaddcon = getContainer('FDM_Upgrade_Additional_Configuration')
        for row in fdmaddcon.Rows:
            if row["FDM_Upgrade_Are_additional_components_required_for_this_FDM"] != "Yes":
                resetAddFDMColumn(fdmaddcon, row.RowIndex)
        fdmaddcon.Calculate()
    
    fdmhostcon = getContainer('FDM_Upgrade_Hardware_to_host_FDM_Server')
    for row in fdmhostcon.Rows:
        if row["FDM_Upgrade_Is_HW_required_for_this_FDM"] != "Yes":
            resetHostFDMColumn(fdmhostcon, row.RowIndex)
    fdmhostcon.Calculate()
            


