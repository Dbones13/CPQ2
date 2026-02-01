att = Product.Attr('HCI_Insight_ExistingLicense_Events_Hundred_Pack').SelectedValue.Display
Product.Attr('HCI_Insight_ExistingLicense_Events_Hundred_Pack').SelectedValue.Display = str(round(float(att)))
if int(round(float(att))) < 0 or int(round(float(att))) > 9:
    Product.Attr('HCI_Insight_ExistingLicense_Events_Hundred_Pack').SelectedValue.Display = '0'