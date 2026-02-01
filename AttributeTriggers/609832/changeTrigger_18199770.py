for i in Product.GetContainerByName("AR_HCI_LABOR_CONTAINER").Rows:
    if Product.Attr('AR_HCI_SELECTALL').GetValue():
        i.IsSelected = True
    else:
        i.IsSelected = False