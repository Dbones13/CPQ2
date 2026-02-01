# GS_LabourChange
from GS_GetPriceFromCPS import getPrice
from GS_Populate_Labour_WTW import populateWTW
from GS_FinalizedActivities import PopulateFinalizedActivities
from GS_CyberProductModule import CyberProduct
import math
from System import DateTime
from GS_PCN_Populate_Write_Ins import updateWriteIn

def resetColumnValue(container , columnName , oldValue , rowIndex):
	for row in container.Rows:
		if row.RowIndex == rowIndex:
			row[columnName] = str(oldValue)

def child_update(Product,labor_list,container_name,product_name,partsummary_list):
	SelectedProducts = Product.GetContainerByName('Cyber Configurations')
	for row in SelectedProducts.Rows:
		if row["Part Desc"] == product_name[container_name][2]:
			activities = row.Product.GetContainerByName('Activities')
			for activity in activities.Rows:
				Trace.Write('Identifier -- '+str(activity['Identifier'])+' ---labor_list-- '+str(labor_list))
				if activity['Identifier'] in labor_list.keys():
					Trace.Write('Inside Child IF')
					val = labor_list[activity['Identifier']]
					activity["PartNumber"] = val[0]
					activity["Activity_Type"] = val[1]
					activity["Activity"] = val[2]
					activity["Hours"] = val[3]
					activity["Edit Hours"] = val[4]
					activity["List_Price"] = val[5]
					activity["Productivity"] = val[6]
					activity["Comments"] = val[7]
					activity["FOWTWCost"] = val[8]
					activity["FO_MPA_Price"] = val[9]
					activity["Error_Message"] = val[10]
					activity["Execution Country"] = val[11]
					activity["Execution_Year"] = val[12]
					activity["Currency"] = val[13]
					activity["CostCurrency"] = val[14]
					activity["Pricing"] = val[15]
					activity['Regional_Cost'] = val[16]
					activity["FO_List_Price"] = val[17]
			partsummary = row.Product.GetContainerByName('AR_Cyber_PartsSummary')
			deletelist = []
			for part_row in partsummary.Rows:
				if part_row['PartNumber'] in partsummary_list.keys():
					val = partsummary_list[part_row['PartNumber']]
					if int(val[1])> 1:
						part_row['Final Quantity'] = val[6]
						part_row['Adj Quantity'] = val[5]
						part_row['Comments'] = val[7]
						part_row['Quantity'] = val[1]
						part_row['PartDescription'] = val[2]
						part_row['PLSG'] = val[3]
						part_row['plsgDescription'] = val[4]
						part_row['Attribute'] = val[0]
					else:
						deletelist.append(part_row.RowIndex)
					partsummary_list.pop(part_row['PartNumber'], None)

			if partsummary_list:			
				for key,val in partsummary_list.items():
					parts = partsummary.AddNewRow(False)
					parts['Attribute'] = 'labor'
					parts['PartNumber'] = str(key)
					parts['Quantity'] =  val[1]
					parts['PartDescription'] = val[2]
					parts['PLSG'] = val[3]
					parts['plsgDescription'] = val[4]
					parts['Adj Quantity'] = val[5]
					parts['Final Quantity'] = val[6]
			
			if len(deletelist) > 0:
				for row_index in sorted(deletelist, reverse=True):
					partsummary.DeleteRow(row_index)

			PopulateFinalizedActivities(row.Product)
			row.ApplyProductChanges()
		if row["Part Desc"] in ['PCN Hardening','Cyber App Control']:
			updateWriteIn(row.Product)

def onContainerCellEdit(Quote, Product, TagParserQuote, container_name, changedCell, changedColumn, rowIndex, newValue, oldValue):
	cyber = CyberProduct(Quote, Product, TagParserQuote)
	quotesalesOrg = Quote.GetCustomField('Sales Area').Content
	quotecurrency = Quote.GetCustomField('Currency').Content
	product_name = {'AR_SMX_Activities':['SMX','AR_Cyber_PartsSummary','SMX','SMX_Execution_Year_Container'],'AR_MSS_Activities':['MSS','AR_MSS_PartsSummary','MSS','MSS_Execution_Year_Container'],'AR_CAC_Activities':['CYBER_APP_CNTRL','AR_CAC_PartsSummary','Cyber App Control','CAC_Execution_Year_Container'],'AR_PCNH_Activities':['PCN','AR_PCNH_PartsSummary','PCN Hardening','PCN_Execution_Year_Container'],'AR_Assessment_Activities':['ASSESSMENT','AR_Assessments_PartsSummary','Assessments','Ass_Execution_Year_Container'],'Generic_System_Activities':['Cyber Generic System','Generic_System_PartsSummary','Cyber Generic System','Generic_Execution_Year_Container']}
	container = Product.GetContainerByName(container_name)
	if changedColumn == "Edit Hours" and (float(newValue) < 0 or float(newValue) > 999999):
		resetColumnValue(container , changedColumn , oldValue , rowIndex)

	elif changedColumn  == "Edit Hours":
		total_hours = 0
		hrs = 0
		onsite_hrs = 0
		offsite_hrs = 0
		for row in container.Rows:
			Trace.Write('Edit Hours --- '+str(row['Edit Hours']))
			if product_name[container_name][0] != 'MSS':
				if row['Activity'] not in ['Travel Time','Cyber Coordination - 10%','Cyber Coordination','Cyber  Coordination 10%','Network Cyber Coordination','Network Travel Time','Cyber Travel Time','FDS/DDS Documentation','Travel (onsite to customer)','Customer Assessment/Evaluation Phase','Final Phase Documentation Preparation','Total','Off-Site','On-Site']:
					total_hours += float(row['Edit Hours']) if row['Edit Hours'] else 0
			else:
				if 'onsite' in row['Activity']:
					total_hours += float(row['Edit Hours']) if row['Edit Hours'] else 0

		cybert_coord_per = total_hours*0.10
		if cybert_coord_per > 0 and cybert_coord_per <= 8:
			cyber_coord_hrs = 8
		elif cybert_coord_per >= 40:
			cyber_coord_hrs = 40
		else:
			cyber_coord_hrs = cybert_coord_per

		for row in container.Rows:
			if row['Activity'] in ['Cyber Coordination - 10%','Cyber Coordination','Cyber  Coordination 10%','Network Cyber Coordination','MSS Cyber Coordination']:
				row['Edit Hours'] = str(int(math.ceil(cyber_coord_hrs)))

		for row in container.Rows:
			if row['Activity'] != 'On-Site' and row['Activity_Type']=='Onsite':
				onsite_hrs += int(float(row['Edit Hours'])) if row['Edit Hours'] else 0
			if row['Activity'] != 'Off-Site' and row['Activity_Type']=='Offsite':
				offsite_hrs += int(float(row['Edit Hours'])) if row['Edit Hours'] else 0

		for row in container.Rows:
			if row['Activity'] == 'Total':
				hrs += onsite_hrs + offsite_hrs
				row['Edit Hours'] = str(hrs)
			if row['Activity'] == 'On-Site':
				row['Edit Hours'] = str(onsite_hrs)
			if row['Activity'] == 'Off-Site':
				row['Edit Hours'] = str(offsite_hrs)
		for row in container.Rows:
			if row['Identifier'] not in ['Total','On-Site','Off-Site']:
				if row["Edit Hours"] in ('','0.0','0'):
					row["FOWTWCost"] = '0'
					row["Regional_Cost"] = '0'
					row["FO_MPA_Price"] = '0'
					row["List_Price"] = '0'
					row["FO_List_Price"] = '0'
					row["Pricing"] = '0'
				else:
					cyber.populateActivityListPricing(container_name,True)
				
		populateWTW([container_name], Product, Quote)
		labor_list = {}
		for row in container.Rows:
			labor_list[row['Identifier']]= [row["PartNumber"],row["Activity_Type"],row["Activity"],row["Hours"],row["Edit Hours"],row["List_Price"],row["Productivity"],row["Comments"],row["FOWTWCost"],row["FO_MPA_Price"],row["Error_Message"],row["Execution Country"],row["Execution_Year"],row["Currency"],row["CostCurrency"],row["Pricing"],row['Regional_Cost'],row["FO_List_Price"]]

		part_qty_NMON_ST = 0
		part_qty_NSER_ST = 0
		part_qty_NCOS_ST = 0
		part_qty_NRSC_ST = 0
		for row in container.Rows: #labor qty each parts
			if row['PartNumber'] == 'SVC-NMON-ST':
				part_qty_NMON_ST += int(float(row['Edit Hours'])) if row['Edit Hours'] else 0
			if row['PartNumber'] == 'SVC-NSER-ST':
				part_qty_NSER_ST += int(float(row['Edit Hours'])) if row['Edit Hours'] else 0
			if row['PartNumber'] == 'SVC-NCOS-ST':
				part_qty_NCOS_ST += int(float(row['Edit Hours'])) if row['Edit Hours'] else 0
			if row['PartNumber'] == 'SVC-NRSC-ST':
				part_qty_NRSC_ST += int(float(row['Edit Hours'])) if row['Edit Hours'] else 0

		part_qty_dict = {'SVC-NMON-ST':part_qty_NMON_ST,'SVC-NSER-ST':part_qty_NSER_ST,'SVC-NCOS-ST':part_qty_NCOS_ST,'SVC-NRSC-ST':part_qty_NRSC_ST}
		labor_part_list = []
		partsSummaryTable = Product.GetContainerByName(product_name[container_name][1])
		for row in partsSummaryTable.Rows:
			if (row['PartNumber']).StartsWith('SVC'):
				labor_part_list.append(row['PartNumber'])

		partsummary_list = {}
		deletelist = []
		partsSummaryTable = Product.GetContainerByName(product_name[container_name][1])
		for key,val in part_qty_dict.items():
			if key not in labor_part_list and val>0:
				partSummary = SqlHelper.GetFirst("SELECT PartNumber, ProductLineDesc, PLSG, PRODUCT_LINE_DESC, PRODUCT_LINE_SUBGROUP_DESC FROM HPS_PRODUCTS_MASTER WHERE PartNumber = '{}'".format(key))
				parts = partsSummaryTable.AddNewRow()
				parts['Attribute'] = 'labor'
				parts['PartNumber'] = str(key)
				parts['Quantity'] =  str(val)
				parts['PartDescription'] = partSummary.ProductLineDesc
				parts['PLSG'] = partSummary.PLSG
				parts['plsgDescription'] = str(partSummary.PRODUCT_LINE_DESC) +"-"+ str(partSummary.PRODUCT_LINE_SUBGROUP_DESC)
				adj_quantity = 0 if parts['Adj Quantity'] == '' else int(parts['Adj Quantity'])
				parts['Final Quantity'] = str(int(parts['Quantity']) + adj_quantity)
				partsummary_list[str(key)] = ['labor',str(val),partSummary.ProductLineDesc ,partSummary.PLSG, parts['plsgDescription'],parts['Adj Quantity'] ,parts['Final Quantity'], parts['Comments']]
		else:
			for row in partsSummaryTable.Rows:
				if (row['PartNumber']).StartsWith('SVC'):
					if row['PartNumber'] == key and val>0:
						row['Quantity'] = str(val)
						adj_quantity = 0 if row['Adj Quantity'] == '' else int(row['Adj Quantity'])
						row['Final Quantity'] = str(int(row['Quantity']) + adj_quantity)
						partsummary_list[str(key)] = ['labor',str(val),row['PartDescription'],row['PLSG'], row['plsgDescription'],row['Adj Quantity'] ,row['Final Quantity'], row['Comments']]
					if row['PartNumber'] == key and val<1:
						partsummary_list[str(key)] = ['labor',str(val),row['PartDescription'],row['PLSG'], row['plsgDescription'],row['Adj Quantity'] ,str(val), row['Comments']]
						deletelist.append(row.RowIndex)
		if len(deletelist) > 0:
			for row_index in sorted(deletelist, reverse=True):
				partsSummaryTable.DeleteRow(row_index)
		if container_name != 'Generic_System_Activities':
			Trace.Write('child update -- -')
			child_update(Product,labor_list,container_name,product_name,partsummary_list)

	elif changedColumn  == "PartNumber":
		current_row = Product.GetContainerByName(container_name).Rows[rowIndex]
		Salesorg = Product.ParseString("<* TABLE ( SELECT Execution_Country_Sales_Org FROM NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING WHERE Execution_County = '{}' ) *>".format(current_row['Execution Country']))
		Cost_Currency = Product.ParseString("<* TABLE ( SELECT Exchange_Rate FROM Currency_ExchangeRate_Mapping WHERE From_Currency = '<* TABLE ( SELECT Cost_Currency_Code FROM HPS_Labor_Cost_Data WHERE Sales_Org = '{}' AND Part_Number = '{}' ) *>' AND To_Currency = '{}' ) *>".format(Salesorg,current_row["PartNumber"],quotecurrency))
		current_row["CostCurrency"] = Cost_Currency if Cost_Currency !='' else '0.00'
		cost = Product.ParseString("<* TABLE ( SELECT Cost_CurrentMonth_Year1 FROM HPS_Labor_Cost_Data WHERE Sales_Org = '{}' AND Part_Number = '{}' ) *> ".format(quotesalesOrg,current_row["PartNumber"]))
		cost_val = cost if cost !='' else 0.00
		if current_row["CostCurrency"] != '':
			unit_cost = float(cost_val) * float(current_row["CostCurrency"]) if current_row["CostCurrency"] else 0
			current_row["Pricing"] = str(round(unit_cost,2))
		priceDict = dict()
		list_set = [current_row['PartNumber']]
		PriceData = getPrice(Quote,priceDict,list_set,TagParserQuote)
		if current_row["Edit Hours"] not in ('','0.0','0'):
			current_row["List_Price"] = str((PriceData.get(current_row['PartNumber'],0.00)))
			current_row["FO_List_Price"] = str(float(PriceData.get(current_row['PartNumber'],0.00)) * float(current_row["Edit Hours"])) if current_row['Edit Hours'] else 0

		populateWTW([container_name], Product, Quote)
		labor_list = {}
		for row in container.Rows:
			labor_list[row['Identifier']]= [row["PartNumber"],row["Activity_Type"],row["Activity"],row["Hours"],row["Edit Hours"],row["List_Price"],row["Productivity"],row["Comments"],row["FOWTWCost"],row["FO_MPA_Price"],row["Error_Message"],row["Execution Country"],row["Execution_Year"],row["Currency"],row["CostCurrency"],row["Pricing"],row['Regional_Cost'],row["FO_List_Price"]]

		part_qty_NMON_ST = 0
		part_qty_NSER_ST = 0
		part_qty_NCOS_ST = 0
		part_qty_NRSC_ST = 0
		for row in container.Rows: #labor qty each parts
			if row['PartNumber'] == 'SVC-NMON-ST':
				part_qty_NMON_ST += int(float(row['Edit Hours'])) if row['Edit Hours'] else 0
			if row['PartNumber'] == 'SVC-NSER-ST':
				part_qty_NSER_ST += int(float(row['Edit Hours'])) if row['Edit Hours'] else 0
			if row['PartNumber'] == 'SVC-NCOS-ST':
				part_qty_NCOS_ST += int(float(row['Edit Hours'])) if row['Edit Hours'] else 0
			if row['PartNumber'] == 'SVC-NRSC-ST':
				part_qty_NRSC_ST += int(float(row['Edit Hours'])) if row['Edit Hours'] else 0

		part_qty_dict = {'SVC-NMON-ST':part_qty_NMON_ST,'SVC-NSER-ST':part_qty_NSER_ST,'SVC-NCOS-ST':part_qty_NCOS_ST,'SVC-NRSC-ST':part_qty_NRSC_ST}

		labor_part_list = []
		partsSummaryTable = Product.GetContainerByName(product_name[container_name][1])
		for row in partsSummaryTable.Rows:
			if (row['PartNumber']).StartsWith('SVC'):
				labor_part_list.append(row['PartNumber'])

		partsummary_list = {}
		deletelist = []
		for key,val in part_qty_dict.items():
			if key not in labor_part_list and val>0:
				partSummary = SqlHelper.GetFirst("SELECT PartNumber, ProductLineDesc, PLSG, PRODUCT_LINE_DESC, PRODUCT_LINE_SUBGROUP_DESC FROM HPS_PRODUCTS_MASTER WHERE PartNumber = '{}'".format(key))
				parts = partsSummaryTable.AddNewRow()
				parts['Attribute'] = 'labor'
				parts['PartNumber'] = str(key)
				parts['Quantity'] =  str(val)
				parts['PartDescription'] = partSummary.ProductLineDesc
				parts['PLSG'] = partSummary.PLSG
				parts['plsgDescription'] = str(partSummary.PRODUCT_LINE_DESC) +"-"+ str(partSummary.PRODUCT_LINE_SUBGROUP_DESC)
				adj_quantity = 0 if parts['Adj Quantity'] == '' else int(parts['Adj Quantity'])
				parts['Final Quantity'] = str(int(parts['Quantity']) + adj_quantity)
				partsummary_list[str(key)] = ['labor',str(val),partSummary.ProductLineDesc ,partSummary.PLSG, parts['plsgDescription'],parts['Adj Quantity'] ,parts['Final Quantity'], parts['Comments']]
			else:
				for row in partsSummaryTable.Rows:
					if (row['PartNumber']).StartsWith('SVC'):
						if row['PartNumber'] == key and val>0:
							row['Quantity'] = str(val)
							adj_quantity = 0 if row['Adj Quantity'] == '' else int(row['Adj Quantity'])
							row['Final Quantity'] = str(int(row['Quantity']) + adj_quantity)
							partsummary_list[str(key)] = ['labor',str(val),row['PartDescription'],row['PLSG'], row['plsgDescription'],row['Adj Quantity'] ,row['Final Quantity'], row['Comments']]
						if row['PartNumber'] == key and val<1:
							partsummary_list[str(key)] = ['labor',str(val),row['PartDescription'],row['PLSG'], row['plsgDescription'],row['Adj Quantity'] ,str(val), row['Comments']]
							deletelist.append(row.RowIndex)
		if len(deletelist) > 0:
			for row_index in sorted(deletelist, reverse=True):
				partsSummaryTable.DeleteRow(row_index)
		if container_name != 'Generic_System_Activities':
			child_update(Product,labor_list,container_name,product_name,partsummary_list)

	elif changedColumn  == "Comments":
		labor_list = {}
		partsummary_list = {}
		for row in container.Rows:
			labor_list[row['Identifier']]= [row["PartNumber"],row["Activity_Type"],row["Activity"],row["Hours"],row["Edit Hours"],row["List_Price"],row["Productivity"],row["Comments"],row["FOWTWCost"],row["FO_MPA_Price"],row["Error_Message"],row["Execution Country"],row["Execution_Year"],row["Currency"],row["CostCurrency"],row["Pricing"],row['Regional_Cost'],row["FO_List_Price"]]
		if container_name != 'Generic_System_Activities':
			child_update(Product,labor_list,container_name,product_name,partsummary_list)

	elif changedColumn  == "Execution Country":
		current_row = Product.GetContainerByName(container_name).Rows[rowIndex]
		current_row.GetColumnByName('Execution Country').SetAttributeValue(current_row["Execution Country"])
		Log.Info("cellchange----country--->"+str(current_row["Execution Country"]))
		Salesorg = Product.ParseString("<* TABLE ( SELECT Execution_Country_Sales_Org FROM NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING WHERE Execution_County = '{}' ) *>".format(current_row['Execution Country']))
		cost_currency = Product.ParseString("<* TABLE ( SELECT Exchange_Rate FROM Currency_ExchangeRate_Mapping WHERE From_Currency = '<* TABLE ( SELECT Cost_Currency_Code FROM HPS_Labor_Cost_Data WHERE Sales_Org = '{}' AND Part_Number = '{}' ) *>' AND To_Currency = '{}' ) *>".format(Salesorg,current_row["PartNumber"],quotecurrency))
		current_row["CostCurrency"] = cost_currency
		if cost_currency !='':
			current_row['Currency'] = quotecurrency
			cost = Product.ParseString("<* TABLE ( SELECT Cost_CurrentMonth_Year1 FROM HPS_Labor_Cost_Data WHERE Sales_Org = '{}' AND Part_Number = '{}' ) *> ".format(quotesalesOrg,current_row["PartNumber"]))
			cost_val = cost if cost !='' else 0.00
			unit_cost = float(cost_val) * float(current_row["CostCurrency"]) if current_row["CostCurrency"] else 0
			current_row["Pricing"] = str(round(unit_cost,2))
		populateWTW([container_name], Product, Quote, True)
		labor_list = {}
		partsummary_list = {}
		for row in container.Rows:
			labor_list[row['Identifier']]= [row["PartNumber"],row["Activity_Type"],row["Activity"],row["Hours"],row["Edit Hours"],row["List_Price"],row["Productivity"],row["Comments"],row["FOWTWCost"],row["FO_MPA_Price"],row["Error_Message"],row["Execution Country"],row["Execution_Year"],row["Currency"],row["CostCurrency"],row["Pricing"],row['Regional_Cost'],row["FO_List_Price"]]
		if container_name != 'Generic_System_Activities':
			child_update(Product,labor_list,container_name,product_name,partsummary_list)

	elif changedColumn  == "Execution_Year":
		current_row = Product.GetContainerByName(container_name).Rows[rowIndex]
		not_allowed = cyber.hide_year(product_name[container_name][2])
		current_row.GetColumnByName('Execution_Year').ReferencingAttribute.SelectDisplayValue(current_row["Execution_Year"])
		current_row.Product.DisallowAttrValues(product_name[container_name][3], *not_allowed)
		current_row.Calculate()
		priceDict = dict()
		list_set = [current_row['PartNumber']]
		PriceData = getPrice(Quote,priceDict,list_set,TagParserQuote)
		Log.Info("cellchange----year--->"+str(current_row["Execution_Year"]))
		if current_row["Edit Hours"] not in ('','0.0','0'):
			if current_row["Execution_Year"] == str(DateTime.Now.Year):
				current_row["List_Price"] = str((PriceData.get(current_row['PartNumber'],0.00)))
				current_row["FO_List_Price"] = str((float(PriceData.get(current_row['PartNumber'],0.00)) * float(current_row["Edit Hours"]))) if current_row['Edit Hours'] else 0
			else:
				if current_row["Execution_Year"] == str(DateTime.Now.Year + 1):
					power = 1
				elif current_row["Execution_Year"] == str(DateTime.Now.Year + 2):
					power = 2
				elif current_row["Execution_Year"] == str(DateTime.Now.Year + 3):
					power = 3	
				salesOrg = Quote.GetCustomField("Sales Area").Content
				LOB = Quote.GetCustomField("Booking LOB").Content
				query = "Select * from YOY_INFLATION_RATE where salesOrg = '{0}' and LOB = '{1}'".format(salesOrg,LOB)
				res = SqlHelper.GetFirst(query)
				price = float(PriceData.get(current_row['PartNumber'],0.00))
				if power == 1 and res is not None:
					inflationRate1 = res.Inflation_Rate
					price = (float(PriceData.get(current_row['PartNumber'],0.00)) * float(1 + float(inflationRate1)))
				elif power == 2 and res is not None:
					inflationRate1 = res.Inflation_Rate
					inflationRate2 = res.Inflation_Rate_Year2
					price = (float(PriceData.get(current_row['PartNumber'],0.00)) * float(1 + float(inflationRate1))* float(1 + float(inflationRate2)))
				elif power == 3 and res is not None:
					inflationRate1 = res.Inflation_Rate
					inflationRate2 = res.Inflation_Rate_Year2
					inflationRate3 = res.Inflation_Rate_Year3
					price = (float(PriceData.get(current_row['PartNumber'],0.00)) * float(1 + float(inflationRate1))* float(1 + float(inflationRate2))* float(1 + float(inflationRate3)))
				else:
					inflationRate = 0.0
				fo_list_price = price if price else 0
				current_row['List_Price'] = str(float(fo_list_price))
				current_row["FO_List_Price"] = str((float(fo_list_price) * float(current_row["Edit Hours"]))) if current_row['Edit Hours'] else 0
		else:
			current_row["FO_List_Price"] = "0.0"
		populateWTW([container_name], Product, Quote, True)
		labor_list = {}
		partsummary_list = {}
		for row in container.Rows:
			labor_list[row['Identifier']]= [row["PartNumber"],row["Activity_Type"],row["Activity"],row["Hours"],row["Edit Hours"],row["List_Price"],row["Productivity"],row["Comments"],row["FOWTWCost"],row["FO_MPA_Price"],row["Error_Message"],row["Execution Country"],row["Execution_Year"],row["Currency"],row["CostCurrency"],row["Pricing"],row['Regional_Cost'],row["FO_List_Price"]]
		if container_name != 'Generic_System_Activities':
			child_update(Product,labor_list,container_name,product_name,partsummary_list)