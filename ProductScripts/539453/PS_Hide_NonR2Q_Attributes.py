def hideAttr(attrList):
    for attr in attrList:
        Product.Attr(attr).Access = AttributeAccess.Hidden
nonR2QAttr = ["Additional displays (0 to 999999)","Total Number of Displays"]
hideAttr(nonR2QAttr)

isR2QFlag = True if Quote.GetCustomField("R2QFlag").Content else False
if isR2QFlag:
	try:
		loc_dict = {"IN":"GES India","CN":"GES China","RO":"GES Romania","UZ":"GES Uzbekistan","None":"None","null":"None"}
		dictdata = eval(Quote.GetGlobal('R2Qdata'))
		if dictdata:
			attr_value = dictdata['R2Q_Project_Questions_Cont'][0][0]['GES_Location']
			geslocation = loc_dict.get(attr_value)
			Product.Attr('Experion_HS_Ges_Location_Labour').SelectDisplayValue(geslocation)
	except:
		Trace.Write("error")
