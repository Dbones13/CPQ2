def getCfValue(cfName):
    return Quote.GetCustomField(cfName).Content
pricingContainerName = "Pricing Parts"
partnumbercont = Product.GetContainerByName(pricingContainerName)

entitlement = getCfValue("Entitlement")
def populateContainer(product):
    partrow=partnumbercont.AddNewRow(product.ProductSystemId,False)
    partrow["Part_Number"]=product.ProductSystemId
    partrow["ItemQuantity"]= "0"
    partrow["Part_Name"]=product.ProductName
    partrow["PLSG"] = product.PLSG
    partrow["PLSG Description"] = product.PLSGDesc
    if partrow.Product.Attributes.GetByName("ItemQuantity") is not None:
        partrow.Product.Attributes.GetByName("ItemQuantity").AssignValue("0")
sql_product=SqlHelper.GetFirst("select ProductSystemId,PLSG,ProductName,PLSGDesc from IAA_PART_SUMMARY join HPS_PRODUCTS_MASTER on IAA_PART_SUMMARY.ProductSystemId = HPS_PRODUCTS_MASTER.PartNumber where IAA_PART_SUMMARY.ValidValue = '{}'".format(entitlement))
if sql_product:
    populateContainer(sql_product)