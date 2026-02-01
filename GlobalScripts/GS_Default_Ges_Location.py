Prod_Attr_map = {"Experion Enterprise System": "Experion_HS_Ges_Location_Labour","Virtualization System": "Virtualization_Ges_Location","C300 System": "C300_GES_Location","3rd Party Devices/Systems Interface (SCADA)": "SCADA_Ges_Location_Labour","Field Device Manager": "FDM_GES_Location","eServer System": "C300_GES_Location","ARO, RESS & ERG System": "ARO GES Location","Digital Video Manager": "DVM_GES_Location","Electrical Substation Data Collector": "C300_GES_Location","Simulation System": "C300_GES_Location","One Wireless System": "OWS_GES Location","Fire and Gas Consultancy Service": "FGC_GES_Location","Public Address General Alarm System": "PAGA_GES_Location","Process Safety Workbench Engineering": "PSW_GES_Location","Fire Detection & Alarm Engineering": "FDA GES Location","Industrial Security (Access Control)": "IS_GES_Location","Experion LX Generic": "Generic_Ges_Location_Labour","Experion HS System": "Experion_HS_Ges_Location_Labour","PlantCruise System": "PlantCruise_Ges_Location_Labour","HC900 System": "HC900_Ges_Location_Labour","Variable Frequency Drive System": "VFD_Ges_Location_Labour","Terminal Manager": "Terminal_Ges_Location_Labour","MasterLogic-50 Generic": "Generic_Ges_Location_Labour","MasterLogic-200 Generic": "Generic_Ges_Location_Labour","Tank Gauging Engineering": "TGE_GES Location","Metering Skid Engineering": "MSE GES Location","PRMS Skid Engineering": "PRMS GES Location","Gas MeterSuite Engineering - C300 Functions": "GAS MeterSuite GES Location","MS Analyser System Engineering": "MSASE_GES_Location","Liquid MeterSuite Engineering - C300 Functions": "LMS_GES_Location","MeterSuite Engineering - MSC Functions": "MSC GES Location","Experion MX System": "MX_HC_GES_Location","MXProLine System": "MXPro_GES_Location","ControlEdge PCD System": "PCD_Ges_Location_Labour","ControlEdge UOC System": "Default_Ges_Location","ControlEdge CN900 System":"Default_Ges_Location","ControlEdge PLC System": "Default_Ges_Location","Safety Manager ESD": "Default_Ges_Location","Safety Manager FGS": "Default_Ges_Location","Safety Manager BMS": "Default_Ges_Location","Safety Manager HIPPS": "Default_Ges_Location","ControlEdge RTU System": "Default_Ges_Location","PMD System": "Default_Ges_Location"}

Value_Code_map_1 = {"IN":"GESIndia","CN":"GESChina","RO":"GESRomania","UZ":"GESUzbekistan","EG":"GESEgypt"}
Value_Code_map_2 = {"IN":"GES India","CN":"GES China","RO":"GES Romania","UZ":"GES Uzbekistan","EG":"GES Egypt"}
Value_Code_map_3 = {"IN":"India","CN":"China","RO":"Romania","UZ":"Uzbekistan","EG":"Egypt"}
Value_Code_map_4 = {"IN":"GES_India","CN":"GES_China","RO":"GES_Romania","UZ":"GES_Uzbekistan","EG":"GES_Egypt"}

if Product.Attr("MSID_GES_Location").SelectedValue.ValueCode != 'None':
	New_Exp_Cnt = Product.GetContainerByName('CE_SystemGroup_Cont')
	if New_Exp_Cnt is not None:
		for sys_grp_row in New_Exp_Cnt.Rows:
			sys_grp_product = sys_grp_row.Product
			sys_grp_cnt = sys_grp_product.GetContainerByName('CE_System_Cont')
			for sys_grp_prods in sys_grp_cnt.Rows:
				if sys_grp_prods.GetColumnByName('Ges_Location_Defaulted').Value == 'N':
					quote_prds = sys_grp_prods.Product
					if quote_prds.Name in Prod_Attr_map:
						if quote_prds.Name in ("ControlEdge UOC System","ControlEdge CN900 System","ControlEdge PLC System","Safety Manager ESD","Safety Manager FGS","Safety Manager BMS","Safety Manager HIPPS","ControlEdge RTU System","PMD System","3rd Party Devices/Systems Interface (SCADA)"):
							default_val = Value_Code_map_1[Product.Attr("MSID_GES_Location").SelectedValue.ValueCode]
						elif quote_prds.Name in ("Experion MX System","MXProLine System"):
							default_val = Value_Code_map_3[Product.Attr("MSID_GES_Location").SelectedValue.ValueCode]
						elif quote_prds.Name in ("Fire and Gas Consultancy Service"):
							default_val = Value_Code_map_4[Product.Attr("MSID_GES_Location").SelectedValue.ValueCode]
						else:
							default_val = Value_Code_map_2[Product.Attr("MSID_GES_Location").SelectedValue.ValueCode]
						success = quote_prds.Attr(Prod_Attr_map[quote_prds.Name]).SelectValue(default_val)
						if success:
							quote_prds.ApplyRules()
						Trace.Write("Updated GES Location --> " + str(quote_prds.Name) + " --> " + str(default_val) + " --> " + str(success))
					sys_grp_prods.GetColumnByName('Ges_Location_Defaulted').Value = 'Y'