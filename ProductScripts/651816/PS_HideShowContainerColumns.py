UOC_RemoteGroup_Cont = Product.GetContainerByName('UOC_RemoteGroup_Cont')

if UOC_RemoteGroup_Cont.Rows.Count > 0:
	for row in UOC_RemoteGroup_Cont.Rows:
		UOC_RG_Name = row.Product.Attr('UOC_RG_Name').GetValue()
		if str(row["Remote Group Name"]) != UOC_RG_Name:
			row.Product.Attr('UOC_RG_Name').AssignValue(str(row["Remote Group Name"]))
			row.ApplyProductChanges()
			row.Calculate()
for i in Product.GetContainerByName('UOC_CG_Controller_Rack_Cont').Rows:
    if i['UOC_Controller_Type'] == "Redundant":
        Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Editable) )*>'.format("UOC_CG_Controller_Rack_Cont","UOC_Redundant_Controller_Physical_Seperation"))
    else:
        Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Hidden) )*>'.format('UOC_CG_Controller_Rack_Cont','UOC_Redundant_Controller_Physical_Seperation'))
hidden = True if TagParserProduct.ParseString('<*CTX( Container(UOC_CG_Controller_Rack_Cont).Column(UOC_Redundant_Controller_Physical_Seperation).GetPermission )*>') == 'Hidden' else False
if  hidden:
    Product.GetContainerByName('UOC_CG_Controller_Rack_Cont').Rows[0].SetColumnValue('UOC_Redundant_Controller_Physical_Seperation', "No")