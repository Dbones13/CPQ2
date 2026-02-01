def getWriteInProductInfo(writeInPartNumber):
    writeInProduct = SqlHelper.GetFirst("SELECT Description, ProductLine, ProductLineDescription, ProductLineSubGroupDescription, ProductLineSubGroup, UnitofMeasure from WriteInProducts where Product = '"+writeInPartNumber+"'")
    if writeInProduct is not None:
        return writeInProduct
    return None

def PopulateChildProduct(containerRow,category):
        containerRow.Product.Attributes.GetByName("Writein_Category").SelectValue(category)
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

def PopulateValidPartsCon(category,partNumber, quantity, extendedDescription, unitListPrice, unitRegionalCost, writeInProductInfo):
    Trace.Write('In Skid Configuration-1')
    containerRow = WriteInProductCon.AddNewRow('WriteIn_cpq')
    containerRow.GetColumnByName('Category').SetAttributeValue(category)
    containerRow["Selected_WriteIn"]     = partNumber
    containerRow["ItemQuantity"]        = quantity
    containerRow["ExtendedDescription"] = extendedDescription
    containerRow["Price"]               = unitListPrice
    containerRow["Cost"]                = unitRegionalCost
    containerRow["Description"]			= writeInProductInfo.Description
    containerRow["Product Line"]		= writeInProductInfo.ProductLine
    containerRow["Product Line Description"] = writeInProductInfo.ProductLineDescription
    containerRow["Product Line Sub Group"] 	 = writeInProductInfo.ProductLineSubGroup
    containerRow["PLSG Description"]	= writeInProductInfo.ProductLineSubGroupDescription
    containerRow["Unit of Measure"]		= writeInProductInfo.UnitofMeasure
    Trace.Write('In skid-22')
    PopulateChildProduct(containerRow,category)
    containerRow.Calculate()
    Trace.Write('In Skid Configuration-2')

WriteInProductCon =  Product.GetContainerByName('Skid_Cofig_WriteInProduct_Con')
lv_WriteIn_Integration_flag='No'
for row in WriteInProductCon.Rows:
    if row.GetColumnByName("Selected_WriteIn").Value=='Write-In Integration Center':
        Trace.Write('In main-1')
        row['ItemQuantity']='6'
        row['Cost'] = str(Product.Attributes.GetByName('Pskid Total Factory Cost').GetValue())
        row['Price'] = str(float(Product.Attributes.GetByName('Pskid Total Factory Cost').GetValue()) * 100 /(100-float(Product.Attributes.GetByName('PSkid Grossmargin in Percentage').GetValue())))
        Trace.Write('In main-2')
        PopulateChildProduct(row,'Common')
        row.Calculate()
        lv_WriteIn_Integration_flag = 'Yes'
        break
if lv_WriteIn_Integration_flag=='No':
    Trace.Write('In main-3')
    category            = 'Common'
    partNumber          = 'Write-In Integration Center'
    quantity            = '1'
    extendedDescription = 'TOTAL FACTORY COST'
    unitListPrice       = str(float(Product.Attributes.GetByName('Pskid Total Factory Cost').GetValue()) * 100 /(100-float(Product.Attributes.GetByName('PSkid Grossmargin in Percentage').GetValue())))
    unitRegionalCost    = str(Product.Attributes.GetByName('Pskid Total Factory Cost').GetValue())
    message = ""
    writeInProductInfo = getWriteInProductInfo(partNumber)
    if writeInProductInfo is not None:
        Trace.Write('In main-4')
        PopulateValidPartsCon(category,partNumber, quantity, extendedDescription, unitListPrice, unitRegionalCost, writeInProductInfo)