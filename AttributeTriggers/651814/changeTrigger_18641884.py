att = Product.Attr('HCI_Insight_ExistingLicense_Single_User').SelectedValue.Display
Product.Attr('HCI_Insight_ExistingLicense_Single_User').SelectedValue.Display = str(round(float(att)))
if int(round(float(att))) < 0 or int(round(float(att))) > 5:
    Product.Attr('HCI_Insight_ExistingLicense_Single_User').SelectedValue.Display = '0'