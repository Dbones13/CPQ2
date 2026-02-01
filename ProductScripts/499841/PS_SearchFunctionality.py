VariantTable = Quote.QuoteTables["VFD_VC_Model_Configuration"]
RecommendedVCpart = Product.GetContainerByName("VFD_Recommended_VC_PartCont")
addRecommendedVCpart = Product.GetContainerByName("VFD_Add_Recommended_VC_PartCont")
RecommendedVCpart.Rows.Clear()

selectedVC = dict()
for row in addRecommendedVCpart.Rows:
    if row.IsSelected:
        selectedVC[(row["VC Model Number"],row["Recommended Spare Part"])] = row["Quantity"]

def getAttrValue(Name):
    return Product.Attr(Name).GetValue()

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
VCModel = getAttrValue("VFD_VC_SearchByVCModel")
description = getAttrValue("VFD_VC_SearchByDescription")
sparePart = getAttrValue("VFD_VC_SearchBySparePart")
variant = getAttrValue("VFD_VC_SearchByVariant")

query = "select Distinct VC_Model,Variant_Selected_by_user,Default_Spare_part,Spare_part,PartName,RecommendationType,Quantity from VFD_VC_SPAREPARTS_MAPPING where "

if sparePart != '':
    Trace.Write("sparePart")
    query += "(Default_Spare_part like '%{}%' or Spare_part like '%{}%') AND ".format(sparePart,sparePart)

if variant != '':
    Trace.Write("variant")
    query += "Variant_Selected_by_user like '%{}%' AND ".format(variant)

if description != '':
    Trace.Write("description")
    query += "PartName like '%{}%' AND ".format(description)

if VCModel != '':
    Trace.Write("VCModel")
    query += "VC_Model like '%{}%' AND ".format(VCModel)

query += "VC_Model in ('{}')".format("','".join(VcModelList))

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