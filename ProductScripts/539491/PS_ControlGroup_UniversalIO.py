isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
Checkproduct = Product.ParseString('<*CTX(Product.RootProduct.PartNumber)*>')
if isR2Qquote and  Checkproduct == "Migration":
    for attr_name in ("LSS_Cabinet_Color?","LSS_Cabinet_Color_Front_Access","LSS_Cabinet_Doors","LSS_Cabinet_Hinge_Type","LSS_Cabinet_Keylock_Type","LSS_Cabinet_Light_Required?","LSS_Cabinet_Thermostat_Required?","LSS_Front_only_Cabinet Doors","LSS_Front_only_Cabinet Hinge Type", "LSS_Front_only_Cabinet_Keylock_Type","LSS_Front_Only_Cabinet_Light_Required?","LSS_Front_only_Cabinet_Thermostat_Required?","LSS_Front_only_Power_Entry","LSS_Front_only_TDI_Power_Supply_Cable_Length","LSS_Power_Entry","LSS_TDI_Power_Supply_Cable_Length","Front_Access_Only","Front_and_Rear_Access","LSS_Cabinet_Base_Required?","LSS_Fan_Voltage","LSS_Front_only_Cabinet_Base_Required?","LSS_Front_Only_Fan_Voltage"):
        Product.DisallowAttr(attr_name)

plc_cont = Product.GetContainerByName('LSS_PLC_connection_transpose')

for row in plc_cont.Rows:
    controlGroup = row.Product.GetContainerByName('PLC_ControlGroup_Cont')
    universalIO = [[int(row1['PLC_UOC_labor_parameter_var_39']), int(row1['PLC_UOC_labor_parameter_var_40']), int(row1['PLC_UOC_labor_parameter_var_41']), int(row1['PLC_UOC_labor_parameter_var_42']), int(row1['PLC_UOC_labor_parameter_var_43'])] for row1 in controlGroup.Rows]
    row['PLC_UOC_labor_parameter_var_39'] = str(sum([i[0] for i in universalIO]))
    row.Product.Attr('PLC_UOC_labor_parameter_var_39').AssignValue(str(sum([i[0] for i in universalIO])))
    row['PLC_UOC_labor_parameter_var_40'] = str(sum([i[1] for i in universalIO]))
    row.Product.Attr('PLC_UOC_labor_parameter_var_40').AssignValue(str(sum([i[1] for i in universalIO])))
    row['PLC_UOC_labor_parameter_var_41'] = str(sum([i[2] for i in universalIO]))
    row.Product.Attr('PLC_UOC_labor_parameter_var_41').AssignValue(str(sum([i[2] for i in universalIO])))
    row['PLC_UOC_labor_parameter_var_42'] = str(sum([i[3] for i in universalIO]))
    row.Product.Attr('PLC_UOC_labor_parameter_var_42').AssignValue(str(sum([i[3] for i in universalIO])))
    row['PLC_UOC_labor_parameter_var_43'] = str(sum([i[4] for i in universalIO]))
    row.Product.Attr('PLC_UOC_labor_parameter_var_43').AssignValue(str(sum([i[4] for i in universalIO])))

bomQty = {'CC-C8DS01':0, 'CC-C8SS01':0, 'CC-CBDD01':0, '900R08-0300':0, '900R12-0300':0, '900R08R-0300':0, '900R12R-0300':0, '900U01-0100':0, '900ES1-100':0}
var_13 = var_15 = var_20 = var_22 = var_36 = 0
plc_cont = Product.GetContainerByName('LSS_PLC_connection_transpose')
for row in plc_cont.Rows:
    childProduct = row.Product
    controlGroup = childProduct.GetContainerByName('PLC_ControlGroup_Cont')
    for cg_row in controlGroup.Rows:
        controlGroupProduct = cg_row.Product
        plc_cont_rows = controlGroupProduct.GetContainerByName('PLC_CG_PartSummary_Cont')
        for row in plc_cont_rows.Rows:
            if row['CE_Part_Number'] in bomQty:
                bomQty[row['CE_Part_Number']] = bomQty[row['CE_Part_Number']] + int(row['CE_Final_Quantity'])
        comm_interface_cont = controlGroupProduct.GetContainerByName('PLC_CG_Comm_Interface_Cont')
        for row in comm_interface_cont.Rows:
            var_22 += float(row['PLC_CDA_Controllers']) + float(row['PLC_OPC_Servers']) + float(row['PLC_Modbus_Master']) + float(row['PLC_Modbus_Slaves']) + float(row['PLC_OPC_Clients'])

uoc_cont = Product.GetContainerByName('LSS_UOC_connection_transpose')
for row in uoc_cont.Rows:
    childProduct = row.Product
    controlGroup = childProduct.GetContainerByName('UOC_ControlGroup_Cont')
    for cg_row in controlGroup.Rows:
        controlGroupProduct = cg_row.Product
        plc_cont_rows = controlGroupProduct.GetContainerByName('UOC_CG_PartSummary_Cont')
        for row in plc_cont_rows.Rows:
            if row['CE_Part_Number'] in bomQty:
                bomQty[row['CE_Part_Number']] = bomQty[row['CE_Part_Number']] + int(row['CE_Final_Quantity'])

bomItems = Product.Attr('PLC_UOC_BOM_Items')
for val in bomItems.Values:
    if val.ValueCode in ['CC-C8DS01', 'CC-C8SS01', 'CC-CBDD01']:
        var_13 += val.Quantity
    elif val.ValueCode in ['900R08-0300', '900R12-0300', '900R08R-0300', '900R12R-0300']:
        var_15 += val.Quantity
    elif val.ValueCode == '900U01-0100':
        var_20 += val.Quantity
    elif val.ValueCode == '900ES1-100':
        var_36 += val.Quantity

var_13 += sum([bomQty[i] for i in bomQty if i in ['CC-C8DS01', 'CC-C8SS01', 'CC-CBDD01']])
var_15 += sum([bomQty[i] for i in bomQty if i in ['900R08-0300', '900R12-0300', '900R08R-0300', '900R12R-0300']])
var_20 += sum([bomQty[i] for i in bomQty if i == '900U01-0100'])
var_36 += sum([bomQty[i] for i in bomQty if i == '900ES1-100'])
Product.Attr('PLC_UOC_labor_parameter_var_13').AssignValue(str(var_13))
Product.Attr('PLC_UOC_labor_parameter_var_15').AssignValue(str(var_15))
Product.Attr('PLC_UOC_labor_parameter_var_20').AssignValue(str(var_20))
Product.Attr('PLC_UOC_labor_parameter_var_36').AssignValue(str(var_36))
Product.Attr('PLC_UOC_labor_parameter_var_22').AssignValue(str(int(var_22)))
