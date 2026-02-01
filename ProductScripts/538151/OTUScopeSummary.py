currentTab = arg.NameOfCurrentTab
if currentTab == "Scope Summary":
	otu_scope_summary_cont = Product.GetContainerByName("OTUServiceProductsEntitlements")
	for i in range(0,1):
		row = otu_scope_summary_cont.AddNewRow(True)
		row['Service Product'] = 'Software Upgrades'
		row['Entitlement'] = 'Software Upgrades'
		row['Type'] = 'Mandatory'