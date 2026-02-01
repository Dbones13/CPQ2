#To update the visibitity of common labor input section
'''scope = Product.Attr('AR_HCI_SCOPE').GetValue()
if scope == "Software":
	Trace.Write('REENDsw-')
	Product.Attr("Header_02_open").Access = AttributeAccess.Hidden
	Product.Attr("ATTCON_02_open").Access = AttributeAccess.Hidden
	Product.Attr("AR_HCI_GES Participation %").Access = AttributeAccess.Hidden
	Product.Attr("AR_HCI_GES Location").Access = AttributeAccess.Hidden
	Product.Attr("R2Q_Alternate_Execution_Country ").Access = AttributeAccess.Hidden
	Product.Attr("ATTCON_02_close").Access = AttributeAccess.Hidden
	Product.Attr("Header_02_close").Access = AttributeAccess.Hidden
elif scope == "Software + Labor":
	Trace.Write('REENDsw+lab-')
	Product.Attr("Header_02_open").Access = AttributeAccess.Editable
	Product.Attr("ATTCON_02_open").Access = AttributeAccess.Editable
	Product.Attr("AR_HCI_GES Participation %").Access = AttributeAccess.Editable
	Product.Attr("AR_HCI_GES Location").Access = AttributeAccess.Editable
	Product.Attr("R2Q_Alternate_Execution_Country ").Access = AttributeAccess.Editable
	Product.Attr("ATTCON_02_close").Access = AttributeAccess.Editable
	Product.Attr("Header_02_close").Access = AttributeAccess.Editable'''
#END
subprd = Product.GetContainerByName('AR_HCI_SUBPRD')
Trace.Write('rows count '+str(subprd.Rows.Count))
if subprd.Rows.Count>1:
	row=subprd.Rows[0]
	edm = row.Product.Attributes.GetByName('AR_Collected_tags').GetValue()
	lab = subprd.Rows[1].Product.Attributes.GetByName('AR_Collected_tags').GetValue()
	Trace.Write('-row  bfe- '+str([edm,lab]))
	if edm == '' or edm != lab:
		row.Product.Attributes.GetByName('AR_Collected_tags').AssignValue(lab)
		#to select the base systen size in EDM product
		tags_option = {'1000':'A 1,000 Tags','2500':'B 2,500 Tags','5000':'C 5,000 Tags', '7500':'D 7,500 Tags', '10000':'E 10,000 Tags', '12500':'F 12,500 Tags', '15000':'G 15,000 Tags', '20000':'H 20,000 Tags', '25000':'J 25,000 Tags', '50000':'K 50,000 Tags', '75000':'L 75,000 Tags', '100000':'M 100,000 Tags', '250000':'N 250,000 Tags', '500000':'P 500,000 Tags', '750000':'Q 750,000 Tags', '1000000':'R 1,000,000 Tags', '1500000':'S 1,500,000 Tags', '2000000':'T 2,000,000 Tags'}
		Trace.Write('q---'+str(tags_option.keys()))
		tags_option_int = [int(tag) for tag in tags_option.keys()]

		if lab != '':
			tag_int = int(lab)
			nearest_highest = [tag for tag in tags_option_int if tag >= tag_int]
			nearest_highest_tag = min(nearest_highest) if nearest_highest else ''
			Trace.Write('1---'+str([nearest_highest,nearest_highest_tag]))
		else:
			nearest_highest_tag = ''

		Final_collected_tag = tags_option.get(str(nearest_highest_tag),'A 1,000 Tags')
		Trace.Write('fFinal_collected_tag--'+str([Final_collected_tag,type(Final_collected_tag)]))
		subprd.Rows[0].Product.Attributes.GetByName('HCI_PHD_Base_System_Size').SelectDisplayValue(Final_collected_tag)
		#to select the base systen size in EDM product