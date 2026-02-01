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
            container.DeleteRow(row_count - flag)

def manage_uoc_configuration(msid_scope, PLC_required):
    cont = get_container("LSS_UOC_connection_transpose")
    manage_rows(cont, PLC_required)
    msid_scope = Product.Attr('Scope').GetValue()
    contObj = Product.GetContainerByName('LSS_UOC_connection_transpose')
    if contObj.Rows.Count > 0:
        for row in contObj.Rows:
            row.Product.Attr('MIgration_Scope_Choices').SelectDisplayValue(msid_scope)
            #row.ApplyProductChanges()

    
msid_scope = Product.Attr('Scope').GetValue()
plc_required = int(Product.Attr("LSS_PLC_Number_of_ControlEdge_UOC_vUOC_confi_req").GetValue() or 0)
manage_uoc_configuration(msid_scope, plc_required)

'''def valueassign(Attributename):
    return Product.Attr(Attributename).AssignValue('0')
Listofatr = ['LSS_Number_of_hard_wired_Analog_Input_for_CE_UOC','LSS_Number_of_hard_wired_Analog_Output_for_CE_UOC','LSS_Number_of_hard_wired_Digital_Input_for_CE_UOC','LSS_Number_of_hard_wired_Digital_Output_for_CE_UOC']
if Product.Attr('LSS_PLC_Number_of_ControlEdge_UOC_vUOC_confi_req').GetValue() > 0:
    for i in Listofatr:
        valueassign(i)'''