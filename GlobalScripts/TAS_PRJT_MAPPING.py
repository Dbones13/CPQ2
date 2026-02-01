import math
def assign_attributes(product, attribute_mapping):
	for attr_name, value in attribute_mapping.items():
			if value and value not in ('0.00', '0', '0.0'):
				product.Attributes.GetByName(attr_name).AssignValue(value)
			if attr_name in ('IS_SAT_Duration_in_Days', 'IS_No_of_Tema_Multis_(0-10)', 'IS_No_of_Gates_(0-100)', 'IS_No_of_EIS_(EBI)/Photo_ID_Training_Session', 'IS_No_of_Tema_Training_Session'):
				product.Attributes.GetByName(attr_name).AssignValue('0')

def select_display_value(product, attribute_mapping):
	for attr_name, value in attribute_mapping.items():
			if value:
				product.Attributes.GetByName(attr_name).SelectDisplayValue(value)

def map_tank_gauging(child_product, value_dict):
	mapping = {'TGE_Number of Horztal Tank w Other(Optilevel)Gauge': value_dict.get("Number_of_Horizontal_Tanks_with_Optilevel_Gauge"),'TGE_Number of Horizontal Tanks w RADAR(GWR) Gauges': value_dict.get("Number_of_ Horizontal_Tanks_with_GWR_Gauges"),'TGE_Number of Vertical Tanks with RADAR Gauge': value_dict.get("Number_of_Vertical_Tanks_with_RADAR_Gauge"),'TGE_Number of Vertical Tanks with SERVO Gauge': value_dict.get("Number_of_Vertical_Tanks_with_SERVO_Gauge")
	}
	assign_attributes(child_product, mapping)

def map_industrial_security(child_product, value_dict):
	integrate_doors = value_dict.get("Number_of_Doors_need_to_Integrate")
	workstation = value_dict.get("Additional_Workstation")
	card_mustering = value_dict.get("Number_of_ Card_Reader_for_Mustering")
	turnstiles_value = value_dict.get("Nos_Of _Turnstiles_Interface")
	input_integrates = ''
	if integrate_doors:
		input_integrates = str(float(integrate_doors) * 2)

	assign_attributes(child_product, {'IS_No_of_Door_Configuration_Field_Wiring_Types': integrate_doors,'IS_No_of_Digital_Inputs_(0-100)': input_integrates,'IS_No_of_Digital_Outputs_(0-100)': integrate_doors,'IS_No_of_Doors_(0-100)': integrate_doors,'IS_No_of_Badging_Stations_(0-5)': integrate_doors,'IS_No_of_Workstation_Configurations_(0-10)': workstation,'IS_No_of_Workstation_Wiring_Diagrams_(0-10)': workstation,'IS_No_of_TWIC_Readers_(0-20)': card_mustering,'IS_No_of_Cardholders_(0-10000)': card_mustering,'IS_No_of_Turnstiles_(0-100)': turnstiles_value, 'IS_No_of_Symbols_Notes_and_Legend_(0-2)': '2', 'IS_No_of_Riser_Diagrams_(0-250)':'5', 'IS_No_of_Door_Details_Drawings_(0-250)':'10', 'IS_No_of_Turnstile_Details_Drawings_(0-25)':'5', 'IS_No_of_Turnstile_Wiring_Detail_Drawings':'5', 'IS_FAT_Duration_in_Days':'5', 'IS_SAT_Duration_in_Days':'0', 'IS_No_of_Tema_Multis_(0-10)':'0', 'IS_No_of_Zones_(0-100)':'3', 'IS_No_of_Gates_(0-100)':'0', 'IS_No_of_Muster_Readers_(0-100)':'1', 'IS_No_of_Custom_EIS_Report_Configurations_(0-100)':'5', 'IS_No_of_Network_Switches_(0-100)':'1', 'IS_No_of_EIS_(EBI)_Servers_(0-10)':'1', 'IS_No_of_EIS_(EBI)_Workstations_(0-50)':'1', 'IS_No_of_Interfaces_to_Other_Systems_(0-15)':'1', 'IS_No_of_Graphics_(0-3000)':'20', 'IS_No_of_EIS_(EBI)/Photo_ID_Training_Session':'0', 'IS_No_of_Tema_Training_Session':'0', 'IS_No_of_Door_Wiring_Detail_Drawings':'5'})

	select_display_value(child_product, {'IS_Informal_Cust_EIS_(EBI)/Photo_ID_Training_Req':'No', 'IS_Informal_Customer_Tema_Training_Required':'No', 'IS_Standard_Customer_Training_Required':'No', 'IS_Wire_List_Required':'Yes', 'IS_SAT_Documentation_Required':'No', 'IS_Updated_Cutsheets_Required':'No', 'IS_Site_Acceptance_Test_Required':'No', 'IS_GES_Location':'GES China'})

def map_terminal_manager(child_product, value_dict):
	terminal_mode = str(value_dict.get("Terminal_Mode_of_Transport"))
	loading_unloading = value_dict.get("Terminal_Number_of_loading/unloading_bays")
	redundancy = value_dict.get("Terminal_Manager_redundancy?")
	batch_controller = value_dict.get("Terminal_Batch_Controller?")
	weighbridge = value_dict.get("Terminal_Weighbridge_Interface_required?")
	sap_erp = value_dict.get("Terminal_SAP_ERP_BSI_Interface_required?")
	card_reader = value_dict.get("Terminal_Card_Reader_Interface_required?")
	enterprise_level = value_dict.get("Terminal_to_be_integrated_at_Enterprise_level")
	web_portal = value_dict.get("Terminal_Web_Portal_required?")
	booking_application = value_dict.get("Terminal_that_require_Slot_Booking_Application")
									
	assign_terminal_attributes(child_product, {'Terminal_Mode_of_Transport': terminal_mode,'Terminal_Number_of_loading/unloading_bays': loading_unloading,'Terminal_Manager_redundancy?': redundancy,'Terminal_Batch_Controller?': batch_controller,'Terminal_Weighbridge_Interface_required?': weighbridge,'Terminal_SAP_ERP_BSI_Interface_required?': sap_erp,'Terminal_Card_Reader_Interface_required?': card_reader,'Terminal_to_be_integrated_at_Enterprise_level': enterprise_level,'Terminal_Web_Portal_required?': web_portal,'Terminal_that_require_Slot_Booking_Application': booking_application})

def assign_terminal_attributes(product, attribute_mapping):
	for attr_name, value in attribute_mapping.items():
		if value and attr_name == 'Terminal_Mode_of_Transport':
			terminal_mode_list = [mode.strip() for mode in value.split(',')]
			Log.Info('terminal_mode_list ' +str(terminal_mode_list))
			cont = product.Attr("Terminal_Mode_of_Transport").Values
			for data in cont:
				if data.Display in terminal_mode_list:
					data.IsSelected = True
				else:
					data.IsSelected = False
				Log.Info('terminal_mode_list1111 ' +str(data.Display) + str(data.IsSelected))
		elif value and attr_name in ["Terminal_Manager_redundancy?","Terminal_Batch_Controller?","Terminal_Weighbridge_Interface_required?","Terminal_SAP_ERP_BSI_Interface_required?","Terminal_Card_Reader_Interface_required?","Terminal_Web_Portal_required?"]:
			product.Attr(attr_name).AssignValue(value)
			product.Attr(attr_name).SelectDisplayValue(value)
			#product.Attributes.GetByName(attr_name).AssignValue(value)
			#product.Attributes.GetByName(attr_name).SelectDisplayValue(value)
		elif value and attr_name in ["Terminal_Number_of_loading/unloading_bays","Terminal_to_be_integrated_at_Enterprise_level","Terminal_that_require_Slot_Booking_Application"]:
			product.Attr(attr_name).AssignValue(value)
			#product.Attributes.GetByName(attr_name).AssignValue(value)
	product.ApplyRules()

def check_empty_value(value):
	return value if value else 0.00

def map_fire_detection(child_product, value_dict):
	horn_value = value_dict.get("Number_of_Horn /Beacons")
	smoke_value = value_dict.get("Number_of_Smoke_Detectors")
	gas_value = value_dict.get("Number_of_Gas_Detectors")
	manualcall_value = value_dict.get("Number_of_Manual_Call_point")
	manualcallexd_value = value_dict.get("Number_of_Manual_Call_Point(Exd)")
	flame_value = value_dict.get("Number_of_Flame_Detectors")
	heat_value = value_dict.get("Number_of_Heat_Detectors")
	sirens_value = value_dict.get("Number_of_Sirens")
	ESD_value = value_dict.get("Number_of_ESD_PB")

	num_xls_panels = value_dict.get("FDA Number of XLS Panels")
	num_xls_interfaces = value_dict.get("FDA Number of XLS Interfaces")
	num_ctrl_module_points = value_dict.get("FDA Number of Control module points")
	num_fnas = value_dict.get("FDA Number of FNAs")
	num_switches = value_dict.get("FDA Number of UL/nonUL Switches")
	num_converters = value_dict.get("FDA Number of Fiber to copper converters")
	num_graphics = value_dict.get("FDA Number of Graphics")

	total_pull_stations = int(check_empty_value(manualcall_value)) + int(check_empty_value(manualcallexd_value))
	total_module_points = int(check_empty_value(smoke_value)) + int(check_empty_value(gas_value)) + int(check_empty_value(flame_value))
	total_SLC_loops = round(
		(int(check_empty_value(smoke_value)) + int(check_empty_value(gas_value)) + int(check_empty_value(flame_value)) +
		int(check_empty_value(manualcall_value)) + int(check_empty_value(manualcallexd_value)) +
		int(check_empty_value(ESD_value)) + int(check_empty_value(horn_value)) +
		int(check_empty_value(heat_value))) / 124
	)
	total_standard_detectors = (
		int(check_empty_value(smoke_value)) + int(check_empty_value(gas_value)) + int(check_empty_value(flame_value)) +
		int(check_empty_value(manualcall_value)) + int(check_empty_value(manualcallexd_value)) +
		int(check_empty_value(ESD_value)) + int(check_empty_value(horn_value)) + int(check_empty_value(heat_value))
	)
	num_isolation_modules = total_SLC_loops + 1

	#Assign numeric/text attributes
	assign_attributes(child_product, {
		'FDA Number of horns': str(horn_value),
		'FDA Number of strobes': str(horn_value),
		'FDA Number of pull stations': str(total_pull_stations),
		'FDA Number of 4-20mA monitor module points': str(total_module_points),
		'FDA Number of SLC Loops': str(total_SLC_loops),
		'FDA Number of Standard Detectors': str(total_standard_detectors),

		'FDA Number of XLS Panels': str(num_xls_panels),
		'FDA Number of XLS Interfaces': str(num_xls_interfaces),
		'FDA Number of Control module points': str(num_ctrl_module_points),
		'FDA Number of FNAs': str(num_fnas),
		'FDA Number of UL/nonUL Switches': str(num_switches),
		'FDA Number of Fiber to copper converters': str(num_converters),
		'FDA Number of Graphics': str(num_graphics),
		'FDA Number of Isolation modules': str(num_isolation_modules)
	})

	#Select dropdown/display values
	select_display_value(child_product, {
		'FDA Functional Description Required': 'Yes',
		'FDA Interface Required': 'Yes',
		'FDA XLS Software Configuration Document Required': 'Yes',
		'FDA Panels Networked': 'Yes',
		'FDA Wire List Required': 'Yes',
		'FDA GES Location': 'GES China'
	})

def map_digital_video_manager(child_product, value_dict):
	hazardousPTZ_value = value_dict.get("Numbers_of_PTZ_Type_Camera_at_Hazardous_Area")
	safePTZ_value = value_dict.get("Numbers_of_PTZ_Type_Camera_at_Safe_Area")
	indoorPTZ_value = value_dict.get("Numbers_of_PTZ_Type_Camera_Indoor")
	hazardousFIXED_value = value_dict.get("Numbers_of_FIXED_Type_Camera_at_Hazardous_Area")
	safeFIXED_value = value_dict.get("Numbers_of_FIXED_Type_Camera_at_Safe_Area")
	indoorFIXED_value = value_dict.get("Numbers_of_FIXED_Type_Camera_Indoor")
	workstations_value = value_dict.get("Numbers_of_CCTV_Work_Stations")

	assign_attributes(child_product, {
		'DVM_Number_of_DVM_Workstations': workstations_value,
		'DVM_Number_of_Explosion_Proof_PTZ_Cameras': str(hazardousPTZ_value),
		'DVM_Number_of_Weather_Proof_PTZ_Cameras': str(safePTZ_value),
		'DVM_Number_of_Interior_PTZ_Cameras': str(indoorPTZ_value),
		'DVM_Number_of_Explosion_Proof_Fixed_Cameras': str(hazardousFIXED_value),
		'DVM_Number_of_Weather_Proof_Fixed_Cameras': str(safeFIXED_value),
		'DVM_Number_of_Interior_Fixed_Cameras': str(indoorFIXED_value)
	})
	select_display_value(child_product, {"DVM_Implementation_Methodology": "Standard Build Estimate",
        "DVM_GES_Location": "GES China"})
	total_cameras = round((int(check_empty_value(hazardousPTZ_value)) + int(check_empty_value(safePTZ_value)) + int(check_empty_value(indoorPTZ_value)) + int(check_empty_value(hazardousFIXED_value)) + int(check_empty_value(safeFIXED_value)) + int(check_empty_value(indoorFIXED_value)))/4)

	dvm_group_container = child_product.GetContainerByName('DVM_System_Group_Cont')
	for row in dvm_group_container.Rows:
		sub_product = row.Product
		if sub_product.Name == 'Digital Video Manager Group':
			attr = sub_product.Attributes.GetByName('DVM_4_Camera_Interface')
			if attr and total_cameras:
				attr.AssignValue(str(total_cameras))
				sub_product.ApplyRules()

def noncpq_prjt_mapping(product, quote):
	selectedProducts = []
	container = product.GetContainerByName('TAS_NON_CPQ_ITEMS')
	container.Rows.Clear()
	r2q_data = quote.GetGlobal('R2Qdata')
	containerDict = eval(r2q_data)
	for key, values in containerDict.items():
		if key == 'R2Q CE_System_Cont':
			for value_dict in values[0]:
				if not isinstance(value_dict, dict):
						continue
				if 'Selected_Products' in value_dict:
					selectedProducts.append(value_dict['Selected_Products'])
	if len(selectedProducts)>0:
		for prds in selectedProducts:
			if prds in ('Skid and Instruments', 'Small Volume Prover', 'Operator Training'):
				#Log.Info("tas--non111--"+str(prds))
				cont_prd = prds.replace(' ','_')
				if prds == 'Skid and Instruments':
					cont_prd = 'Skid_and_Field_Instruments_(loose_items)'
				elif prds == 'Operator Training':
					cont_prd = 'Operator_Training_(Class_room)'
				else:
					cont_prd = cont_prd
				new_row = container.AddNewRow(cont_prd + '_cpq',True)
				new_row['Part_Number'] = str(prds)
				#product.Attributes.GetByName('AR_TAS_LINE_ITEM').AssignValue(prds)
				#product.Attributes.GetByName('AR_TAS_LINE_ITEM').SelectDisplayValue(prds)

def r2q_to_prjt_mapping(product, quote):
	total = ''
	#check_expansion = product.ParseString('<*CTX( Product.RootProduct.Name.Translated )*>')
	#if check_expansion == 'New / Expansion Project' and quote.GetCustomField('R2QFlag').Content == 'Yes':
	r2q_data = quote.GetGlobal('R2Qdata')
	containerDict = eval(r2q_data)
	for key, values in containerDict.items():
		if key != 'R2Q CE_System_Cont' or not (len(values) > 1 and isinstance(values[1], list)):
			continue

		for value_dict in values[1]:
			if not isinstance(value_dict, dict):
				continue

			row = product.GetContainerByName('CE_SystemGroup_Cont').Rows[0]
			for attr in row.Product.Attributes:
				system_cont_rows = attr.Product.GetContainerByName('CE_System_Cont').Rows
				for child_row in system_cont_rows:
					for child_attr in child_row.Product.Attributes:
						child_product = child_attr.Product
						if child_product.Name == 'Tank Gauging Engineering':
							map_tank_gauging(child_product, value_dict)
						elif child_product.Name == 'Industrial Security (Access Control)':
							map_industrial_security(child_product, value_dict)
						elif child_product.Name == 'Digital Video Manager':
							map_digital_video_manager(child_product, value_dict)
						elif child_product.Name == 'Fire Detection & Alarm Engineering':
							map_fire_detection(child_product, value_dict)
						break
def r2q_to_prjt_terminal_mapping(product, quote):
	r2q_data = quote.GetGlobal('R2Qdata')
	containerDict = eval(r2q_data)
	for key, values in containerDict.items():
		if key != 'R2Q CE_System_Cont' or not (len(values) > 1 and isinstance(values[1], list)):
			continue

		for value_dict in values[1]:
			if not isinstance(value_dict, dict):
				continue
			for name,data in value_dict.items():
				if name == "Terminal_Mode_of_Transport":
					map_terminal_manager(product, value_dict)
					product.Attr('Terminal_value_set').AssignValue('')
					product.ParseString('<* ExecuteScript(Mode_of_transport) *>')
					break