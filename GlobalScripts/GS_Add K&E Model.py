#KE Restructure - Ashokkumar
def getproductsystemID(partnumber):
	ProductData=SqlHelper.GetFirst("Select SYSTEM_ID,PRODUCT_NAME from products where PRODUCT_CATALOG_CODE  ='"+partnumber+"' and PRODUCT_ACTIVE = 'True'")
	return ProductData

partNumber = Product.Attr("K&E Model Number").SelectedValue.ValueCode
container = Product.GetContainerByName("K&E Configuration")
Product.Attr("K&E Selected Model").AssignValue(partNumber)

systemId = getproductsystemID(partNumber).SYSTEM_ID.strip().encode('unicode_escape')
productName = getproductsystemID(partNumber).PRODUCT_NAME.strip().encode('unicode_escape')
row = container.AddNewRow(systemId)
row["Part Number"] = partNumber
row["ItemQuantity"] = "1"
Product.Attr('KE_Part_Number').AssignValue(str(partNumber))
Product.Attr('KE_Part_Name').AssignValue(str(productName))
Product.Attr('KE_Part_Number').Access = AttributeAccess.ReadOnly
Product.Attr('KE_Part_Name').Access = AttributeAccess.ReadOnly

Product.Attr('KE_Software_Release').SelectDisplayValue('R530')
Product.Attr('KE_Additional_Hard_Disk').SelectDisplayValue('No')
Product.Attr('KE_C300_Horizontal_Mounting_Kit').SelectDisplayValue('No')
Product.Attr('KE_COA_License_Type').SelectDisplayValue('Windows Professional COA')
Product.Attr('KE_Control_Solver_License').SelectDisplayValue('50ms')
Product.Attr('KE_Controller Experion peer to peer connectivity').SelectDisplayValue('No')
Product.Attr('KE_Does_installed_APP').SelectDisplayValue('No')
Product.Attr('KE_EBR_Media_Delivery').SelectDisplayValue('Electronic Download')
Product.Attr('KE_EBR_Release').SelectDisplayValue('R520')
Product.Attr('KE_EBR_Required').SelectDisplayValue('No')
Product.Attr('KE_Experion_Base_Media_Delivery').SelectDisplayValue('Electronic Download')
Product.Attr('KE_Hardware_Selection').SelectDisplayValue('Dell T5860XL')
Product.Attr('KE_ISA_Adapter_Required').SelectDisplayValue('No')
Product.Attr('KE_SESP').SelectDisplayValue('No')
Product.Attr('KE_Node_Type').SelectDisplayValue('HP DL 320 G11')