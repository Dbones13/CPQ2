for attribute in Product.Attributes:
    if attribute.Required and not attribute.SelectedValue and attribute.DisplayType != "Container":
        Product.DisallowAttr('RTU Groups')
        Product.DisallowAttr('Add Group')
        Product.DisallowAttr('Number of Groups')
        msg = '{} field is mandatory'.format(attribute.GetLabel())
        if not Product.Messages.Contains(msg):
            Product.Messages.Add(msg)