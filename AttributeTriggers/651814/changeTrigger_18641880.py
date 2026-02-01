att = Product.Attr('HCI_AFM_ExistingLicense_Tag_License_Unlimited').SelectedValue.Display
Product.Attr('HCI_AFM_ExistingLicense_Tag_License_Unlimited').SelectedValue.Display = str(round(float(att)))
if int(round(float(att))) < 0 or int(round(float(att))) > 999:
    Product.Attr('HCI_AFM_ExistingLicense_Tag_License_Unlimited').SelectedValue.Display = '0'