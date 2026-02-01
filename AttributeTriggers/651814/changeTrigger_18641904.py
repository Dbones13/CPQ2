if Product.Attr('HCI_PHD_BGP_SUPPORT').SelectedValue:
	att = Product.Attr('HCI_PHD_BGP_SUPPORT').SelectedValue.Display
	#Product.Attr('HCI_PHD_BGP_SUPPORT').SelectedValue.Display = str(int(round(float(att))))
	if int(round(float(att))) < 0:
		Product.Attr('HCI_PHD_BGP_SUPPORT').SelectedValue.Display = '1'