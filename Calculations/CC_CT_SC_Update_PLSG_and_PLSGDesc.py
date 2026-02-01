#CC_CT_SC_Update_PLSG_and_PLSGDesc
if Quote.GetCustomField('Quote Type').Content in ('Contract New','Contract Renewal'):
	plsgDict = dict()
	plsgDescDict = dict()
	result = SqlHelper.GetList("SELECT SC_Module, SAP_PL_PLSG as PLSG, SAP_PLSG_Description as PLSGDesc FROM SAP_PLSG_LOB_MAPPING WHERE SC_Module !='NULL'")
	if result:
		for row in result:
			if row.SC_Module not in plsgDict.keys():
				plsgDict[row.SC_Module] = row.PLSG
				plsgDescDict[row.SC_Module] = row.PLSGDesc
		for item in Quote.MainItems:
			if item.PartNumber in plsgDict.keys():
				item.QI_PLSG.Value 		= plsgDict.get(item.PartNumber, '')
				item.QI_PLSGDesc.Value 	= plsgDescDict.get(item.PartNumber, '')
        for i in Quote.Items:
            if len(list(i.AsMainItem.Children))==0:
                i.QI_PLLOB.Value = 'LSS'