def assets_container_update(assets_container,service_product,exchange_rate=1,SESPName=''):
	per_device_database = SqlHelper.GetList("select Name,Price from SC_Hardcode_Price where Name in ('Enhanced-Servers','Enhanced-Workstations','Enhanced-Windows','Enhanced-TPN NODES','Enhanced-CONTROLLERS','Enhanced-Switches','Enhanced-SCADA','Enhanced-Safety Manager')")
	per_device = {}
	for i in per_device_database:
		per_device[i.Name] = float(i.Price) * exchange_rate
	pr_servers = per_device['Enhanced-Servers']
	pr_workstations = per_device['Enhanced-Workstations']
	pr_windows = per_device['Enhanced-Windows']
	pr_tpn = per_device['Enhanced-TPN NODES']
	pr_controllers = per_device['Enhanced-CONTROLLERS']
	pr_switches = per_device['Enhanced-Switches']
	pr_scada = per_device['Enhanced-SCADA']
	pr_safety = per_device['Enhanced-Safety Manager']
	if service_product == 'Enabled Services - Enhanced':
		for asset in assets_container.Rows:
			asset_list_price = (int(float(asset['Servers'])) * float(pr_servers)) + (int(float(asset['Workstations'])) * float(pr_workstations)) + (int(float(asset['Windows - Other'])) * float(pr_windows)) + (int(float(asset['TPN Nodes'])) * float(pr_tpn)) + (int(float(asset['Controllers'])) * float(pr_controllers)) + (int(float(asset['Switches'])) * float(pr_switches)) +  (int(float(asset['SCADA Servers'])) * float(pr_scada)) + (int(float(asset['Safety Manager'])) * float(pr_safety))
			asset['List Price'] = str(asset_list_price/2) if SESPName == 'System Evolution Program' else str(asset_list_price)
		else:
			assets_container.Calculate()
	elif service_product == 'Enabled Services - Essential':
		asset_per_device_essential = SqlHelper.GetFirst("select * from SC_HARDCODE_VALUES where Name = N'{0}'".format('Essentials % of Enhanced')).Value
		for asset in assets_container.Rows:
			asset_list_price = ( ( int(float(asset['Servers'])) * float(pr_servers)) + (int(float(asset['Workstations'])) * float(pr_workstations)) + (int(float(asset['Windows - Other'])) * float(pr_windows)) + (int(float(asset['TPN Nodes'])) * float(pr_tpn)) + (int(float(asset['Controllers'])) * float(pr_controllers)) + (int(float(asset['Switches'])) * float(pr_switches)) + (int(float(asset['SCADA Servers'])) * float(pr_scada)) + (int(float(asset['Safety Manager'])) * float(pr_safety)))  * float(asset_per_device_essential)
			asset['List Price'] = str(asset_list_price/2) if SESPName == 'System Evolution Program' else str(asset_list_price)
		else:
			assets_container.Calculate()

def customer_has_cyber_refresh(entitlement_value,Customer_has_cyber_attr,enhanced_no_vse_attr,data_broker_attr):
	if entitlement_value == 'Enabled Services - Enhanced':
		for i in Customer_has_cyber_attr.Values:
			if i.IsSelected == False:
				for j in enhanced_no_vse_attr.Values:
					j.IsSelected = True
			else:
				for j in enhanced_no_vse_attr.Values:
					j.IsSelected = False
	elif entitlement_value == 'Enabled Services - Essential':
		for i in enhanced_no_vse_attr.Values:
			i.IsSelected = False
		for k in data_broker_attr.Values:
			k.IsSelected = False

def L3_L4_Refresh(L3_L4_Mover_Essential_attr,Customer_has_cyber_attr,essential_select_option_attr,data_broker_attr):
	for i in L3_L4_Mover_Essential_attr.Values:
		if i.IsSelected == True:
			for j in Customer_has_cyber_attr.Values:
				if j.IsSelected == False:
					for k in essential_select_option_attr.Values:
						k.IsSelected = True
				else:
					for i in essential_select_option_attr.Values:
						i.IsSelected = False
		else:
			for i in essential_select_option_attr.Values:
				i.IsSelected = False
			for k in data_broker_attr.Values:
					k.IsSelected = False

def enhanced_no_vse_refresh(enhanced_no_vse_attr,essential_select_option_attr,data_broker_attr):
	for i in enhanced_no_vse_attr.Values:
		for j in essential_select_option_attr.Values:
			if i.IsSelected == True or j.IsSelected == True:
				for k in data_broker_attr.Values:
					k.IsSelected = True
			else:
				for k in data_broker_attr.Values:
					k.IsSelected = False

def udc_calculation_refresh(per_device_hardcode_prices_query,entitlement_value,udc_data_base_query_value,recommended_udc_servers_attr,l3_l4_move_attr,Product,per_device):
	servers = Product.GetContainerByName('Asset_details_ServiceProd').TotalRow['Servers']
	workstations = Product.GetContainerByName('Asset_details_ServiceProd').TotalRow['Workstations']
	window = Product.GetContainerByName('Asset_details_ServiceProd').TotalRow['Windows - Other']
	if 1 == 1:
		val = float(servers) + float(workstations) + float(window)
		if float(val) >=  float(udc_data_base_query_value):
			new_udc = float(val) / float(udc_data_base_query_value)
			recommended_udc_servers_attr.AssignValue('')
			if float(new_udc)-int(new_udc)>0: # CXCPQ-90635:07/15/2024 Added logic to fix round up issue
				new_udc=int(new_udc)+1
			else:
				new_udc=int(new_udc)
			recommended_udc_servers_attr.AssignValue(str(new_udc))
		elif float(val) > 0 and float(val) < float(udc_data_base_query_value):
			recommended_udc_servers_attr.AssignValue('1')
		else:
			recommended_udc_servers_attr.AssignValue('0')

def l3_l4_refresh(recommended_udc_servers_attr,l3_l4_move_attr,Product):
	independantArea = Product.Attr('#_of_independent_"areas"_enabledServicesModel').GetValue()
	UDEService = recommended_udc_servers_attr.GetValue()
	if independantArea != "" and independantArea is not None and not independantArea.isalpha() :
		if UDEService != '':
			if float(independantArea) > float(UDEService):
				l3_l4_move_attr.AssignValue(str(round(float(independantArea),2)))
			else:
				l3_l4_move_attr.AssignValue(str(round(float(UDEService),2)))
		else:
			l3_l4_move_attr.AssignValue(str(round(float(independantArea),2)))
	else:
		Product.Attr('#_of_independent_"areas"_enabledServicesModel').AssignValue('0.00')
		l3_l4_move_attr.AssignValue(str(round(float(UDEService),2)))

def matrikon_refresh(data_broker_attr,l3_l4_move_attr,per_device_for_matrikon,Product,exchange_rate):
	qty = 0
	for i in data_broker_attr.Values:
		if i.IsSelected == True:
			if l3_l4_move_attr.GetValue() != '':
				qty = float((l3_l4_move_attr).GetValue())
			list_price = qty * per_device_for_matrikon
			Product.Attr('Matrix License').AssignValue(str(round(float(list_price)*exchange_rate,2)))
		else:
			qty = 0
			Product.Attr('Matrix License').AssignValue('0.00')