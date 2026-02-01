att = Product.Attr('HCI_Insight_Standard_Cores').SelectedValue.Display
Product.Attr('HCI_Insight_Standard_Cores').SelectedValue.Display = str(round(float(att)))
if int(round(float(att))) < 4 or int(round(float(att))) > 100:
    Product.Attr('HCI_Insight_Standard_Cores').SelectedValue.Display = '0'