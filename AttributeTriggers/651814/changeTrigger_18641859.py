att = Product.Attr('HCI_PHD_ExistingLicense_Peer_Tags_Lincensed').SelectedValue.Display
Product.Attr('HCI_PHD_ExistingLicense_Peer_Tags_Lincensed').SelectedValue.Display = str(round(float(att)))
if int(round(float(att))) < 0 or int(round(float(att))) > 9999999:
    Product.Attr('HCI_PHD_ExistingLicense_Peer_Tags_Lincensed').SelectedValue.Display = '0'