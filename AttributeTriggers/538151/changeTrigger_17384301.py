# MODULE IMPORTS START

from GS_EanbledServices_functions import customer_has_cyber_refresh,L3_L4_Refresh,enhanced_no_vse_refresh,matrikon_refresh

#MODULE IMPORTS END

#VARIABLE INTAILSATION STARTED

	#NON CONTAINER ATTR VARIABLES - START

serv_prod_attr = Product.Attr('SC_HWOS_Service_Product_ScopeSummary')
entitlement_value = Product.Attr('EnabledService_Entitlement').GetValue()
Customer_has_cyber_attr = Product.Attr('Customer_has_cyber_enabledServicesModel')
L3_L4_Mover_Essential_attr = Product.Attr('L3_L4_FILE_MOVER_ESSENTIAL_enabledServicesModel')
enhanced_no_vse_attr = Product.Attr('enhanced_and_no_vse_enabledServicesModel')
data_broker_attr = Product.Attr('data_broker_needed_enabledServicesModel')
essential_select_option_attr = Product.Attr('essentail_select_the_option_enabledServicesModel')
recommended_udc_servers_attr = Product.Attr('#_of_recommended_udc_servers_enabledServicesModel')
l3_l4_move_attr = Product.Attr('#_l3_l4_file_move_licenses_enabledServicesModel')

	#NON CONTAINER ATTR VARIABLES - END


	#DATABASE QUERY VARIABLES - START

per_device_for_matrikon = float(SqlHelper.GetFirst("select * from sc_hardcode_values where name = 'Matrikon Node(USD)'").Value) + float(SqlHelper.GetFirst("select * from sc_hardcode_values where name = 'Matrikon Client(USD)'").Value)

	#DATABASE QUERY VARIABLES - END

	#EVENT BASED VARIABLES - START

#currentTab = arg.NameOfCurrentTab

	#EVENT BASED VARIABLES - START

#VARIABLE INTAILSATION ENDED

##################

customer_has_cyber_refresh(entitlement_value,Customer_has_cyber_attr,enhanced_no_vse_attr,data_broker_attr)

#################
L3_L4_Refresh(L3_L4_Mover_Essential_attr,Customer_has_cyber_attr,essential_select_option_attr,data_broker_attr)

#########################

enhanced_no_vse_refresh(enhanced_no_vse_attr,essential_select_option_attr,data_broker_attr)

################## MATRIKON##########
#Matrix License
exRate = float(Quote.GetCustomField("SC_CF_EXCHANGE_RATE").Content) if Quote.GetCustomField("SC_CF_EXCHANGE_RATE").Content else 1
per_device_for_matrikon = float(per_device_for_matrikon/2) if Product.Attr('SC_Service_Product').GetValue() =="System Evolution Program" else per_device_for_matrikon
matrikon_refresh(data_broker_attr,l3_l4_move_attr,per_device_for_matrikon,Product, exRate)