import GS_Labor_Report_Util
from GS_Winest_Labor_Price_Cost import service_material_map
msidcont_list = [ 'MSID_Labor_FDM_Upgrade_Con', 'MSID_Labor_LM_to_ELMM_Con', 'MSID_Labor_FSC_to_SM_con', 
'MSID_Labor_xPM_to_C300_Migration_Con', 'MSID_Labor_CB-EC_Upgrade_to_C300-UHIO_con', 
'MSID_Labor_C200_Migration_Con', 'MSID_Labor_TCMI_Con', 'MSID_Labor_EHPM_HART_IO_Con', 
'MSID_Labor_Orion_Console_Con', 'MSID_Labor_EHPM_C300PM_Con', 'MSID_Labor_TPS_TO_EXPERION_Con', 
'MSID_Labor_ELCN_Con', 'MSID_Labor_EBR_Con', 'MSID_Labor_OPM_Engineering', 'MSID_Labor_LCN_One_Time_Upgrade_Engineering', 
'MSID_Labor_Project_Management', 'MSID_Additional_Custom_Deliverables', 'MSID_Labor_FSC_to_SM_audit_Con', 
'MSID_Labor_XP10_Actuator_Upgrade_con', 'MSID_Labor_Graphics_Migration_con', 'MSID_Labor_FSCtoSM_IO_con', 
'MSID_Labor_CD_Actuator_con', 'MSID_Labor_CWS_RAE_Upgrade_con', '3rd_Party_PLC_UOC_Labor', 
'MSID_Labor_Virtualization_con', 'MSID_Labor_QCS_RAE_Upgrade_con', 'MSID_Labor_Generic_System1_Cont', 
'MSID_Labor_Generic_System2_Cont', 'MSID_Labor_Generic_System3_Cont', 'MSID_Labor_Generic_System4_Cont', 
'MSID_Labor_Generic_System5_Cont', 'MSID_Labor_TPA_con', 'MSID_Labor_FSC_to_SM_IO_Audit_Con', 
'MSID_Labor_ELEPIU_con']
HCI_config_list = ["HCI_PHD_EngineeringLabour","HCI_PHD_ProjectManagement2","HCI_PHD_ProjectManagement","HCI_PHD_AdditionalDeliverables"]
prodcont_dict = {'MSID_Labor_OPM_Engineering':'OPM','MSID_Labor_LCN_One_Time_Upgrade_Engineering':'LCN One Time Upgrade',
'MSID_Labor_EBR_Con':'EBR' ,'MSID_Labor_ELCN_Con':'ELCN','MSID_Labor_Virtualization_con':'Virtualization System Migration',
'MSID_Labor_Graphics_Migration_con':'Graphics Migration' ,'MSID_Labor_EHPM_HART_IO_Con':'EHPM HART IO','MSID_Labor_EHPM_C300PM_Con':'EHPM/EHPMX/ C300PM',
'MSID_Labor_Orion_Console_Con':'Orion Console', 'MSID_Labor_TPS_TO_EXPERION_Con':'TPS to Experion','MSID_Labor_TCMI_Con':'TCMI',
'MSID_Labor_C200_Migration_Con':'C200 Migration', 'MSID_Labor_CB-EC_Upgrade_to_C300-UHIO_con':'CB-EC Upgrade to C300-UHIO',
'MSID_Labor_FSC_to_SM_con':'FSC to SM','MSID_Labor_FSC_to_SM_audit_Con':'FSC to SM', 'MSID_Labor_FSCtoSM_IO_con':'FSC to SM',
'MSID_Labor_FSC_to_SM_IO_Audit_Con':'FSC to SM','MSID_Labor_xPM_to_C300_Migration_Con':'xPM to C300 Migration', 'MSID_Labor_FDM_Upgrade_Con':'FDM Upgrade',
'MSID_Labor_LM_to_ELMM_Con':'LM to ELMM ControlEdge PLC','MSID_Labor_XP10_Actuator_Upgrade_con':'XP10 Actuator Upgrade' ,
'3rd_Party_PLC_UOC_Labor':'3rd Party PLC to ControlEdge PLC/UOC','MSID_Labor_CWS_RAE_Upgrade_con':'CWS RAE Upgrade',
'MSID_Labor_QCS_RAE_Upgrade_con':'QCS RAE Upgrade', 'MSID_Labor_CD_Actuator_con':'CD Actuator I-F Upgrade','MSID_Labor_TPA_con':'TPA/PMD Migration',
'MSID_Labor_Generic_System1_Cont':'Generic System Migration', 'MSID_Labor_Generic_System2_Cont':'Generic System Migration',
'MSID_Labor_Generic_System3_Cont':'Generic System Migration', 
'MSID_Labor_Generic_System4_Cont':'Generic System Migration','MSID_Labor_Generic_System5_Cont':'Generic System Migration', 
'MSID_Labor_ELEPIU_con':'ELEPIU ControlEdge RTU Migration Engineering','MSID_Labor_Project_Management':'Migration',
'MSID_Additional_Custom_Deliverables':'Migration','Generic_System_Activities':'Cyber Generic System','AR_SMX_Activities':'SMX',
'AR_Assessment_Activities':'Assessments','AR_PCNH_Activities':'PCN Hardening','AR_MSS_Activities':'MSS','AR_CAC_Activities':'Cyber App Control',
'Cyber_Labor_Project_Management':'Cyber','AR_Cyber_AdditionalCustomDeliverable':'Cyber'}
cyberlist=['Generic_System_Activities','AR_SMX_Activities','AR_Assessment_Activities','AR_PCNH_Activities','AR_MSS_Activities',
'AR_CAC_Activities','Cyber_Labor_Project_Management']
is_pm = ''
def pick(normal_key, pm_key):
		return pm_key if is_pm else normal_key

def row_get(row, key, default=None):
		"""Safely access container row fields using dict-style indexing."""
		try:
				return row[key]
		except Exception:
				return default
def getFloat(Var):
		if Var:
				return float(Var)
		return 0.00
def getHciPlsg(eng):
		plsg = SqlHelper.GetFirst("select Service_Material from CT_HCI_PHD_LABORMATERIAL where Labor = '{0}'".format(eng))
		if plsg != None:
				material =  plsg.Service_Material
				plsg = SqlHelper.GetFirst("select PLSG from HPS_LABOR_PLSG_MAPPING where Part_Num = '{0}'".format(material))
				if plsg != None:
					return plsg.PLSG
				else:
						plsg = SqlHelper.GetFirst("select PLSG from HPS_PRODUCTS_MASTER where PartNumber = '{0}'".format(material))
						if plsg != None:
								return plsg.PLSG
		else:
			return ''
def hci_eng(eng):
		material = SqlHelper.GetFirst("select Service_Material from CT_HCI_PHD_LABORMATERIAL where Labor = '{0}'".format(eng))
		if material != None:
				return material.Service_Material
		else:
				return ''
def getLssPlsg(fo_lbr):
		plsg = ''
		plsg = SqlHelper.GetFirst("select PLSG from HPS_LABOR_PLSG_MAPPING where Part_Num = '{0}'".format(fo_lbr))
		if plsg != None:
				return plsg.PLSG
		else:
				plsg = SqlHelper.GetFirst("select PLSG from HPS_PRODUCTS_MASTER where PartNumber = '{0}'".format(fo_lbr))
				if plsg != None:
						return plsg.PLSG
				else:
					return '' 
labor_sys_del = []
sys_grp_name = ''

Prod_Cont_map = GS_Labor_Report_Util.Master_Prod_Cont_map
Cont_col_map = GS_Labor_Report_Util.Master_Cont_col_map
Cont_Labor_map = GS_Labor_Report_Util.Master_Cont_Labor_map

salesOrg = ""
Sales_Org_Country = ""
salesArea = TagParserQuote.ParseString('<* QuoteProperty (Sales Area) *>')
if salesArea:
		Sales_Org_Country = SqlHelper.GetFirst("SELECT Execution_County from EXECUTION_COUNTRY_SALES_ORG_MAPPING where Execution_Country_Sales_Org = '{}'".format(salesArea))
		if Sales_Org_Country:
				salesOrg = Sales_Org_Country.Execution_County
else:
		Log.Info("Sales Area is not Defined for this Qoute")
for Item in Quote.MainItems:
		if Item.ProductName == 'New / Expansion Project':
				#Trace.Write("1. Found")
				#Trace.Write(Item.ProductName)
				#Trace.Write(Item.PartNumber)
				for prod in Prod_Cont_map:
						if prod == Item.ProductName:
								#Trace.Write("2. Found")
								#Trace.Write(Item.ProductName)
								Item.EditConfiguration()
								for attr in Prod_Cont_map[prod]:
										#Trace.Write(attr)
										cont = Product.GetContainerByName(attr)
										if cont:
												for cont_rows in cont.Rows:
														del_list = []
														del_list.append(Item.ProductName)
														del_list.append(Item.PartNumber)
														del_list.append(attr)
														del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][0]).Value)
														if "Addi" not in attr:
																del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][1]).Value)
																del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][2]).Value)
														else:
																del_list.append(0)
																del_list.append(0)
														del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][3]).Value)
														del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][4]).DisplayValue)
														ges_eng = str(cont_rows.GetColumnByName(Cont_col_map[attr][4]).DisplayValue) if cont_rows.GetColumnByName(Cont_col_map[attr][4]).DisplayValue!='' else "SYS GES Eng-XO-CN"
														del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][5]).Value)
														del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][6]).DisplayValue)
														fo_1 = cont_rows.GetColumnByName(Cont_col_map[attr][6]).DisplayValue
														del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][7]).Value)
														if "Addi" not in attr:
																del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][8]).DisplayValue)
																fo_2 = cont_rows.GetColumnByName(Cont_col_map[attr][8]).DisplayValue
																del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][9]).Value)
														else:
																del_list.append('')
																fo_2 = ''
																del_list.append(0)
														Exe_Country = cont_rows.GetColumnByName(Cont_col_map[attr][10]).Value
														del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][10]).Value)
														del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][11]).Value)
														fo_cost = cont_rows.GetColumnByName(Cont_col_map[attr][12]).Value
														if fo_cost == '' or fo_cost == None:
																del_list.append(0)
														else:
																del_list.append(fo_cost)
														ges_cost = cont_rows.GetColumnByName(Cont_col_map[attr][13]).Value
														if ges_cost == '' or ges_cost == None:
																del_list.append(0)
														else:
																del_list.append(ges_cost)
														plsg = ''
														if fo_1 != '' or fo_1 != None:
																plsg = GS_Labor_Report_Util.get_plsg(fo_1)
														elif fo_2 != '' or fo_2 != None:
																plsg = GS_Labor_Report_Util.get_plsg(fo_2)
														del_list.append(plsg)
														ges_plsg = ''
														if ges_eng != '' and ges_eng != None:
																ges_plsg = GS_Labor_Report_Util.get_plsg(ges_eng)
														del_list.append('Project')
														if Exe_Country == salesOrg:
																del_list.append('Front Office Labor')
														else:
																del_list.append('Intercompany Labor')
														if ges_eng != '' and ges_eng != None and ges_eng != 'None':
																if ges_eng[-5] == "B":
																		del_list.append('GES Back -office Labor')
																elif ges_eng[-5] == "F":
																		del_list.append('GES On-site Labor')
																else:
																		del_list.append('')
														else:
																del_list.append('')
														del_list.append(salesOrg)
														lob_labor = GS_Labor_Report_Util.get_LOB_Labor(plsg)
														del_list.append(lob_labor)
														ges_lob_labor = GS_Labor_Report_Util.get_LOB_Labor(ges_plsg)
														del_list.append(ges_lob_labor)
														del_list.append(ges_plsg)
														del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][14]).Value)
														del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][15]).Value)
														del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][16]).Value)
														del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][17]).Value)
														labor_sys_del.append(del_list)
				#break
				New_Exp_Cnt = Product.GetContainerByName('CE_SystemGroup_Cont')
				if New_Exp_Cnt is not None:
						for sys_grp_row in New_Exp_Cnt.Rows:
								if sys_grp_row.GetColumnByName('Scope').Value == 'HWSWLABOR':
										sys_grp_prouct = sys_grp_row.Product
										sys_grp_name = sys_grp_row.GetColumnByName('Child Product Name').Value
										if sys_grp_row.GetColumnByName("Include_Generic_System").Value == "Yes":
												sys_grp_generic_cnt = sys_grp_prouct.GetContainerByName('PMC_Generic_System_Cont')
												if sys_grp_generic_cnt.Rows.Count > 0:
														for sys_grp_generic_prods in sys_grp_generic_cnt.Rows:
																quote_generic_prds = sys_grp_generic_prods.Product
																for generic_prd in Prod_Cont_map:
																		if generic_prd == quote_generic_prds.Name:
																				for generic_attr in Prod_Cont_map[generic_prd]:
																						generic_cont = quote_generic_prds.GetContainerByName(generic_attr)
																						if generic_cont:
																								for generic_cont_rows in generic_cont.Rows:
																										del_list = []
																										del_list.append(quote_generic_prds.Name)
																										del_list.append(sys_grp_generic_prods.GetColumnByName('Generic System Name').Value)
																										del_list.append(generic_attr)
																										del_list.append(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][0]).Value)
																										if "Addi" not in generic_attr:
																												del_list.append(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][1]).Value)
																												del_list.append(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][2]).Value)
																										else:
																												del_list.append(0)
																												del_list.append(0)
																										del_list.append(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][3]).Value)
																										del_list.append(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][4]).DisplayValue)
																										ges_eng = str(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][4]).DisplayValue) if generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][4]).DisplayValue!='' else "SYS GES Eng-XO-CN"
																										del_list.append(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][5]).Value)
																										del_list.append(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][6]).DisplayValue)
																										fo_1 = generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][6]).DisplayValue
																										del_list.append(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][7]).Value)
																										if "Addi" not in generic_attr:
																												del_list.append(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][8]).DisplayValue)
																												fo_2 = generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][8]).DisplayValue
																												del_list.append(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][9]).Value)
																										else:
																												del_list.append('')
																												fo_2 = ''
																												del_list.append(0)
																										del_list.append(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][10]).Value)
																										Exe_Country = generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][10]).Value
																										del_list.append(generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][11]).Value)
																										fo_cost = generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][12]).Value
																										if fo_cost == '' or fo_cost == None:
																												del_list.append(0)
																										else:
																												del_list.append(fo_cost)
																										ges_cost = generic_cont_rows.GetColumnByName(Cont_col_map[generic_attr][13]).Value
																										if ges_cost == '' or ges_cost == None:
																												del_list.append(0)
																										else:
																												del_list.append(ges_cost)
																										plsg = ''
																										if fo_1 != '' or fo_1 != None:
																												plsg = GS_Labor_Report_Util.get_plsg(fo_1)
																										elif fo_2 != '' or fo_2 != None:
																												plsg = GS_Labor_Report_Util.get_plsg(fo_2)
																										del_list.append(plsg)
																										ges_plsg = ''
																										if ges_eng != '' and ges_eng != None:
																												ges_plsg = GS_Labor_Report_Util.get_plsg(ges_eng)
																										del_list.append(sys_grp_name)
																										if Exe_Country == salesOrg:
																												del_list.append('Front Office Labor')
																										else:
																												del_list.append('Intercompany Labor')
																										if ges_eng != '' and ges_eng != None and ges_eng != 'None':
																												if ges_eng[-5] == "B":
																														del_list.append('GES Back -office Labor')
																												elif ges_eng[-5] == "F":
																														del_list.append('GES On-site Labor')
																												else:
																														del_list.append('')
																										else:
																												del_list.append('')
																										del_list.append(salesOrg)
																										lob_labor = GS_Labor_Report_Util.get_LOB_Labor(plsg)
																										del_list.append(lob_labor)
																										ges_lob_labor = GS_Labor_Report_Util.get_LOB_Labor(ges_plsg)
																										del_list.append(ges_lob_labor)
																										del_list.append(ges_plsg)
																										del_list.append(cont_rows.GetColumnByName(Cont_col_map[generic_attr][14]).Value)
																										del_list.append(cont_rows.GetColumnByName(Cont_col_map[generic_attr][15]).Value)
																										del_list.append(cont_rows.GetColumnByName(Cont_col_map[generic_attr][16]).Value)
																										del_list.append(cont_rows.GetColumnByName(Cont_col_map[generic_attr][17]).Value)
																										labor_sys_del.append(del_list)
										sys_grp_cnt = sys_grp_prouct.GetContainerByName('CE_System_Cont')
										for sys_grp_prods in sys_grp_cnt.Rows:
												quote_prds = sys_grp_prods.Product
												for prod in Prod_Cont_map:
														if prod == quote_prds.Name:
																#Trace.Write("2. Found")
																#Trace.Write(quote_prds.Name)
																for attr in Prod_Cont_map[prod]:
																		#Trace.Write(attr)
																		cont = quote_prds.GetContainerByName(attr)
																		if cont:
																				for cont_rows in cont.Rows:
																						del_list = []
																						del_list.append(quote_prds.Name)
																						del_list.append(sys_grp_prods.GetColumnByName('Product Name').Value)
																						del_list.append(attr)
																						del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][0]).Value)
																						if "Addi" not in attr:
																								del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][1]).Value)
																								del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][2]).Value)
																						else:
																								del_list.append(0)
																								del_list.append(0)
																						del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][3]).Value)
																						if prod == "Measurement IQ System":
																								del_list.append('')
																								ges_eng = "SYS GES Eng-XO-CN"
																								del_list.append(0)
																								del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][6]).Value)
																								fo_1 = cont_rows.GetColumnByName(Cont_col_map[attr][6]).Value
																						else:
																								del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][4]).DisplayValue)
																								ges_eng = str(cont_rows.GetColumnByName(Cont_col_map[attr][4]).DisplayValue) if cont_rows.GetColumnByName(Cont_col_map[attr][4]).DisplayValue!='' else "SYS GES Eng-XO-CN"
																								del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][5]).Value)
																								del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][6]).DisplayValue)
																								fo_1 = cont_rows.GetColumnByName(Cont_col_map[attr][6]).DisplayValue
																						del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][7]).Value)
																						if "Addi" not in attr:
																								if prod == "Measurement IQ System":
																										del_list.append('')
																										fo_2 = ''
																										del_list.append(0)
																								else:
																										del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][8]).DisplayValue)
																										fo_2 = cont_rows.GetColumnByName(Cont_col_map[attr][8]).DisplayValue
																										del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][9]).Value)
																						else:
																								del_list.append('')
																								fo_2 = ''
																								del_list.append(0)
																						del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][10]).Value)
																						Exe_Country = cont_rows.GetColumnByName(Cont_col_map[attr][10]).Value
																						del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][11]).Value)
																						fo_cost = cont_rows.GetColumnByName(Cont_col_map[attr][12]).Value
																						if fo_cost == '' or fo_cost == None:
																								del_list.append(0)
																						else:
																								del_list.append(fo_cost)
																						if prod == "Measurement IQ System":
																								del_list.append(0)
																						else:
																								ges_cost = cont_rows.GetColumnByName(Cont_col_map[attr][13]).Value
																								if ges_cost == '' or ges_cost == None:
																										del_list.append(0)
																								else:
																										del_list.append(ges_cost)
																						plsg = ''
																						if fo_1 != '' or fo_1 != None:
																								plsg = GS_Labor_Report_Util.get_plsg(fo_1)
																						elif fo_2 != '' or fo_2 != None:
																								plsg = GS_Labor_Report_Util.get_plsg(fo_2)
																						del_list.append(plsg)
																						ges_plsg = ''
																						if ges_eng != '' and ges_eng != None:
																								ges_plsg = GS_Labor_Report_Util.get_plsg(ges_eng)
																						del_list.append(sys_grp_name)
																						if Exe_Country == salesOrg:
																								del_list.append('Front Office Labor')
																						else:
																								del_list.append('Intercompany Labor')
																						if ges_eng != '' and ges_eng != None and ges_eng != 'None':
																								if ges_eng[-5] == "B":
																										del_list.append('GES Back -office Labor')
																								elif ges_eng[-5] == "F":
																										del_list.append('GES On-site Labor')
																								else:
																										del_list.append('')
																						else:
																								del_list.append('')
																						del_list.append(salesOrg)
																						lob_labor = GS_Labor_Report_Util.get_LOB_Labor(plsg)
																						del_list.append(lob_labor)
																						ges_lob_labor = GS_Labor_Report_Util.get_LOB_Labor(ges_plsg)
																						del_list.append(ges_lob_labor)
																						del_list.append(ges_plsg)
																						del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][14]).Value)
																						if prod == "Measurement IQ System":
																								del_list.append(0)
																						else:
																								del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][15]).Value)
																						del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][16]).Value)
																						if prod == "Measurement IQ System":
																								del_list.append(0)
																						else:
																								del_list.append(cont_rows.GetColumnByName(Cont_col_map[attr][17]).Value)
																						labor_sys_del.append(del_list)
		elif Item.ProductName == 'Winest Labor Import':
				cont_list = ['Winest Labor Container','Winest Additional Labor Container']
				for cont in cont_list:
						container = Item.SelectedAttributes.GetContainerByName(cont)
						if container:
								for cont_rows in container.Rows:
										if getFloat(cont_rows['Final Hrs']) == 0:
												continue;
										del_list = []
										del_list.append(Item.ProductName) #0
										del_list.append(Item.PartNumber) #1
										del_list.append(cont) #2
										del_list.append(cont_rows['Deliverable']) #3
										if "Addi" not in cont:
												del_list.append(cont_rows['Calculated Hrs']) #4
												del_list.append(cont_rows['Productivity']) #5
										else:
												del_list.append(0) #4
												del_list.append(0) #5
										del_list.append(cont_rows['Final Hrs']) #6
										if 'GES' in cont_rows['Service Material']:
												del_list.append(service_material_map[cont_rows['Service Material']]) #7
												del_list.append(100) #8
												del_list.append('') #9
												del_list.append(0) #10
										else:
												del_list.append('') #7
												del_list.append(0) #8
												del_list.append(service_material_map[cont_rows['Service Material']]) #9
												del_list.append(100) #10
										del_list.append('') #11
										del_list.append(0) #12
										del_list.append(cont_rows['Execution Country']) #13
										del_list.append(cont_rows['Execution Year']) #14
										if 'GES' in cont_rows['Service Material']:
												del_list.append(0) #15
												del_list.append(cont_rows['Regional_Cost']) #16
										else:
												del_list.append(cont_rows['Regional_Cost']) #15
												del_list.append(0) #16
										plsg = ''
										if 'GES' not in cont_rows['Service Material']:
												plsg = GS_Labor_Report_Util.get_plsg(service_material_map[cont_rows['Service Material']])
										del_list.append(plsg) #17
										ges_plsg = ''
										if 'GES' in cont_rows['Service Material']:
												ges_plsg = GS_Labor_Report_Util.get_plsg(service_material_map[cont_rows['Service Material']])
										Area= cont_rows['Area'] if cont_rows['Area'] else 'No Area'
										del_list.append(Area) #18
										#del_list.append('') #18
										if 'GES' in cont_rows['Service Material']:
												del_list.append('') #19
												if (cont_rows['Service Material'])[-4] == "B":
														del_list.append('GES Back -office Labor') #20
												elif (cont_rows['Service Material'])[-4] == "F":
														del_list.append('GES On-site Labor') #20
												else:
														del_list.append('') #20
										else:
												if cont_rows['Execution Country'] == salesOrg:
														del_list.append('Front Office Labor') #19
												else:
														del_list.append('Intercompany Labor') #19
												del_list.append('') #20
										del_list.append(salesOrg) #21
										lob_labor = GS_Labor_Report_Util.get_LOB_Labor(plsg)
										del_list.append(lob_labor) #22
										ges_lob_labor = GS_Labor_Report_Util.get_LOB_Labor(ges_plsg)
										del_list.append(ges_lob_labor) #23
										del_list.append(ges_plsg) #24
										labor_sys_del.append(del_list)
		elif Item.ProductName == 'MSID_New':
				try:
						for cont in msidcont_list:
								del_list = []
								container = Item.SelectedAttributes.GetContainerByName(cont)
								if container:
										for cont_rows in container.Rows:
												if cont_rows['Deliverable'] not in ('Total','Off-Site','On-Site'):
														del_list = []
														del_list.append(prodcont_dict[cont]) #0
														del_list.append(prodcont_dict[cont]) #1
														del_list.append(cont) #2
														del_list.append(cont_rows['Deliverable']) #3
														del_list.append(cont_rows['Calculated_Hrs']) #4
														del_list.append(cont_rows['Adjustment_Productivity']) #5
														del_list.append(cont_rows['Final_Hrs']) #6
														ges_eng=cont_rows['GES_Eng']
														del_list.append(cont_rows['GES_Eng']) #7
														del_list.append(cont_rows['GES_Eng_Percentage_Split']) #8
														fo_1=cont_rows['FO_Eng']
														del_list.append(cont_rows['FO_Eng']) #9
														del_list.append(cont_rows['FO_Eng_Percentage_Split']) #10
														del_list.append('') #11
														del_list.append(0) #12
														del_list.append(cont_rows['Execution_Country']) #13
														del_list.append(cont_rows['Execution_Year']) #14
														del_list.append(cont_rows['Regional_Cost']) #15
														del_list.append(cont_rows['GES_Regional_Cost']) #16
														plsg = ''
														plsg = getLssPlsg(fo_1)
														del_list.append(plsg) #17
														ges_plsg = ''
														ges_plsg = getLssPlsg(ges_eng)
														ges_office = ges_eng.split('_')
														len_geseng = len(ges_office)
														office_str = ''
														if ges_eng != '' and ges_eng != None and ges_eng != 'None':
															if len_geseng > 1:
																off_str = len_geseng-2
																if ges_office[off_str][-1] == "B":
																	office_str = "GES Back -office Labor"
																elif ges_office[off_str][-1] == "F":  
																	office_str = 'GES On-site Labor'
																else:
																	office_str = ""
														Area= 'MSID_New'
														del_list.append(Area) #18
														if cont_rows['Execution_Country'] == salesOrg:
																del_list.append('Front Office Labor') #19
														else:
																del_list.append('Intercompany Labor') #19
														del_list.append(office_str) #20
														del_list.append(salesOrg) #21
														lob_labor = GS_Labor_Report_Util.get_LOB_Labor(plsg)
														del_list.append(lob_labor) #22
														ges_lob_labor = GS_Labor_Report_Util.get_LOB_Labor(ges_plsg)
														del_list.append(ges_lob_labor) #23
														del_list.append(ges_plsg) #24
														del_list.append(cont_rows['FOUnitWTWCost'])
														del_list.append(cont_rows['GES_Regional_Cost'])
														del_list.append(cont_rows['FO_ListPrice'])
														del_list.append(cont_rows['GES_ListPrice'])
														labor_sys_del.append(del_list)
				except Exception as ex:
						Log.Info('CA_PASLaborDeliverables  Error-->>'+str(ex))
		elif Item.ProductName == 'HCI Labor Config':
					Item.EditConfiguration()
					main_cont = Product.GetContainerByName('HCI_PHD_Selected_Products')
					for cont in main_cont.Rows:
							for child in HCI_config_list:
									child_cont = cont.Product.GetContainerByName(child)
									if child_cont:
											for cont_rows in child_cont.Rows:
													if cont_rows['Eng'] not in ('','None',None):
															del_list = []
															del_list.append(cont.Product.Name) #0
															del_list.append(cont.Product.Name) #1
															del_list.append(child) #2
															del_list.append(cont_rows['Deliverable']) #3
															del_list.append(cont_rows['Calculated Hrs']) #4
															del_list.append(cont_rows['Productivity']) #5
															del_list.append(cont_rows['Final Hrs']) #6
															#ges_eng=cont_rows['GES_Eng']
															fo_1 = cont_rows['ENG']
															engg = hci_eng(fo_1)
															if 'GES' in cont_rows['ENG']:
																	del_list.append(engg) #7
																	del_list.append(100) #8
																	del_list.append('') #9
																	del_list.append(0) #10
															else:
																	del_list.append('') #7
																	del_list.append(0) #8
																	del_list.append(engg) #9
																	del_list.append(100) #10
															del_list.append('') #11
															del_list.append(0) #12
															del_list.append(cont_rows['Execution Country']) #13
															del_list.append(cont_rows['Execution Year']) #14
															eng_total = getFloat(cont_rows['Eng Total Regional Cost'])
															del_list.append(eng_total) #15
															del_list.append(0) #16
															plsg = getHciPlsg(fo_1)
															del_list.append(plsg) #17
															Area= 'HCI Labor Config'
															del_list.append(Area) #18
															if cont_rows['Execution Country'] == salesOrg:
																	del_list.append('Front Office Labor') #19
															else:
																	del_list.append('Intercompany Labor') #19
															office_str = 'GES Back -office Labor' if 'GES' in engg else ''
															del_list.append(office_str) #20
															del_list.append(salesOrg) #21
															lob_labor = GS_Labor_Report_Util.get_LOB_Labor(plsg)
															del_list.append(lob_labor) #22
															del_list.append(0) #23
															del_list.append('') #24
															del_list.append(cont_rows['Eng Total WTW Cost'])
															del_list.append(0)
															del_list.append(cont_rows['Eng Total List Price'])
															del_list.append(0)
															labor_sys_del.append(del_list)
		elif Item.ProductName == 'HCI Labor Upload':
				container = Item.SelectedAttributes.GetContainerByName('AR_HCI_LABOR_CONTAINER')
				if container:
						for cont_rows in container.Rows:
								if cont_rows['ProductLine'] == 'Total':
									continue
								del_list = []
								del_list.append(Item.ProductName) #0
								del_list.append(Item.PartNumber) #1
								del_list.append('AR_HCI_LABOR_CONTAINER') #2
								del_list.append(cont_rows['Deliverable']) #3
								del_list.append(cont_rows['CalculatedHours']) #4
								del_list.append(cont_rows['Productivity']) #5
								del_list.append(cont_rows['FinalHours']) #6
								del_list.append('') #7
								del_list.append('') #8
								fo_1 = cont_rows['LaborResource']
								del_list.append(cont_rows['LaborResource']) #9
								del_list.append('') #10
								del_list.append('') #11
								del_list.append(0) #12
								del_list.append(cont_rows['ExecutionCountry']) #13
								del_list.append(cont_rows['ExecutionYear']) #14
								del_list.append(cont_rows['TransferCost']) #15
								del_list.append(0) #16
								plsg = getLssPlsg(fo_1)
								del_list.append(plsg) #17
								Area= 'HCI Labor Upload'
								del_list.append(Area) #18
								if cont_rows['ExecutionCountry'] == salesOrg:
										del_list.append('Front Office Labor') #19
								else:
										del_list.append('Intercompany Labor') #19
								del_list.append('') #20
								del_list.append(salesOrg) #21
								lob_labor = GS_Labor_Report_Util.get_LOB_Labor(plsg)
								del_list.append(lob_labor) #22
								del_list.append(0) #23
								del_list.append('') #24
								del_list.append(cont_rows['W2WCost'])
								del_list.append(0)
								del_list.append(cont_rows['TotalListPrice'])
								del_list.append(0)
								labor_sys_del.append(del_list)
		elif Item.ProductName == 'Cyber':
				try:
						for cont in cyberlist:
								del_list = []
								container = Item.SelectedAttributes.GetContainerByName(cont)
								if container:
										for cont_rows in container.Rows:
												del_list = []
												if cont=='Cyber_Labor_Project_Management':
																is_pm='Cyber_Labor_Project_Management'
												else:
														is_pm=''
												if row_get(cont_rows, pick('Activity', 'Deliverable'), '') not in ('Total','Off-Site','On-Site'):
														del_list.append(prodcont_dict[cont]) #0
														del_list.append(prodcont_dict[cont]) #1
														del_list.append(cont) #2
														del_list.append(row_get(cont_rows, pick('Activity', 'Deliverable'), '')) #3
														del_list.append(row_get(cont_rows, pick('Hours', 'Calculated_Hrs'), '')) #4
														del_list.append(row_get(cont_rows, pick('Productivity', 'Adjustment_Productivity'), '')) #5
														del_list.append(row_get(cont_rows, pick('Edit Hours', 'Final_Hrs'), '')) #6
														del_list.append('') #7
														del_list.append('') #8
														fo_1=row_get(cont_rows, pick('PartNumber', 'FO_Eng'), '')
														del_list.append(row_get(cont_rows, pick('PartNumber', 'FO_Eng'), '')) #9
														del_list.append(100) #10
														del_list.append('') #11
														del_list.append(0) #12
														del_list.append(row_get(cont_rows, pick('Execution Country', 'Execution_Country'), '')) #13
														del_list.append(cont_rows['Execution_Year']) #14
														del_list.append(cont_rows['Regional_Cost']) #15
														del_list.append(0) #16
														plsg = getLssPlsg(fo_1)
														del_list.append(plsg) #17
														del_list.append('Cyber') #18
														if cont_rows['Execution Country'] == salesOrg:
																		del_list.append('Front Office Labor') #19
														else:
																		del_list.append('Intercompany Labor') #19
														del_list.append('')#20
														del_list.append(salesOrg) #21
														lob_labor = GS_Labor_Report_Util.get_LOB_Labor(plsg)
														del_list.append(lob_labor) #22
														del_list.append('') #23
														del_list.append('') #24
														del_list.append(row_get(cont_rows, pick('FOWTWCost', 'FOUnitWTWCost'), ''))
														del_list.append(0)
														del_list.append(row_get(cont_rows, pick('FO_List_Price', 'FO_ListPrice'), ''))
														del_list.append(0)
														labor_sys_del.append(del_list)
				except Exception as ex:
						Log.Info('CA_PASLaborDeliverables  cyberError-->>'+str(ex))
		
GS_Labor_Report_Util.Store_Lbr_Dtls_in_QT(Quote, Cont_Labor_map, labor_sys_del)