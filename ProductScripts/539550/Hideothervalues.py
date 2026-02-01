if Product.Attr('isProductLoaded').GetValue() == 'True':
	import datetime
	specific_location = {'GESChina': ['HPS_GES_P350B_CN', 'HPS_GES_P350F_CN'], 'GESIndia': ['HPS_GES_P350B_IN', 'HPS_GES_P350F_IN'],'GESRomania':['HPS_GES_P350B_RO', 'HPS_GES_P350F_RO'],'GESUzbekistan':['HPS_GES_P350B_UZ','HPS_GES_P350F_UZ'],'GESEgypt':['HPS_GES_P350B_EG','HPS_GES_P350F_EG']}

	def disallow(location, dropdownlist):
		if location:
			for i in dropdownlist:
				if i.ValueCode in location:
					i.Allowed = True
				elif i.ValueCode not in location:
					i.Allowed = False

	remove_deliverables = ['PMD Engineering Plan', 'PMD Procure Materials & Services', 'PMD Customer Training', 'PMD Project Close Out Report']
	gesloc = Product.GetContainerByName('PMD_Labour_Details').Rows[0].GetColumnByName('PMD_Ges_Location')
	Trace.Write(gesloc.Value)
	if gesloc.Value != "None":
		deliverables = Product.GetContainerByName('PMD Engineering Labor Container')
		for row in deliverables.Rows:
			if row['Deliverable'] not in remove_deliverables or gesloc.Value != "None":
				location = row.GetColumnByName('GES Eng')
				value_list = location.ReferencingAttribute.Values
				disallow(specific_location[gesloc.Value], value_list)
		deliverables.Calculate()
        custom_deliverables = Product.GetContainerByName('PMD Labor Additional Custom Deliverable')
        for deliverable in custom_deliverables.Rows:
            if gesloc.Value != "None":
                deliverable_location = deliverable.GetColumnByName('GES Eng')
                dropdown_values = deliverable_location.ReferencingAttribute.Values
                disallow(specific_location[gesloc.Value], dropdown_values)
        custom_deliverables.Calculate()