from GS_UpdateLaborPrices import updatelaborItemPrices
lineItemCont = Product.GetContainerByName("Winest_Labor_PriceCost_Cont")
updatelaborItemPrices(Quote, lineItemCont, True)