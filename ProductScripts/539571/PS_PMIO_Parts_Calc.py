import GS_C300_IO_Calc, GS_SerC_Part_Calcs
Product.ExecuteRulesOnce = True
#CXCPQ-52347
parts_dict = GS_SerC_Part_Calcs.getParts52347(Product, {})
#CXCPQ-54439 - Part calculation of user stories CXCPQ-54003, CXCPQ-54609 are included inside this story
parts_dict = GS_SerC_Part_Calcs.getParts54439(Product, parts_dict)
if len(parts_dict) > 0:
    GS_C300_IO_Calc.setIOCount(Product, 'Series_C_RG_Part_Summary', parts_dict)
Product.ApplyRules()
Product.ExecuteRulesOnce = False