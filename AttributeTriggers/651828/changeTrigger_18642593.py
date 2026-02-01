orionAttr = ["Flex Station Qty (0-60)","Orion_2P_Base_Unit_Left", "Orion Console Left Auxiliary Equipment Unit (0-40)","Orion_3P_Base_Unit_Left","Orion Console Display Size","Orion Console Display Devices (0-4)", "Orion Console Membrane KB Type","Orion_Console_Units_Config"]
station_required = Product.Attr('Orion Stations required').GetValue()

if station_required == "Yes":
	for attr in orionAttr:
		Product.AllowAttr(attr)
	#Product.AllowAttr("Flex Station Qty (0-60)")
	Product.Attr("Flex Station Qty (0-60)").AssignValue("0")
	Product.Attr("Orion_2P_Base_Unit_Left").AssignValue("0")
	Product.Attr("Orion Console Left Auxiliary Equipment Unit (0-40)").AssignValue("0")
	Product.Attr("Orion_3P_Base_Unit_Left").AssignValue("0")
	Product.Attr("Orion Console Display Devices (0-4)").AssignValue("1")
	Product.Attr("Orion Console Display Size").SelectDisplayValue("55 inch NTS")
	Product.Attr("Orion Console Membrane KB Type").SelectDisplayValue("None")
	Product.Attr("Orion Console 2Position Base Unit (0-20)").AssignValue(Product.Attr("Orion_2P_Base_Unit_Left").GetValue())
	Product.Attr("Orion Console 3Position Base Unit (0-20)").AssignValue(Product.Attr("Orion_3P_Base_Unit_Left").GetValue())
else:
	for attr in orionAttr:
		Product.DisallowAttr(attr)
	Product.DisallowAttr("Orion_Aux_Qty_Less_Stn_Qty")
	Product.DisallowAttr("Orion_Pos_Base_Less_Stn_Qty")
	Product.DisallowAttr("Flex Station Hardware Selection TPS")