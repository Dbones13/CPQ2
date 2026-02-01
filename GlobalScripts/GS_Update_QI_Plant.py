from CF_UTILS import CF_CONSTANTS, get_custom_field_value, split_after_comma

#CXCPQ-59003:Update quote lineitems when Plant is selected at header level
custom_field_name = CF_CONSTANTS.get("QUOTE_LEVEL_PLANT_FIELD")
full_plant_value = get_custom_field_value(Quote, custom_field_name)
plant_code,plant_value = split_after_comma(full_plant_value)
q_type=Quote.GetCustomField("Quote Type").Content
#Quote.GetCustomField('CF_Plant_Prevent_Calc').Content = 'true'
v_bookingLOB=Quote.GetCustomField('Booking LOB').Content
if plant_value !='' and ((q_type == 'Parts and Spot' and  v_bookingLOB== "PMC") or v_bookingLOB== "HCP"):
    for i in Quote.Items:
        #Trace.Write("i['QI_Plant'].Value-->"+str(i['QI_Plant'].Value)+"---i['QI_prev_plant_value'].Value-->"+str(i['QI_prev_plant_value'].Value)+"---plant_value--"+str(plant_value))
        if plant_value != i['QI_Plant'].Value:
            i['QI_prev_plant_value'].Value = i['QI_Plant'].Value
            i['QI_Plant'].Value = plant_value
        else:
            i['QI_Plant'].Value=plant_value
            i['QI_prev_plant_value'].Value=plant_value
        #i['QI_Plant'].Value=plant_value
        #i['QI_prev_plant_value'].Value=plant_value