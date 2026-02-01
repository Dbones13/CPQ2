plc_container=Product.GetContainerByName('LSS_PLC_connection_transpose').Rows
uoc_container=Product.GetContainerByName('LSS_UOC_connection_transpose').Rows
var_3=0
for i in plc_container:
    if i['LSS_PLC_Installed_Vendor'] in ['Rockwell PLC5','Honeywell IPC 620 Standalone','Rockwell SLC500'] :
        var_3+=1
for i in uoc_container:
    if i['Installed PLC Vendor'] in ['Rockwell PLC5','Honeywell IPC 620 Standalone','Rockwell SLC500']:
        var_3+=1
Product.Attr('PLC_UOC_labor_parameter_var_3').AssignValue(str(var_3))