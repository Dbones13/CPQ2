def getWriteInProductInfo(writeInPartNumber):
    writeInProduct = SqlHelper.GetFirst("SELECT Description, ProductLine, ProductLineDescription, ProductLineSubGroupDescription, ProductLineSubGroup, UnitofMeasure from WriteInProducts where Product = '"+writeInPartNumber+"'")
    if writeInProduct is not None:
        return writeInProduct
    else:
        writeInProduct = SqlHelper.GetFirst("SELECT ProductLine, ProductLineDescription, ProductLineSubGroupDescription, ProductLineSubGroup, UnitofMeasure from THIRDPARTYWRITEINPARTS")
    return None

def PopulateChildProduct(containerRow):
        containerRow.Product.Attributes.GetByName("WriteInProductsChoices").SelectDisplayValue(str(containerRow["WriteInProducts"]))
        containerRow.Product.Attributes.GetByName("Selected_WriteIn").AssignValue(str(containerRow["WriteInProducts"]))
        containerRow.Product.Attributes.GetByName("ItemQuantity").AssignValue(str(containerRow["ItemQuantity"]))
        containerRow.Product.Attributes.GetByName("Extended Description").AssignValue(str(containerRow["ExtendedDescription"]))
        containerRow.Product.Attributes.GetByName("Price").AssignValue(str(containerRow["Price"]))
        containerRow.Product.Attributes.GetByName("cost").AssignValue(str(containerRow["Cost"]))
        containerRow.Product.Attributes.GetByName("Description").AssignValue(str(containerRow["Description"]))
        containerRow.Product.Attributes.GetByName("Product Line").AssignValue(str(containerRow["Product Line"]))
        containerRow.Product.Attributes.GetByName("Product Line Description").AssignValue(str(containerRow["Product Line Description"]))
        containerRow.Product.Attributes.GetByName("Product line sub group").AssignValue(str(containerRow["Product Line Sub Group"]))
        containerRow.Product.Attributes.GetByName("PLSG description").AssignValue(str(containerRow["PLSG Description"]))
        containerRow.Product.Attributes.GetByName("Unit of Measure").AssignValue(str(containerRow["Unit of Measure"]))

def PopulateValidPartsCon(product, category,partNumber, quantity, extendedDescription, unitListPrice, unitRegionalCost, writeInProductInfo):
    try:
        WriteInProduct_container = product.GetContainerByName("WriteInProduct")
        containerRow = WriteInProduct_container.AddNewRow('WriteIn_cpq', False)
        containerRow.GetColumnByName('Category').SetAttributeValue(category)
        containerRow["WriteInProducts"]     = partNumber
        containerRow["ItemQuantity"]        = quantity
        containerRow["ExtendedDescription"] = extendedDescription
        containerRow["Price"]               = unitListPrice
        containerRow["Cost"]                = unitRegionalCost
        containerRow["Description"]			= extendedDescription #writeInProductInfo.Description
        containerRow["Product Line"]		= writeInProductInfo.ProductLine
        containerRow["Product Line Description"] = writeInProductInfo.ProductLineDescription
        containerRow["Product Line Sub Group"] 	 = writeInProductInfo.ProductLineSubGroup
        containerRow["PLSG Description"]	= writeInProductInfo.ProductLineSubGroupDescription
        containerRow["Unit of Measure"]		= writeInProductInfo.UnitofMeasure
        PopulateChildProduct(containerRow)
        Log.Info("{},{},{},{},{},{}".format(containerRow["Description"],containerRow["Product Line"],containerRow["Product Line Description"],containerRow["Product Line Sub Group"],containerRow["PLSG Description"],containerRow["Unit of Measure"]))
        containerRow.Product.ApplyRules()
        containerRow.ApplyProductChanges()
        WriteInProduct_container.Calculate()
    except Exception, e:
        Log.Error("WriteIn:: Valid Parts Exception: "+str(e))