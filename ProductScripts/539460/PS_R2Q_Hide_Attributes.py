if Quote.GetCustomField("isR2QRequest").Content =='Yes':
	Product.DisallowAttrValues('xPM_Select_the_migration_scenario','xPM to EHPM')