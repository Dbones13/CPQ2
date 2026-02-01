if Product.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows.Count > 0:
	label = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0]
	label.GetColumnByName('SM_Percent_Installed_Spare_IO').HeaderLabel = "Percent Installed Spare IOs (0-100%)"