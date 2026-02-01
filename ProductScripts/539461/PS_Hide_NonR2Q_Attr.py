isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
checkproduct= Product.ParseString('<*CTX(Product.RootProduct.PartNumber)*>')
if isR2Qquote and checkproduct == 'Migration':
    Product.Attr('R2QRequest').AssignValue('Yes')
    Product.Attr("R2Q_QuoteNumber").AssignValue(str(Quote.CompositeNumber))
    uoc_attributes_to_hide = [
        'UOC_Exp_PKS_software_release',
        'UOC_Shielded_Terminal_Strip',
        'UOC_IO_Filler_Module',
        'UOC_IO_Spare',
        'UOC_IO_Slot_Spare',
        'UOC_Cluster',
        'UOC_Starter_Kit',
        'UOC_Starter_ Kit_with_Experion_License'
    ]

    for attr in uoc_attributes_to_hide:
        Product.ParseString('<*CTX( Container({}).Column("{}").SetPermission({}) )*>'.format('UOC_Common_Questions_Cont', attr, 'Hidden'))
    if Product.GetContainerByName('UOC_Labor_Details').Rows.Count:
        Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName('UOC_Process_Type_Labour').SetAttributeValue('Continuous')
else:
    Product.Attr('R2QRequest').AssignValue('')


isR2QFlag = True if Quote.GetCustomField("R2QFlag").Content else False
if isR2QFlag:
	try:
		loc_dict = {"IN":"GES India","CN":"GES China","RO":"GES Romania","UZ":"GES Uzbekistan","None":"None","null":"None"}
		dictdata = eval(Quote.GetGlobal('R2Qdata'))
		if dictdata:
			attr_value = dictdata['R2Q_Project_Questions_Cont'][0][0]['GES_Location']
			geslocation = loc_dict.get(attr_value)
			cont = Product.GetContainerByName('UOC_Labor_Details')
			if cont.Rows.Count > 0:
				for row in cont.Rows:
					row.GetColumnByName('UOC_Ges_Location_Labour').SetAttributeValue(geslocation)
					row['UOC_Ges_Location_Labour'] = geslocation
	except:
		Trace.Write("error")