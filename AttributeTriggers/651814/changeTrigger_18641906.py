att = Product.Attr('HCI_PHD_ESCALATIONFACTOR').SelectedValue.Display
Product.Attr('HCI_PHD_ESCALATIONFACTOR').SelectedValue.Display = str(round(float(att)))
if int(round(float(att))) < 0:
    Product.Attr('HCI_PHD_ESCALATIONFACTOR').SelectedValue.Display = '1'