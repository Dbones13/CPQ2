att = Product.Attr('HCI_PHD_ExistingLicense_Tags_Base_Size').SelectedValue.Display
Product.Attr('HCI_PHD_ExistingLicense_Tags_Base_Size').SelectedValue.Display = str(round(float(att)))
if int(round(float(att))) < 0 or int(round(float(att))) > 9999:
    Product.Attr('HCI_PHD_ExistingLicense_Tags_Base_Size').SelectedValue.Display = '0'