plc_container=Product.GetContainerByName('LSS_PLC_connection_transpose').Rows
uoc_container=Product.GetContainerByName('LSS_UOC_connection_transpose').Rows
var_61=0
for i in plc_container:
    if i['LSS_PLC_Installed_Vendor'] in ['Rockwell ControlLogix','Rockwell MicroLogix','Schneider Modicon Quatum','GE 90-70','GE 90-30'] :
        var_61+=1
for i in uoc_container:
    if i['Installed PLC Vendor'] in ['Rockwell ControlLogix','Rockwell MicroLogix','Schneider Modicon Quatum','GE 90-70','GE 90-30']:
        var_61+=1
Product.Attr('PLC_UOC_labor_parameter_var_61').AssignValue(str(var_61))