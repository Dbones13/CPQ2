att = Product.Attr('HCI_AFM_Additional_Media').SelectedValue.Display
Product.Attr('HCI_AFM_Additional_Media').SelectedValue.Display = str(round(float(att)))
if int(round(float(att))) < 0 or int(round(float(att))) > 5:
    Product.Attr('HCI_AFM_Additional_Media').SelectedValue.Display = '0'