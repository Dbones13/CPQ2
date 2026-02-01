VariantTable = Quote.QuoteTables["VCModelConfiguration"]
RecommendedVCpart = Product.GetContainerByName("Recommended_VC_PartCont")

def getVcModels(Quote):
    partsQty = dict()
    for item in Quote.Items:
        if item.QI_SparePartsFlag.Value == "Spare Part":
            partsQty[item.PartNumber] = item.Quantity
    return partsQty

def getVariantQuotetable():
    VcModelList = []
    tableData = dict()
    for row in VariantTable.Rows:
        VcModel = row["PartNumber"]
        if VcModel not in VcModelList:
            VcModelList.append(VcModel)
            tableData[row["PartNumber"]] = list()
        if row["AttributeValueSystemId"] not in tableData[row["PartNumber"]]:
            tableData[row["PartNumber"]].append(row["AttributeValueSystemId"])
    return tableData,VcModelList

def populateRecommendedVCparts(part):
    vcRow = RecommendedVCpart.AddNewRow()
    vcRow["VC Model Number"] = part.VC_Model
    vcRow["Selected Variant"] = part.Variant_Selected_by_user
    vcRow["Recommended Spare Part"] = part.Default_Spare_part if part.Default_Spare_part else part.Spare_part
    vcRow["Spare Part Description"] = part.PartName
    vcRow["Spare Parts Type"] = part.RecommendationType
    vcRow["Quantity"] = part.Quantity

tableData,VcModelList = getVariantQuotetable()
VcModelList.append('')
query = ("select Distinct VC_Model,Variant_Selected_by_user,Default_Spare_part,Spare_part,PartName,RecommendationType,Quantity from VC_SPAREPARTS_MAPPING where VC_Model in ('{}')").format("','".join(VcModelList))
VCmodelData = SqlHelper.GetList(query)

if VCmodelData is not None:
    for part in VCmodelData:
        if part.Default_Spare_part != '':
            populateRecommendedVCparts(part)
        else:
            for key in tableData.keys():
                for variant in tableData.get(key):
                    if variant == part.Variant_Selected_by_user:
                        populateRecommendedVCparts(part)
partsQty = getVcModels(Quote)
for row in RecommendedVCpart.Rows:
    if row["Recommended Spare Part"] in partsQty:
        row.IsSelected = True
        row["Quantity"] = str(partsQty[row["Recommended Spare Part"]])
RecommendedVCpart.Calculate()