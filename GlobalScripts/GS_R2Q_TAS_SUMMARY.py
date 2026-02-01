import GS_APIGEE_Integration_Util
excel_Url, header = GS_APIGEE_Integration_Util.GetR2QAPIGEEAuthDetails()

def getSFQuoteID():
	from CPQ_SF_IntegrationModules import CL_SalesforceIntegrationModules
	class_sf_integration_modules = CL_SalesforceIntegrationModules(Quote, TagParserQuote, None, Session)
	class_sf_integration_modules = CL_SalesforceIntegrationModules(Quote, TagParserQuote, None, Session)
	bearerToken = class_sf_integration_modules.get_auth2_token()
	headers = class_sf_integration_modules.get_authorization_header(bearerToken)
	query = "?q="+"select+Id+from+Quote+where+Quote_ID__c={cartId}+and+Owner_ID__c={ownerId}".format(cartId = str(Quote.QuoteId),ownerId = str(Quote.UserId))
	quoteID = class_sf_integration_modules.call_soql_api(headers, query)
	if len(quoteID.records) != 0:
			for q in quoteID.records:
				SFQuoteID = str(q.Id)
			return SFQuoteID

def get_tas_values(containerDict):
	SFQuoteId = getSFQuoteID()
	tank_gauging = vertical_tank = radar_gauge = servo_gauge = optilevel_gauge = hor_gwr_gauge = ""
	integrate_doors = workstation = card_mustering = turnstiles_value = ""
	no_entry_gate = exit_pcdet = no_exist_gate = entry_identification = entry_pcdet = exist_identification = ""
	weight_truck_loading = weight_rail_loading = weight_idenitification = ""
	personnel_access = photo_badging = bay_queue= seal_entry =""
	SVP_S005 = SVP_S120 = SVP_S085 = SVP_S050= SVP_S035= SVP_S025 = SVP_S015 = ""
	guide_wave = mscl_1_arm = mscl_2_arm = mscl_3_arm= mscl_4_arm = mscl_5_arm = mscl_6_arm = pressure_transmit =""
	termo_couple = temp_transmit = temp_gauges = pressure_transmit = pressure_relief = differnt_transmit = perssure_gauges = cb_plus_bc = ""
	Cctv_PTZ_Safe = Cctv_PTZ_Haz = Cctv_Fix_Indoor =Cctv_55_Screen_Count = Cctv_Fix_Safe =Cctv_Fix_Haz = Cctv_PTZ_Indoor = Cctv_Req = Cctv_WorkStation_Count =""
	FnG_Gas_Detectors_Count = FnG_Manual_Call_Point_Count = FnG_Flame_Detectors_Count = FnG_Smoke_Detector_Count = ""
	FnG_ESD_PB_Exd_Count = FnG_Horns_Beacons_Count = FnG_Heat_Detectors_Count = FnG_Scope = FnG_Call_Point_Exd_Count = FnG_Sirens_Count =  onsite_training = pcdet_val = turnstiles_interface = biometric_interface =""

	for key, values in containerDict.items():
		if key == 'R2Q CE_System_Cont':
			if len(values) > 1 and isinstance(values[1], list):
				for value_dict in values[1]:
					if not isinstance(value_dict, dict):
						continue
					tank_gauging = value_dict.get("Tank_Gauging_System_Required?", tank_gauging)
					vertical_tank = value_dict.get("Water_Measuremen_Required_for_Vertica_Tanks", vertical_tank)
					radar_gauge = value_dict.get("Number_of_Vertical_Tanks_with_RADAR_Gauge", radar_gauge)
					servo_gauge = value_dict.get("Number_of_Vertical_Tanks_with_SERVO_Gauge", servo_gauge)
					optilevel_gauge = value_dict.get("Number_of_Horizontal_Tanks_with_Optilevel_Gauge", optilevel_gauge)
					hor_gwr_gauge = value_dict.get("Number_of_ Horizontal_Tanks_with_GWR_Gauges", hor_gwr_gauge)

					integrate_doors = value_dict.get("Number_of_Doors_need_to_Integrate", integrate_doors)
					workstation = value_dict.get("Additional_Workstation", workstation)
					card_mustering = value_dict.get("Number_of_ Card_Reader_for_Mustering", card_mustering)
					turnstiles_value = value_dict.get("Nos_Of _Turnstiles_Interface", turnstiles_value)
					no_entry_gate = value_dict.get("Number_of_Entry_Gates", no_entry_gate)
					exit_pcdet = value_dict.get("Exit_Gate_PCDET_Required", exit_pcdet)
					no_exist_gate = value_dict.get("Number_of_Exit_Gates", no_exist_gate)
					entry_identification = value_dict.get("Entry_Identification_Method", entry_identification)
					entry_pcdet = value_dict.get("Entry_Gate_PCDET_Required", entry_pcdet)
					exist_identification = value_dict.get("Exit_Identification_Method", exist_identification)
					weight_truck_loading = value_dict.get("Number_of_WeighBridge_for_Truck_Loading", weight_truck_loading)
					weight_rail_loading = value_dict.get("Number_of_WeighBridge_for_Rail_Loading", weight_rail_loading)
					weight_idenitification = value_dict.get("Identification_method", weight_idenitification)
					personnel_access = value_dict.get("Personnel_Access_Required", personnel_access)
					photo_badging = value_dict.get("Photo_ID_Badging_Workstation_and_Printer", photo_badging)
					bay_queue = value_dict.get("Number_of_Bay_Queue_Display_Required", bay_queue)
					seal_entry = value_dict.get("Seal_Entry_Required", seal_entry)
					pcdet_val = value_dict.get("PCDET_Required", pcdet_val)
					turnstiles_interface = value_dict.get("Nos_Of _Turnstiles_Interface", turnstiles_interface)
					biometric_interface = value_dict.get("Nos_Of_Biometric_Access_Interface", biometric_interface)

					SVP_S005 = value_dict.get("Number_of_SVP_S005", SVP_S005)
					SVP_S015 = value_dict.get("Number_of_SVP_S015", SVP_S015)
					SVP_S025 = value_dict.get("Number_of_SVP_S025", SVP_S025)
					SVP_S035 = value_dict.get("Number_of_SVP_S035", SVP_S035)
					SVP_S050 = value_dict.get("Number_of_SVP_S050", SVP_S050)
					SVP_S085 = value_dict.get("Number_of_SVP_S085", SVP_S085)
					SVP_S120 = value_dict.get("Number_of_SVP_S120", SVP_S120)

					guide_wave = value_dict.get("Number_Of_Guided_Wave_Radar", guide_wave)
					mscl_1_arm = value_dict.get("MSCL_1_Arm_BCU", mscl_1_arm)
					mscl_2_arm = value_dict.get("MSCL_2_Arm_BCU", mscl_2_arm)
					mscl_3_arm = value_dict.get("MSCL_3_Arm_BCU", mscl_3_arm)
					mscl_4_arm = value_dict.get("MSCL_4_Arm_BCU", mscl_4_arm)
					mscl_5_arm = value_dict.get("MSCL_5_Arm_BCU", mscl_5_arm)
					mscl_6_arm = value_dict.get("MSCL_6_Arm_BCU", mscl_6_arm)
					differnt_transmit = value_dict.get("Nos_Of_Differential_Pressure_Transmitters", differnt_transmit)
					pressure_relief = value_dict.get("Nos_Of_Pressure_Relief_Value", pressure_relief)
					pressure_transmit = value_dict.get("Nos_Of_Pressure_Transmitters", pressure_transmit)
					temp_gauges = value_dict.get("Nos_Of_Temperature_Gauges", temp_gauges)
					temp_transmit= value_dict.get("Nos_Of_Temperature_Transmitters", temp_transmit)
					termo_couple= value_dict.get("Nos_Of_Termocouple", termo_couple)
					perssure_gauges= value_dict.get("No_Of_Pressure_Gauges", perssure_gauges)
					cb_plus_bc= value_dict.get("1010_CB_Plus_BC", cb_plus_bc)

					Cctv_PTZ_Safe = value_dict.get("Numbers_of_PTZ_Type_Camera_at_Safe_Area", Cctv_PTZ_Safe)
					Cctv_PTZ_Haz = value_dict.get("Numbers_of_PTZ_Type_Camera_at_Hazardous_Area", Cctv_PTZ_Haz)
					Cctv_Fix_Indoor = value_dict.get("Numbers_of_FIXED_Type_Camera_Indoor", Cctv_Fix_Indoor)
					Cctv_55_Screen_Count = value_dict.get("Numbers_of_55_Big_Screen_Monitor", Cctv_55_Screen_Count)
					Cctv_Fix_Safe = value_dict.get("Numbers_of_FIXED_Type_Camera_at_Safe_Area", Cctv_Fix_Safe)
					Cctv_Fix_Haz = value_dict.get("Numbers_of_FIXED_Type_Camera_at_Hazardous_Area", Cctv_Fix_Haz)
					Cctv_PTZ_Indoor = value_dict.get("Numbers_of_PTZ_Type_Camera_Indoor", Cctv_PTZ_Indoor)
					Cctv_Req = value_dict.get("CCTV_System_Required", Cctv_Req)
					Cctv_WorkStation_Count = value_dict.get("Numbers_of_CCTV_Work_Stations", Cctv_WorkStation_Count)

					FnG_Gas_Detectors_Count = value_dict.get("Number_of_Gas_Detectors", FnG_Gas_Detectors_Count)
					FnG_Manual_Call_Point_Count = value_dict.get("Number_of_Manual_Call_point", FnG_Manual_Call_Point_Count)
					FnG_Flame_Detectors_Count = value_dict.get("Number_of_Flame_Detectors", FnG_Flame_Detectors_Count)
					FnG_Smoke_Detector_Count = value_dict.get("Number_of_Smoke_Detectors", FnG_Smoke_Detector_Count)
					FnG_ESD_PB_Exd_Count = value_dict.get("Number_of_ESD_PB", FnG_ESD_PB_Exd_Count)
					FnG_Horns_Beacons_Count = value_dict.get("Number_of_Horn /Beacons", FnG_Horns_Beacons_Count)
					FnG_Heat_Detectors_Count = value_dict.get("Number_of_Heat_Detectors", FnG_Heat_Detectors_Count)
					FnG_Call_Point_Exd_Count = value_dict.get("Number_of_Manual_Call_Point(Exd)", FnG_Call_Point_Exd_Count)
					FnG_Sirens_Count = value_dict.get("Number_of_Sirens", FnG_Sirens_Count)
					FnG_Scope = value_dict.get("FG_System", FnG_Scope)

					onsite_training = value_dict.get("Onsite_Class_Room_Training_Required", onsite_training)
					
					
	Fin_JSON_Structure = {"Module": "TAS","ActionName":Product_Name,"CPQQuoteNumber": QuoteNumber,"SFQuoteID": SFQuoteId}
	if Product_Name == 'Industrial Security (Access Control)_TAGBIT':
		Fin_JSON_Structure["Entry_And_Exit_Gates"] = {"Entry_Gate_Count": no_entry_gate,"Exit_Gate_PCDET_Req": exit_pcdet,"Exit_Gate_Count": no_exist_gate,"Entry_Identification": entry_identification,"Entry_Gate_PCDET_Req": entry_pcdet,"Exit_Identification": exist_identification}
		Fin_JSON_Structure["Weigh_Bridge_Interface"] = {"Weigh_Bridge_Count_Truck_Loading": weight_truck_loading,"Weigh_Bridge_Count_Rail_Loading": weight_rail_loading,"Weigh_Bridge_Identification_Method": weight_idenitification, "PCDET_Required":pcdet_val}
		Fin_JSON_Structure["Personnal_Access_System"] = {"Doors_To_Integrate_Count": integrate_doors,"Personal_Access_Req": personnel_access,"Number_of_Card_Reader_for_Mustering": card_mustering,"Additional_Workstation": workstation,"Photo_ID_Badging_Workstation_and_Printer": photo_badging, "Nos_Of_Turnstiles_Interface":turnstiles_interface, "Nos_Of_Biometric_Access_Interface":biometric_interface}

	elif Product_Name == 'Fire Detection & Alarm Engineering_TAGBIT':
		Fin_JSON_Structure["Fire_And_Gas_System"] = {"FnG_Gas_Detectors_Count": FnG_Gas_Detectors_Count,"FnG_Manual_Call_Point_Count": FnG_Manual_Call_Point_Count,"FnG_Flame_Detectors_Count": FnG_Flame_Detectors_Count,"FnG_Smoke_Detector_Count": FnG_Smoke_Detector_Count,"FnG_ESD_PB_Exd_Count": FnG_ESD_PB_Exd_Count,"FnG_Horns_Beacons_Count": FnG_Horns_Beacons_Count,"FnG_Heat_Detectors_Count": FnG_Heat_Detectors_Count,"FnG_Manual_Call_Point_Count_Exd": FnG_Call_Point_Exd_Count,"FnG_Sirens_Count": FnG_Sirens_Count,"FnG_Scope": FnG_Scope}

	elif Product_Name == 'Tank Gauging Engineering_TAGBIT':
		Fin_JSON_Structure["Tank_Gauging_System"] = {"Hor_Tanks_With_GWR": hor_gwr_gauge,"Tank_Gauge_Req": tank_gauging,"Water_Mesure_Req": vertical_tank,"Ver_Tanks_With_Radar": radar_gauge,"Ver_Tanks_With_Servo": servo_gauge,"Hor_Tanks_With_Optilevel": optilevel_gauge}

	elif Product_Name == 'Digital Video Manager_TAGBIT':
		Fin_JSON_Structure["CCTV"] = {"Cctv_Fix_Indoor": Cctv_Fix_Indoor,"Cctv_PTZ_Safe": Cctv_PTZ_Safe,"Cctv_PTZ_Haz": Cctv_PTZ_Haz,"Cctv_55_Screen_Count": Cctv_55_Screen_Count,"Cctv_Fix_Safe": Cctv_Fix_Safe,"Cctv_Req": Cctv_Req,"Cctv_WorkStation_Count": Cctv_WorkStation_Count,"Cctv_Fix_Haz": Cctv_Fix_Haz,"Cctv_PTZ_Indoor": Cctv_PTZ_Indoor}

	elif Product_Name == 'Small Volume Prover_TAGBIT':
		Fin_JSON_Structure["Small_Volume_Prover"] = {"SVP_S085_12": SVP_S085,"SVP_S015_6": SVP_S015,"SVP_S050_8": SVP_S050,"SVP_S025_6": SVP_S025,"SVP_S035_8": SVP_S035,"SVP_S120_16": SVP_S120,"SVP_S005_3": SVP_S005}

	elif Product_Name == 'Skid and Instruments_TAGBIT':
		Fin_JSON_Structure["Skid_and_Instruments"] = {"MSCL_5_Arm_BCU": mscl_5_arm,"Number_Of_Guided_Wave_Radar": guide_wave,"MSCL_2_Arm_BCU": mscl_2_arm,"Nos_Of_Temperature_Transmitters": temp_transmit,"MSCL_4_Arm_BCU": mscl_4_arm,"Nos_Of_Temperature_Gauges": temp_gauges,"MSCL_1_Arm_BCU": mscl_1_arm,"Nos_Of_1010_CB_Plus_BC": cb_plus_bc,"Nos_Of_Pressure_Transmitters": pressure_transmit,"No_Of_Pressure_Gauges": perssure_gauges,"MSCL_6_Arm_BCU": mscl_6_arm,"Nos_Of_Termocouple": termo_couple,"MSCL_3_Arm_BCU": mscl_3_arm,"Nos_Of_Pressure_Relief_Value": pressure_relief,"Nos_Of_Differential_Pressure_Transmitters": differnt_transmit}

	elif Product_Name == 'Operator Training_TAGBIT':
		Fin_JSON_Structure["Operator_Training"] = {"Onsite_Class_Room_Training_Required": onsite_training}
	
	#Trace.Write('Final_JSON ==> ' + str(JsonHelper.Serialize(Fin_JSON_Structure)))
	return Fin_JSON_Structure
	
'''def get_tas_values(Product):
	SFQuoteId = getSFQuoteID()
	system_cont = Product.GetContainerByName('R2Q CE_System_Cont').Rows
	optilevel_value = gwr_value = radar_value = servo_value=integrate_doors=card_mustering=turnstiles_value=no_entry_gate=exit_pcdet=no_exist_gate=entry_identification=entry_pcdet=exist_identification=weight_truck_loading=weight_rail_loading=tank_gauging=vertical_tank=radar_gauge=servo_gauge=optilevel_gauge=hor_gwr_gauge= ''
	for row in system_cont:
		if row['Selected_Products']=='Industrial Security (Access Control)':
			Trace.Write("isnind--")
			for attr in row.Product.Attributes:
				personnel_access = get_attr_value('Personnel_Access_Required',attr)
				photo_badging = get_attr_value('Photo_ID_Badging_Workstation_and_Printer',attr)
				integrate_doors = get_attr_value('Number_of_Doors_need_to_Integrate',attr)
				workstation = get_attr_value("Additional_Workstation",attr)
				card_mustering = get_attr_value("Number_of_ Card_Reader_for_Mustering",attr)
				turnstiles_value = get_attr_value("Nos_Of _Turnstiles_Interface",attr)
				no_entry_gate = get_attr_value("Number_of_Entry_Gates",attr)
				exit_pcdet = get_attr_value("Exit_Gate_PCDET_Required",attr)
				no_exist_gate = get_attr_value("Number_of_Exit_Gates",attr)
				entry_identification = get_attr_value("Entry_Identification_Method",attr)
				entry_pcdet = get_attr_value("Entry_Gate_PCDET_Required",attr)
				exist_identification = get_attr_value("Exit_Identification_Method",attr)
				weight_truck_loading = get_attr_value("Number_of_WeighBridge_for_Truck_Loading",attr)
				weight_rail_loading = get_attr_value("Number_of_WeighBridge_for_Rail_Loading",attr)
				weight_idenitification = get_attr_value("Identification_method",attr)
		elif row['Selected_Products']=='Tank Gauging Engineering':
			for attr in row.Product.Attributes:
				tank_gauging = get_attr_value("Tank_Gauging_System_Required?",attr)
				optilevel_value = get_attr_value("Number_of_Horizontal_Tanks_with_Optilevel_Gauge",attr)
				gwr_value = get_attr_value("Number_of_ Horizontal_Tanks_with_GWR_Gauges",attr)
				radar_value = get_attr_value("Number_of_Vertical_Tanks_with_RADAR_Gauge",attr)
				servo_value = get_attr_value("Number_of_Vertical_Tanks_with_SERVO_Gauge",attr)
				hor_gwr_gauge = get_attr_value("Number_of_ Horizontal_Tanks_with_GWR_Gauges",attr)
				vertical_tank = get_attr_value("Water_Measuremen_Required_for_Vertica_Tanks",attr)
				
	Fin_JSON_Structure = {"Module":"TAS","Bay_Queue_Display":{"Bay_Queue_Disp_Req":"2"},"Entry_And_Exit_Gates":{"Entry_Gate_Count":no_entry_gate,"Exit_Gate_PCDET_Req":exit_pcdet,"Exit_Gate_Count":no_exist_gate,"Entry_Identification":entry_identification,"Entry_Gate_PCDET_Req":entry_pcdet,"Exit_Identification":exist_identification},"Fire_And_Gas_System":{"FnG_Gas_Detectors_Count":"1","FnG_Manual_Call_Point_Count":"1","FnG_Flame_Detectors_Count":"1","FnG_Smoke_Detector_Count":"1","FnG_ESD_PB_Exd_Count":"2","FnG_Horns_Beacons_Count":"1","FnG_Heat_Detectors_Count":"2","FnG_Call_Point_Exd_Count":"2","FnG_Sirens_Count":"2","FnG_Scope":""},"Weigh_Bridge_Interface":{"Weigh_Bridge_Count_Truck_Loading":weight_truck_loading,"Weigh_Bridge_Count_Rail_Loading":weight_rail_loading,"Weigh_Bridge_Identification_Method":weight_idenitification},"Tank_Gauging_System":{"Hor_Tanks_With_Radar":hor_gwr_gauge,"Tank_Gauge_Req":tank_gauging,"Water_Mesure_Req":vertical_tank,"Ver_Tanks_With_Radar":radar_gauge,"Ver_Tanks_With_Servo":servo_gauge,"Hor_Tanks_With_Other":optilevel_gauge},"CCTV":{"Cctv_Fix_Indoor":"1","Cctv_PTZ_Safe":"1","Cctv_PTZ_Haz":"1","Cctv_55_Screen_Count":"1","Cctv_Fix_Safe":"1","Cctv_Req":"No","Cctv_WorkStation_Count":"1","Cctv_Fix_Haz":"1","Cctv_PTZ_Indoor":"1"},"Skid and Instruments":{"MSCL_5_Arm_BCU":"2","Number_Of_Guided_Wave_Radar":"2","MSCL_2_Arm_BCU":"2","Nos_Of_Temperature_Transmitters":"2","MSCL_4_Arm_BCU":"2","Nos_Of_Temperature_Gauges":"2","MSCL_1_Arm_BCU":"2","1010_CB_Plus_BC":"2","Nos_Of_Pressure_Transmitters":"2","No_Of_Pressure_Gauges":"2","MSCL_6_Arm_BCU":"2","Nos_Of_Termocouple":"2","MSCL_3_Arm_BCU":"2","Nos_Of_Pressure_Relief_Value":"2","Nos_Of_Differential_Pressure_Transmitters":"2"},"Personnal_Access_System":{"Doors_To_Integrate_Count":integrate_doors,"Personal_Access_Req":personnel_access,"Number_of_ Card_Reader_for_Mustering":card_mustering,"Additional_Workstation":workstation,"Photo_ID_Badging_Workstation_and_Printer":photo_badging},"Seal_Entry":{"Seal_Entry_Req":"No"},"Small_Volume_Prover":{"SVP_S085_12":"2","SVP_S015_6":"2","SVP_S050_8":"2","SVP_S025_6":"2","SVP_S035_8":"2","SVP_S120_16":"1","SVP_S005_3":"2"},"CPQQuoteNumber":QuoteNumber,"SFQuoteID":SFQuoteId,"TAS_Status":"241","Operator Training":{"Onsite_Class_Room_Training_Required":"XLS140"}}
	
	Trace.Write('Final_JSON ==> ' + str(JsonHelper.Serialize(Fin_JSON_Structure)))
	return Fin_JSON_Structure '''
	
def get_attr_value(attr_name,attr):
	return attr.Product.Attr(attr_name).GetValue()

try:
	QuoteNumber = Param.QuoteNumber
	Quote = QuoteHelper.Edit(QuoteNumber) #Param.Quote
	#Log.Info("tas--action--"+str(Param.ActionName))
	Product_Name = Param.ActionName
	#for item in Quote.MainItems:
		#if item.PartNumber == 'PRJT R2Q':
			#Product = item.EditConfiguration()
	containerDict = Quote.GetGlobal('R2Qdata')
	APIGEE_Credentials = SqlHelper.GetFirst("Select Value from HPS_INTEGRATION_PARAMS Where [Key]='APIGEE_Credentials'").Value
	APIGEE_R2Q_URL = SqlHelper.GetFirst("Select Value from HPS_INTEGRATION_PARAMS Where [Key]='APIGEE_URL'").Value
	tokenUrl = "{}/v2/oauth/accesstoken".format(APIGEE_R2Q_URL)
	responseToken=AuthorizedRestClient.GetClientCredentialsGrantOAuthToken(APIGEE_Credentials,tokenUrl)
	final_request_body = get_tas_values(eval(containerDict))
	Req_Token = "{} {}".format(responseToken["token_type"], responseToken["access_token"])
	Url="https://it.api-beta.honeywell.com/cpq/r2q/sfdc/v1/cpqtor2q/tas/generate-part-summary"
	header = {"Content-Type" : "application/json","Authorization" : "{}".format(Req_Token),"HON-Org-Id" : "PMT-HPS" }
	res = RestClient.Post(Url,RestClient.SerializeToJson(str(final_request_body)),header)
	#Trace.Write("resp--"+str(res)+"---"+str(final_request_body))
	Log.Info('GS_R2Q_TAS_SUMMARY response-->>'+str(res)+"--request--"+str(final_request_body))
	#if res == 'Successfully generated the TAS output file':
	'''server_request ={'QuoteNumber':str(QuoteNumber),'UserName':str(User.UserName),'CartId':str(Quote.QuoteId),'Module':'TAS','RevisionNumber': str(Quote.RevisionNumber),'Action':'Update','Status':'Success','Action_List':[{'ActionName':str(Product_Name),'ScriptName':'GS_R2Q_TAS_SUMMARY'}]}
	res = RestClient.Post(excel_Url, RestClient.SerializeToJson(str(server_request)),header)
	Log.Info('GS_R2Q_TAS_SUMMARY server_request=>> Req: {} -- Res: {}'.format(server_request, res))'''
except Exception as ex:
	Log.Info('GS_R2Q_TAS_SUMMARY Error-->>'+str(ex))
	final_request_body={'QuoteNumber':str(Param.QuoteNumber),'CartId':str(Param.CartId),'RevisionNumber': str(Param.RevisionNumber),'UserName':str(User.UserName),'Module':'TAS','Action':'Update','Status':'Fail','Action_List':[{'ActionName':'TAS Module','ScriptName':'GS_R2Q_TAS_SUMMARY','ErrorMessage':str(ex)}]}
	RestClient.Post(excel_Url, RestClient.SerializeToJson(str(final_request_body)),header)