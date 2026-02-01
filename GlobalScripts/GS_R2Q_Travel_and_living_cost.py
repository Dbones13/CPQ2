from GS_R2Q_Product_Attribute_ContColms import MigrationProductsAttributesContainerColumns as PRD
import GS_R2Q_Migration_BOM_Parts
def get_writein_product():
    return SqlHelper.GetFirst("SELECT Product FROM WRITEINPRODUCTS (nolock) WHERE product = 'Write-In Travel and Living'")

def get_writein_product_details():
    return SqlHelper.GetFirst("""
        SELECT PA.PRODUCT_ID, PA.PRODUCT_NAME
        FROM products PA
        INNER JOIN product_versions PV ON PV.product_id = PA.PRODUCT_ID
        WHERE PA.PRODUCT_NAME = '{}' AND PV.is_active = 'True'
    """.format('Write-in Products'))
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
def proposal_pricing(Quote):
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

def addOrUpdateWriteIn():
 
    writeInProductQuery = get_writein_product()
    
    if writeInProductQuery:
        # Get product details
        getWriteinPrd = get_writein_product_details()
        WriteinPrd_Id = int(getWriteinPrd.PRODUCT_ID)
        
        # Create product
        WriteinProduct = ProductHelper.CreateProduct(WriteinPrd_Id)
        WriteinProdCont = WriteinProduct.GetContainerByName('WriteInProduct')
        
        # Add new row to container
        containerRow = WriteinProdCont.AddNewRow('WriteIn_cpq', False)
        containerRow.GetColumnByName('Category').SetAttributeValue('Common')
        containerRow["Selected_WriteIn"] = str(writeInProductQuery.Product)
        
        # Fetch pricing details
        unit_list_price, unit_regional_cost = proposal_pricing(Quote)
        containerRow["Price"] = str(unit_list_price)
        containerRow["Cost"] = str(unit_regional_cost)
        
        # Assign attribute values
        product_attrs = containerRow.Product.Attributes
        product_attrs.GetByName("Writein_Category").SelectValue('Common')
        product_attrs.GetByName("Selected_WriteIn").AssignValue(str(containerRow["Selected_WriteIn"]))
        product_attrs.GetByName("Price").AssignValue(str(containerRow["Price"]))
        product_attrs.GetByName("cost").AssignValue(str(containerRow["Cost"]))
        
        containerRow.Product.ApplyRules()
        containerRow.ApplyProductChanges()
        containerRow.Calculate()
        
        WriteinProdCont.MakeAllRowsSelected()
        WriteinProdCont.Calculate()
        WriteinProduct.AddToQuote()
        #Quote.Save(False)


# Execute the function
isR2Qquote = bool(Quote.GetCustomField('R2QFlag').Content) 
BookingLOB = Quote.GetCustomField('Quote Tab Booking LOB').Content
matching_item = next((item for item in Quote.MainItems if item.Description == "Travel and Living"), None)  
saveAction = Quote.GetCustomField("R2Q_Save").Content
if saveAction != 'Save' and isR2Qquote and BookingLOB =='LSS' and not matching_item:
    addOrUpdateWriteIn()