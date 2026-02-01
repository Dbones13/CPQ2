def hideAttr(attrList):
	for attr in attrList:
		Product.Attr(attr).Access = AttributeAccess.Hidden

def hideContainerColumns(contColumnList):
	for contColumn in contColumnList:
		for col in contColumnList[contColumn]:
			TagParserProduct.ParseString('<*CTX( Container({0}).Column({1}).SetPermission(Hidden) )*>'.format(contColumn,col))

nonR2QContColumn = {"ELCN_Basic_Information": ["ELCN_Additional_Switches_needed", "ELCN_Qty_of_Additional_Switches"]}

nonR2QAttr = ["ATT_ELCN_Additional_hours","ELCN_Cabinet_Depth_Size","ELCN_Cabinet_Door_Type","ELCN_Cabinet_Keylock_Type","ELCN_Cabinet_Hinge_Type","ELCN_Cabinet_Thermostat_Required","ELCN_Cabinet_Base_Required","ELCN_Cabinet_Color","ELCN_Power_Supply_Voltage"]

isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content =='Yes' else False
if isR2Qquote:
	Product.Attr('R2QRequest').AssignValue('Yes')
	Product.Attr("R2Q_QuoteNumber").AssignValue(str(Quote.CompositeNumber))
	cont = Product.GetContainerByName('ELCN_Basic_Information').Rows
	for i in cont:
		if i['ELCN_Type_of_Cabinet_where_the_ELCN_Bridge'] == 'In New Server Cabinet':
			Product.Attr('ELCN_Cabinet_Depth_Size').SelectDisplayValue('800 cm')
			Product.Attr('ELCN_Power_Supply_Voltage').SelectDisplayValue('120V, 60 Hz')
			Product.Attr('ELCN_Cabinet_Door_Type').SelectDisplayValue('Standard')
			Product.Attr('ELCN_Cabinet_Keylock_Type').SelectDisplayValue('Standard')
			Product.Attr('ELCN_Cabinet_Hinge_Type').SelectDisplayValue('130 Degrees')
			Product.Attr('ELCN_Cabinet_Thermostat_Required').SelectDisplayValue('No')
			Product.Attr('ELCN_Cabinet_Base_Required').SelectDisplayValue('No')
			Product.Attr('ELCN_Cabinet_Color').SelectDisplayValue('Gray-RAL7035')
	hideContainerColumns(nonR2QContColumn)
	hideAttr(nonR2QAttr)