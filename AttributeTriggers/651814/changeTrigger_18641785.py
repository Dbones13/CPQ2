att = Product.Attr('HCI_PHD_Standard Device').SelectedValue.Display
Product.Attr('HCI_PHD_Standard Device').SelectedValue.Display = str(round(float(att)))
if int(round(float(att))) < 0 or int(round(float(att))) > 9999:
    Product.Attr('HCI_PHD_Standard Device').SelectedValue.Display = '0'