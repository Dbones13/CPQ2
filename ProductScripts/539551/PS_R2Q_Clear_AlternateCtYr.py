if Quote.GetCustomField("isR2QRequest").Content == 'Yes':
	from GS_R2Q_Product_Attribute_ContColms import MigrationProductsAttributesContainerColumns as msidCont

	def clearFavoritesExecution():
		msidProduct = Product.GetContainerByName('CONT_Migration_MSID_Selection').Rows
		alternate_country = Quote.GetCustomField('R2Q_Alternate_Execution_Country').Content
		for prd in msidProduct:
			for cont in msidCont.msidNewContainers:
				prd.Product.GetContainerByName(cont).Rows.Clear()

	clearFavoritesExecution()