import GS_DEF_CONT_ATT_DICT as upd
labor_part_qty_dict = {}
labor_part_unit_cost_dict = {}
labor_part_avg_unit_cost_cnt = {}
labor_part_avg_unit_cost_dict = {}
ScriptExecutor.Execute('GS_CA_PopulatelaborTypesTable')
ScriptExecutor.Execute('GS_CA_PopulateServicematerials')
ScriptExecutor.Execute('GS_CA_PASLaborDeliverables')
upd.cost_plsg_lob_upd(Quote)
def sumUp(productName, partNumber, cost, plsg,qty,wtw_cost,list_price,sell_price):
	if not labor_part_avg_unit_cost_cnt.get((productName, partNumber)):
		labor_part_avg_unit_cost_cnt[(productName, partNumber)] = 1
		labor_part_avg_unit_cost_dict[(productName, partNumber)] = (float(cost) * float(qty), plsg )
		labor_part_unit_cost_dict[(Item.ProductName, Item.PartNumber)] = (float(cost), plsg, wtw_cost, list_price, sell_price)
	else:
		labor_part_avg_unit_cost_cnt[(productName, partNumber)] = int(labor_part_avg_unit_cost_cnt[(productName, partNumber)]) + 1
		if labor_part_qty_dict[(productName, partNumber)]: # Error thowing on Generate document - Attempted to divide by zero.
			avg=((float(cost) * int(qty))+float(labor_part_avg_unit_cost_dict[(productName, partNumber)][0]))/(labor_part_qty_dict[(productName, partNumber)])
			labor_part_avg_unit_cost_dict[(productName, partNumber)] = ((float(labor_part_avg_unit_cost_dict[(productName, partNumber)][0])+float(float(cost) * int(qty))), plsg)
			current_wtw = labor_part_unit_cost_dict[(Item.ProductName, Item.PartNumber)][2]
			current_wtw += wtw_cost
			current_list = labor_part_unit_cost_dict[(Item.ProductName, Item.PartNumber)][3]
			current_list += list_price
			current_sell_price = labor_part_unit_cost_dict[(Item.ProductName, Item.PartNumber)][4]
			current_sell_price += sell_price
			labor_part_unit_cost_dict[(Item.ProductName, Item.PartNumber)] = (float(avg), plsg,current_wtw,current_list,current_sell_price)

def get_part_plsg(lbr_part):
	plsg = ''
	plsg = SqlHelper.GetFirst("select PLSG from HPS_LABOR_PLSG_MAPPING where Part_Num = '{0}'".format(lbr_part))
	if plsg != None:
		return plsg.PLSG
	else:
		return ''
#i=0
booking_LOB = Quote.GetCustomField('Booking LOB').Content
PRJT_item = [Item.RolledUpQuoteItem for Item in Quote.MainItems if Item.PartNumber == 'PRJT']
for Item in Quote.MainItems:
	if Item.PartNumber.startswith('HPS_') or Item.PartNumber.startswith('ADV_') or Item.PartNumber.startswith('SVC') or Item.PartNumber == "SVC-NT-EIT-E-FD-NC" or Item.QI_Winest_Import.Value =='True':
		if (Item.ProductName, Item.PartNumber) in labor_part_qty_dict:
			labor_part_qty_dict[(Item.ProductName, Item.PartNumber)] = labor_part_qty_dict[(Item.ProductName, Item.PartNumber)] + int(Item.Quantity)
		else:
			labor_part_qty_dict[(Item.ProductName, Item.PartNumber)] = int(Item.Quantity)
		plsg = ''
		#plsg = get_part_plsg(Item.PartNumber)
		plsg = Item['QI_PLSG'].Value
		wtw_cost = Item['QI_ExtendedWTWCost'].Value
		#unit_wtw_cost = Item['QI_UnitWTWCost'].Value
		list_price = Item.ExtendedListPrice
		#unit_list_price = Item.ListPrice
		sell_price = Item.ExtendedAmount
		#unit_sell_price = Item.NetPrice
		#labor_part_unit_cost_dict[(Item.ProductName, Item.PartNumber)] = (float(Item.Cost), plsg)
		sumUp(Item.ProductName, Item.PartNumber,float(Item.Cost),plsg,int(Item.Quantity),wtw_cost,list_price,sell_price)
		#Trace.Write('-->wtw-cost-check'+str(['wtwcost',Item['QI_ExtendedWTWCost'].Value,'unit wtw',Item['QI_UnitWTWCost'].Value,'List price',Item.ExtendedListPrice,'unit list price',Item.ListPrice,'sell-price->',Item.ExtendedAmount,'Unit sell-->',Item.NetPrice]))
QT_Table = Quote.QuoteTables["PAS_Labor_Parts"]
QT_Table.Rows.Clear()
Trace.Write("Labor Parts Count = "+str((labor_part_qty_dict)))
for prod_name, prod_num in labor_part_qty_dict:
	newRow = QT_Table.AddNewRow()
	newRow['Material_Name'] = prod_name
	newRow['Material_Num'] = prod_num
	newRow['Material_Qty'] = labor_part_qty_dict[(prod_name, prod_num)]
	newRow['Material_Cost'] = labor_part_unit_cost_dict[(prod_name, prod_num)][0]
	newRow['Material_TotalCost'] = labor_part_avg_unit_cost_dict[(prod_name, prod_num)][0]
	newRow['PLSG'] = labor_part_unit_cost_dict[(prod_name, prod_num)][1]
	newRow['Total_WtW_Cost'] = labor_part_unit_cost_dict[(prod_name, prod_num)][2] if labor_part_unit_cost_dict[(prod_name, prod_num)][2] else 0
	newRow['Total_List_Price'] = labor_part_unit_cost_dict[(prod_name, prod_num)][3] if labor_part_unit_cost_dict[(prod_name, prod_num)][3] else 0
	newRow['Total_Sell_Price'] = labor_part_unit_cost_dict[(prod_name, prod_num)][4] if labor_part_unit_cost_dict[(prod_name, prod_num)][4] else 0
	#Material Name	Material Num	Material Qty	Material Cost	Material Total Cost	PL
#Unit WTW Cost	Total WTW Cost	Unit List Price	Total List Price	Unit Sell Price	Total Sell Price
QT_Table.Save()