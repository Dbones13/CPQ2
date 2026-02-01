DeskMonting_attr = ["DMS Flex Station Qty 0_60","DMS No of Displays 0_4", "DMS IKB or OEP"]
if Product.Attr('DMS Desk Mounting Stations required').GetValue() == "Yes":
	for attr in DeskMonting_attr:
		Product.AllowAttr(attr)
        Product.Attr('DMS IKB or OEP').SelectDisplayValue('None')
	Product.Attr("DMS Flex Station Qty 0_60").AssignValue("0")
	Product.Attr("DMS No of Displays 0_4").AssignValue("1")
else:
	for attr in DeskMonting_attr:
		Product.DisallowAttr(attr)
	Product.DisallowAttr("DMS Flex Station Hardware Selection")