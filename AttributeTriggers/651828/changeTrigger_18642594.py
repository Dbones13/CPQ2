station_qty = Product.Attr('Flex Station Qty (0-60)').GetValue() if Product.Attr('Flex Station Qty (0-60)').GetValue() else 0
if int(station_qty) > 0:
	Product.AllowAttr('Flex Station Hardware Selection TPS')
else:
	Product.DisallowAttr('Flex Station Hardware Selection TPS')
Aux_eqp = int(Product.Attr("Orion Console Left Auxiliary Equipment Unit (0-40)").GetValue()) if Product.Attr("Orion Console Left Auxiliary Equipment Unit (0-40)").GetValue() else 0
Flex_qty = int(Product.Attr("Flex Station Qty (0-60)").GetValue()) if Product.Attr("Flex Station Qty (0-60)").GetValue() else 0
Pbase_unit_2 = int(Product.Attr("Orion Console 2Position Base Unit (0-20)").GetValue()) if Product.Attr("Orion Console 2Position Base Unit (0-20)").GetValue() else 0
Pbase_unit_3 = int(Product.Attr("Orion Console 3Position Base Unit (0-20)").GetValue()) if Product.Attr("Orion Console 3Position Base Unit (0-20)").GetValue() else 0

if (3*Aux_eqp) < Flex_qty:
	Product.AllowAttr("Orion_Aux_Qty_Less_Stn_Qty")
else:
	Product.DisallowAttr("Orion_Aux_Qty_Less_Stn_Qty")
if ((2* Pbase_unit_2)+(3* Pbase_unit_3)) < Flex_qty:
	Product.AllowAttr("Orion_Pos_Base_Less_Stn_Qty")
else:
	Product.DisallowAttr("Orion_Pos_Base_Less_Stn_Qty")