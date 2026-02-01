currentTab = arg.NameOfCurrentTab
system_id = ['OTU_DVM_System_cpq','EBR_1_cpq','Experion_PKS_cpq','FDM_cpq','HS_cpq','Simulation_cpq','OTS_cpq','e-Server_cpq','OTU_ExperionOffprocess_cpq','TPN_System_cpq']
otu_msid = Product.GetContainerByName("OTU_MSID")
if currentTab == 'OTU':
    Product.Attr('OTU_ServiceProduct').AssignValue("Software Upgrades")
    Product.Attr("OTU_ServiceProduct").Access = AttributeAccess.ReadOnly
    Product.Attr('OTU_Entitlement').AssignValue("Software Upgrades")
    Product.Attr("OTU_Entitlement").Access = AttributeAccess.ReadOnly
    Product.Attr("OTU_Contract").AssignValue(Product.Attr('SC_Service_Product').GetValue())
    Product.Attr("OTU_Contract").Access = AttributeAccess.ReadOnly
    if otu_msid.Rows.Count == 0:
        for i in system_id:
            if 'dvm' in i.lower():
                row = otu_msid.AddNewRow(i,True)
                row['MSIDs'] = 'M15984-EX01'
                row['System Name'] = "DVM System"
                row['System Number'] = "0"
            elif 'ebr' in i.lower():
                row = otu_msid.AddNewRow(i,True)
                row['MSIDs'] = 'M15984-EX01'
                row['System Name'] = "EBR"
                row['System Number'] = "0"
            elif 'experion' in i.lower():
                row = otu_msid.AddNewRow(i,True)
                row['MSIDs'] = 'M15984-EX01'
                row['System Name'] = "Experion PKS"
                row['System Number'] = "0"
            elif 'fdm' in i.lower():
                row = otu_msid.AddNewRow(i,True)
                row['MSIDs'] = 'M15984-EX01'
                row['System Name'] = "FDM"
                row['System Number'] = "0"
            elif 'hs' in i.lower():
                row = otu_msid.AddNewRow(i,True)
                row['MSIDs'] = 'M15984-EX01'
                row['System Name'] = "HS"
                row['System Number'] = "0"
            elif 'simulation' in i.lower():
                row = otu_msid.AddNewRow(i,True)
                row['MSIDs'] = 'M15984-EX01'
                row['System Name'] = "Simulation"
                row['System Number'] = "0"
            elif 'ots' in i.lower():
                row = otu_msid.AddNewRow(i,True)
                row['MSIDs'] = 'M15984-EX01'
                row['System Name'] = "OTS"
                row['System Number'] = "0"
            elif 'e-server' in i.lower():
                row = otu_msid.AddNewRow(i,True)
                row['MSIDs'] = 'M15984-EX01'
                row['System Name'] = "e-Server"
                row['System Number'] = "0"
            elif 'eop' in i.lower():
                row = otu_msid.AddNewRow(i,True)
                row['MSIDs'] = 'M15984-EX01'
                row['System Name'] = "Experion Off Process"
                row['System Number'] = "0"
            elif 'tpn' in i.lower():
                row = otu_msid.AddNewRow(i,True)
                row['MSIDs'] = 'M15984-EX01'
                row['System Name'] = "TPN System"
                row['System Number'] = "0"