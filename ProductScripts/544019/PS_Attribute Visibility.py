def hideAttr(product , attr):
    product.Attr(attr).Access = AttributeAccess.Hidden

packageContainerName = "K&E Configuration"
pricingContainerName = "Pricing Parts"
nonPricingContainerName = "Non Pricing Parts"

for attr in Product.Attributes:
    attr.Access = AttributeAccess.Editable
    if attr.DisplayType == "Container":
        container = Product.GetContainerByName(attr.Name)
        if container.Rows.Count == 0:
            attr.Access = AttributeAccess.Hidden
if Product.GetContainerByName(packageContainerName).Rows.Count != 0:
    hideAttr(Product , "Add Package")
    hideAttr(Product , "K&E Model Number")