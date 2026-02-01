#Trace.Write('aaaaa')
value = Product.Attr('CE_Scope_Choices').GetValue()
#Trace.Write('value ' + str(value))
addrow = Product.GetContainerByName('R2Q CE_System_Cont')
for row in addrow.Rows:
	if row.Product.Name == 'R2Q ControlEdge PLC System':
		row.Product.Attr('CE_Scope_Choices').SelectDisplayValue(value)
		if value == "HW/SW + LABOR":
			row.Product.Attr('PLC_Labour_Details').Access = AttributeAccess.Editable
		elif value == "HW/SW":
			row.Product.Attr('PLC_Labour_Details').Access = AttributeAccess.Hidden