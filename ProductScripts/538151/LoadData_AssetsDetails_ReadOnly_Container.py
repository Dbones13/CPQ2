from CPQ_SF_SC_Modules import CL_SC_Modules
from GS_EanbledServices_functions import assets_container_update,customer_has_cyber_refresh,L3_L4_Refresh,enhanced_no_vse_refresh,udc_calculation_refresh,l3_l4_refresh,matrikon_refresh

from System import DateTime
from System.Globalization import CultureInfo

def getDateTimeOBJ(dateString, dateFormat):
	try:
		return DateTime.Parse(dateString)
	except:
		return

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
if currentTab == 'Enabled Services':
	if entitlement_value == 'Enabled Services - Enhanced':
		Product.Attr('L3_L4_FILE_MOVER_ESSENTIAL_enabledServicesModel').Access = AttributeAccess.Editable
	else:
		#for i in Product.Attr('L3_L4_FILE_MOVER_ESSENTIAL_enabledServicesModel').Values:
		#	i.IsSelected = False
		Product.Attr('Customer_has_cyber_enabledServicesModel').Access = AttributeAccess.ReadOnly

if currentTab == "Scope Summary":
	assetContainerRows = Product.GetContainerByName("Asset_Details_ServiceProd").Rows
	readOnlyAssetContainer = Product.GetContainerByName("Asset_details_ServiceProd_ReadOnly")
	readOnlyAssetContainer.Clear()
	for row in assetContainerRows:
		readRow = readOnlyAssetContainer.AddNewRow(False)
		readRow["MSID"] = row["MSID"] if row["MSID"] is not None else ""
		readRow["Servers"] = row["Servers"] if row["Servers"] is not None else ""
		readRow["Workstations"] = row["Workstations"] if row["Workstations"] is not None else ""
		readRow["Windows - Other"] = row["Windows - Other"] if row["Windows - Other"] is not None else ""
		readRow["TPN Nodes"] = row["TPN Nodes"] if row["TPN Nodes"] is not None else ""
		readRow["Controllers"] = row["Controllers"] if row["Controllers"] is not None else ""
		readRow["Switches"] = row["Switches"] if row["Switches"] is not None else ""
		readRow["SCADA Servers"] = row["SCADA Servers"] if row["SCADA Servers"] is not None else ""
		readRow["Safety Manager"] = row["Safety Manager"] if row["Safety Manager"] is not None else ""
		readRow['List Price'] = row["List Price"] if row["List Price"] is not None else ""
	else:
		readOnlyAssetContainer.CalculateTotals()
	Product.Attr("EnabledServices_servprod").Access = AttributeAccess.ReadOnly
	Product.Attr("EnabledService_Entitlement").Access = AttributeAccess.ReadOnly
	Product.Attr("A360Contract_SESPEnable").Access = AttributeAccess.ReadOnly
	Product.Attr("SESP_Enabled_Service_Product_ReadOnly").Access = AttributeAccess.ReadOnly
	Product.Attr("SESP_Enabled_Service_A360_ReadOnly").Access = AttributeAccess.ReadOnly
if currentTab == 'Enabled Services':
	if Product.Attr('SC_Service_Product').GetValue() == 'SESP Value Remote Plus' or Product.Attr('SC_Service_Product').GetValue() == 'SESP Value Plus' or Product.Attr('SC_Service_Product').GetValue() == 'System Evolution Program':
		Product.Attr('CurrentSupportContract_EnabledService').AssignValue(Product.Attr('SC_Service_Product').GetValue())
	else:
		Product.Attr('CurrentSupportContract_EnabledService').AssignValue('')
	Product.Attr("EnabledServices_servprod").Access = AttributeAccess.Editable
	Product.Attr("EnabledService_Entitlement").Access = AttributeAccess.ReadOnly
	Product.Attr("A360Contract_SESPEnable").Access = AttributeAccess.Editable
	Product.Attr("CurrentSupportContract_EnabledService").Access = AttributeAccess.ReadOnly
	Product.Attr('#_of_recommended_udc_servers_enabledServicesModel').Access = AttributeAccess.ReadOnly
	Product.Attr('#_l3_l4_file_move_licenses_enabledServicesModel').Access = AttributeAccess.ReadOnly
	Product.Attr("Matrix License").Access = AttributeAccess.ReadOnly
	########################################## Below code is to update the contract dates for enable service model.
	#Product.Attr('SC_HWOS_Service_Product').AssignValue('Enabled Services Model')
	#Product.Attr('CurrentSupportContract_EnabledService').AssignValue('None')
	if Quote:
		Trace.Write('000000000000')
		duration = Quote.GetCustomField('SC_CF_CONTRACTDURYR').Content.split(' ')[0]

		prev_c_start_date = Product.Attr('PreviousQuoteCStartDate_EnabledServices')
		prev_c_end_date = Product.Attr('PreviousQuoteCEndDate_EnabledServices')

		prd_c_start_date = Product.Attr('ContractStartDate_EnabledService')
		prd_c_end_date = Product.Attr('ContractEndDate_EnabledService')

		#prev_c_start_date_p = UserPersonalizationHelper.ToUserFormat(getDateTimeOBJ(prev_c_start_date.GetValue(),'mm/d/yyyy')) if getDateTimeOBJ(prev_c_start_date.GetValue(),'mm/d/yyyy') else None

		#prev_c_end_date_p = UserPersonalizationHelper.ToUserFormat(getDateTimeOBJ(prev_c_end_date.GetValue(),'mm/d/yyyy')) if getDateTimeOBJ(prev_c_end_date.GetValue(),'mm/d/yyyy') else None

		# Commented to test other event for the same use case.
		"""if Quote:
			curr_c_start_date = Quote.GetCustomField('EGAP_Contract_Start_Date').Content
			curr_c_end_date = Quote.GetCustomField('EGAP_Contract_End_Date').Content
		Trace.Write('PREV STArt date -> '+str(prev_c_start_date_p) + " ------- "+ "END DATE -> "+str(prev_c_end_date_p))
		Trace.Write("CURRENT START Date  --> " + str(curr_c_start_date) +"=-------"+"END DATE -> "+str(curr_c_end_date))
		if prev_c_start_date_p:
			if prev_c_start_date_p != curr_c_start_date:
				prd_c_start_date.AssignValue(curr_c_start_date)
				prev_c_start_date.AssignValue(curr_c_start_date)
			else:
				if prd_c_start_date.GetValue() == '':
					prd_c_start_date.AssignValue(curr_c_start_date)
				else:
					pass
		if prev_c_end_date_p:
			if prev_c_end_date_p != curr_c_end_date:
				prd_c_end_date.AssignValue(curr_c_end_date)
				prev_c_end_date.AssignValue(curr_c_end_date)
			else:
				if prd_c_end_date.GetValue() == '':
					prd_c_end_date.AssignValue(curr_c_end_date)"""
		con = Product.GetContainerByName('SC_SESP_MultiSites')


	##############
	class_contact_modules = CL_SC_Modules(Quote, TagParserQuote, None, Session)
	msid_names = {}
	assetContName = 'SC_Select_MSID_Cont' if Product.Attr('SC_Product_Type').GetValue() != "Renewal" else 'SC_Models_Scope_Renewal'
	#assetContainerRows = Product.GetContainerByName("SC_Select_MSID_Cont").Rows
	assetContainerRows = Product.GetContainerByName(assetContName).Rows
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
		msidList = []
		if Assets.Rows.Count == 0:
			for asset in assetContainerRows:
				#check msid is already added
				if asset['MSIDs'] in msidList:
					continue
				if asset.IsSelected == True:
					msidList.append(asset['MSIDs'])
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
			##else:
			Assets.Calculate()
		else:
			#Msids = Product.GetContainerByName('SC_Select_MSID_Cont')
			Msids = Product.GetContainerByName(assetContName)
			unselected_msids_list = [ i['MSIDs'] for i in Msids.Rows if i.IsSelected == False]
			unselected_msids_list = list(set(unselected_msids_list))
			selected_msids_list = [ i['MSIDs'] for i in Msids.Rows if i.IsSelected == True]
			selected_msids_list = list(set(selected_msids_list))
			#remove duplicate msid from the unselected msid list
			for msid in unselected_msids_list:
				if msid in selected_msids_list:
					unselected_msids_list.remove(msid)
			Assets = Product.GetContainerByName('Asset_details_ServiceProd')
			selected_assets = [i['MSID'] for i in Assets.Rows]
			asset_delete_ids = [i.RowIndex for i in Assets.Rows if i['MSID'] in unselected_msids_list]
			""""if len(asset_delete_ids) > 0:
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
					#check msid is already added
					if selected_msid in msidList:
						continue
					if selected_msid not in selected_assets:
						msidList.append(selected_msid)
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
				Assets.Calculate()
	else:
		Msids = Product.GetContainerByName(assetContName)
		unselected_msids_list = [ i['MSIDs'] for i in Msids.Rows if i.IsSelected == False]
		Assets = Product.GetContainerByName('Asset_details_ServiceProd')
		asset_delete_ids = [i.RowIndex for i in Assets.Rows if i['MSID'] in unselected_msids_list]
		if len(asset_delete_ids) > 0:
			asset_delete_ids.sort(reverse=True)
			for x in asset_delete_ids:
				Assets.DeleteRow(x)
	#else:
	#	Assets = Product.GetContainerByName('Asset_details_ServiceProd')
	#	Assets.Rows.Clear()
	################
	if Product.Attr('EnabledServices_servprod').SelectedValue:
		Product.Attr('EnabledService_Entitlement').AssignValue(Product.Attr('EnabledServices_servprod').SelectedValue.Display)
	else:
		#Product.Messages.Add('Please select a Service Product.')
		pass
	############# So that enter logic for matrikon executes..
	Product.Attr('SC_HWOS_Service_Product_ScopeSummary').AssignValue(str(Product.Attr('EnabledService_Entitlement').GetValue()))
	if Product.Attr('EnabledService_Entitlement').GetValue() == 'Enabled Services - Enhanced':
		Product.Attr('L3_L4_FILE_MOVER_ESSENTIAL_enabledServicesModel').Access = AttributeAccess.Editable
	else:
		Product.Attr('Customer_has_cyber_enabledServicesModel').Access = AttributeAccess.ReadOnly
		
	############ SO that it refreshes the asssets container

	assets_container = Product.GetContainerByName('Asset_details_ServiceProd') #to be commented later
	service_product = Product.Attr('EnabledService_Entitlement').GetValue() #to be commented later
	exchange_rate = 1
	if Quote:
		exchange_rate = float(Quote.GetCustomField('Exchange Rate').Content)
	assets_container_update(assets_container,service_product,exchange_rate, Product.Attr('SC_Service_Product').GetValue())
	summ_cont = Product.GetContainerByName('ES_Asset_Summary')
	if summ_cont.Rows.Count > 0:
		summ_cont.Rows[0].Calculate()
	##############

	customer_has_cyber_refresh(entitlement_value,Customer_has_cyber_attr,enhanced_no_vse_attr,data_broker_attr)

	#################

	L3_L4_Refresh(L3_L4_Mover_Essential_attr,Customer_has_cyber_attr,essential_select_option_attr,data_broker_attr)

	#############################
	
	enhanced_no_vse_refresh(enhanced_no_vse_attr,essential_select_option_attr,data_broker_attr)

	####################
	#UDC calc START
	udc_calculation_refresh(per_device_hardcode_prices_query,entitlement_value,udc_data_base_query_value,recommended_udc_servers_attr,l3_l4_move_attr,Product,per_device)
			#UDC CALC END
	######################### UPDating licenses after udc update ###############3
	l3_l4_refresh(recommended_udc_servers_attr,l3_l4_move_attr,Product)

	#Matrix License
	per_device_for_matrikon = float(per_device_for_matrikon/2) if Product.Attr('SC_Service_Product').GetValue() =="System Evolution Program" else per_device_for_matrikon
	matrikon_refresh(data_broker_attr,l3_l4_move_attr,per_device_for_matrikon,Product,exRate)

	##############
	customerCyberValue = Product.Attr('Customer_has_cyber_enabledServicesModel').Values
	isCustomerSelected = [value.IsSelected for value in customerCyberValue][0]
	if isCustomerSelected:
		Product.Attr("L3_L4_FILE_MOVER_ESSENTIAL_enabledServicesModel").Access = AttributeAccess.Editable
		Product.Attr('#_of_independent_"areas"_enabledServicesModel').Access = AttributeAccess.Editable
		Product.Attr("#_of_recommended_udc_servers_enabledServicesModel").Access = AttributeAccess.ReadOnly
		Product.Attr("#_l3_l4_file_move_licenses_enabledServicesModel").Access = AttributeAccess.ReadOnly
	else:
		Product.Attr("L3_L4_FILE_MOVER_ESSENTIAL_enabledServicesModel").Access = AttributeAccess.Editable
		Product.Attr('#_of_independent_"areas"_enabledServicesModel').Access = AttributeAccess.Editable
		Product.Attr("#_of_recommended_udc_servers_enabledServicesModel").Access = AttributeAccess.ReadOnly
		Product.Attr("#_l3_l4_file_move_licenses_enabledServicesModel").Access = AttributeAccess.ReadOnly
		Product.Attr("DurationOfPlan_enabledServices").Access = AttributeAccess.ReadOnly
   ###################
	if Product.Attr('EnabledService_Entitlement').GetValue() == 'Enabled Services - Enhanced':
		Product.Attr('L3_L4_FILE_MOVER_ESSENTIAL_enabledServicesModel').Access = AttributeAccess.Editable
	else:
		#for i in Product.Attr('L3_L4_FILE_MOVER_ESSENTIAL_enabledServicesModel').Values:
		#	i.IsSelected = False
		Product.Attr('Customer_has_cyber_enabledServicesModel').Access = AttributeAccess.ReadOnly

		Product.Attr('Customer_has_cyber_enabledServicesModel').Access = AttributeAccess.ReadOnly
		Product.Attr('#_of_independent_"areas"_enabledServicesModel').Access = AttributeAccess.Editable
		Product.Attr("#_of_recommended_udc_servers_enabledServicesModel").Access = AttributeAccess.ReadOnly
		Product.Attr("#_l3_l4_file_move_licenses_enabledServicesModel").Access = AttributeAccess.ReadOnly
		Product.Attr("DurationOfPlan_enabledServices").Access = AttributeAccess.ReadOnly
   ###################
	if Product.Attr('EnabledService_Entitlement').GetValue() == 'Enabled Services - Enhanced':
		Product.Attr('L3_L4_FILE_MOVER_ESSENTIAL_enabledServicesModel').Access = AttributeAccess.Editable
	else:
		#for i in Product.Attr('L3_L4_FILE_MOVER_ESSENTIAL_enabledServicesModel').Values:
		#	i.IsSelected = False
		Product.Attr('Customer_has_cyber_enabledServicesModel').Access = AttributeAccess.ReadOnly