from GS_R2Q_Product_Attribute_ContColms import MigrationProductsAttributesContainerColumns as PRD
import GS_R2Q_Migration_BOM_Parts
def getFloat(Var):
	return float(Var) if Var else 0

def getFinalHours(row, Total_cost):
	if row["Deliverable"] not in ('Off-Site', 'On-Site', 'Total'):
		Total_cost += round(getFloat(row["Regional_Cost"]))
	return Total_cost

def appendproducts(item):
	selectedProducts = GS_R2Q_Migration_BOM_Parts.getSelectedProducts(item)
	if any(upgrade in selectedProducts for upgrade in ['FDM Upgrade 1', 'FDM Upgrade 2', 'FDM Upgrade 3']):
		selectedProducts.append('FDM Upgrade')
	if "FSC to SM" in selectedProducts:
		selectedProducts.append('FSC to SM Audit')
	if "FSC to SM IO Migration" in selectedProducts:
		selectedProducts.append('FSC to SM IO Audit')
	return selectedProducts
def proposal_pricing(Quote,item):
	for item in Quote.MainItems:
		if item.ProductName in ("MSID_New") :
			Total_cost = 0
			selectedProducts = appendproducts(item)
			for product in selectedProducts:
					Trace.Write(str(PRD.product_containers))
					container = item.SelectedAttributes.GetContainerByName(PRD.product_containers.get(product))
					if container:
						for row in filter(lambda x: x['Deliverable_Type'] == 'Onsite' , container.Rows):
							Total_cost = getFinalHours(row, Total_cost)
	unit_regional_cost = Total_cost * 0.25
	total_Expense_cost_factor = unit_regional_cost*0.10
	unit_list_price = unit_regional_cost+total_Expense_cost_factor
	#Quote.GetCustomField("Travel_List_Price").Content = str(total_Expense_ListPrice)
	return unit_list_price,unit_regional_cost