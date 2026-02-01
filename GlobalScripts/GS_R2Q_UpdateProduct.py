import GS_APIGEE_Integration_Util

Log.Info('GS_R2Q_UpdateProduct Param-->>'+str(JsonHelper.Serialize(Param)))
excel_Url, header = GS_APIGEE_Integration_Util.GetR2QAPIGEEAuthDetails()
try:
	QuoteNumber = Param.QuoteNumber
	Quote = QuoteHelper.Edit(QuoteNumber)
	if Quote.GetCustomField('R2Q_Save').Content == 'Submit':
		Quote.SetGlobal('R2Q_UpdateProduct', 'True')
		for item in Quote.MainItems:
			if item.PartNumber == 'Migration':
				Product = item.EditConfiguration()
				'''migration_new_cont = Product.GetContainerByName('CONT_Migration_MSID_Selection')
				for MigrationNew in migration_new_cont.Rows:
					if 'Virtualization System' in MigrationNew['Selected Products'] or 'Virtualization System Migration' in MigrationNew['Selected Products']:
						for childproduct in MigrationNew.Product.GetContainerByName('CONT_MSID_SUBPRD').Rows:
							if 'Virtualization System' in childproduct['Selected_Products']:
								for subchaildproduct in childproduct.Product.Attributes:
									if subchaildproduct.Name == 'VS_Platform_Options':
										platform_opt=str(childproduct.Product.Attr(subchaildproduct.Name).GetValue())
										if platform_opt == 'Essentials - Lifecycle Bid':
											childproduct.Product.Attr('Virtualization_Platform_Options').SelectDisplayValue(str('Essentials Platforms-Dell Servers'))
										elif platform_opt in ['Number of Performance A Servers (0-9 per cluster)','Number of Performance B Servers (0-9 per cluster)']:
											childproduct.Product.Attr('Virtualization_Platform_Options').SelectDisplayValue(str('Premium Platforms Gen 3 - Performance A/B'))
											vs_24port=subchaildproduct.Product.Attr('VS_24Port_Rack_Required').GetValue()
											vs_48port=subchaildproduct.Product.Attr('VS_48Port_Rack_Required').GetValue()
											#vs_cluster=subchaildproduct.Product.Attr('VS_Number_of_Clusters_in_the_network').GetValue()
											thlevelcontainerRows = subchaildproduct.Product.GetContainerByName('Virtualization_cluster_transpose').AddNewRow()
											thlevelcontainerRows.Product.Attr('Virtualization_of_24_Port_Top_of_Rack_Switch').AssignValue(str(vs_24port))
											thlevelcontainerRows.Product.Attr('Virtualization_of_48_Port_Top_of_Rack_Switch').AssignValue(str(vs_48port))
											thlevelcontainerRows.Product.Attr('Virtualization_Number_of_A_VxRail_E660_Servers').AssignValue('3')
											thlevelcontainerRows.Product.Attr('Virtualization_Number_of_B_VxRail_E660_Servers').AssignValue('0')
										elif platform_opt == 'Premium Platforms 2 node pair (0-4)':
											childproduct.Product.Attr('Virtualization_Platform_Options').SelectDisplayValue(str('Premium Platforms Gen 3 - 2 node cluster'))
									elif subchaildproduct.Name == 'VS_Use_Own_OS_License':
										VS_License=str(childproduct.Product.Attr(subchaildproduct.Name).GetValue())
										if str(VS_License) == "Yes":
											childproduct.Product.Attr('Virtualization_DataCenter_OS_to_be_offered').SelectDisplayValue(str('No'))
										else:
											childproduct.Product.Attr('Virtualization_DataCenter_OS_to_be_offered').SelectDisplayValue(str('Yes'))'''
				Product.UpdateQuote()
		Quote.SetGlobal('R2Q_UpdateProduct', '')
		Log.Info('GS_R2Q_UpdateProduct --  Update Completed --')
	final_request_body={'QuoteNumber':str(Param.QuoteNumber),'CartId':str(Param.CartId),'RevisionNumber': str(Param.RevisionNumber),'UserName':str(User.UserName),'Module':'Migration','Action':'Update','Status':'Success','Action_List':[{'ActionName':'UpdateProduct','ScriptName':'GS_R2Q_UpdateProduct'}]}
	res = RestClient.Post(excel_Url, RestClient.SerializeToJson(str(final_request_body)),header)
	Log.Info('GS_R2Q_UpdateProduct Success =>> Req: {} -- Res: {}'.format(final_request_body, res))
except Exception as ex:
	Log.Info('GS_R2Q_UpdateProduct Fail-->>'+str(ex))
	final_request_body={'QuoteNumber':str(Param.QuoteNumber),'CartId':str(Param.CartId),'RevisionNumber': str(Param.RevisionNumber),'UserName':str(User.UserName),'Module':'Migration','Action':'Update','Status':'Fail','Action_List':[{'ActionName':'UpdateProduct','ScriptName':'GS_R2Q_UpdateProduct','ErrorMessage':str(ex)}]}
	res = RestClient.Post(excel_Url, RestClient.SerializeToJson(str(final_request_body)),header)
	Log.Info('GS_R2Q_UpdateProduct Failed =>> Req: {} -- Res: {}'.format(final_request_body, res))