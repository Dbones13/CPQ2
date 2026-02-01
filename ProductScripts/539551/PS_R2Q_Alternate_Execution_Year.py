if Quote.GetCustomField("isR2QRequest").Content == 'Yes':
	from GS_R2Q_Product_Attribute_ContColms import MigrationProductsAttributesContainerColumns as msidCont

	def alternateExecutionYear():
		msidProduct = Product.GetContainerByName('CONT_Migration_MSID_Selection').Rows
		execution_year = Quote.GetCustomField('R2Q_PRJT_Execution_Year').Content
		for prd in msidProduct:
			for cont in msidCont.msidNewContainers:
				for row in prd.Product.GetContainerByName(cont).Rows:
					if row['FO_Eng'] != '':
						row['Execution_Year'] = execution_year

	alternateExecutionYear()
	Session['R2Q_CompositeNumber'] = Quote.CompositeNumber