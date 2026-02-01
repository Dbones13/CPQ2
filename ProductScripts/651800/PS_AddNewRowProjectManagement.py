if Product.Attr('R2QRequest').GetValue() != 'Yes':
	msid_scope = Product.Attr('CYBER_Scope_Choices').GetValue()
	subprd_container = Product.GetContainerByName('Cyber Configurations')
	isPMavail = False
	isPojectManagement = False

	for pm_data in Product.GetContainerByName('Cyber_Labor_Project_Management').Rows:
		if pm_data['Final_Hrs'] != '':
			if float(pm_data['Final_Hrs']) > 0:
				isPojectManagement = True
				break

	for row in subprd_container.Rows:
		if row['Part Desc'] == 'Project Management':
			isPMavail = True

	if msid_scope in ['LABOR','HW/SW/LABOR'] and subprd_container.Rows.Count > 0 and not isPMavail and isPojectManagement:
		newRow = subprd_container.AddNewRow('Project_Management_cpq')
		newRow['Part Desc'] = 'Project Management'
	elif subprd_container.Rows.Count == 1 and isPMavail:
		subprd_container.Rows.Clear()