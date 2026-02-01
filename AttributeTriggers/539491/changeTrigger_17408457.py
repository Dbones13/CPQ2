def get_container(name):
    return Product.GetContainerByName(name)

def hide_attribute(attribute_name):
    Product.DisallowAttr(attribute_name)

def show_attribute(attribute_name):
    Product.AllowAttr(attribute_name)

def manage_rows(container, required_count):
    row_count = container.Rows.Count
    if row_count < required_count:
        for _ in range(row_count, required_count):
            container.AddNewRow(False)
    elif row_count > required_count:
        flag = 0
        for _ in range(required_count, row_count):
            flag += 1
            container.DeleteRow(row_count -flag)
            
def GetAttributePermission(name):
    return Product.Attr(name).Allowed

def manage_plc_groups(msid_scope, plc_groups):
    cont = get_container("LSS_PLC_connection_transpose")
    manage_rows(cont, plc_groups)
    contObj = Product.GetContainerByName('LSS_PLC_connection_transpose')
    if contObj.Rows.Count > 0:
        for row in contObj.Rows:
            row.Product.Attr('MIgration_Scope_Choices').SelectDisplayValue(msid_scope)
    Product.Attr('MIgration_Scope_Choices').SelectDisplayValue(msid_scope)
    
msid_scope = Product.Attr('Scope').GetValue()
plc_groups = int(Product.Attr("LSS_PLC_Number_of_ControlEdge_PLC_Groups_required").GetValue() or 0)
manage_plc_groups(msid_scope, plc_groups)


'''def valueassign(Attributename):
	return Product.Attr(Attributename).AssignValue('0')
Listofatr = ['LSS_PLC_Total_of_3rd_Party_PLC_via_PCDI','LSS_PLC_Total_of_3rd_Party_PLC_via_Scada','LSS_PLC_Total_of_3rd_Party_PLC_via_HPM_SI','LSS_PLC_Total_of_3rd_Party_PLC_via_EPLCG']
if Product.Attr('LSS_PLC_Number_of_ControlEdge_PLC_Groups_required').GetValue() > 0:
	for i in Listofatr:
		valueassign(i)'''