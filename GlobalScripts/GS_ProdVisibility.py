scopeval = Product.Attr('MIgration_Scope_Choices').GetValue()
# List of base products
baseProd = ['Graphics Migration','TCMI','FSC to SM','FSC to SM IO Migration','FDM Upgrade 1', 'Integrated Automation Assessment','XP10 Actuator Upgrade','CWS RAE Upgrade', 'QCS RAE Upgrade', 'CD Actuator I-F Upgrade', 'TPA/PMD Migration', 'Generic System Migration', 'FDM Upgrade 2', 'FDM Upgrade 3', 'ELEPIU ControlEdge RTU Migration Engineering','Trace Software', 'Virtualization System']
selectedprd = Product.Attr('MSID_PRDCHOICES').GetValue().split(', ')

# Retrieve values from attributes only once
attrs = {
	'current_tpn_release': 'MSID_Current_TPN_Release',
	'future_tpn_release': 'MSID_Future_TPN_Release',
	'current_experion_release': 'MSID_Current_Experion_Release',
	'fel_data_gathering_required': 'MSID_FEL_Data_Gathering_Required',
	'future_experion_release': 'MSID_Future_Experion_Release',
	'acceptance_test_required': 'MSID_Acceptance_Test_Required',
    'is_site_acceptance_test_required':'MSID_Is_Site_Acceptance_Test_Required',
	'is_switch_configuration_in_honeywell_scope': 'MSID_Is_Switch_Configuration_in_Honeywell_Scope',
	'is_fte_based_system_already_installed_on_site': 'MSID_Is_FTE_based_System_already_installed_on_Site',
	'construction_work_package_doc_req':'EHPM_HART_IO_Construction_Work_Package_doc_require',
	'construction_work_package_doc_prep':'Yes-No Selection','does_the_customer_want_honeywell':'ATTR_COMQESYORN',
	'regional_migration_princpal':'Regional_Migration_Principal_Efforts_Required',
    'Active_Service_Contract':'MSID_Active_Service_Contract'
}

values = {key: Product.Attributes.GetByName(attrs[key]).GetValue() for key in attrs}

# Append products based on conditions
if values['construction_work_package_doc_req']:
	baseProd.append('EHPM HART IO')
if values['construction_work_package_doc_prep']:
	baseProd.append('Orion Console')
if values['construction_work_package_doc_prep'] and values['does_the_customer_want_honeywell']:
	baseProd.append('LM to ELMM ControlEdge PLC')
if values['current_experion_release'] and values['future_experion_release']:
	baseProd.append('Non-SESP Exp Upgrade')

if values['current_tpn_release'] and values['future_tpn_release']:
	baseProd.append('LCN One Time Upgrade')

if scopeval in ['LABOR','HW/SW/LABOR']:
	baseProd.append('Graphics Migration')
	if values['future_experion_release'] and values['acceptance_test_required']:
		baseProd.append('CB-EC Upgrade to C300-UHIO')
	if values['current_experion_release'] and values['fel_data_gathering_required'] and values['future_experion_release'] and values['regional_migration_princpal']:
		baseProd.append('OPM')
	if values['is_fte_based_system_already_installed_on_site']:
		baseProd.extend(['LM to ELMM ControlEdge PLC', '3rd Party PLC to ControlEdge PLC/UOC'])
	if values['regional_migration_princpal']:
		baseProd.extend(['EBR','Virtualization System Migration','Orion Console','FSC to SM'])
	if values['fel_data_gathering_required'] and values['future_experion_release'] and values['acceptance_test_required'] and values['is_switch_configuration_in_honeywell_scope'] and values['regional_migration_princpal']:
		baseProd.append('TPS to Experion')
	if values['future_experion_release'] and values['is_switch_configuration_in_honeywell_scope'] and values['is_fte_based_system_already_installed_on_site'] and values['regional_migration_princpal']:
		baseProd.append('C200 Migration')
	if values['is_site_acceptance_test_required'] and values['future_experion_release'] and values['is_switch_configuration_in_honeywell_scope']:
		baseProd.append('xPM to C300 Migration')
	if values['fel_data_gathering_required'] and values['regional_migration_princpal'] and values['is_site_acceptance_test_required']:
		baseProd.append('ELCN')
	if values['fel_data_gathering_required'] and values['regional_migration_princpal']:
		baseProd.append('EHPM/EHPMX/ C300PM')
	if Product.Attr('MSID_Active_Service_Contract').Allowed and not values['Active_Service_Contract']:
		dellst=['CB-EC Upgrade to C300-UHIO','EHPM/EHPMX/ C300PM','OPM','LM to ELMM ControlEdge PLC', '3rd Party PLC to ControlEdge PLC/UOC','EBR','Virtualization System Migration','Orion Console','FSC to SM','TPS to Experion','C200 Migration','xPM to C300 Migration','ELCN']
		baseProd=list(set(baseProd)-set(dellst))
else:
	if values['current_experion_release'] and values['future_experion_release']:
		baseProd.append('OPM')
	if values['future_experion_release'] and values['is_switch_configuration_in_honeywell_scope']:
		baseProd.extend(['xPM to C300 Migration','C200 Migration'])
	if values['future_experion_release']:
		baseProd.extend(['TPS to Experion','CB-EC Upgrade to C300-UHIO'])
			 
	baseProd.extend(['LM to ELMM ControlEdge PLC', '3rd Party PLC to ControlEdge PLC/UOC','EBR','EHPM/EHPMX/ C300PM','ELCN','Virtualization System Migration'])
	baseProd.remove('Generic System Migration')


prdcont = Product.GetContainerByName('CONT_MSID_SUBPRD')
if prdcont.Rows.Count > 0:
	if scopeval not in ['LABOR']:
		baseProd.append('Spare Parts')
	'''for row in prdcont.Rows:
		if row['Selected_Products'] in selectedprd:
			selectedprd.remove(row['Selected_Products'])'''

# Remove duplicates by converting to set and back to list
visible_prd = set([prduct for prduct in baseProd if prduct in selectedprd])
Trace.Write("visible_prd-> "+str(visible_prd))
# Generate API response
ApiResponse = ApiResponseFactory.JsonResponse(visible_prd)