#KE Restructure - Ashokkumar
packageContainerName = "K&E Configuration"
pricingContainerName = "Pricing Parts"
nonPricingContainerName = "Non Pricing Parts"

packageContainer = Product.GetContainerByName(packageContainerName)
partnumbercont = Product.GetContainerByName(pricingContainerName)
nonPricingCont = Product.GetContainerByName(nonPricingContainerName)

partnumbercont.Rows.Clear()
nonPricingCont.Rows.Clear()
packageContainer.Rows.Clear()
for attr in Product.Attributes:
    container = Product.GetContainerByName(attr.Name)
    attr.Access = AttributeAccess.Hidden

Product.ResetAttr('K&E Selected Model')
Product.ResetAttr('K&E Model Number')
Product.Attr('K&E Model Number').Access = AttributeAccess.Editable
Product.Attr('Add Package').Access = AttributeAccess.Editable