def getFloat(val):
	if val:
		return float(val)
	return 0.0
    
def getWriteInProductInfo(writeInPartNumber):
    writeInProduct = SqlHelper.GetFirst("SELECT Category,Description, ProductLine, ProductLineDescription, ProductLineSubGroupDescription, ProductLineSubGroup, UnitofMeasure,Cost,IsPSkidFactoryPart from WriteInProducts where Product = '"+writeInPartNumber+"'")
    if writeInProduct is not None:
        return writeInProduct
    return None

def PopulateChildProduct(containerRow):
        containerRow.Product.Attributes.GetByName("Writein_Category").SelectValue(str(containerRow["Category"]))
        containerRow.Product.Attributes.GetByName("Selected_WriteIn").AssignValue(str(containerRow["Selected_WriteIn"]))
        containerRow.Product.Attributes.GetByName("ItemQuantity").AssignValue(str(containerRow["ItemQuantity"]))
        containerRow.Product.Attributes.GetByName("Extended Description").AssignValue(containerRow["ExtendedDescription"])
        containerRow.Product.Attributes.GetByName("Price").AssignValue(str(containerRow["Price"]))
        containerRow.Product.Attributes.GetByName("cost").AssignValue(str(containerRow["Cost"]))
        containerRow.Product.Attributes.GetByName("Description").AssignValue(containerRow["Description"])
        containerRow.Product.Attributes.GetByName("Product Line").AssignValue(str(containerRow["Product Line"]))
        containerRow.Product.Attributes.GetByName("Product Line Description").AssignValue(str(containerRow["Product Line Description"]))
        containerRow.Product.Attributes.GetByName("Product line sub group").AssignValue(str(containerRow["Product Line Sub Group"]))
        containerRow.Product.Attributes.GetByName("PLSG description").AssignValue(str(containerRow["PLSG Description"]))
        containerRow.Product.Attributes.GetByName("Unit of Measure").AssignValue(str(containerRow["Unit of Measure"]))
        containerRow.ApplyProductChanges()


def PopulateWriteInCon(partNumber, quantity, extendedDescription, unitListPrice, unitRegionalCost, writeInProductInfo):
    try:
        WriteInProductCon = Product.GetContainerByName("Skid_Cofig_WriteInProduct_Con")
        containerRow = WriteInProductCon.AddNewRow('WriteIn_cpq')
        containerRow.GetColumnByName('Category').SetAttributeValue(str(writeInProductInfo.Category))
        containerRow["Selected_WriteIn"]     = str(partNumber)
        containerRow["ItemQuantity"]        = str(quantity)
        containerRow["ExtendedDescription"] = extendedDescription        
        containerRow["Cost"]                = unitRegionalCost
        containerRow["Price"]               = unitListPrice
        containerRow["Description"]			= writeInProductInfo.Description
        containerRow["Product Line"]		= writeInProductInfo.ProductLine
        containerRow["Product Line Description"] = writeInProductInfo.ProductLineDescription
        containerRow["Product Line Sub Group"] 	 = writeInProductInfo.ProductLineSubGroup
        containerRow["PLSG Description"]	= writeInProductInfo.ProductLineSubGroupDescription
        containerRow["Unit of Measure"]		= writeInProductInfo.UnitofMeasure
        containerRow.ApplyProductChanges()
        
        PopulateChildProduct(containerRow)
        containerRow.Calculate()
        
        
    except Exception, e:
        Trace.Write('Error while PopulateWriteInCon')
        
skidCon = Product.GetContainerByName("PRODUCTIZED _SKID_BOM")
WriteInProductCon = Product.GetContainerByName("Skid_Cofig_WriteInProduct_Con")
WriteInProductCon.Rows.Clear()

for Vrow in skidCon.Rows:
    if str(Vrow['Type'])=='W' and  str(Vrow['Error Message'])=='' and str(Vrow['Part Number'])!='':
        writeInProductInfo = getWriteInProductInfo(str(Vrow['Part Number']))
        PopulateWriteInCon(str(Vrow['Part Number']), str(Vrow['Qty']), str(Vrow['ExtendedDescription']),str(Vrow['Unit List Price']) , str(Vrow['Unit Cost']), writeInProductInfo)
        #PopulateWriteInCon(category,partNumber, quantity, extendedDescription, unitListPrice, unitRegionalCost, writeInProductInfo)
if getFloat(Product.Attributes.GetByName('Pskid Total Factory Cost').GetValue())>0 and getFloat(Product.Attributes.GetByName('PSkid Grossmargin in Percentage').GetValue())<100:
    lv_win_unitListPrice       = str(getFloat(Product.Attributes.GetByName('Pskid Total Factory Cost').GetValue()) * 100 /(100-getFloat(Product.Attributes.GetByName('PSkid Grossmargin in Percentage').GetValue())))
    lv_win_unitRegionalCost    = str(Product.Attributes.GetByName('Pskid Total Factory Cost').GetValue())
    writeIn_Integ_ProductInfo = getWriteInProductInfo('Write-In Integration Center')
    PopulateWriteInCon('Write-In Integration Center', '1', 'TOTAL FACTORY COST', lv_win_unitListPrice, lv_win_unitRegionalCost, writeIn_Integ_ProductInfo)