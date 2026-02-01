for item in Quote.MainItems:
    if item.ProductName in ("WriteIn", "TPC System Name","Winest Labor Import") or item.PartNumber in ("PRJT", "Migration","HCI_LABOR"):
        product=item.EditConfiguration()
        if item.ProductName == "TPC System Name":
            product.ParseString('<* ExecuteScript(ResetProductPricing) *>')
        elif item.ProductName == "Winest Labor Import":
            product.ParseString('<* ExecuteScript(PS_Refresh_Labor_Containers_Data)*>')
        elif item.PartNumber == "HCI_LABOR":
            Trace.Write("inside CA_UpdateWritein")
            product.ParseString('<* ExecuteScript(HCI_LaborCostUpdate)*>')
        product.UpdateQuote()