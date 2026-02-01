def calc_software_rtu_system(attrs, parts_dict):

     #CXCPQ-21353-
	 if int(attrs.Gas_and_Liquid_Meter_Run_License) > 0:
	     parts_dict["SP-MRUN01"] = {'Quantity' : int(attrs.Gas_and_Liquid_Meter_Run_License), 'Description': 'ONE METER RUN'}
	 #CXCPQ-21354-
	 if int(attrs.RTU_ELEPIU_Library_License) > 0:
	     parts_dict["SP-LEPIU1"] = {'Quantity' : int(attrs.RTU_ELEPIU_Library_License), 'Description': 'ELEPIU Library'}
	 #CXCPQ-21355-
	 if int(attrs.UpgradeKit_RTU_Non_Redundant) > 0:
	     parts_dict["SC-ZRTU01"] = {'Quantity' : int(attrs.UpgradeKit_RTU_Non_Redundant), 'Description': 'RTU Upgrade Kit for SC-UCMX01 to SC-UCMX02'}	 

	 return parts_dict