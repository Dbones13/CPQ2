if Quote.GetCustomField("isR2QRequest").Content == 'Yes':
	Trace.Write("insidether2qrequest")
	from GS_R2Q_Product_Attribute_ContColms import MigrationProductsAttributesContainerColumns as msidCont

	def get_float_value(cont, col):
		val = 0.0
		if cont[col]:
			val = float(cont[col])
		return val

	def alternateCountry():
		msidProduct = Product.GetContainerByName('CONT_Migration_MSID_Selection').Rows
		alternate_country = Quote.GetCustomField('R2Q_Alternate_Execution_Country').Content
		#execution_year = Quote.GetCustomField('R2Q_PRJT_Execution_Year').Content
		for prd in msidProduct:
			for cont in msidCont.msidNewContainers:
				for row in prd.Product.GetContainerByName(cont).Rows:
					if row['FO_Eng'] != '':
						#row['Execution_Year'] = execution_year
						gesSplit = get_float_value(row, 'GES_Eng_Percentage_Split')
						regSplit = get_float_value(row, 'FO_Eng_Percentage_Split')
						gesCostValue = get_float_value(row, 'GES_Regional_Cost')
						regCostValue = get_float_value(row, 'Regional_Cost')
						final_hrs_value = get_float_value(row, 'Final_Hrs')
						#if cont == 'MSID_Labor_Project_Management':
							#Log.Info('row["Execution_Year"] = ' + str(row['Execution_Year']) + ' gesSplit = ' + str(abs(gesSplit)) + ' gesCostValue = ' + str(abs(gesCostValue)) + ' regSplit = ' + str(abs(regSplit)) + ' regCostValue = ' + str(abs(regCostValue)) + ' final_hrs_value = ' + str(abs(final_hrs_value)))
						if abs(final_hrs_value) > 1e-9 and ((abs(gesSplit) > 1e-9 and abs(gesCostValue) < 1e-9) or (abs(regSplit) > 1e-9 and abs(regCostValue) < 1e-9)):
							Trace.Write("finalhrs"+str(final_hrs_value)+"gesSplit"+str(gesSplit)+"gesCostValue"+str(gesCostValue)+"regSplit"+str(regSplit)+"regCostValue"+str(regCostValue))
							#if cont == 'MSID_Labor_Project_Management':
								#Log.Info('Coming here')
							row['Execution_Country'] = alternate_country
							ScriptExecutor.Execute('R2Q_PS_PopulateGESCost')

	alternateCountry()
	Session['R2Q_CompositeNumber'] = Quote.CompositeNumber