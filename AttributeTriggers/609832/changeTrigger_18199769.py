Productivity = Product.Attr('AR_HCI_PRODUCTIVITY').GetValue()
if (Productivity != '' and int(Productivity)<0) or (Productivity != '' and int(Productivity)>100):
    Product.Attr('AR_HCI_PRODUCTIVITY').AssignValue('')