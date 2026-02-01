att = Product.Attr('HCI_Insight_Standard_Device_CALs').SelectedValue.Display
Product.Attr('HCI_Insight_Standard_Device_CALs').SelectedValue.Display = str(round(float(att)))
if int(round(float(att))) < 0 or int(round(float(att))) > 9999:
    Product.Attr('HCI_Insight_Standard_Device_CALs').SelectedValue.Display = '0'