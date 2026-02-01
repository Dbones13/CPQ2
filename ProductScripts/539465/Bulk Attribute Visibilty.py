def makeVisible(val):
    for attribute in Product.Attributes:
        if attribute.GetHint() == "Bulk Update Attributes":
            attribute.Allowed = val

container = Product.GetContainerByName("RTU Groups")
makeVisible(container.HasSelectedRow)