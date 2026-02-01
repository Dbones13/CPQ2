import sys

def float_cast(n):
	if n == '' or n is None:
		Log.Write("Invalid argument for cast to float in GS_PMD_ReadAttrs, returned 0.00")
		return float(0)
	else:
		return float(n)

class AttrStorage:
	def __init__(self, Product):
		## Product: PMD System
		if Product.Name == "PMD System":
			### Begin: Controllers for Application Processing
			
			## Container: PMD_Controllers_2xProfibus_cont
			contr_2xprofib_cont = Product.GetContainerByName('PMD_Controllers_2xProfibus_cont').Rows[0]
			self.nrfce_profib_dp = float_cast(contr_2xprofib_cont.GetColumnByName('PMD_NRFCE_ProfibusDP').Value)
			self.rfce_profib_dp = float_cast(contr_2xprofib_cont.GetColumnByName('PMD_RFCE_ProfibusDP').Value)
			
			## Container: PMD_Controllers_2xProfinet_cont
			contr_2xprofin_cont = Product.GetContainerByName('PMD_Controllers_2xProfinet_cont').Rows[0]
			self.nrfce_profin_pn = float_cast(contr_2xprofin_cont.GetColumnByName('PMD_NRFCE_ProfinetPN').Value)
			
			## Container: PMD_Cabinet_Rack_Mounting_cont
			cabin_rack_mount_cont = Product.GetContainerByName('PMD_Cabinet_Rack_Mounting_cont').Rows[0]
			self.fce_cab_max8 = float_cast(cabin_rack_mount_cont.GetColumnByName('PMD_FCECabinet_Max8').Value)
			self.cab_max16 = float_cast(cabin_rack_mount_cont.GetColumnByName('PMD_Cabinet_Max16').Value)
			self.cab_1000mm = float_cast(cabin_rack_mount_cont.GetColumnByName('PMD_1000mm_Cabinet').Value)
			self.air_exch_90W = float_cast(cabin_rack_mount_cont.GetColumnByName('PMD_AirExchange_90W').Value)
			
			## Container: PMD_Field_Pow_Supp_Cont
			field_pow_supp_cont = Product.GetContainerByName('PMD_Field_Pow_Supp_Cont').Rows[0]
			self.red_24vdc_pwr_supp = float_cast(field_pow_supp_cont.GetColumnByName('PMD_24VDC_Redundant_Power Supply').Value)
			
			### End: Controllers for Application Processing
			### Begin: Miscelleanous Profibus_Profinet Components
			
			## Container: PMD_Profibus_Connectors_cont
			profib_conn_cont = Product.GetContainerByName('PMD_Profibus_Connectors_cont').Rows[0]
			self.profib_conn_rs485 = float_cast(profib_conn_cont.GetColumnByName('PMD_PROFIBUS_Connector_RS485').Value)
			self.profib_conn_rs485_PGSST =float_cast( profib_conn_cont.GetColumnByName('PMD_PROFIBUS connector RS485_PG-SST').Value)
			self.profib_fastconn_rs485 = float_cast(profib_conn_cont.GetColumnByName('PMD_PROFIBUS_FastConnet_ RS485').Value)
			self.profib_fastconn_rs485_PGSST = float_cast(profib_conn_cont.GetColumnByName('PMD_PROFIBUS_FastConnet_ RS485_PG-SST').Value)
			
			## Container: PMD_Profibus_Active_End_Resistors_cont
			profib_active_end_resist_cont = Product.GetContainerByName('PMD_Profibus_Active_End_Resistors_cont').Rows[0]
			self.active_te = float_cast(profib_active_end_resist_cont.GetColumnByName('PMD_Active_TE_for_Profibus').Value)
			
			## Container: PMD_Profibus_Repeaters_cont
			profib_repeat_cont = Product.GetContainerByName('PMD_Profibus_Repeaters_Cont').Rows[0]
			self.repeater = float_cast(profib_repeat_cont.GetColumnByName('PMD_Repeater_for_Profibus').Value)
			self.repeater_profib_diag = float_cast(profib_repeat_cont.GetColumnByName('PMD_Repeater_for_Profibus_Diagnosis').Value)
			
			## Container: PMD_Profibus_Coupler_cont
			profib_coupler_cont = Product.GetContainerByName('PMD_Profibus_Coupler_cont').Rows[0]
			self.dp_coupler = float_cast(profib_coupler_cont.GetColumnByName('PMD_DP_Coupler_ProfibusDP_Networks').Value)
			self.ab7646f_anybus = float_cast(profib_coupler_cont.GetColumnByName('PMD_AB7646-F_Anybus_X-gateway').Value)
			
			## Container: PMD_PN_DP_Gateways_cont
			pn_dp_gates_cont = Product.GetContainerByName('PMD_PN_DP_Gateways_cont').Rows[0]
			self.anybus_x = float_cast(pn_dp_gates_cont.GetColumnByName('PMD_Anybus_X-gateway').Value)
			
			## Container: PMD_Profibus_PA_cont
			profib_pa_cont = Product.GetContainerByName('PMD_Profibus_PA_cont').Rows[0]
			self.dp_pa_link = float_cast(profib_pa_cont.GetColumnByName('PMD_DP_PA_Link').Value)
			self.dp_pa_coupler = float_cast(profib_pa_cont.GetColumnByName('PMD_DP_PA_Coupler').Value)
			
			## Container: PMD_Optical_Link_Modules_cont
			optical_link_mods_cont = Product.GetContainerByName('PMD_Optical_Link_Modules_cont').Rows[0]
			self.olm_g11_glass_fo_cable = float_cast(optical_link_mods_cont.GetColumnByName('PMD_OLM_G11_Glass_FO_Cable').Value)
			self.olm_g12_glass_fo_cable = float_cast(optical_link_mods_cont.GetColumnByName('PMD_OLM_G12_Glass_FO_Cable').Value)
			self.olm_p11_plastic_fo_cable = float_cast(optical_link_mods_cont.GetColumnByName('PMD_OLM_P11_Plastic_FO_Cable').Value)
			self.olm_p12_plastic_fo_cable = float_cast(optical_link_mods_cont.GetColumnByName('PMD_OLM_P12_Plastic_FO_Cable').Value)
			
			## Container: PMD_Profinet_Switches_cont
			profin_switches_cont = Product.GetContainerByName('PMD_Profinet_Switches_cont').Rows[0]
			self.scalance_xc206_2 = float_cast(profin_switches_cont.GetColumnByName('PMD_SCALANCE_XC206-2_Switch').Value)
			self.scalance_x101_1 = float_cast(profin_switches_cont.GetColumnByName('PMD_SCALANCE X101-1').Value)
			
			### End: Miscelleanous Profibus_Profinet Components
			### Begin: PMD_Process_Interfacing_with_Extended_IO
			
			## Container: PMD_CC_Cards
			cc_cards_cont = Product.GetContainerByName('PMD_CC_Cards').Rows[0]
			self.analog_oc = float_cast(cc_cards_cont.GetColumnByName('PMD_Analog_OC').Value)
			self.analog_ic = float_cast(cc_cards_cont.GetColumnByName('PMD_Analog_IC').Value)
			self.binary_oc = float_cast(cc_cards_cont.GetColumnByName('PMD_Binary_OC').Value)
			self.power_boc_115v = float_cast(cc_cards_cont.GetColumnByName('PMD_Power_BOC_115V').Value)
			self.power_boc_230v = float_cast(cc_cards_cont.GetColumnByName('PMD_Power_BOC_230V').Value)
			self.binary_ic_16ch = float_cast(cc_cards_cont.GetColumnByName('PMD_Binary_IC_16Channel').Value)
			self.binary_ic_24ch = float_cast(cc_cards_cont.GetColumnByName('PMD_Binary_IC_24Channel').Value)
			self.power_bic_115v = float_cast(cc_cards_cont.GetColumnByName('PMD_Power_BIC_115V').Value)
			self.power_bic_230v = float_cast(cc_cards_cont.GetColumnByName('PMD_Power_BIC_230V').Value)
			#added by adarsh - PMD_IO_Space_req
			self.io_space_req = float_cast(cc_cards_cont.GetColumnByName('PMD_IO_Space_Req').Value)
			
			## Container: PMD_IO_Ext_Rack_cont
			io_ext_rack_cont = Product.GetContainerByName('PMD_IO_Ext_Rack_cont').Rows[0]
			self.er_ccct = float_cast(io_ext_rack_cont.GetColumnByName('PMD_ER_CCCT').Value)
			self.er_ccct_r = float_cast(io_ext_rack_cont.GetColumnByName('PMD_ER_CCCT_R').Value)
			
			## Container: PMD_Optional_Item_IO_cont
			opt_item_io_cont = Product.GetContainerByName('PMD_Optional_Item_IO_cont').Rows[0]
			self.ioc = float_cast(opt_item_io_cont.GetColumnByName('PMD_IOC').Value)
			self.ioc_aldix = float_cast(opt_item_io_cont.GetColumnByName('PMD_IOC_Aldix').Value)
			
			## Container: PMD_IO_Extension_Cabinet_cont
			io_ext_cab_cont = Product.GetContainerByName('PMD_IO_Extension_Cabinet_cont').Rows[0]
			self.dual_cc = float_cast(io_ext_cab_cont.GetColumnByName('PMD_Dual_Sided_CC').Value)
			self.single_cc_600 = float_cast(io_ext_cab_cont.GetColumnByName('PMD_Single_Sided_CC_600').Value)
			self.single_cc_400 = float_cast(io_ext_cab_cont.GetColumnByName('PMD_Single_Sided_CC_400').Value)
			self.furn_pie = float_cast(io_ext_cab_cont.GetColumnByName('PMD_Furnished_PIE').Value)
			self.wiremaking_ccb = float_cast(io_ext_cab_cont.GetColumnByName('PMD_Wiremaking_CCB').Value)
			self.wiremaking_half = float_cast(io_ext_cab_cont.GetColumnByName('PMD_Wiremaking_Half').Value)
			
			## Container: PMD_General_Inputs
			####gen_input_cont = Product.GetContainerByName('PMD_General_Inputs').Rows[0]
			####self.r_or_nr = gen_input_cont.GetColumnByName('PMD_Redundant_or_NonRedundant').Value
			####self.v_or_nv = gen_input_cont.GetColumnByName('PMD_Virtual_or_NVirtual').Value
			
			## Begin PMD Profibus Device SB Containers
			## Container: PMD_Profibus_Drives_cont
			self.prof_drives_devs = {}
			prof_drives_cont = Product.GetContainerByName('PMD_Profibus_Drives_Cont')
			for row in prof_drives_cont.Rows:
				if row.GetColumnByName('Device').Value == "PMD_ABB":
					self.prof_drives_devs["PMD_ABB"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_Siemans":
					self.prof_drives_devs["PMD_Siemans"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_Danfoss":
					self.prof_drives_devs["PMD_Danfoss"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_Lenze":
					self.prof_drives_devs["PMD_Lenze"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_VaconNX":
					self.prof_drives_devs["PMD_VaconNX"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_VaconCX":
					self.prof_drives_devs["PMD_VaconCX"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_Toshiba":
					self.prof_drives_devs["PMD_Toshiba"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_Control":
					self.prof_drives_devs["PMD_Control"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_Eurotherm":
					self.prof_drives_devs["PMD_Eurotherm"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_SIEISPA":
					self.prof_drives_devs["PMD_SIEISPA"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_PDL":
					self.prof_drives_devs["PMD_PDL"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_Telemecanique":
					self.prof_drives_devs["PMD_Telemecanique"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_SD700":
					self.prof_drives_devs["PMD_SD700"] = float_cast(1)
			
			## Container: PMD_Profibus_Links_and_Gateways_cont
			self.prof_links_gates_devs = {}
			prof_links_gates_cont = Product.GetContainerByName('PMD_Profibus_Links_and_Gateways_Cont')
			for row in prof_links_gates_cont.Rows:
				if row.GetColumnByName('Device').Value == "PMD_SiemensPA":
					self.prof_links_gates_devs["PMD_SiemensPA"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_SiemensDP":
					self.prof_links_gates_devs["PMD_SiemensDP"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_Siemens_20E":
					self.prof_links_gates_devs["PMD_Siemens_20E"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_GEASi":
					self.prof_links_gates_devs["PMD_GEASi"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_ASiDP":
					self.prof_links_gates_devs["PMD_ASiDP"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_CU9600":
					self.prof_links_gates_devs["PMD_CU9600"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_CANCBM":
					self.prof_links_gates_devs["PMD_CANCBM"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_SiemensCPU":
					self.prof_links_gates_devs["PMD_SiemensCPU"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_ToshibaS3":
					self.prof_links_gates_devs["PMD_ToshibaS3"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_GEFanuc":
					self.prof_links_gates_devs["PMD_GEFanuc"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_ASiCon":
					self.prof_links_gates_devs["PMD_ASiCon"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_SiemensS7":
					self.prof_links_gates_devs["PMD_SiemensS7"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_Anybus":
					self.prof_links_gates_devs["PMD_Anybus"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_SiemensIM":
					self.prof_links_gates_devs["PMD_SiemensIM"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_GE_FANUC":
					self.prof_links_gates_devs["PMD_GE_FANUC"] = float_cast(1)
			
			## Container: PMD_Profibus_Motor_Starters and_CD_cont
			self.prof_motor_start_cd_devs = {}
			prof_motor_start_cd_cont = Product.GetContainerByName('PMD_Profibus_Motor_Starters and_CD_cont')
			for row in prof_motor_start_cd_cont.Rows:
				if row.GetColumnByName('Device').Value == "PMD_ABBINSUM":
					self.prof_motor_start_cd_devs["PMD_ABBINSUM"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_SiemensSc":
					self.prof_motor_start_cd_devs["PMD_SiemensSc"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_UMC22":
					self.prof_motor_start_cd_devs["PMD_UMC22"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_SiemensSPD":
					self.prof_motor_start_cd_devs["PMD_SiemensSPD"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_UMC22V2":
					self.prof_motor_start_cd_devs["PMD_UMC22V2"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_Metso":
					self.prof_motor_start_cd_devs["PMD_Metso"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_Norgren":
					self.prof_motor_start_cd_devs["PMD_Norgren"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_ABBMNS":
					self.prof_motor_start_cd_devs["PMD_ABBMNS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_SiemensSSS":
					self.prof_motor_start_cd_devs["PMD_SiemensSSS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_MNSIS":
					self.prof_motor_start_cd_devs["PMD_MNSIS"] = float_cast(1)
			
			## Container: PMD_Other_Profibus_DP-Devices_cont
			self.prof_other_devs = {}
			prof_other_dev_cont = Product.GetContainerByName('PMD_Other_Profibus_DP-Devices_cont')
			for row in prof_other_dev_cont.Rows:
				if row.GetColumnByName('Device').Value == "PMD_AiRanger":
					self.prof_other_devs["PMD_AiRanger"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_Eilersen":
					self.prof_other_devs["PMD_Eilersen"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_RAUTE":
					self.prof_other_devs["PMD_RAUTE"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_HNC100":
					self.prof_other_devs["PMD_HNC100"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_VMAC260":
					self.prof_other_devs["PMD_VMAC260"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_Auma":
					self.prof_other_devs["PMD_Auma"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_EM277":
					self.prof_other_devs["PMD_EM277"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_DIRIS":
					self.prof_other_devs["PMD_DIRIS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_SiemensS7_315":
					self.prof_other_devs["PMD_SiemensS7_315"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_Vogel":
					self.prof_other_devs["PMD_Vogel"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_Numatics":
					self.prof_other_devs["PMD_Numatics"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_Rexroth":
					self.prof_other_devs["PMD_Rexroth"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_GWT":
					self.prof_other_devs["PMD_GWT"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_RexrothDC":
					self.prof_other_devs["PMD_RexrothDC"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_ELCIS":
					self.prof_other_devs["PMD_ELCIS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_BurnerCon":
					self.prof_other_devs["PMD_BurnerCon"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_ABBTE":
					self.prof_other_devs["PMD_ABBTE"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_applicom":
					self.prof_other_devs["PMD_applicom"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_VAMP255":
					self.prof_other_devs["PMD_VAMP255"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_DPSlaves":
					self.prof_other_devs["PMD_DPSlaves"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_SiemensDR":
					self.prof_other_devs["PMD_SiemensDR"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_AtlasCC":
					self.prof_other_devs["PMD_AtlasCC"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_IDEACOD":
					self.prof_other_devs["PMD_IDEACOD"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_MTS":
					self.prof_other_devs["PMD_MTS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_RauteDos":
					self.prof_other_devs["PMD_RauteDos"] = float_cast(1)
			
			## Container: PMD_Profibus_Modular_IO_Cont
			self.prof_mod_io_devs = {}
			prof_mod_io_cont = Product.GetContainerByName('PMD_Profibus_Modular_IO_Cont')
			for row in prof_mod_io_cont.Rows:
				if row.GetColumnByName('Device').Value == "PMD_GEFanucSS":
					self.prof_mod_io_devs["PMD_GEFanucSS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_GEFanucMS":
					self.prof_mod_io_devs["PMD_GEFanucMS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_GEFanucLS":
					self.prof_mod_io_devs["PMD_GEFanucLS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_MTLSS":
					self.prof_mod_io_devs["PMD_MTLSS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_MTLMS":
					self.prof_mod_io_devs["PMD_MTLMS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_MTLLS":
					self.prof_mod_io_devs["PMD_MTLLS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_SiemensETSS":
					self.prof_mod_io_devs["PMD_SiemensETSS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_SiemensETMS":
					self.prof_mod_io_devs["PMD_SiemensETMS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_SiemensETLS":
					self.prof_mod_io_devs["PMD_SiemensETLS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_SmETSS":
					self.prof_mod_io_devs["PMD_SmETSS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_SmETMS":
					self.prof_mod_io_devs["PMD_SmETMS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_SmETLS":
					self.prof_mod_io_devs["PMD_SmETLS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_ET200SSS":
					self.prof_mod_io_devs["PMD_ET200SSS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_ET200SMS":
					self.prof_mod_io_devs["PMD_ET200SMS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_ET200SLS":
					self.prof_mod_io_devs["PMD_ET200SLS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_VersamaxSS":
					self.prof_mod_io_devs["PMD_VersamaxSS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_VersamaxMS":
					self.prof_mod_io_devs["PMD_VersamaxMS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_VersamaxLS":
					self.prof_mod_io_devs["PMD_VersamaxLS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_BechoffSS":
					self.prof_mod_io_devs["PMD_BechoffSS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_BechoffMS":
					self.prof_mod_io_devs["PMD_BechoffMS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_BechoffLS":
					self.prof_mod_io_devs["PMD_BechoffLS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_WagoSS":
					self.prof_mod_io_devs["PMD_WagoSS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_WagoMS":
					self.prof_mod_io_devs["PMD_WagoMS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_WagoLS":
					self.prof_mod_io_devs["PMD_WagoLS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_PhoenixSS":
					self.prof_mod_io_devs["PMD_PhoenixSS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_PhoenixMS":
					self.prof_mod_io_devs["PMD_PhoenixMS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_PhoenixLS":
					self.prof_mod_io_devs["PMD_PhoenixLS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_PhoenixILSS":
					self.prof_mod_io_devs["PMD_PhoenixILSS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_PhoenixILMS":
					self.prof_mod_io_devs["PMD_PhoenixILMS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_PhoenixILLS":
					self.prof_mod_io_devs["PMD_PhoenixILLS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_SattConSS":
					self.prof_mod_io_devs["PMD_SattConSS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_SattConMS":
					self.prof_mod_io_devs["PMD_SattConMS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_SattConLS":
					self.prof_mod_io_devs["PMD_SattConLS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_SiemSS":
					self.prof_mod_io_devs["PMD_SiemSS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_SiemMS":
					self.prof_mod_io_devs["PMD_SiemMS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_SiemLS":
					self.prof_mod_io_devs["PMD_SiemLS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_CEAGSS":
					self.prof_mod_io_devs["PMD_CEAGSS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_CEAGMS":
					self.prof_mod_io_devs["PMD_CEAGMS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_CEAGLS":
					self.prof_mod_io_devs["PMD_CEAGLS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_TURCKSS":
					self.prof_mod_io_devs["PMD_TURCKSS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_TURCKMS":
					self.prof_mod_io_devs["PMD_TURCKMS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_TURCKLS":
					self.prof_mod_io_devs["PMD_TURCKLS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_CerabarPT":
					self.prof_mod_io_devs["PMD_CerabarPT"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_ValmetCT":
					self.prof_mod_io_devs["PMD_ValmetCT"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_PnixSS":
					self.prof_mod_io_devs["PMD_PnixSS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_PnixMS":
					self.prof_mod_io_devs["PMD_PnixMS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_PnixLS":
					self.prof_mod_io_devs["PMD_PnixLS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_ABBS800SS":
					self.prof_mod_io_devs["PMD_ABBS800SS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_ABBS800MS":
					self.prof_mod_io_devs["PMD_ABBS800MS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_ABBS800LS":
					self.prof_mod_io_devs["PMD_ABBS800LS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_HoneywellSS":
					self.prof_mod_io_devs["PMD_HoneywellSS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_HoneywellMS":
					self.prof_mod_io_devs["PMD_HoneywellMS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_HoneywellLS":
					self.prof_mod_io_devs["PMD_HoneywellLS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_HoneywellML":
					self.prof_mod_io_devs["PMD_HoneywellML"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_SIETCSS":
					self.prof_mod_io_devs["PMD_SIETCSS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_SIETCMS":
					self.prof_mod_io_devs["PMD_SIETCMS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_SIETCLS":
					self.prof_mod_io_devs["PMD_SIETCLS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_DPV1SS":
					self.prof_mod_io_devs["PMD_DPV1SS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_DPV1MS":
					self.prof_mod_io_devs["PMD_DPV1MS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_DPV1LS":
					self.prof_mod_io_devs["PMD_DPV1LS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_PepperlSS":
					self.prof_mod_io_devs["PMD_PepperlSS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_PepperlMS":
					self.prof_mod_io_devs["PMD_PepperlMS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_PepperlLS":
					self.prof_mod_io_devs["PMD_PepperlLS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_ET200iSPSS":
					self.prof_mod_io_devs["PMD_ET200iSPSS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_ET200iSPMS":
					self.prof_mod_io_devs["PMD_ET200iSPMS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_ET200iSPLS":
					self.prof_mod_io_devs["PMD_ET200iSPLS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_EXCOMSS":
					self.prof_mod_io_devs["PMD_EXCOMSS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_EXCOMMS":
					self.prof_mod_io_devs["PMD_EXCOMMS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_EXCOMLS":
					self.prof_mod_io_devs["PMD_EXCOMLS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_BK31XXXSS":
					self.prof_mod_io_devs["PMD_BK31XXXSS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_BK31XXXMS":
					self.prof_mod_io_devs["PMD_BK31XXXMS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_BK31XXXLS":
					self.prof_mod_io_devs["PMD_BK31XXXLS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_AXIOLINESS":
					self.prof_mod_io_devs["PMD_AXIOLINESS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_AXIOLINEMS":
					self.prof_mod_io_devs["PMD_AXIOLINEMS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_AXIOLINELS":
					self.prof_mod_io_devs["PMD_AXIOLINELS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_EXTSS":
					self.prof_mod_io_devs["PMD_EXTSS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_EXTMS":
					self.prof_mod_io_devs["PMD_EXTMS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_EXTLS":
					self.prof_mod_io_devs["PMD_EXTLS"] = float_cast(1)
			
			## Container: PMD_Profibus_Displays_cont
			self.prof_disp_devs = {}
			prof_disp_cont = Product.GetContainerByName('PMD_Profibus_Displays_Cont')
			for row in prof_disp_cont.Rows:
				if row.GetColumnByName('Device').Value == "PMD_Siebert":
					self.prof_disp_devs["PMD_Siebert"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_ESAVT":
					self.prof_disp_devs["PMD_ESAVT"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_PP17":
					self.prof_disp_devs["PMD_PP17"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_ProFace":
					self.prof_disp_devs["PMD_ProFace"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_SiebertS302":
					self.prof_disp_devs["PMD_SiebertS302"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_SiemPP7":
					self.prof_disp_devs["PMD_SiemPP7"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_SiemOP":
					self.prof_disp_devs["PMD_SiemOP"] = float_cast(1)
			
			## Container: PMD_Profinet_Device_Support_blocks_cont
			self.profin_sb_devs = {}
			profin_dev_supp_block_cont = Product.GetContainerByName('PMD_Profinet_Device_Support_blocks_cont')
			for row in profin_dev_supp_block_cont.Rows:
				if row.GetColumnByName('Device').Value == "PMD_DSBGEN":
					self.profin_sb_devs["PMD_DSBGEN"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_ET200MPSS":
					self.profin_sb_devs["PMD_ET200MPSS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_ET200MPMS":
					self.profin_sb_devs["PMD_ET200MPMS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_ET200MPLS":
					self.profin_sb_devs["PMD_ET200MPLS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_ET200SSS":
					self.profin_sb_devs["PMD_ET200SSS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_ET200SMS":
					self.profin_sb_devs["PMD_ET200SMS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_ET200SLS":
					self.profin_sb_devs["PMD_ET200SLS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_ET200SPSS":
					self.profin_sb_devs["PMD_ET200SPSS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_ET200SPMS":
					self.profin_sb_devs["PMD_ET200SPMS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_ET200SPLS":
					self.profin_sb_devs["PMD_ET200SPLS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_ET200MSS":
					self.profin_sb_devs["PMD_ET200MSS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_ET200MMS":
					self.profin_sb_devs["PMD_ET200MMS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_ET200MLS":
					self.profin_sb_devs["PMD_ET200MLS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_BL20SS":
					self.profin_sb_devs["PMD_BL20SS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_BL20MS":
					self.profin_sb_devs["PMD_BL20MS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_BL20LS":
					self.profin_sb_devs["PMD_BL20LS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_AXIOSS":
					self.profin_sb_devs["PMD_AXIOSS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_AXIOMS":
					self.profin_sb_devs["PMD_AXIOMS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_AXIOLS":
					self.profin_sb_devs["PMD_AXIOLS"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_ProV":
					self.profin_sb_devs["PMD_ProV"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_VaconFC":
					self.profin_sb_devs["PMD_VaconFC"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_900IO":
					self.profin_sb_devs["PMD_900IO"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_ABBFC":
					self.profin_sb_devs["PMD_ABBFC"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_IBPROXY":
					self.profin_sb_devs["PMD_IBPROXY"] = float_cast(1)
				if row.GetColumnByName('Device').Value == "PMD_PFCoupler":
					self.profin_sb_devs["PMD_PFCoupler"] = float_cast(1)
			
			## Container: PMD_Pulse_input_IO_KIT_PMD_Profibus_Profinet_cont
			pulse_inp_io_kit_profib_profin_cont = Product.GetContainerByName('PMD_Pulse_input_IO_KIT_PMD_Profibus_Profinet_cont').Rows[0]
			self.profib = float_cast(pulse_inp_io_kit_profib_profin_cont.GetColumnByName('PMD_PROFIBUS').Value)
			self.profin = float_cast(pulse_inp_io_kit_profib_profin_cont.GetColumnByName('PMD_PRIFINET').Value)
			self.add_2 = float_cast(pulse_inp_io_kit_profib_profin_cont.GetColumnByName('PMD_Add+2').Value)
			self.pi_card_pwr_supp = float_cast(pulse_inp_io_kit_profib_profin_cont.GetColumnByName('PMD_24VDC').Value)
			self.pfipb = float_cast(pulse_inp_io_kit_profib_profin_cont.GetColumnByName('PMD_PFIPB').Value)
			self.pfipn = float_cast(pulse_inp_io_kit_profib_profin_cont.GetColumnByName('PMD_PFIPN').Value)
			
			## Container: PMD_Cross_Connection_Cabinets_cont
			cross_conn_cab_cont = Product.GetContainerByName('PMD_Cross_Connection_Cabinets_Cont').Rows[0]
			self.ssccc = float_cast(cross_conn_cab_cont.GetColumnByName('PMD_SSCCC').Value)
			self.dsccc = float_cast(cross_conn_cab_cont.GetColumnByName('PMD_DSCCC').Value)
			self.sscc_1200 = float_cast(cross_conn_cab_cont.GetColumnByName('PMD_SSCC1200').Value)
			self.dscc_1200 = float_cast(cross_conn_cab_cont.GetColumnByName('PMD_DSCC1200').Value)
			self.sscc_482 = float_cast(cross_conn_cab_cont.GetColumnByName('PMD_SSCC482').Value)
			self.dscc_482 = float_cast(cross_conn_cab_cont.GetColumnByName('PMD_DSCC482').Value)
			self.sscc_d400 = float_cast(cross_conn_cab_cont.GetColumnByName('PMD_SSCCD400').Value)
			
			cross_conn_cab_cont_plcio = Product.GetContainerByName('PMD_Cross_Connection_Cabinets_Cont_PLCIO').Rows[0]
			self.ssccc_2 = float_cast(cross_conn_cab_cont_plcio.GetColumnByName('PMD_SSCCC').Value)
			self.dsccc_2 = float_cast(cross_conn_cab_cont_plcio.GetColumnByName('PMD_DSCCC').Value)
			self.sscc_1200_2 = float_cast(cross_conn_cab_cont_plcio.GetColumnByName('PMD_SSCC1200').Value)
			self.dscc_1200_2 = float_cast(cross_conn_cab_cont_plcio.GetColumnByName('PMD_DSCC1200').Value)
			self.sscc_482_2 = float_cast(cross_conn_cab_cont_plcio.GetColumnByName('PMD_SSCC482').Value)
			self.dscc_482_2 = float_cast(cross_conn_cab_cont_plcio.GetColumnByName('PMD_DSCC482').Value)
			self.sscc_d400_2 = float_cast(cross_conn_cab_cont_plcio.GetColumnByName('PMD_SSCCD400').Value)
			
			## Container: PMD_Cross_Connection_Cabling_Terminal_cont
			cross_conn_cabl_term_cont = Product.GetContainerByName('PMD_Cross_Connection_Cabling_Terminal_cont').Rows[0]
			self.tpctb = float_cast(cross_conn_cabl_term_cont.GetColumnByName('PMD_TPCTB').Value)
			self.wmpcp = float_cast(cross_conn_cabl_term_cont.GetColumnByName('PMD_WMPCP').Value)
			
			## Container: PMD_Cross_Connection_Cabling_Terminal_cont_PLCIO
			cross_conn_cabl_term_cont_plcio = Product.GetContainerByName('PMD_Cross_Connection_Cabling_Terminal_cont_PLCIO').Rows[0]
			self.tpctb_2 = float_cast(cross_conn_cabl_term_cont_plcio.GetColumnByName('PMD_TPCTB').Value)
			self.wmpcp_2 = float_cast(cross_conn_cabl_term_cont_plcio.GetColumnByName('PMD_WMPCP').Value)

			## Container: PMD_Field Power Supply_cont
			field_power_supply_cont = Product.GetContainerByName('PMD_Field Power Supply_cont').Rows[0]
			self.fps_10a = float_cast(field_power_supply_cont.GetColumnByName('PMD_FPS10A').Value)
			self.fps_20a = float_cast(field_power_supply_cont.GetColumnByName('PMD_FPS20A').Value)

			## Container: PMD_Field Power Supply_cont_PLCIO
			field_power_supply_cont_plcio = Product.GetContainerByName('PMD_Field Power Supply_Cont_PLCIO').Rows[0]
			self.fps_10a_2 = float_cast(field_power_supply_cont_plcio.GetColumnByName('PMD_FPS10A').Value)
			self.fps_20a_2 = float_cast(field_power_supply_cont_plcio.GetColumnByName('PMD_FPS20A').Value)
			
			## Container: PMD_System Power Supply_cont
			sys_power_supply_cont = Product.GetContainerByName('PMD_System Power Supply_cont').Rows[0]
			self.pdc_ds = float_cast(sys_power_supply_cont.GetColumnByName('PMD_PDCDS').Value)
			self.pds_230vac = float_cast(sys_power_supply_cont.GetColumnByName('PMD_230VAC').Value)
			self.pds_24vdc = float_cast(sys_power_supply_cont.GetColumnByName('PMD_24VDCPDS').Value)

			## Container: PMD_Add_on_Licenses
			add_on_licenses = Product.GetContainerByName('PMD_Add_on_Licenses').Rows[0]
			self.des_mod = float_cast(add_on_licenses.GetColumnByName('PMD_Design_Module').Value)
			self.des_mod_mr = float_cast(add_on_licenses.GetColumnByName('PMD_Design_Module_Monthly_Rent').Value)
						
			## Container: PMD_CE_UOC_Licences
			uoc_licenses = Product.GetContainerByName('PMD_CE_UOC_Licences').Rows[0]
			self.prc_sol = float_cast(uoc_licenses.GetColumnByName('PMD_Process_Solver').Value)

            ## Container: PMD_CE_IO_Rack_Cab
			pmd_plc_io_rack_cab = Product.GetContainerByName('PMD_CE_IO_Rack_Cab').Rows[0]
			self.pmd_plc_rack_8 = float_cast(pmd_plc_io_rack_cab.GetColumnByName('PMD_CE_PLC_8').Value)
			self.pmd_plc_rack_12 = float_cast(pmd_plc_io_rack_cab.GetColumnByName('PMD_CE_PLC_12').Value)
			self.pmd_plc_cab = float_cast(pmd_plc_io_rack_cab.GetColumnByName('PMD_CE_PLC_IO').Value)

			## Container: PMD_IO_ControlEdge_PLC_IO_Cards
			pmd_plc_io_cards = Product.GetContainerByName('PMD_IO_ControlEdge_PLC_IO_Cards').Rows[0]
			self.pmd_plc_univ_io = float_cast(pmd_plc_io_cards.GetColumnByName('PMD_Uni_IO').Value)
			self.pmd_plc_univ_ai = float_cast(pmd_plc_io_cards.GetColumnByName('PMD_Uni_AI').Value)
			self.pmd_plc_di_16 = float_cast(pmd_plc_io_cards.GetColumnByName('PMD_DI_16').Value)
			self.pmd_plc_di_32 = float_cast(pmd_plc_io_cards.GetColumnByName('PMD_DI_32').Value)
			self.pmd_plc_do_8 = float_cast(pmd_plc_io_cards.GetColumnByName('PMD_DO_8').Value)
			self.pmd_plc_do_32 = float_cast(pmd_plc_io_cards.GetColumnByName('PMD_DO_32').Value)
			self.pmd_io_space_2 = float_cast(pmd_plc_io_cards.GetColumnByName('PMD_IO_Space_Req_2').Value)