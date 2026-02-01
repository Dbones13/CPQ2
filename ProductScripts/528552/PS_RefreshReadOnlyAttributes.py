from GS_SESP_OTU_SFDC import OTU_SFDC
int_sfdc = OTU_SFDC()
msid = Product.Attr('MSIDChild_OTU_SESP').GetValue()
msid_lis = [str(msid)]
site = [str(Product.Attr('SITEC_OTU_SESP').GetValue())]
sfdc_res = int_sfdc.sfdc_response(Quote,Product,TagParserQuote,Session,msid_lis,site)

#Refresh readonly attributes
if sfdc_res.totalSize > 0:
    int_sfdc.fdm_auditTrailDevicePoints_sf_value(Product,'AduitTrailDevicePoints_FDMC_OTU_SESP','Field Device Manager',msid,['HC-AT0016', 'HC-AT0032', 'HC-AT0064', 'HC-AT0128', 'HC-AT0256', 'HC-AT0512', 'HC-AT1024', 'HC-AT2048', 'HC-AT4096', 'HC-AT8192', 'HC-AT016K'],sfdc_res)
    int_sfdc.eop_base_units_sf_value(Product,'BaseUnits_EOPC_OTU_SESP','Experion Off Process',msid,['EP-ETS001','EP-ETSU01','EP-ETSU05','EP-ETSU10','EP-ETSU50'],sfdc_res)
    int_sfdc.hs_experionHsPoints_sf_value(Product,'ExpHSPoints_HSC_OTU_SESP','HS',msid,['EP-HME01K','EP-HME02K','EP-HME05K','EP-HME08K','EP-HME100','EP-HME16K' ,'EP-HSTA01'],sfdc_res)
    int_sfdc.fdm_baseLicense_sf_value(Product,'FDMBaseLic_FDMC_OTU_SESP','Field Device Manager',msid,['HC-SV0001' , 'HC-SV0000'],sfdc_res)
    int_sfdc.fdm_fdmClients_sf_value(Product,'FDMClients_FDMC_OTU_SESP','Field Device Manager',msid,'HC-CLNT00',sfdc_res)
    int_sfdc.fdm_fdmMuxInterfaces_sf_value(Product,'MUXInterfaces_V1_FDMC_OTU_SESP','Field Device Manager',msid,['HC-HMOMX1','HC-HM0000'],sfdc_res)
    int_sfdc.fdm_fdmMuxInterfaces_sf_value1(Product,'MUXInterfaces_V2_FDMC_OTU_SESP',"Field Device Manager",msid,['HC-MM0000','HC-MMOMX1'],sfdc_res)
    int_sfdc.fdm_RciInterfaces__sf_value(Product,'RCIIntefaces_FDMC_OTU_SESP','Field Device Manager',msid,['HC-RIOMX1','HC-SM0000','HC-RI0000'],sfdc_res)
    int_sfdc.experion_serverRedundency_sf_value(Product,'ServerRedundancy_EXPC_OTU_SESP','Experion',msid,['EP-RBASE1','ES-RBASE1'],sfdc_res)
    int_sfdc.fdm_ServiceDevicePoints_sf_value(Product,'ServiceDevicePoints_FDMC_OTU_SESP','Field Device Manager',msid,['HC-SV0016', 'HC-SV0032', 'HC-SV0064', 'HC-SV0128', 'HC-SV0256', 'HC-SV0512', 'HC-SV1024', 'HC-SV2048', 'HC-SV4096', 'HC-SV8192', 'HC-SV016K'],sfdc_res)
else:
	Product.Attr('BaseUnits_EOPC_OTU_SESP').AssignValue('160')
	Product.Attr('ServerRedundancy_EXPC_OTU_SESP').AssignValue('No')