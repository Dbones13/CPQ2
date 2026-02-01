VariantTable = Quote.QuoteTables["VFD_VC_Model_Configuration"]
RecommendedVCpart = Product.GetContainerByName("VFD_Recommended_VC_PartCont")
addRecommendedVCpart = Product.GetContainerByName("VFD_Add_Recommended_VC_PartCont")
RecommendedVCpart.Rows.Clear()

def resetAttr(name):
    Product.DisallowAttr(name)
    Product.AllowAttr(name)

selectedVC = dict()
for row in addRecommendedVCpart.Rows:
    item = Quote.GetItemByUniqueIdentifier(row.UniqueIdentifier)
    if row.IsSelected and item:
        row["Quantity"] = str(item.Quantity)
        selectedVC[(row["VC Model Number"],row["Recommended Spare Part"])] = row["Quantity"]

resetAttr("VFD_VC_SearchByVCModel")
resetAttr("VFD_VC_SearchByDescription")
resetAttr("VFD_VC_SearchBySparePart")
resetAttr("VFD_VC_SearchByVariant")

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

    qty = selectedVC.get((vcRow["VC Model Number"] , vcRow["Recommended Spare Part"]))
    if qty:
        vcRow.IsSelected = True
        vcRow["Quantity"] = qty

tableData,VcModelList = getVariantQuotetable()
VcModelList.append('')
query = ("select Distinct VC_Model,Variant_Selected_by_user,Default_Spare_part,Spare_part,PartName,RecommendationType,Quantity from VFD_VC_SPAREPARTS_MAPPING where VC_Model in ('{}')").format("','".join(VcModelList))
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
RecommendedVCpart.Calculate()