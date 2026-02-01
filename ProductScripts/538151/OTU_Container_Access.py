currentTab = arg.NameOfCurrentTab
if currentTab == 'OTU':
    Product.Attr('OTU_ServiceProduct').AssignValue("Software Upgrades")
    Product.Attr("OTU_ServiceProduct").Access = AttributeAccess.ReadOnly
    Product.Attr('OTU_Entitlement').AssignValue("Software Upgrades")
    Product.Attr("OTU_Entitlement").Access = AttributeAccess.ReadOnly
    Product.Attr("OTU_Contract").AssignValue(Product.Attr('SC_Service_Product').GetValue())
    Product.Attr("OTU_Contract").Access = AttributeAccess.ReadOnly
    msid_cont = Product.GetContainerByName('SC_Select_MSID_Cont')
    out_msid = Product.GetContainerByName('OTU_MSID')
    out_msid.Clear()
    SP = []
    for row in msid_cont.Rows:
        rowname=row['MSIDs']
        SP.append(rowname)
    for row1 in msid_cont.Rows:
        system_id = ""
        if "dvm system" in row1['System Name'].lower():
            system_id = "OTU_DVM_System_cpq"
        elif "ebr" in row1['System Name'].lower():
            system_id = "EBR_1_cpq"
        elif "experion" in row1['System Name'].lower():
            system_id = "Experion_PKS_cpq"
        elif "fdm" in row1['System Name'].lower():
            system_id = "FDM_cpq"
        elif "hs" in row1['System Name'].lower():
            system_id = "HS_cpq"
        elif "simulation" in row1['System Name'].lower():
            system_id = "Simulation_cpq"
        elif 'ots' in row1['System Name'].lower():
            system_id = "OTS_cpq"
        elif "e-server" in row1['System Name'].lower():
            system_id = "e-Server_cpq"
        elif "eop" in row1['System Name'].lower():
            system_id = "OTU_ExperionOffprocess_cpq"
        Hidden_row = out_msid.AddNewRow(system_id,True)
    	Hidden_row['MSIDs'] = row1['MSIDs']
    	Hidden_row['System Name'] = row1['System Name']
    	Hidden_row['System Number'] = row1['System Number']
        scope_summary_msid_cont = Product.GetContainerByName('SC_SESP Models')
        out_msid_cont = Product.GetContainerByName('OTU_System_Details')
        out_msid_cont.Clear()
        SP = []
        for row in out_msid_cont.Rows:
            rowname=row['MSID']
            SP.append(rowname)
            Hidden_row = out_msid_cont.AddNewRow(True)
            Hidden_row['MSID'] = row1['MSIDs']
            Hidden_row['System Number'] = row1['System_Number']
            Hidden_row['System'] = row1['System_Name']
            Hidden_row['Models'] = row1['Model#']
            Hidden_row['Description'] = row1['Description']
            Hidden_row['Qty'] = row1['Qty']
            Hidden_row['Unit List price'] = row1['List Price']
            Hidden_row['Unit Cost price'] = row1['Unit Price']