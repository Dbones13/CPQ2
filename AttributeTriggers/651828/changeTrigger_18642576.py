DeskAttr = ["Server Node Type_desk","Desk _Mount_Server"]
rackAttr = ["Rack_Mount_Server","Server_NodeType"]
if Product.Attr('Server Mounting').GetValue() == "Cabinet":
	for attr in rackAttr:
		Product.AllowAttr(attr)
	for attr in DeskAttr:
		Product.DisallowAttr(attr)
	Product.Attr("Server_NodeType").SelectDisplayValue("SVR_STD_DELL_Rack_RAID1")
else:
	for attr in DeskAttr:
		Product.AllowAttr(attr)
	for attr in rackAttr:
		Product.DisallowAttr(attr)
	Product.Attr("Server Node Type_desk").SelectDisplayValue("SVR_STD_DELL_Tower_RAID1")
	#Log.Info("changeServer Node Type_deskwwwwwwwwwwwww")