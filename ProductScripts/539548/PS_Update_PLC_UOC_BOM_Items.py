dict_attr = {}
for i in Product.GetContainerByName("CONT_MSID_SUBPRD").Rows:
	if i['Selected_Products'] =="3rd Party PLC to ControlEdge PLC/UOC":
		attr=i.Product.Attr('PLC_UOC_BOM_Items').Values
		for k in attr:
			if int(k.Quantity) > 0:
				dict_attr[str(k.Display)] = str(k.Quantity)


if len(dict_attr) > 0:
	pvs=Product.Attr('PLC_UOC_BOM_Items').Values
	val = dict_attr.keys()
	for av in pvs:
		if av.Display in val:
			av.IsSelected=True
			av.Quantity=int(dict_attr[av.Display])
		else:
			av.IsSelected=False
			av.Quantity= 0

"""Exp_Ent_Grp_Part_Summary = Product.Attr('PLC_UOC_BOM_Items').GetValue()
if Exp_Ent_Grp_Part_Summary != '':
	Exp_Ent_Grp_Part_Summary_Replace = "'"+Exp_Ent_Grp_Part_Summary.replace(', ',"' as PartNumber UNION SELECT '")+"'"
	Exp_Ent_Grp_Part_Summary_Query= 'select {} as PartNumber'.format(Exp_Ent_Grp_Part_Summary_Replace)
	Product.GetContainerByName('MSID_Third_Party_PLC_Added_Parts_Common_Container').LoadFromDatabase(Exp_Ent_Grp_Part_Summary_Query, 'PartNumber')


for i in Product.GetContainerByName("MSID_Third_Party_PLC_Added_Parts_Common_Container").Rows:
	if str(i['Quantity']) in ('0', ''):
		i['Quantity'] = str(dict_attr[i['PartNumber']])
		i['Final Quantity'] = str(i['Quantity'])"""