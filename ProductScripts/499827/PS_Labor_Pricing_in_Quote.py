from GS_UpdateLaborPrices import updatelaborItemPrices

labor_cont = Product.GetContainerByName('Labor_PM_PriceCost_Cont')
updatelaborItemPrices(Quote, labor_cont, True)

sys_groups = Product.GetContainerByName("CE_SystemGroup_Cont").Rows
for row in sys_groups:
    for cont in ('CE_System_Cont','PMC_Generic_System_Cont'):
        for pdt in row.Product.GetContainerByName(cont).Rows:
            updatelaborItemPrices(Quote, pdt.Product.GetContainerByName('Labor_PriceCost_Cont'), False)