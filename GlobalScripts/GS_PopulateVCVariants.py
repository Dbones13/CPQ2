VariantTable = Quote.QuoteTables["VCModelConfiguration"]
VC_Model = Product.PartNumber

def getVaraintsData(Product):
    VariantList = []
    for attr in Product.Attributes:
        for value in attr.SelectedValues:
            if value.SystemId not in VariantList:
                VariantList.append(value.SystemId)
    return VariantList

def getSparePartsData(VC_Model,VariantList):
    SparePartsList = []
    query = ("select VC_Model,Variant_Selected_by_user,Default_Spare_part,Spare_part,PartName,RecommendationType,Quantity from VC_SPAREPARTS_MAPPING where VC_Model = '' or VC_Model in ('{}')").format(VC_Model)
    VCmodelData = SqlHelper.GetList(query)
    if VCmodelData is not None:
        for part in VCmodelData:
            if part.Default_Spare_part != '':
                SparePartsList.append(part.Default_Spare_part) 
            else:
                for variant in VariantList:
                    if variant == part.Variant_Selected_by_user:
                        SparePartsList.append(part.Spare_part)
        return SparePartsList


VariantList =getVaraintsData(Product)
SparePartsList = getSparePartsData(VC_Model,VariantList)
canEditProduct = False
for item in Quote.MainItems:
    if item.QI_SparePartsFlag.Value == "Spare Part":
        product = item.EditConfiguration()
        canEditProduct = True
        break

if canEditProduct:
    RecommendedVCpart = product.GetContainerByName("Recommended_VC_PartCont")
    for row in RecommendedVCpart.Rows:
        if row["VC Model Number"] == VC_Model:
            if row["Recommended Spare Part"] not in SparePartsList:
                row.IsSelected = False
    product.UpdateQuote()