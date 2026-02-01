category = Product.Attr('R2Q Select Category').GetValue()
if category == 'TA System':
	Product.Attr('R2Q_Project_Questions_TAS_Cont').Access = AttributeAccess.Editable
	if Product.Attr('R2Q_Type_of_TAS_System').GetValue() == "":
		Quote.GetCustomField("R2Q_Type_of_TAS_System").Content = 'Non-Red'
	Quote.GetCustomField("R2Q_Type_of_TAS_System").Content = Product.Attr('R2Q_Type_of_TAS_System').GetValue()
else:
	Product.Attr('R2Q_Project_Questions_TAS_Cont').Access = AttributeAccess.Hidden

fut_attr = Product.GetContainerByName('R2Q_Project_Questions_Cont')
for rowENB in fut_attr.Rows:
	attribute = rowENB.GetColumnByName("R2Q_PRJT_Proposal Language").ReferencingAttribute
	for value in attribute.Values:
		if category == 'TA System':
			#Trace.Write('aaa' + str(value.Display))
			if value.Display in ('French','Chinese','German','Korean','Portuguese'):
				value.Allowed = False
		else:
			#Trace.Write('aaa' + str(value.Display))
			if value.Display in ('English','Spanish','French','Chinese','German'):
				value.Allowed = True
	rowENB.ApplyProductChanges()
	rowENB.Calculate()