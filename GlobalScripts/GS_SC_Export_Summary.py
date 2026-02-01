jsonObject = {}
templateName = ''
### Updated New logic to eliminate if-elif-else -Lahu- -start ####
if (Param is not None and Param.name is not None):
	name = str(Param.name)
	templateNames={'MES_Renewal_Summary':'SC_MES_Renewal_Summary',
				'SC_ThirdParty_Renewal_Summary':'SC_ThirdParty_Renewal_Summary',
				'Cyber_Renewal_Summary':'SC_Cyber_Renewal_Summary',
				'Hardware_Refresh_Renewal_Summary':'SC_HardwareRefresh_Renewal_Summary',
				'Hardware_Warranty_Renewal_Summary':'SC_HardwareWarranty_Renewal_Summary',
				'Renewal_Summary':'SC_SESP_Renewal_Summary',
				'BGP_Renewal_Summary':'SC_BGP_Renewal_Summary',
				'Honeywell_Digital_Prime':'SC_HDP_Renewal_Summary',
				'QCS_4_0':'SC_QCS_Renewal_Summary',
				'RQUP_Renewal_Summary':'SC_RQUP_Renewal_Summary',
				'CBM_Renewal_Summary':'CBM_Renewal_summary',
				'SC_ES_Renewal_Summary':'SC_ES_Renewal_Summary',
				'SC_Parts_Management_Summary':'SC_PartsManagement_Renewal_Summary',
				'SC_Parts_Replacement_Summary':'SC_PartsReplacement_Renewal_Summary',
				'SC_Labor_Module_Renewal_Summary':'SC_Labor_Renewal_Summary',
				'QT_SC_Trace_Renewal_Summary':'SC_Trace_Renewal_Summary',
				'Workforce_Excellence_Program':'WEP_RenewalSummary',
                'SC_LocalStandbySupport_Renewal_Summary':'SC_LocalSupportStandby_Renewal_Summary',
                'Genericl_Module_Renewal_Summary':'GenericModule_RenewalSummary'
				}
	templateName=templateNames.get(name)
### Updated New logic to eliminate if-elif-else. -Lahu- -End ####
if templateName:
	Quote.GenerateDocument(templateName, GenDocFormat.EXCEL)
	jsonObject['href'] = TagParserQuote.ParseString('<*CTX( Quote.LastGeneratedDocument.Link )*>').replace('http','https')
ApiResponse = ApiResponseFactory.JsonResponse(jsonObject)