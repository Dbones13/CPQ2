att = Product.Attr('HCI_Insight_SaaS_license').SelectedValue.Display
Product.Attr('HCI_Insight_SaaS_license').SelectedValue.Display = str(round(float(att)))
if int(round(float(att))) < 0 or int(round(float(att))) > 10000:
    Product.Attr('HCI_Insight_SaaS_license').SelectedValue.Display = '0'