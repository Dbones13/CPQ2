if Quote.GetCustomField("isR2QRequest").Content == 'Yes':

	def clearFavoritesExecution():
		SelectedProducts = Product.GetContainerByName('Cyber Configurations')
		for row in SelectedProducts.Rows:
			Log.Info("--Part Desc--"+str(row['Part Desc']))
			if row['Part Desc'] not in ['Project Management','Cyber Generic System']:
				row.Product.GetContainerByName('Activities').Rows.Clear()
				row.Product.GetContainerByName('AR_Cyber_PartsSummary').Rows.Clear()
				row.Product.GetContainerByName('Final_Activities').Rows.Clear()

	clearFavoritesExecution()