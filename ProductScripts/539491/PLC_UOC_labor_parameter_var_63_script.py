plc_container=Product.GetContainerByName('LSS_PLC_connection_transpose').Rows
uoc_container=Product.GetContainerByName('LSS_UOC_connection_transpose').Rows
var_63=0
for i in plc_container:
    if i['LSS_PLC_Installed_Vendor'] in ['Siemens Simatic S5 Series', 'Honeywell S9000','Honeywell RTU','Honeywell Master Logic PLC','Honeywell HC900']:
        var_63+=1
for i in uoc_container:
    if i['Installed PLC Vendor'] in ['Siemens Simatic S5 Series', 'Honeywell S9000','Honeywell RTU','Honeywell Master Logic PLC','Honeywell HC900']:
        var_63+=1
Product.Attr('PLC_UOC_labor_parameter_var_63').AssignValue(str(var_63))