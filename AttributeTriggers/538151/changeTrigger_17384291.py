from GS_EanbledServices_functions import assets_container_update,customer_has_cyber_refresh,matrikon_refresh,L3_L4_Refresh,udc_calculation_refresh,l3_l4_refresh,enhanced_no_vse_refresh
#VARIABLE INTAILSATION STARTED

Product.Attr('EnabledService_Entitlement').AssignValue(Product.Attr('EnabledServices_servprod').SelectedValue.Display)
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

	#CONTAINER ATTR VARIABLES - START

assets_container = Product.GetContainerByName('Asset_details_ServiceProd')
service_product = Product.Attr('EnabledServices_servprod').GetValue()

	#CONTAINER ATTR VARIABLES - END

	#DATABASE QUERY VARIABLES - START

per_device_hardcode_prices_query = SqlHelper.GetList("select Name, Price from SC_Hardcode_Price")
per_device = float(SqlHelper.GetFirst("select * from SC_HARDCODE_VALUES where Name = N'{0}'".format('Essentials % of Enhanced')).Value)
udc_data_base_query_value = SqlHelper.GetFirst("select * from sc_hardcode_values where Name = 'Asset/Agent Limit/UDC'").Value
per_device_for_matrikon = float(SqlHelper.GetFirst("select * from sc_hardcode_values where name = 'Matrikon Node(USD)'").Value) + float(SqlHelper.GetFirst("select * from sc_hardcode_values where name = 'Matrikon Client(USD)'").Value)

	#DATABASE QUERY VARIABLES - END

	#EVENT BASED VARIABLES - START

#currentTab = arg.NameOfCurrentTab

	#EVENT BASED VARIABLES - START

#VARIABLE INTAILSATION ENDED


customerCyberValue = Product.Attr('Customer_has_cyber_enabledServicesModel').Values
isCustomerSelected = [value.IsSelected for value in customerCyberValue][0]
if isCustomerSelected:
	#Product.Attr('#_of_independent_"areas"_enabledServicesModel').AssignValue('0.00')
	#Product.Attr("L3_L4_FILE_MOVER_ESSENTIAL_enabledServicesModel").Access = AttributeAccess.Hidden
	Product.Attr('#_of_independent_"areas"_enabledServicesModel').Access = AttributeAccess.Hidden
	Product.Attr("#_of_recommended_udc_servers_enabledServicesModel").Access = AttributeAccess.Hidden
	Product.Attr("#_l3_l4_file_move_licenses_enabledServicesModel").Access = AttributeAccess.Hidden
	if entitlement_value == 'Enabled Services - Enhanced':
		Product.Attr("L3_L4_FILE_MOVER_ESSENTIAL_enabledServicesModel").Access = AttributeAccess.ReadOnly
		"""for i in L3_L4_Mover_Essential_attr.Values:
			i.IsSelected = False"""
	elif entitlement_value == 'Enabled Services - Essential':
		Product.Attr("L3_L4_FILE_MOVER_ESSENTIAL_enabledServicesModel").Access = AttributeAccess.Editable
		for i in L3_L4_Mover_Essential_attr.Values:
			i.IsSelected = False
else:
	Product.Attr('#_of_independent_"areas"_enabledServicesModel').Access = AttributeAccess.Editable
	Product.Attr("#_of_recommended_udc_servers_enabledServicesModel").Access = AttributeAccess.ReadOnly
	Product.Attr("#_l3_l4_file_move_licenses_enabledServicesModel").Access = AttributeAccess.ReadOnly
	Product.Attr("DurationOfPlan_enabledServices").Access = AttributeAccess.ReadOnly
	if entitlement_value == 'Enabled Services - Enhanced':
		Product.Attr("L3_L4_FILE_MOVER_ESSENTIAL_enabledServicesModel").Access = AttributeAccess.ReadOnly
		"""for i in L3_L4_Mover_Essential_attr.Values:
			i.IsSelected = False"""
	elif entitlement_value == 'Enabled Services - Essential':
		Product.Attr("L3_L4_FILE_MOVER_ESSENTIAL_enabledServicesModel").Access = AttributeAccess.Editable
		"""for i in L3_L4_Mover_Essential_attr.Values:
			i.IsSelected = False"""

############# So that enter logic for matrikon executes..

Product.Attr('SC_HWOS_Service_Product_ScopeSummary').AssignValue(str(Product.Attr('EnabledService_Entitlement').GetValue()))
if Product.Attr('EnabledService_Entitlement').GetValue() == 'Enabled Services - Enhanced':
	for i in Product.Attr('L3_L4_FILE_MOVER_ESSENTIAL_enabledServicesModel').Values:
		i.IsSelected = True
	Product.Attr('L3_L4_FILE_MOVER_ESSENTIAL_enabledServicesModel').Access = AttributeAccess.ReadOnly
else:
	#for i in Product.Attr('L3_L4_FILE_MOVER_ESSENTIAL_enabledServicesModel').Values:
		#i.IsSelected = False
	Product.Attr('L3_L4_FILE_MOVER_ESSENTIAL_enabledServicesModel').Access = AttributeAccess.Editable

############ SO that it refreshes the asssets container
assets_container = Product.GetContainerByName('Asset_details_ServiceProd')
service_product = Product.Attr('EnabledServices_servprod').GetValue() 
#Log.Info('Service_product ->'+str(service_product))
Product_type = Product.Attr('SC_Product_Type').GetValue()
exchange_rate = 1
if Quote:
	exchange_rate = float(Quote.GetCustomField('Exchange Rate').Content)
if Product_type != 'Renewal':
	assets_container_update(assets_container,service_product,exchange_rate, Product.Attr('SC_Service_Product').GetValue())
##############
customer_has_cyber_refresh(entitlement_value,Customer_has_cyber_attr,enhanced_no_vse_attr,data_broker_attr)
#################

L3_L4_Refresh(L3_L4_Mover_Essential_attr,Customer_has_cyber_attr,essential_select_option_attr,data_broker_attr)

#############################

enhanced_no_vse_refresh(enhanced_no_vse_attr,essential_select_option_attr,data_broker_attr)

####################
#UDC calc START

udc_calculation_refresh(per_device_hardcode_prices_query,entitlement_value,udc_data_base_query_value,recommended_udc_servers_attr,l3_l4_move_attr,Product,per_device)

######################### UPDating licenses after udc update ###############3

l3_l4_refresh(recommended_udc_servers_attr,l3_l4_move_attr,Product)

#Matrix License
exRate = float(Quote.GetCustomField("SC_CF_EXCHANGE_RATE").Content) if Quote.GetCustomField("SC_CF_EXCHANGE_RATE").Content else 1
per_device_for_matrikon = float(per_device_for_matrikon/2) if Product.Attr('SC_Service_Product').GetValue() =="System Evolution Program" else per_device_for_matrikon
exRate = float(Quote.GetCustomField("SC_CF_EXCHANGE_RATE").Content) if Quote.GetCustomField("SC_CF_EXCHANGE_RATE").Content else 1
matrikon_refresh(data_broker_attr,l3_l4_move_attr,per_device_for_matrikon,Product, exRate)

####################### if service product is enhanced then order type is required.##################
if Product.Attr('EnabledService_Entitlement'):
	if Product.Attr('EnabledService_Entitlement').GetValue() == 'Enabled Services - Enhanced':
		Product.Attr('OrderType_EnabledService').Required = True
	else:
		Product.Attr('OrderType_EnabledService').Required = True
#Product.Attr('#_of_independent_"areas"_enabledServicesModel').AssignValue('0.00')
serPrd = Product.Attr("EnabledServices_servprod").GetValue()
Product.Attr("SESP_Enabled_Service_Product_ReadOnly").AssignValue(serPrd)

#Scope Removal
Product_type = Product.Attr('SC_Product_Type').GetValue()
if Product_type == 'Renewal':
	ScriptExecutor.Execute('GS_SC_ES_Scope_Removal')