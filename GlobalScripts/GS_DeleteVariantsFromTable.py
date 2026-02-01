guId = sender.QuoteItemGuid

Quote.QuoteTables['FME_Invalid_Parts'].Rows.Clear() #CXCPQ-90702 - The invalid parts table is not being erased

VariantTable = Quote.QuoteTables["VCModelConfiguration"]
rows_to_delete = [row.Id for row in VariantTable.Rows if row["CartItemGUID"] == guId]
for row_id in rows_to_delete:
	VariantTable.DeleteRow(row_id)
VariantTable.Save()

def Vf_AddedVCParts(container, part_number):
	vfaddedVCParts = product.GetContainerByName(container)
	if vfaddedVCParts.Rows.Count > 0:
		for row in vfaddedVCParts.Rows:
			if row["VC Model Number"] == part_number:
				row.IsSelected = False
		product.UpdateQuote()

can_edit_product = False
can_edit_vfd_product = False
part_number = sender.PartNumber 

for item in Quote.MainItems:
	if item.QI_SparePartsFlag.Value == "Spare Part":
		vfdquery = SqlHelper.GetFirst("Select VFD_VC_Model from VFD_VC_Models(nolock) where VFD_VC_Model = '{}'".format(item.QI_ParentVcModel.Value))
		product = item.EditConfiguration()
		if vfdquery:
			can_edit_vfd_product = True
		else:
			can_edit_product = True
		break

if can_edit_product:
	Vf_AddedVCParts("Add_Recommended_VC_PartCont", part_number)

if can_edit_vfd_product:
	Vf_AddedVCParts("VFD_Add_Recommended_VC_PartCont", part_number)