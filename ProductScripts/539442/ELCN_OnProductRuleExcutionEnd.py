contObj = Product.GetContainerByName('ELCN_Upgrade_New_ELCN_Nodes')
noofGateways = 0
for row in contObj.Rows:
    networkGateways = 0 if row['ELCN_Qty_of_Network_Gateways'] == '' else float(row['ELCN_Qty_of_Network_Gateways'])
    noofGateways += networkGateways

if noofGateways > 0 and not Product.Attr('ELCN_Select_Switch_configuration_required').Allowed:
    Product.AllowAttr('ELCN_Select_Switch_configuration_required')
elif noofGateways <= 0:
    Product.DisallowAttr('ELCN_Select_Switch_configuration_required')
    Product.DisallowAttr('ATT_ELCN_Qty_of_NGs_more_than_100mts')
    Product.DisallowAttr('ELCN_Select_type_of_fiber_optic_switch')