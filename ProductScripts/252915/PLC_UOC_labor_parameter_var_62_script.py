plc_container=Product.GetContainerByName('LSS_PLC_connection_transpose').Rows
uoc_container=Product.GetContainerByName('LSS_UOC_connection_transpose').Rows
var_62=0
for i in plc_container:
    if i['LSS_PLC_Installed_Vendor'] in ['Siemens Simatic S7 Series','GE Bentley Nevada'] :
        var_62+=1
for i in uoc_container:
    if i['Installed PLC Vendor'] in ['Siemens Simatic S7 Series','GE Bentley Nevada']:
        var_62+=1
Product.Attr('PLC_UOC_labor_parameter_var_62').AssignValue(str(var_62))