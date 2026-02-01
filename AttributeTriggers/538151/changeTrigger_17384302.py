# MODULE IMPORTS START

from GS_EanbledServices_functions import l3_l4_refresh,matrikon_refresh,udc_calculation_refresh

#MODULE IMPORTS END

#VARIABLE INTAILSATION STARTED

	#NON CONTAINER ATTR VARIABLES - START
entitlement_value = Product.Attr('EnabledService_Entitlement').GetValue()
Customer_has_cyber_attr = Product.Attr('Customer_has_cyber_enabledServicesModel')
data_broker_attr = Product.Attr('data_broker_needed_enabledServicesModel')
recommended_udc_servers_attr = Product.Attr('#_of_recommended_udc_servers_enabledServicesModel')
l3_l4_move_attr = Product.Attr('#_l3_l4_file_move_licenses_enabledServicesModel')

	#NON CONTAINER ATTR VARIABLES - END
	#DATABASE QUERY VARIABLES - START
udc_data_base_query_value = SqlHelper.GetFirst("select * from sc_hardcode_values where Name = 'Asset/Agent Limit/UDC'").Value
per_device_for_matrikon = float(SqlHelper.GetFirst("select * from sc_hardcode_values where name = 'Matrikon Node(USD)'").Value) + float(SqlHelper.GetFirst("select * from sc_hardcode_values where name = 'Matrikon Client(USD)'").Value)
per_device_hardcode_prices_query = SqlHelper.GetList("select Name, Price from SC_Hardcode_Price")
per_device = float(SqlHelper.GetFirst("select * from SC_HARDCODE_VALUES where Name = N'{0}'".format('Essentials % of Enhanced')).Value)

	#DATABASE QUERY VARIABLES - END


#VARIABLE INTAILSATION ENDED
###### negative value check
independent_areas = Product.Attr('#_of_independent_"areas"_enabledServicesModel').GetValue()
if float(independent_areas) < 0:
    Trace.Write('444444444')
    Product.Messages.Add('Negative Values are not valid')
    Product.Attr('#_of_independent_"areas"_enabledServicesModel').AssignValue('0')




#############
l3_l4_refresh(recommended_udc_servers_attr,l3_l4_move_attr,Product)

###############
udc_calculation_refresh(per_device_hardcode_prices_query,entitlement_value,udc_data_base_query_value,recommended_udc_servers_attr,l3_l4_move_attr,Product,per_device)

################## MATRIKON##########
#Matrix License
exRate = float(Quote.GetCustomField("SC_CF_EXCHANGE_RATE").Content) if Quote.GetCustomField("SC_CF_EXCHANGE_RATE").Content else 1
per_device_for_matrikon = float(per_device_for_matrikon/2) if Product.Attr('SC_Service_Product').GetValue() =="System Evolution Program" else per_device_for_matrikon
matrikon_refresh(data_broker_attr,l3_l4_move_attr,per_device_for_matrikon,Product, exRate)