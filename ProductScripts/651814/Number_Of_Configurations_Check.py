no_of_configurations = 0
first_edit = Product.Attr("HCI_EDM_First_Edit_Check").GetValue()
if first_edit == "":
	for i in Quote.MainItems:
		if i.PartNumber == 'HCI_EDM':
			no_of_configurations = no_of_configurations+1
	total_config = no_of_configurations+1
	Product.Attr('HCI_EDM_First_Edit_Check').AssignValue('True')
	Product.Attr('Number_Of_Configurations_EDM').AssignValue(str(total_config))
	first_edit = Product.Attr("HCI_EDM_First_Edit_Check").GetValue()
	no_of_config = Product.Attr("Number_Of_Configurations_EDM").GetValue()
	Trace.Write("first_edit--->"+str(first_edit)+"No_of_config"+str(no_of_config))
Log.Info("first_edit--->"+str(first_edit)+"No_of_config"+str(no_of_config))