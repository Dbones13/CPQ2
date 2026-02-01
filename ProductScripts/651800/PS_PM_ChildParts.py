if Product.Attr('R2QRequest').GetValue() != 'Yes':
	def getFloat(Var):
		if Var:
			return float(Var)
		return 0

	def lineItemContainer(Product,final_activities,Part_Con):
		PMSummary = Product.GetContainerByName(Part_Con)
		
		updated_item_list_dict = {}
		
		for part_row in PMSummary.Rows:
			updated_item_list_dict[part_row['PartNumber']] = int(float(part_row['Final Quantity']))
		
		delete_list = []
		
		for row in final_activities.Rows:
			part_number = row.Product.PartNumber
			if part_number in updated_item_list_dict.keys() and updated_item_list_dict[part_number] >0:
				row.Product.Attr("ItemQuantity").AssignValue(str(updated_item_list_dict[part_number]))
				row.ApplyProductChanges()            
				updated_item_list_dict.pop(part_number, None)
			else:
				delete_list.append(row.RowIndex)

		if delete_list:
			for row_index in sorted(delete_list, reverse=True):
				final_activities.DeleteRow(row_index)

		if updated_item_list_dict:
			for part_number,final_quantity in updated_item_list_dict.items():
				if final_quantity>0:
					newRow = final_activities.AddNewRow(part_number, False)
					newRow.Product.Attr("ItemQuantity").AssignValue(str(final_quantity))
					newRow.ApplyProductChanges()

	isPojectManagement = False
	for pm_data in Product.GetContainerByName('Cyber_Labor_Project_Management').Rows:
		if pm_data['Final_Hrs'] != '':
			if float(pm_data['Final_Hrs']) > 0:
				isPojectManagement = True
				break

	isgeneric = False
	for row in Product.GetContainerByName('Generic_System_Activities').Rows:
		if row['Edit Hours'] != '':
			if float(row['Edit Hours']) > 0:
				isgeneric = True
				break

	delrow_index = 0
	SelectedProducts = Product.GetContainerByName('Cyber Configurations')
	for data in SelectedProducts.Rows:
		if data["Part Desc"] =='Project Management' and isPojectManagement:
			Trace.Write('Proj Management')
			final_activities = data.Product.GetContainerByName('Final_Activities')
			lineItemContainer(Product,final_activities,'MSID_PM_Added_Parts_Common_Container')
			final_activities.Calculate()
			data.Product.ApplyRules()
			data.ApplyProductChanges()
		elif data["Part Desc"] =='Cyber Generic System' and isgeneric:
			Trace.Write('Cyber Generic System')
			final_activities = data.Product.GetContainerByName('Final_Activities')
			lineItemContainer(Product,final_activities,'Generic_System_PartsSummary')
			final_activities.Calculate()
			data.Product.ApplyRules()
			data.ApplyProductChanges()
		elif data["Part Desc"] =='Project Management':
			delrow_index = data.RowIndex

	if delrow_index != 0:
		SelectedProducts.DeleteRow(delrow_index)