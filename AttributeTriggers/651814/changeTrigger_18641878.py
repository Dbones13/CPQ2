att = Product.Attr('HCI_AFM_ExistingLicense_Tag_License_10000').SelectedValue.Display
Product.Attr('HCI_AFM_ExistingLicense_Tag_License_10000').SelectedValue.Display = str(round(float(att)))
if int(round(float(att))) < 0 or int(round(float(att))) > 99:
    Product.Attr('HCI_AFM_ExistingLicense_Tag_License_10000').SelectedValue.Display = '0'