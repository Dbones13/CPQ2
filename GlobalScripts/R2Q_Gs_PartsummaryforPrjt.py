import GS_APIGEE_Integration_Util
from TAS_PRJT_MAPPING import r2q_to_prjt_mapping,r2q_to_prjt_terminal_mapping,noncpq_prjt_mapping
excel_Url, header = GS_APIGEE_Integration_Util.GetR2QAPIGEEAuthDetails()
Log.Info('R2Q_Gs_PartsummaryforPrjt Param -->>'+JsonHelper.Serialize(Param))
Log.Info('R2Q_Gs_PartsummaryforPrjt QuoteNumber-->>'+str(Param.QuoteNumber))

try:
	QuoteNumber = Param.QuoteNumber
	ProcessPrd = Param.ActionName.replace("Generate PartSummary - ", "")
	Quote = QuoteHelper.Edit(QuoteNumber)
	Quote.GetCustomField("isR2QRequest").Content = 'True'
	Quote.SetGlobal('PerformanceUpload', "Yes")
	tagbit_map = False
	for item in Quote.MainItems:
		if item.PartNumber == 'PRJT':
			newProd = item.EditConfiguration()
			Log.Info('inside - PRJT : {}'.format(Quote.GetGlobal('PerformanceUpload')))
			Session['R2QProductName'] = Param.ActionName.replace("Generate PartSummary - ", "")
			#getPrd = SqlHelper.GetFirst("SELECT PA.PRODUCT_ID, PA.PRODUCT_NAME FROM products PA INNER JOIN product_versions PV ON PV.product_id = PA.PRODUCT_ID WHERE PA.PRODUCT_NAME = 'New / Expansion Project' AND PV.is_active = 'True'")
			#prd_id = int(getPrd.PRODUCT_ID)
			#newProd = ProductHelper.CreateProduct(prd_id)
	

			def Executeremotepartsummary(Product):
				if Product.Attr('PERF_ExecuteScripts').GetValue()=='SCRIPT_RUN':
					Product.ApplyRules()
					Product.ParseString('<* ExecuteScript(PS_RG_label_parts) *>')
					Product.ParseString('<* ExecuteScript(PS_SerC_C300_RG_Parts) *>')
					Product.ParseString('<* ExecuteScript(PS_SerC_C300_RG_Parts_2) *>')
					Product.ParseString('<* ExecuteScript(C300_shipping_crate_parts_RG) *>')
					Product.ParseString('<* ExecuteScript(PS_mcar_part_add_RG) *>')
					Product.ParseString('<* ExecuteScript(SerC_PowerSupply_Parts) *>')
					Product.ApplyRules()
					Product.ParseString('<* ExecuteScript(PS_C300_UMC_Parts) *>')
					Product.ParseString('<* ExecuteScript(PS_C300_CNM_PartCals) *>')
					#Product.ParseString('<* ExecuteScript(PS_C300_UMC_Parts) *>')
					#Product.ParseString('<* ExecuteScript(PS_mcar_part_add_RG) *>')
					if Product.Attr('total_family_CG_ios_doc').GetValue() < "1" and Product.Attr('pmio_ioss').GetValue() < "1":
						Product.ParseString('<* ExecuteScript(C300_shipping_crate_parts_RG) *>')
						Product.ParseString('<* ExecuteScript(SerC_PowerSupply_Parts) *>')
						#Product.ApplyRules()

				isR2QRequest= Quote.GetCustomField("isR2QRequest").Content
				if isR2QRequest or Product.Tabs.GetByName('Part Summary').IsSelected==True:
					cont = Product.GetContainerByName('Series_C_RG_Part_Summary_Cont')
					if cont:
						for row in cont.Rows:
							update=False
							if int(row["Final_Quantity"]) > 0:
								if row.IsSelected == False:
									row.IsSelected = True
									row.Calculate()
									update=True
								if row.Product.Attributes.GetByName('ItemQuantity'):
									if int(row["Final_Quantity"]) !=  row.Product.Attr('ItemQuantity').GetValue():
										row.Product.Attr('ItemQuantity').AssignValue(row["Final_Quantity"])
										update=True
								else:
									Product.ErrorMessages.Add('Item Quantity missing from part number {}, please contact the Admin'.format(row.Product.PartNumber))
								if update == True:
									row.ApplyProductChanges()
							else:
								if row.IsSelected == True:
									row.IsSelected = False
						cont.Calculate()
					Product.Attr('PERF_ExecuteScripts').AssignValue('')
					Product.ApplyRules()

			for ChildProduct in newProd.GetContainerByName('CE_SystemGroup_Cont').Rows:
				Log.Info('inside - CE_SystemGroup_Cont')
				selected_products = [p.strip() for p in ChildProduct['Selected_Products'].split('<br>')]
				for subproduct in selected_products:
					if subproduct != ProcessPrd:
						continue
					#Session['R2QRunScript'] = "False"
					Log.Info('running - CE_SystemGroup_Cont')
					if subproduct in ("C300 System","Experion Enterprise System", "Safety Manager ESD", "Safety Manager FGS", "3rd Party Devices/Systems Interface (SCADA)","eServer System", "ControlEdge UOC System","Field Device Manager"):
						
						for ChildProduct1 in ChildProduct.Product.GetContainerByName('CE_System_Cont').Rows:
							if ChildProduct1['Product Name'] != ProcessPrd:
								continue
							if ChildProduct1['Product Name'] == "C300 System":
								if ChildProduct1.Product.GetContainerByName('Series_C_Control_Groups_Cont'):
									for ChildProduct2 in ChildProduct1.Product.GetContainerByName('Series_C_Control_Groups_Cont').Rows:
										for ChildProduct3 in ChildProduct2.Product.GetContainerByName('Series_C_Remote_Groups_Cont').Rows:
											ChildProduct3.Product.Attr('PERF_ExecuteScripts').AssignValue('SCRIPT_RUN')
											ChildProduct3.Product.ApplyRules()
											ChildProduct3.Product.ParseString('<* ExecuteScript(Trigger to script execution) *>')
											Executeremotepartsummary(ChildProduct3.Product)
																																																																												
										ChildProduct2.Product.ApplyRules()
								#ChildProduct1.Product.ApplyRules()
								ChildProduct1.Product.ParseString('<* ExecuteScript(PS_Calculate_C300_Labor_Hours ) *>')
								ChildProduct1.Product.ParseString('<* ExecuteScript(PS_Calc_Final_Hrs ) *>')
								ChildProduct1.Product.ParseString('<* ExecuteScript(PS_Populate_C300_Labor_Price_Cost ) *>')
								ChildProduct1.Product.ApplyRules()
								ChildProduct1.ApplyProductChanges()
							try:
								if ChildProduct1['Product Name'] == "Experion Enterprise System":
									if ChildProduct1.Product.GetContainerByName('Experion_Enterprise_Cont'):
										ChildProduct1.Product.ApplyRules()
										ChildProduct1.Product.Attr('PERF_ExecuteScripts').AssignValue('SCRIPT_RUN')
										ChildProduct1.Product.ParseString('<* ExecuteScript(PS_Exp_Ent_Sys_Upd_Parts_for_Quote) *>')
										for ChildProduct2 in ChildProduct1.Product.GetContainerByName('Experion_Enterprise_Cont').Rows:
											ChildProduct2.Product.Attr('PERF_ExecuteScripts').AssignValue('SCRIPT_RUN')
											ChildProduct2.Product.ApplyRules()
											ChildProduct2.Product.ParseString('<* ExecuteScript(PS_exp_ent_grp_parts) *>')
											ChildProduct2.Product.ParseString('<* ExecuteScript(PS_exp_ent_grp_parts_2) *>')
											ChildProduct2.Product.ParseString('<* ExecuteScript(PS_GET_EBR_Parts) *>')
											ChildProduct2.Product.ParseString('<* ExecuteScript(PS_PartSummary) *>')
							except Exception as e:
								Log.Info("Experion Enterprise System >>> {0}".format(e))
							if ChildProduct1['Product Name'] in ("Safety Manager ESD", "Safety Manager FGS"):
								Log.Info('inside - Safety Manager')
								if ChildProduct1.Product.GetContainerByName('SM_ControlGroup_Cont'):
									ChildProduct1.Product.Attr('PERF_ExecuteScripts').AssignValue('SCRIPT_RUN')
									#for scr in chd.childProductScripts1:
										#ChildProduct1.Product.ParseString('<* ExecuteScript({}) *>'.format(scr))
									for ChildProduct2 in ChildProduct1.Product.GetContainerByName('SM_ControlGroup_Cont').Rows:
										ChildProduct2.Product.Attr('PERF_ExecuteScripts').AssignValue('SCRIPT_RUN')
										#for scr in chd.childProductScripts2:
											#ChildProduct2.Product.ParseString('<* ExecuteScript({}) *>'.format(scr))
										for ChildProduct3 in ChildProduct2.Product.GetContainerByName('SM_RemoteGroup_Cont').Rows:
											ChildProduct3.Product.Attr('PERF_ExecuteScripts').AssignValue('SCRIPT_RUN')
											#for scr in chd.childProductScripts3:
												#ChildProduct3.Product.ParseString('<* ExecuteScript({}) *>'.format(scr))
											ChildProduct3.Product.ApplyRules()
										ChildProduct2.Product.ApplyRules()
									ChildProduct1.Product.ApplyRules()

							if ChildProduct1['Product Name'] == "3rd Party Devices/Systems Interface (SCADA)":
								if ChildProduct1.Product.GetContainerByName('Scada_CCR_Unit_Cont'):
									for ChildProduct2 in ChildProduct1.Product.GetContainerByName('Scada_CCR_Unit_Cont').Rows:
										ChildProduct2.Product.ApplyRules()
										ChildProduct2.Product.ParseString('<* ExecuteScript(PS_Populate_Third_Party_parts) *>')
										ChildProduct2.Product.ParseString('<* ExecuteScript(PS_Update_Container_Product_Qty) *>')
								ChildProduct1.Product.ApplyRules()
							if ChildProduct1['Product Name'] == "Field Device Manager":
								if ChildProduct1.Product.GetContainerByName('FDM_System_Group_Cont'):
									for ChildProduct2 in ChildProduct1.Product.GetContainerByName('FDM_System_Group_Cont').Rows:
										ChildProduct2.Product.ApplyRules()
										ChildProduct2.Calculate()
										ChildProduct2.Product.ParseString('<* ExecuteScript(FDM_BOM) *>')
								ChildProduct1.Product.ApplyRules()
								
								
								
							try:
								if ChildProduct1['Product Name'] == "eServer System":
									if ChildProduct1.Product.GetContainerByName('ES_Group'):
										ChildProduct1.Product.ApplyRules()
										for ChildProduct2 in ChildProduct1.Product.GetContainerByName('ES_Group').Rows:
											ChildProduct2.Product.ApplyRules()
											ChildProduct2.Product.ParseString('<* ExecuteScript(PS_Update_Container_Product_Qty) *>')
											ChildProduct2.Product.ParseString('<* ExecuteScript(PS_PartSummary_System) *>')
											ChildProduct2.Product.ParseString('<* ExecuteScript(PS_AddParts) *>')
							except Exception as e:
								Log.Info("eServer System >>> {0}".format(e))
							try:
								if ChildProduct1['Product Name'] == "ControlEdge UOC System":
									if ChildProduct1.Product.GetContainerByName('UOC_ControlGroup_Cont'):
										ChildProduct1.Product.ApplyRules()
										ChildProduct1.Product.ParseString('<* ExecuteScript(PS_UOC_LI_PartSummary) *>')
										for ChildProduct2 in ChildProduct1.Product.GetContainerByName('UOC_ControlGroup_Cont').Rows:
											ChildProduct2.Product.ApplyRules()
											ChildProduct2.Product.ParseString('<* ExecuteScript(PS_CG_Part_Summary ) *>')
											ChildProduct2.Product.ParseString('<* ExecuteScript(PS_SetFinalQty_default) *>')
											ChildProduct2.Product.ParseString('<* ExecuteScript(PS_UOC_CG_LI_PartSummary) *>')
											ChildProduct2.Product.ParseString('<* ExecuteScript(PS_UOC_Sys_Cabinets_Qty) *>')
											for ChildProduct3 in ChildProduct2.Product.GetContainerByName('UOC_RemoteGroup_Cont').Rows:
												ChildProduct3.Product.ApplyRules()
												ChildProduct3.Product.ParseString('<* ExecuteScript(PS_RG_Part_Summary ) *>')
												ChildProduct3.Product.ParseString('<* ExecuteScript(PS_UOC_RG_LI_Part_Summary ) *>')
							except Exception as e:
								Log.Info("ControlEdge UOC System >>> {0}".format(e))

							try:
								if ChildProduct1['Product Name'] == "ControlEdge PLC System":
									if ChildProduct1.Product.GetContainerByName('PLC_ControlGroup_Cont'):
										ChildProduct1.Product.ApplyRules()
										ChildProduct1.Product.ParseString('<* ExecuteScript(PS_PLC_LI_PartSummary) *>')
										for ChildProduct2 in ChildProduct1.Product.GetContainerByName('PLC_ControlGroup_Cont').Rows:
											ChildProduct2.Product.ApplyRules()
											ChildProduct2.Product.ParseString('<* ExecuteScript(PS_CG_Part_Summary ) *>')
											ChildProduct2.Product.ParseString('<* ExecuteScript(PS_SetFinalQty_default) *>')
											ChildProduct2.Product.ParseString('<* ExecuteScript(PS_PLC_CG_LI_PartSummary) *>')
											ChildProduct2.Product.ParseString('<* ExecuteScript(PS_PLC_Sys_Cabinets_Qty) *>')
											for ChildProduct3 in ChildProduct2.Product.GetContainerByName('PLC_RemoteGroup_Cont').Rows:
												ChildProduct3.Product.ApplyRules()
												ChildProduct3.Product.ParseString('<* ExecuteScript(PS_RG_Part_Summary ) *>')
												ChildProduct3.Product.ParseString('<* ExecuteScript(PS_PLC_RG_LI_Part_Summary ) *>')
							except Exception as e:
								Log.Info("ControlEdge PLC System >>> {0}".format(e))
							try:
								if ChildProduct1['Product Name'] == "Digital Video Manager":
									if ChildProduct1.Product.GetContainerByName('DVM_System_Group_Cont'):
										ChildProduct1.Product.ApplyRules()
										ChildProduct1.Product.ParseString('<* ExecuteScript(PS_DVM_Upd_Parts_for_Quote) *>')
										for ChildProduct2 in ChildProduct1.Product.GetContainerByName('DVM_System_Group_Cont').Rows:
											ChildProduct2.Product.ApplyRules()
											ChildProduct2.Product.ParseString('<* ExecuteScript(PS_DVM_Grp_Upd_Parts_for_Quote ) *>')
							except Exception as e:
								Log.Info("Digital Video Manager >>> {0}".format(e))

						#ChildProduct.Product.ApplyRules()
					elif subproduct in ('Industrial Security (Access Control)', 'Tank Gauging Engineering', 'Digital Video Manager', 'Fire Detection & Alarm Engineering'):
						tagbit_map = True
					elif subproduct == "Terminal Manager":
						for ChildProduct1 in ChildProduct.Product.GetContainerByName('CE_System_Cont').Rows:
							if ChildProduct1['Product Name'] == "Terminal Manager":
								r2q_to_prjt_terminal_mapping(ChildProduct1.Product,Quote)
				#if 'New - Expansion Project' == ProcessPrd:
				#	Log.Info('system group PRJT')
				#	ChildProduct.Product.ParseString('<* ExecuteScript(PS_ScriptOnAddtoQuote) *>')
				#	ChildProduct.Product.ParseString('<* ExecuteScript(PS_DocumentTables_Non_ICSS_SG) *>')
				newProd.ParseString('<* ExecuteScript(PS_R2Q_ProjectQueCont) *>')
				Log.Info('system group PRJT Out: --{}--  --{}--'.format(ChildProduct.Product.Name, ProcessPrd))
			if tagbit_map:
				r2q_to_prjt_mapping(newProd,Quote)
			noncpq_prjt_mapping(newProd,Quote)
			newProd.ApplyRules()
			Log.Info('inside - PRJT : {}'.format(Quote.GetGlobal('PerformanceUpload')))
			Quote.SetGlobal('PerformanceUpload', "Yes")
			Log.Info('Update - PRJT : {}'.format(Quote.GetGlobal('PerformanceUpload')))
			newProd.UpdateQuote()
			Quote.SetGlobal('PerformanceUpload', "")
			Log.Info('Update completed - PRJT : {}'.format(Quote.GetGlobal('PerformanceUpload')))
	Log.Info('R2Q_Gs_PartsummaryforPrjt Success-->>')
	final_request_body={'QuoteNumber':str(QuoteNumber),'CartId':str(Param.CartId),'RevisionNumber': str(Param.RevisionNumber),'UserName':str(User.UserName),'Module':'New/Expansion','Action':'Update','Status':'Success','Action_List':[{'ActionName':Param.ActionName,'ScriptName':'R2Q_Gs_PartsummaryforPrjt'}]}
	Log.Info('R2Q_Gs_PartsummaryforPrjt Success final request body -->> ', str(final_request_body))
	RestClient.Post(excel_Url, RestClient.SerializeToJson(str(final_request_body)),header)
	
except Exception as ex:
	Log.Info('R2Q_Gs_PartsummaryforPrjt Error-->>'+str(ex))
	final_request_body={'QuoteNumber':str(QuoteNumber),'CartId':str(Param.CartId),'RevisionNumber': str(Param.RevisionNumber),'UserName':str(User.UserName),'Module':'New/Expansion','Action':'Update','Status':'Fail','Action_List':[{'ActionName':Param.ActionName if Param else 'Generate PartSummary','ScriptName':'R2Q_Gs_PartsummaryforPrjt','ErrorMessage':str(ex)}]}
	RestClient.Post(excel_Url, RestClient.SerializeToJson(str(final_request_body)),header)