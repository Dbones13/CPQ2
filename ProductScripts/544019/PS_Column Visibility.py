packageContainerName = "K&E Configuration"
Parts = ['TP-ZAMEAP','TP-ZAM2EA','TP-ZWDTF2','TP-ZA2AC1','TP-ZSDRA1','TP-ZSDRS1','TP-ZWDRA2','TP-ZSDRD1','TP-ZSDRE1','TP-ZSDRB1','TP-ZSDRC1','TP-ZSDRK1','TP-ZSDRJ1','TP-ZSHRD1','TP-ZSDRL1','TP-ZSHRA1','TP-ZSDRP1','TP-ZSDRQ1','TP-ZWDTA2','TP-ZESVT2','TP-ZG2ES1','TP-ZUSEV4','TP-ZG2EV4','TP-ZA2EV3','TP-ZAMEV3','TP-ZAMEV4','TP-ZUSER2']
packageContainer = Product.GetContainerByName(packageContainerName)
for row in packageContainer.Rows:
	product = row.Product
	if Product.Attr("K&E Selected Model").GetValue() in Parts:
		Product.AllowAttr('KE_EBR_Release')
		Product.AllowAttr('KE_EBR_Media_Delivery')
		if Product.Attr('KE_EBR_Media_Delivery').GetValue() in (None, ''):
			Product.Attr('KE_EBR_Media_Delivery').SelectDisplayValue('Electronic Download')
		Product.Attr('KE_EBR_Release').SelectDisplayValue('R520')
		if Product.Attr("KE_EBR_Required").GetValue() == "No":
			Product.DisallowAttr('KE_EBR_Release')
			Product.DisallowAttr('KE_EBR_Media_Delivery')
if Product.Name == 'Experion Station Upgrade':
	Product.DisallowAttrValues('KE_Software_Release', 'R520')
if Product.Name == 'Experion Controller Upgrade':
	Product.Attr('KE_Controller P2P Connectivity Licenses').Access = AttributeAccess.Hidden
	p2p_conct = Product.Attr('KE_Controller Experion peer to peer connectivity').GetValue()
	if p2p_conct in ('Yes', 'yes'):
		Product.Attributes.GetByName('KE_Controller P2P Connectivity Licenses').AssignValue('1')
	else:
		Product.Attributes.GetByName('KE_Controller P2P Connectivity Licenses').AssignValue('0')