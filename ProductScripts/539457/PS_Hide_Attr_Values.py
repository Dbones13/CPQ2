if Product.Name == "Virtualization System":
	tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
	allowed_count = 0
	expected_count = 4
	#condition to run the below script only on Labor Deliverables tab
	if 'Labor Deliverables' in tabs:
		def hideColumn(container,Column):
			Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Hidden) )*>'.format(container,Column))
			Product.ParseString('<*CTX( Container({}).Row(1).Column({}).Set() )*>'.format(container,Column))

		def visibleColumn(container,Column):
			Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Editable) )*>'.format(container,Column))
		col_lst = ["GES Eng","GES Eng % Split","GES_Unit_Regional_Cost","GES_Regional_Cost","GES_ListPrice","GES_WTW_Cost","GES_MPA_Price"]
		gesLocation = Product.Attr('Virtualization_Ges_Location').GetValue()
		if gesLocation == "None" or gesLocation == "":
			for col in col_lst:
				hideColumn("Virtualization_Labor_Deliverable",col)
				hideColumn("Virtualization_Additional_Custom_Deliverables",col)
			Product.DisallowAttr('Virtualization_Labor_GES_Perct')
			Product.DisallowAttr('Virtualization_Labor_GES_Additonal_Perct')
		else:
			for col in col_lst:
				visibleColumn("Virtualization_Labor_Deliverable",col)
				visibleColumn("Virtualization_Additional_Custom_Deliverables",col)
			Product.AllowAttr('Virtualization_Labor_GES_Perct')
			Product.AllowAttr('Virtualization_Labor_GES_Additonal_Perct')

		years_list = Product.Attr('Virtualization_Labor_Execution_Year').Values
		for year in years_list:
			allowed_count = allowed_count + 1 if year.Allowed else allowed_count
		#condition to run the below script only when the year attribute has more than the expected (4) items
		if allowed_count > expected_count:
			import datetime
			current_year = datetime.datetime.now().year
			#hide years which are less the current year or greater than current year + 4
			def hide_year(Product, current_year, attribute_name, expected_count, max_year ):
				years_list = Product.Attr(attribute_name).Values
				for year in years_list:
					if int(year.ValueCode) in range(current_year + 4, max_year):
						Product.DisallowAttrValues(attribute_name, year.ValueCode)
					elif int(year.ValueCode) < current_year:
						Product.DisallowAttrValues(attribute_name, year.ValueCode)

			max_year = 2037
			for attribute_name in ['Virtualization_Labor_Execution_Year', 'Virtualization_Labor_Execution_Year_adc']:
				hide_year(Product, current_year, attribute_name, expected_count, max_year)
				
		specific_location = {'GES China': ['HPS_GES_P350B_CN', 'HPS_GES_P350F_CN'], 'GES India': ['HPS_GES_P350B_IN', 'HPS_GES_P350F_IN'], 'GES Romania':['HPS_GES_P350B_RO', 'HPS_GES_P350F_RO'], 'GES Uzbekistan':['HPS_GES_P350B_UZ', 'HPS_GES_P350F_UZ'],'GES Egypt':['HPS_GES_P350B_EG', 'HPS_GES_P350F_EG']}
		def disallow(location, dropdownlist):
			if location:
				for i in dropdownlist:
					if i.ValueCode not in location:
						i.Allowed = False
					elif i.ValueCode in location:
						i.Allowed = True
		gesloc = Product.Attr('Virtualization_Ges_Location').SelectedValue.ValueCode
		if gesloc != "None" or gesloc != "":
			for cont in ['Virtualization_Labor_Deliverable','Virtualization_Additional_Custom_Deliverables']:
				deliverables = Product.GetContainerByName(cont)
				for row in deliverables.Rows:
					location = row.GetColumnByName('GES Eng')
					value_list = location.ReferencingAttribute.Values
					try:
						disallow(specific_location[gesloc], value_list)
					except:
						Trace.Write("error")
					row.Calculate()
				deliverables.Calculate()