from GS_SESP_OTU_SFDC import OTU_SFDC
int_sfdc = OTU_SFDC()
msid = Product.Attr('MSIDChild_OTU_SESP').GetValue()
msid_lis = [str(msid)]
site = [str(Product.Attr('SITEC_OTU_SESP').GetValue())]
sfdc_res = int_sfdc.sfdc_response(Quote,Product,TagParserQuote,Session,msid_lis,site)
#Trace.Write("sfdc_res" + str(sfdc_res))
"""system_list = []
if sfdc_res is not None and sfdc_res != '':
	msid_1 = sfdc_res.records[0]
	product_code = msid_1['Parent']['ProductCode']
	query = SqlHelper.GetList("Select System_Name From SC_CT_System_Parent_Product_Code_Mapping Where Parent_Product_Code = '{}'".format(product_code))
	if query is not None:
		for row in query:
			system_list.append(row.System_Name)"""

def populate_dvm_sfdc_fields():
	int_sfdc.dvm_cameras_sf_value(Product,'Cameras_DVMC_OTU_SESP','Digital Video Manager',msid,'EP-DVML01',sfdc_res)
	int_sfdc.dvm_intExplr_sf_value(Product,'IntExplClients_DVMC_OTU_SESP','Digital Video Manager',msid,'EP-DVMIEC',sfdc_res)
	int_sfdc.common_calculation(Product,'EP_DVML01_DVMC_OTU_SESP','Digital Video Manager',msid,['EP-DVML01'],sfdc_res)
	int_sfdc.experion_serverRedundency_sf_value(Product,'EP_DVMR01_DVMC_OTU_SESP','Digital Video Manager',msid,['EP-DVMR01'],sfdc_res)
def populate_eop_sfdc_fields():
	int_sfdc.eop_base_units_sf_value(Product,'BaseUnits_EOPC_OTU_SESP','Experion Off Process',msid,['EP-ETS001','EP-ETSU01','EP-ETSU05','EP-ETSU10','EP-ETSU50'],sfdc_res)
def populate_hs_sfdc_fields():
	int_sfdc.hs_experionHsPoints_sf_value(Product,'ExpHSPoints_HSC_OTU_SESP','HS',msid,['EP-HME01K','EP-HME02K','EP-HME05K','EP-HME08K','EP-HME100','EP-HME16K'],sfdc_res)
	int_sfdc.experion_serverRedundency_sf_value(Product,'ServerRedundancy_HSC_OTU_SESP','HS',msid,['EP-HMRBAS'],sfdc_res)
	int_sfdc.common_calculation(Product,'Stations_HSC_OTU_SESP','HS',msid,['EP-HSTA01'],sfdc_res)
	int_sfdc.common_calculation(Product,'EP_HMBASE_HSC_OTU_SESP','HS',msid,['EP-HMBASE'],sfdc_res)
	serverRedundancy = Product.Attr('ServerRedundancy_HSC_OTU_SESP').GetValue()
	hsStations = int(float(Product.Attr('Stations_HSC_OTU_SESP').GetValue()))
	hsBase =  int(float(Product.Attr('EP_HMBASE_HSC_OTU_SESP').GetValue()))
	sqlQty = hsStations
	if hsBase > 0:
		sqlQty += 1
	if serverRedundancy == 'Yes':
		sqlQty += 1
	Product.Attr('MZSQLCL4_HSC_OTU_SESP').AssignValue(str(sqlQty))
	"""int_sfdc.hs_EP_BRWE06_sf_value(Product,'EPBRWE06_HSC_OTU_SESP','HS',msid,["EP-BRWE06","EP-BRWE05","EP-BRWE04","EP-BRWE03","EP-BRWE02" ,"EP-BRWE01","ES-BRWR06" ,"ES-BRWR05","ES-BRWR04" ,"ES-BRWR03","ES-BRWR02" , "ES-BRWR01"],sfdc_res)
	int_sfdc.hs_EP_BRVE06_sf_value(Product,'EPBRVE06_HSC_OTU_SESP','HS',msid,['EP-BRVE06','EP-BRVE05','EP-BRVE04','EP-BRVE03','EP-BRVE02','EP-BRVE01','ES-BRVR06','ES-BRVR05','ES-BRVR04','ES-BRVR03','ES-BRVR02','ES-BRVR01'],sfdc_res)
	int_sfdc.hs_EP_BRSE06_sf_value(Product,'EPBRSE06_HSC_OTU_SESP','HS',msid,['EP-BRSE06','EP-BRSE05','EP-BRSE04','EP-BRSE03','EP-BRSE02','EP-BRSE01','ES-BRSR06','ES-BRSR05',' ES-BRSR04','ES-BRSR03','ES-BRSR062','ES-BRSR01'],sfdc_res)"""
def populate_experion_sfdc_fields():
	int_sfdc.experion_experionProcessPoints_sf_value(Product,'ExpProcessPoints_EXPC_OTU_SESP','Experion',msid,['EP-DPR01K', 'EP-DPR02K', 'EP-DPR05K', 'EP-DPR100', 'EP-DPR10K', 'ES-DPR01K', 'ES-DPR02K', 'ES-DPR05K', 'ES-DPR100', 'ES-DPR10K'],sfdc_res)
	int_sfdc.experion_experionScadaPoints_sf_value(Product,'ExpSCADAPoints_EXPC_OTU_SESP','Experion',msid,['EP-DSC01K', 'EP-DSC02K', 'EP-DSC05K', 'EP-DSC100', 'EP-DSC10K', 'ES-DSC01K', 'ES-DSC02K', 'ES-DSC05K', 'ES-DSC100', 'ES-DSC10K'],sfdc_res)
	int_sfdc.experion_experionFlexStations_sf_value(Product,'FlexStations_EXPC_OTU_SESP','Experion',msid,['EP-STAT05', 'EP-STAT10','ES-STAT01','EP-STAT01'],sfdc_res)
	int_sfdc.experion_experionConsoleStations_sf_value(Product,'ConsoleStations_EXPC_OTU_SESP','Experion',msid,['EP-STAC05', 'EP-STAC10','EP-STAC01','ES-STAC01'],sfdc_res)
	int_sfdc.common_calculation(Product,'NoOfIntExpTps_EXPC_OTU_SESP','Experion',msid,["EP-CONTPS", "EP-SRVTPS"],sfdc_res)
	"""int_sfdc.experion_EP_BRWE06_sf_value(Product,'EPBRWE06_EXPC_OTU_SESP','Experion',msid,['EP-BRWE06', 'EP-BRWE05', 'EP-BRWE04', 'EP-BRWE03', 'EP-BRWE02', 'EP-BRWE01', 'ES-BRWR06', 'ES-BRWR05', 'ES-BRWR04', 'ES-BRWR03', 'ES-BRWR02', 'ES-BRWR01'],sfdc_res)
	int_sfdc.experion_EP_BRVE06_sf_value(Product,'EPBRVE06_EXPC_OTU_SESP','Experion',msid,['EP-BRVE06', 'EP-BRVE05', 'EP-BRVE04', 'EP-BRVE03', 'EP-BRVE02', 'EP-BRVE01', 'ES-BRVR06', 'ES-BRVR05', 'ES-BRVR04', 'ES-BRVR03', 'ES-BRVR02', 'ES-BRVR01'],sfdc_res)
	int_sfdc.experion_EP_BRSE06_sf_value(Product,'EPBRSE06_EXPC_OTU_SESP','Experion',msid,['EP-BRSE06', 'EP-BRSE05', 'EP-BRSE04', 'EP-BRSE03', 'EP-BRSE02', 'EP-BRSE01', 'ES-BRSR06', 'ES-BRSR05', 'ES-BRSR04', 'ES-BRSR03', 'ES-BRSR062', 'ES-BRSR01'],sfdc_res)"""
	int_sfdc.experion_serverRedundency_sf_value(Product,'ServerRedundancy_EXPC_OTU_SESP','Experion',msid,['EP-RBASE1','ES-RBASE1'],sfdc_res)
def populate_eserver_sfdc_fields():
	int_sfdc.eServer_PremiumAccesUser_sf_value(Product,'eServerPAU_ESSC_OTU_SESP','Eserver',msid,['EP-ESPREM', 'EP-ETPREM'],sfdc_res)
	"""int_sfdc.eServer_EP_BRWE06_sf_value(Product,'EPBRWE06_ESSC_OTU_SESP','Eserver',msid,['EP-BRWE06', 'EP-BRWE05', 'EP-BRWE04', 'EP-BRWE03', 'EP-BRWE02', 'EP-BRWE01', 'ES-BRWR06', 'ES-BRWR05', 'ES-BRWR04', 'ES-BRWR03', 'ES-BRWR02', 'ES-BRWR01'],sfdc_res)
	int_sfdc.eServer_EP_BRVE06_sf_value(Product,'EPBRVE06_ESSC_OTU_SESP','Eserver',msid,['EP-BRVE06', 'EP-BRVE05', 'EP-BRVE04', 'EP-BRVE03', 'EP-BRVE02', 'EP-BRVE01', 'ES-BRVR06', 'ES-BRVR05', 'ES-BRVR04', 'ES-BRVR03', 'ES-BRVR02', 'ES-BRVR01'],sfdc_res)
	int_sfdc.eServer_EP_BRSE06_sf_value(Product,'EPBRSE06_ESSC_OTU_SESP','Eserver',msid,['EP-BRSE06', 'EP-BRSE05', 'EP-BRSE04', 'EP-BRSE03', 'EP-BRSE02', 'EP-BRSE01', 'ES-BRSR06', 'ES-BRSR05', 'ES-BRSR04', 'ES-BRSR03', 'ES-BRSR02', 'ES-BRSR01'],sfdc_res)"""

"""def populate_simulationSystem_sfdc_fields():
	int_sfdc.simulation_EP_BRWE06_sf_value(Product,'EPBRWE06_SSC_OTU_SESP','Simulation System',msid,['EP-BRWE06', 'EP-BRWE05', 'EP-BRWE04', 'EP-BRWE03', 'EP-BRWE02', 'EP-BRWE01', 'ES-BRWR06', 'ES-BRWR05', 'ES-BRWR04', 'ES-BRWR03', 'ES-BRWR02', 'ES-BRWR01'],sfdc_res)
	int_sfdc.simulation_EP_BRVE06_sf_value(Product,'EPBRVE06_SSC_OTU_SESP','Simulation System',msid,['EP-BRVE06', 'EP-BRVE05', 'EP-BRVE04', 'EP-BRVE03', 'EP-BRVE02', 'EP-BRVE01', 'ES-BRVR06', 'ES-BRVR05', 'ES-BRVR04', 'ES-BRVR03', 'ES-BRVR02', 'ES-BRVR01'],sfdc_res)
	int_sfdc.simulation_EP_BRSE06_sf_value(Product,'EPBRSE06_SSC_OTU_SESP','Simulation System',msid,['EP-BRSE06', 'EP-BRSE05', 'EP-BRSE04', 'EP-BRSE03', 'EP-BRSE02', 'EP-BRSE01', 'ES-BRSR06', 'ES-BRSR05', 'ES-BRSR04', 'ES-BRSR03', 'ES-BRSR02', 'ES-BRSR01'],sfdc_res)"""

def populate_fdm_sfdc_fields():
	int_sfdc.fdm_baseLicense_sf_value(Product,'FDMBaseLic_FDMC_OTU_SESP','Field Device Manager',msid,['HC-SV0001' , 'HC-SV0000'],sfdc_res)
	int_sfdc.fdm_ServiceDevicePoints_sf_value(Product,'ServiceDevicePoints_FDMC_OTU_SESP','Field Device Manager',msid,['HC-SV0016', 'HC-SV0032', 'HC-SV0064', 'HC-SV0128', 'HC-SV0256', 'HC-SV0512', 'HC-SV1024', 'HC-SV2048', 'HC-SV4096', 'HC-SV8192', 'HC-SV016K'],sfdc_res)
	int_sfdc.fdm_auditTrailDevicePoints_sf_value(Product,'AduitTrailDevicePoints_FDMC_OTU_SESP','Field Device Manager',msid,['HC-AT0016', 'HC-AT0032', 'HC-AT0064', 'HC-AT0128', 'HC-AT0256', 'HC-AT0512', 'HC-AT1024', 'HC-AT2048', 'HC-AT4096', 'HC-AT8192', 'HC-AT016K'],sfdc_res)
	int_sfdc.fdm_RciInterfaces__sf_value(Product,'RCIIntefaces_FDMC_OTU_SESP','Field Device Manager',msid,['HC-RIOMX1','HC-SM0000','HC-RI0000'],sfdc_res)
	int_sfdc.fdm_fdmClients_sf_value(Product,'FDMClients_FDMC_OTU_SESP','Field Device Manager',msid,'HC-CLNT00',sfdc_res)
	int_sfdc.fdm_fdmMuxInterfaces_sf_value(Product,'MUXInterfaces_V1_FDMC_OTU_SESP','Field Device Manager',msid,['HC-HMOMX1','HC-HM0000'],sfdc_res)
	int_sfdc.fdm_fdmMuxInterfaces_sf_value1(Product,'MUXInterfaces_V2_FDMC_OTU_SESP',"Field Device Manager",msid,['HC-MM0000','HC-MMOMX1'],sfdc_res)

def populate_evst_sfdc_fields():
	int_sfdc.evst_serverRedundancy_sf_value(Product,'ServerRedundancy_ESTVC_OTU_SESP','ESVT',msid,['EP-RBASE1','ES-RBASE1'],sfdc_res)
	int_sfdc.evst_ExperionProcessPoints_sf_value(Product,'ExpProcessPoints_ESTVC_OTU_SESP','ESVT',msid,["EP-DPR01K", "EP-DPR02K", "EP-DPR05K", "EP-DPR100", "EP-DPR10K", "ES-DPR01K", "ES-DPR02K", "ES-DPR05K", "ES-DPR100", "ES-DPR10K"],sfdc_res)
	int_sfdc.evst_experionScadaPoints_sf_value(Product,'ExpSCADAPoints_ESTVC_OTU_SESP','ESVT',msid,["EP-DSC01K", "EP-DSC02K", "EP-DSC05K", "EP-DSC100", "EP-DSC10K", "ES-DSC01K", "ES-DSC02K", "ES-DSC05K", "ES-DSC100", "ES-DSC10K"],sfdc_res)
	int_sfdc.evst_FlexStations_sf_value(Product,'flexStations_ESTVC_OTU_SESP','ESVT',msid,["EP-STAT01", "EP-STAT05", "EP-STAT10", "ES-STAT01"],sfdc_res)
	int_sfdc.evst_consoleStations_sf_value(Product,'ConsoleStations_ESTVC_OTU_SESP','ESVT',msid,["EP-STAC01", "EP-STAC05", "EP-STAC10", "ES-STAC01"],sfdc_res)
	int_sfdc.common_calculation(Product,'NoOfIntExpTps_ESTVC_OTU_SESP','ESVT',msid,["EP-CONTPS", "EP-SRVTPS"],sfdc_res)
	"""int_sfdc.evst_ep_brwe06_sf_value(Product,'EPBRWE06_ESTVC_OTU_SESP','ESVT',msid,['EP-BRWE06', 'EP-BRWE05', 'EP-BRWE04', 'EP-BRWE03', 'EP-BRWE02', 'EP-BRWE01', 'ES-BRWR06', 'ES-BRWR05', 'ES-BRWR04', 'ES-BRWR03', 'ES-BRWR02', 'ES-BRWR01'],sfdc_res)
	int_sfdc.evst_ep_brse06_sf_value(Product,'EPBRVE06_ESTVC_OTU_SESP','ESVT',msid,['EP-BRVE06', 'EP-BRVE05', 'EP-BRVE04', 'EP-BRVE03', 'EP-BRVE02', 'EP-BRVE01', 'ES-BRVR06', 'ES-BRVR05', 'ES-BRVR04', 'ES-BRVR03', 'ES-BRVR02', 'ES-BRVR01'],sfdc_res)
	int_sfdc.evst_ep_brve06_sf_value(Product,'EPBRSE06_ESTVC_OTU_SESP','ESVT',msid,['EP-BRSE06', 'EP-BRSE05', 'EP-BRSE04', 'EP-BRSE03', 'EP-BRSE02', 'EP-BRSE01', 'ES-BRSR06', 'ES-BRSR05', 'ES-BRSR04', 'ES-BRSR03', 'ES-BRSR062', 'ES-BRSR01'],sfdc_res)"""
	#int_sfdc.evst_serverRedundancy_sf_value(Product,'ServerRedundancy_ESTVC_OTU_SESP',"ESVT",msid,['EP-RBASE1','ES-RBASE1'],sfdc_res)
	#int_sfdc.evst_mz_sqlcl4_sf_value(Product,'MZSQLCL4_ESTVC_OTU_SESP','ESVT',msid,[],sfdc_res)
	#int_sfdc.evst_ep_iaddvm_sf_value(Product,'EPCOAS16_ESTVC_OTU_SESP','ESVT',msid,[],sfdc_res)
	#int_sfdc.evst_ep_coaw10_sf_value(Product,'EPCOAW10_ESTVC_OTU_SESP','ESVT',msid,[],sfdc_res)

def populate_experionTPS_sfdc_fields():
	int_sfdc.experionTps_ep_coaw10_sf_value(Product,'EPABV020_TPSC_OTU_SESP','Experion-TPS',msid,'EP-ABV020',sfdc_res)
	int_sfdc.experionTPS_ep_coas16_sf_value(Product,'EPCONTPS_TPSC_OTU_SESP','Experion-TPS',msid,'EP-CONTPS',sfdc_res)
	#int_sfdc.experionTPS_ep_coas16_sf_value(Product,'EPSRVTPS_TPSC_OTU_SESP','Experion-TPS',msid,'EP-SRVTPS',sfdc_res)

def populate_ebr_sfdc_fields():
	int_sfdc.common_calculation(Product,'EPBRWE06_EBR_OTU_SESP','EBR',msid,["EP-BRWE06","EP-BRWE05","EP-BRWE04","EP-BRWE03","EP-BRWE02" ,"EP-BRWE01","ES-BRWR06" ,"ES-BRWR05","ES-BRWR04" ,"ES-BRWR03","ES-BRWR02" , "ES-BRWR01"],sfdc_res)
	int_sfdc.common_calculation(Product,'EPBRVE06_EBR_OTU_SESP','EBR',msid,['EP-BRVE06','EP-BRVE05','EP-BRVE04','EP-BRVE03','EP-BRVE02','EP-BRVE01','ES-BRVR06','ES-BRVR05','ES-BRVR04','ES-BRVR03','ES-BRVR02','ES-BRVR01'],sfdc_res)
	int_sfdc.common_calculation(Product,'EPBRSE06_EBR_OTU_SESP','EBR',msid,['EP-BRSE06','EP-BRSE05','EP-BRSE04','EP-BRSE03','EP-BRSE02','EP-BRSE01','ES-BRSR06','ES-BRSR05',' ES-BRSR04','ES-BRSR03','ES-BRSR062','ES-BRSR06'],sfdc_res)

###### Populating sfdc fields to all the child systems.
populate_dvm_sfdc_fields()
populate_eop_sfdc_fields()
populate_hs_sfdc_fields()
populate_experion_sfdc_fields()
populate_eserver_sfdc_fields()
##populate_simulationSystem_sfdc_fields()
populate_fdm_sfdc_fields()
populate_evst_sfdc_fields()
populate_experionTPS_sfdc_fields()
populate_ebr_sfdc_fields()