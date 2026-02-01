def hideAttr(attrList):
	for attr in attrList:
		Product.Attr(attr).Access = AttributeAccess.Hidden

Product.Attr('Terminal_Blank_Experion_Server_(ESV)').Access = AttributeAccess.ReadOnly
if Quote.GetCustomField('isR2QRequest').Content == 'Yes':
	r2q_hideList = ['Terminal_TM_Test_System_required?', 'Terminal_Media_kit_required', 'Terminal_Experion_Client_PC', 'Terminal_FTE_Switch', 'Terminal_Blank_Experion_Server_(ESV)', 'Terminal_Experion_Server_Hardware', 'Terminal_Additional_Hard_Drive', 'Terminal_Additional_Memory', 'Terminal_Optional_DVD', 'Terminal_Display_Required', 'Terminal_Trackball', 'Terminal_Cabinet_Mounting_Type', 'Terminal_Ges_Location_Labour', 'Terminal_TM_System_Complexity', 'Terminal_Feature_Type', 'Terminal_Number_of_Days_per_Design_Review', 'Terminal_Number_of_Reviews', 'Terminal_Number_of_Days_for_TM_FAT', 'Terminal_Number_of_Engineer_for_FAT', 'Terminal_Number_of_Days_for_TM_SAT', 'Terminal_Number_of_Engineer_for_SAT', 'Terminal_No_of_Reports_with_Simple_Changes', 'Terminal_No_of_Reports_with_Complex_Changes', 'Terminal_Number_of_New_Simple_Reports', 'Terminal_Number_of_New_Moderate_Reports', 'Terminal_Number_of_New_Complex_Reports', 'Terminal_Number_of_Simple_Screens_for_new_UI', 'Terminal_Number_of_Moderate_Screens_for_new_UI', 'Terminal_Number_of_Complex_Screens_for_new_UI']
	hideAttr(r2q_hideList)
	#Trace.Write('hide attr at final-->')
	if Product.Attr('Terminal_SAP_ERP_BSI_Interface_required?').GetValue() == 'Yes' and Product.GetContainerByName('Terminal_SAP_ERP_BSI_Interface_Scope').Rows.Count == 0:
		Workflow_Container = Product.GetContainerByName("Terminal_SAP_ERP_BSI_Interface_Scope")
		addrow = Workflow_Container.AddNewRow(False)
		for row in Workflow_Container.Rows:
			row["Complexity"] = 'Moderate'
			row.GetColumnByName('Complexity').SetAttributeValue("Moderate")
			row["Type"] = 'Standard'
			row.GetColumnByName('Type').SetAttributeValue("Standard") 
			row.GetColumnByName('Truck Road').ReferencingAttribute.SelectValue("Y")
			row.GetColumnByName('Rail Wagon').ReferencingAttribute.SelectValue("Y")
			row.GetColumnByName('Marine').ReferencingAttribute.SelectValue("Y")
			row.GetColumnByName('Pipeline').ReferencingAttribute.SelectValue("Y")
			row.Calculate()
	if Product.Attr('Terminal_Batch_Controller?').GetValue() == 'Honeywell':
		Workflow_Container = Product.GetContainerByName("Terminal_Devices_Scope")
		for row in Workflow_Container.Rows:
			if row["Element"] =="BCU (MSC-L)":
				row["Complexity"] = 'Moderate'
				row.GetColumnByName('Complexity').SetAttributeValue("Moderate")
				row["Type"] = 'Standard'
				row.GetColumnByName('Type').SetAttributeValue("Standard") 
				row.GetColumnByName('Truck Road').ReferencingAttribute.SelectValue("Y")
				row.GetColumnByName('Rail Wagon').ReferencingAttribute.SelectValue("Y")
				row["Marine"] = 'Y'
				row.GetColumnByName('Marine').ReferencingAttribute.SelectValue("Y")
				row.GetColumnByName('Pipeline').ReferencingAttribute.SelectValue("Y")
				row.Calculate()
	get_val = Product.Attr("Terminal_Mode_of_Transport").Values
	for itr_val in get_val:
		Workflow_Container = Product.GetContainerByName("Terminal_Workflow_Scope")
		if itr_val.Display == "Truck loading/unloading" and itr_val.IsSelected == True:
			for row in Workflow_Container.Rows:
				if row["Element"] in ("Entry Gate","Reporting Office","Bay Que","BoL Office","Exit Gate","PC DET"):
					row["Complexity"] = 'Moderate'
					row.GetColumnByName('Complexity').SetAttributeValue("Moderate")
					row["Type"] = 'Standard'
					row.GetColumnByName('Type').SetAttributeValue("Standard") 
					row.GetColumnByName('Truck Road').ReferencingAttribute.SelectValue("Y")
					row.Calculate()
				if row["Element"] in ("Loading/Dispatch","Unloading/Receipt"):
					row["Complexity"] = 'Moderate'
					row.GetColumnByName('Complexity').SetAttributeValue("Moderate")
					row["Type"] = 'Standard'
					row.GetColumnByName('Type').SetAttributeValue("Standard") 
					row.GetColumnByName('Truck Road').ReferencingAttribute.SelectValue("Y")
					row.GetColumnByName('Rail Wagon').ReferencingAttribute.SelectValue("Y")
					row.GetColumnByName('Marine').ReferencingAttribute.SelectValue("Y")
					row.GetColumnByName('Pipeline').ReferencingAttribute.SelectValue("Y")
					row.Calculate()
				if row["Element"] in ('Weigh Bridge (IN)','Weigh Bridge (OUT)') and Product.Attr('Terminal_Weighbridge_Interface_required?').GetValue() == 'Yes':
					row["Complexity"] = 'Moderate'
					row.GetColumnByName('Complexity').SetAttributeValue("Moderate")
					row["Type"] = 'Standard'
					row.GetColumnByName('Type').SetAttributeValue("Standard") 
					row.GetColumnByName('Truck Road').ReferencingAttribute.SelectValue("Y")
					row.Calculate()
				if row["Element"] =='Mercury Terminal':
					row.GetColumnByName('Truck Road').ReferencingAttribute.SelectValue("N")
					row["Complexity"] = 'Moderate'
					row.GetColumnByName('Complexity').SetAttributeValue("Moderate")
					row["Type"] = 'Standard'
					row.GetColumnByName('Type').SetAttributeValue("Standard")
					row.Calculate()