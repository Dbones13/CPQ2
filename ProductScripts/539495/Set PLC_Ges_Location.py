#To set the column value 'PLC_Ges_Location'
Checkproduct = Product.ParseString('<*CTX(Product.RootProduct.PartNumber)*>')
gesLocation = Product.Attr('PLC_Ges_Location').GetValue()
defaultLocation = Product.Attr('Default_Ges_Location').GetValue()
gesMapping = {'GES India':'GESIndia','GES China':'GESChina','GES Romania':'GESRomania','GES Uzbekistan':'GESUzbekistan','None':'None'}

Log.Info("GES attribute value: " + str(gesLocation))
if Quote.GetCustomField('R2QFlag').Content == "Yes" and Checkproduct == "PRJT":
	if defaultLocation == 'None' or defaultLocation == '':
		Product.Attr('Default_Ges_Location').SelectValue(gesMapping.get(gesLocation))
    	Log.Info("Default_Ges_Location---"+ str(Product.Attr('Default_Ges_Location').GetValue()))


'''if Product.Attr("CE_Scope_Choices").GetValue() == 'HW/SW':
    Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Hidden) )*>'.format('PLC_Labour_Details','PLC_Process_Type'))
elif Product.Attr("CE_Scope_Choices").GetValue() == 'HW/SW + LABOR':
    Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Editable) )*>'.format('PLC_Labour_Details','PLC_Process_Type'))'''

if Checkproduct == "PRJT":
    Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Hidden) )*>'.format('PLC_Labour_Details','PLC_Process_Type'))
else:
    Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Hidden) )*>'.format('PLC_Labour_Details','PLC_Number_of_Sequences'))
    Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Hidden) )*>'.format('PLC_Labour_Details','PLC_3rd_Party_Communication_Signals'))
    if Product.Attr("CE_Scope_Choices").GetValue() == 'HW/SW':
        Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Hidden) )*>'.format('PLC_Labour_Details','PLC_Process_Type'))
    elif Product.Attr("CE_Scope_Choices").GetValue() == 'HW/SW + LABOR':
        Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Editable) )*>'.format('PLC_Labour_Details','PLC_Process_Type'))