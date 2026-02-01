# MODULE IMPORTS START

from CPQ_SF_SC_Modules import CL_SC_Modules
from GS_EanbledServices_functions import assets_container_update,customer_has_cyber_refresh,L3_L4_Refresh,enhanced_no_vse_refresh,udc_calculation_refresh,l3_l4_refresh,matrikon_refresh

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

	#CONTAINER ATTR VARIABLES - START

assets_container = Product.GetContainerByName('Asset_details_ServiceProd')
service_product = Product.Attr('EnabledServices_servprod').GetValue()

	#CONTAINER ATTR VARIABLES - END

	#DATABASE QUERY VARIABLES - START

per_device_hardcode_prices_query = SqlHelper.GetList("select Name, Price from SC_Hardcode_Price")
per_device = float(SqlHelper.GetFirst("select * from SC_HARDCODE_VALUES where Name = N'{0}'".format('Essentials % of Enhanced')).Value)
udc_data_base_query_value = SqlHelper.GetFirst("select * from sc_hardcode_values where Name = 'Asset/Agent Limit/UDC'").Value
exRate = float(Quote.GetCustomField("SC_CF_EXCHANGE_RATE").Content) if Quote.GetCustomField("SC_CF_EXCHANGE_RATE").Content else 1
SC_Currency = Quote.GetCustomField("SC_CF_CURRENCY").Content
per_device_for_matrikon = float(SqlHelper.GetFirst("select * from sc_hardcode_values where name = 'Matrikon Node(USD)'").Value) + float(SqlHelper.GetFirst("select * from sc_hardcode_values where name = 'Matrikon Client(USD)'").Value)

	#DATABASE QUERY VARIABLES - END

	#EVENT BASED VARIABLES - START

currentTab = arg.NameOfCurrentTab

	#EVENT BASED VARIABLES - START

#VARIABLE INTAILSATION ENDED

# SNIPPET 1 START - This is basically to make a checkbox readonly when service product in enhanced.

serv_prod_attr.AssignValue(str(entitlement_value))
if entitlement_value == 'Enabled Services - Enhanced':
	for i in L3_L4_Mover_Essential_attr.Values:
		i.IsSelected = True
	L3_L4_Mover_Essential_attr.Access = AttributeAccess.ReadOnly
elif entitlement_value == 'Enabled Services - Essential':
	#for i in L3_L4_Mover_Essential_attr.Values:
		#i.IsSelected = False
	L3_L4_Mover_Essential_attr.Access = AttributeAccess.Editable

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


#SNIPPET 1 END.

# SNIPPET 2 START - LOADING THE ASSETS CONTAINER WITH THE SELECTED MSID'S ON TAB CHANGE.

if currentTab == 'Scope Summary':
	class_contact_modules = CL_SC_Modules(Quote, TagParserQuote, None, Session)
	msid_names = {}
	assetContainerRows = Product.GetContainerByName("SC_Select_MSID_Cont").Rows
	msid_list = [j["MSIDs"] for j in assetContainerRows if j.IsSelected == True]
	if len(msid_list) > 0:
		TopologyData = class_contact_modules.get_Topology_aggregate_Data(msid_list)
		msid_names = {}
		database_category_by_topology = SqlHelper.GetList("select Category,Topology_Name from SC_CT_TOPOLOGY_MAPPING")
		for msid in msid_list:
			msid_names[str(msid)] = {}
		records = None
		if TopologyData:
			records = TopologyData.records
		if records:
			for record in records:
				record_topology = record['TopologyName']
				for database_topo_record in database_category_by_topology:
					if database_topo_record.Topology_Name.ToString() == record_topology.ToString():
						if str(record['Quantity']) == "":
							record['Quantity'] = 0
						if database_topo_record.Category not in msid_names[str(record["MISD"])]:
							msid_names[str(record["MISD"])][str(database_topo_record.Category)] = int(record['Quantity'])
						else:
							msid_names[str(record["MISD"])][str(database_topo_record.Category)] = int(msid_names[str(record["MISD"])][str(database_topo_record.Category)]) + int(record.Quantity)

		Assets = Product.GetContainerByName('Asset_details_ServiceProd')
		#Assets.Rows.Clear()
		if Assets.Rows.Count == 0:
			for asset in assetContainerRows:
				if asset.IsSelected == True:
					row = Assets.AddNewRow(False)
					row['MSID'] = asset['MSIDs']
					row['Servers'] = str(msid_names[str(asset['MSIDs'])].get('Servers')) if msid_names[str(asset['MSIDs'])].get('Servers', None)  is not None else '0'
					row['Workstations'] = str(msid_names[str(asset['MSIDs'])].get('Workstations')) if msid_names[str(asset['MSIDs'])].get('Workstations', None)  is not None else '0'
					row['Windows - Other'] = str(msid_names[str(asset['MSIDs'])].get('Windows - Other')) if msid_names[str(asset['MSIDs'])].get('Windows - Other', None)  is not None else '0'
					row['TPN Nodes'] = str(msid_names[str(asset['MSIDs'])].get('TPN Nodes')) if msid_names[str(asset['MSIDs'])].get('TPN Nodes', None)  is not None else '0'
					row['Controllers'] = str(msid_names[str(asset['MSIDs'])].get('Controllers')) if msid_names[str(asset['MSIDs'])].get('Controllers', None)  is not None else '0'
					row['Switches'] = str(msid_names[str(asset['MSIDs'])].get('Switches')) if msid_names[str(asset['MSIDs'])].get('Switches', None)  is not None else '0'
					row['SCADA Servers'] = str(msid_names[str(asset['MSIDs'])].get('SCADA')) if msid_names[str(asset['MSIDs'])].get('SCADA', None)  is not None else '0'
					row['Safety Manager'] = str(msid_names[str(asset['MSIDs'])].get('Safety Manager')) if msid_names[str(asset['MSIDs'])].get('Safety Manager', None)  is not None else '0'
			else:
				Assets.Calculate()
		else:
			Msids = Product.GetContainerByName('SC_Select_MSID_Cont')
			unselected_msids_list = [ i['MSIDs'] for i in Msids.Rows if i.IsSelected == False]
			unselected_msids_list = list(set(unselected_msids_list))
			selected_msids_list = [ i['MSIDs'] for i in Msids.Rows if i.IsSelected == True]
			Assets = Product.GetContainerByName('Asset_details_ServiceProd')
			selected_assets = [i['MSID'] for i in Assets.Rows]
			selected_msids_list = list(set(selected_msids_list))
			asset_delete_ids = [i.RowIndex for i in Assets.Rows if i['MSID'] in unselected_msids_list]
			"""if len(asset_delete_ids) > 0:
				Assets.DeleteRow(asset_delete_ids[0])
			if len(asset_delete_ids) > 1:
				x = 1
				for j in asset_delete_ids[1:]:
					Assets.DeleteRow(j-x)
					x = x + 1"""
			if len(asset_delete_ids) > 0:
				asset_delete_ids.sort(reverse=True)
				for x in asset_delete_ids:
					Assets.DeleteRow(x)
			if len(selected_msids_list) > 0:
				for selected_msid in selected_msids_list:
					if selected_msid not in selected_assets:
						row = Assets.AddNewRow(False)
						row['MSID'] = selected_msid
						row['Servers'] = str(msid_names[str(selected_msid)].get('Servers')) if msid_names[str(selected_msid)].get('Servers', None)  is not None else '0'
						row['Workstations'] = str(msid_names[str(selected_msid)].get('Workstations')) if msid_names[str(selected_msid)].get('Workstations', None)  is not None else '0'
						row['Windows - Other'] = str(msid_names[str(selected_msid)].get('Windows - Other')) if msid_names[str(selected_msid)].get('Windows - Other', None)  is not None else '0'
						row['TPN Nodes'] = str(msid_names[str(selected_msid)].get('TPN Nodes')) if msid_names[str(selected_msid)].get('TPN Nodes', None)  is not None else '0'
						row['Controllers'] = str(msid_names[str(selected_msid)].get('Controllers')) if msid_names[str(selected_msid)].get('Controllers', None)  is not None else '0'
						row['Switches'] = str(msid_names[str(selected_msid)].get('Switches')) if msid_names[str(selected_msid)].get('Switches', None)  is not None else '0'
						row['SCADA Servers'] = str(msid_names[str(selected_msid)].get('SCADA')) if msid_names[str(selected_msid)].get('SCADA', None)  is not None else '0'
						row['Safety Manager'] = str(msid_names[str(selected_msid)].get('Safety Manager')) if msid_names[str(selected_msid)].get('Safety Manager', None)  is not None else '0'
	else:
		Msids = Product.GetContainerByName('SC_Select_MSID_Cont')
		unselected_msids_list = [ i['MSIDs'] for i in Msids.Rows if i.IsSelected == False]
		#selected_msids_list = [ i['MSIDs'] for i in Msids.Rows if i.IsSelected == True]
		Assets = Product.GetContainerByName('Asset_details_ServiceProd')
		#selected_assets = [i['MSID'] for i in Assets.Rows]
		asset_delete_ids = [i.RowIndex for i in Assets.Rows if i['MSID'] in unselected_msids_list]
		if len(asset_delete_ids) > 0:
			asset_delete_ids.sort(reverse=True)
			for x in asset_delete_ids:
				Assets.DeleteRow(x)
	#else:
	#	Assets = Product.GetContainerByName('Asset_details_ServiceProd')
	#	Assets.Rows.Clear()

	
	# SNIPPET 2 - END

#SNIPPET 3 START -  SO that it refreshes the asssets container
exchange_rate = 1
if Quote:
	exchange_rate = float(Quote.GetCustomField('Exchange Rate').Content)
assets_container_update(assets_container,service_product,exchange_rate)
summ_cont = Product.GetContainerByName('ES_Asset_Summary')
if summ_cont.Rows.Count > 0:
	summ_cont.Rows[0].Calculate()

#SNIPPET 3 END.

#SNIPPET 4 START - IF Customer has cyber is checked logic for enhaced and essential.

customer_has_cyber_refresh(entitlement_value,Customer_has_cyber_attr,enhanced_no_vse_attr,data_broker_attr)

#SNIPPET 4 END.

#SNIPPET 5 START - Refreshs the logic for L3 L4

L3_L4_Refresh(L3_L4_Mover_Essential_attr,Customer_has_cyber_attr,essential_select_option_attr,data_broker_attr)

#SNIPPET 5 END.

#SNIPPET 6 START

enhanced_no_vse_refresh(enhanced_no_vse_attr,essential_select_option_attr,data_broker_attr)

#SNIPPET 6 END

#SNIPPET 7 START - UDC CALCULATION LOGIC

udc_calculation_refresh(per_device_hardcode_prices_query,entitlement_value,udc_data_base_query_value,recommended_udc_servers_attr,l3_l4_move_attr,Product,per_device)

# SNIPPET 7 END - UDC CALC END
#SNIPPET 8 START - UPDATE l3 l4 license

l3_l4_refresh(recommended_udc_servers_attr,l3_l4_move_attr,Product)

# SNIPPET 8 END.

#SNIPPET 9 START - Matrix License

matrikon_refresh(data_broker_attr,l3_l4_move_attr,per_device_for_matrikon,Product,exRate)

#SNIPPET 9 END.

############################### SO THAT HEADER LABELS WILL BE IN SYNC WITH QUOTE CURRENCY ################
if Quote:
	currency = Quote.SelectedMarket.CurrencyCode
else:
	currency = 'USD'
Product.GetContainerByName('Asset_details_ServiceProd').TotalRow.Columns['List Price'].HeaderLabel = 'List Price' + " (" + currency +")"