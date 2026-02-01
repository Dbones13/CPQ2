def laborcont_update(containerDict):
	exp_dict = ['Number of Operator Console Sections','Number of Server Types','Number of Station Types','Total Number of Displays','Number of Modbus Interfaces','Number of OPC Interfaces','Number of Fieldbus Devices','Number of Profibus Devices','Number of EtherNet IP Devices','Number of EtherNet IP Interface Cards','Number of Profibus Interface Cards','Number of Console Sections with Hardwired IO','Number of FTE Communities','Number of FTE Community Locations','Number of Locations with FTE Switches','Number of Types of Network Devices','Number of Modbus Interfaces Types','Number of Profibus Interface Types','Number of EtherNet IP Interface Types','Number of OPC Interface Types']
	for key, values in containerDict.items():
		#Trace.Write(key)
		if values and len(values) > 0 and key == 'R2Q CE_System_Cont':
			order_products = {"Experion":[]}
			for indx, selected_Product_order in enumerate(values[0]):
				if selected_Product_order['Selected_Products'] ==  'R2Q Experion Enterprise System':
					order_products["Experion"] = values[1][indx]

			if order_products["Experion"]:
				for attrname, attrvalue in order_products['Experion'].items():
					if attrname in exp_dict:
						Product.Attr(attrname).AssignValue(attrvalue) if Product.Attr(attrname).DisplayType != "DropDown" else Product.Attr(attrname).SelectDisplayValue(attrvalue)
	container = Product.GetContainerByName("Experion_Ent_Displays_Shapes_Faceplates")
	if container.Rows.Count > 0:
		for row in container.Rows:
			if row["Displays/Shapes/Faceplates"] == "Total Number of Displays":
				display = float(Product.Attr('Additional displays (0 to 999999)').GetValue() or 0) + float(Product.Attr('Total Number of Displays').GetValue() or 0)
				row["customer Data"] = str(display)
def delete_key_recursive(SelectedAttsData, key_to_delete):
	if isinstance(SelectedAttsData, dict):  # If the element is a dictionary
		if key_to_delete in SelectedAttsData:
			del SelectedAttsData[key_to_delete]
		for k, v in SelectedAttsData.items():
			delete_key_recursive(v, key_to_delete)
	elif isinstance(SelectedAttsData, list):  # If the element is a list
		for item in SelectedAttsData:
			delete_key_recursive(item, key_to_delete)

saveAction = Quote.GetCustomField("R2Q_Save").Content
isR2Qquote = True if Quote.GetCustomField("R2QFlag").Content else False
if isR2Qquote and saveAction != 'Save':
	QuoteId = Quote.CompositeNumber
	dictdata = eval(Quote.GetGlobal('R2Qdata'))
	if dictdata is not None and dictdata !='':
		attrdict = dictdata
		delete_key_recursive(attrdict, 'R2Q_CONFIGURATION')
		laborcont_update(attrdict)