att = Product.Attr('HCI_Insight_Additional_Media_Copies').SelectedValue.Display
Product.Attr('HCI_Insight_Additional_Media_Copies').SelectedValue.Display = str(round(float(att)))
if int(round(float(att))) < 0 or int(round(float(att))) > 5:
    Product.Attr('HCI_Insight_Additional_Media_Copies').SelectedValue.Display = '0'