def getRegionalCostFormula(product , quoteType):
    formula = ""
    nonPricingContainer = product.GetContainerByName("Non Pricing Parts")
    if product.Type.Name == "Honeywell Labor":
        formula = "<*TotalPriceWoLI *> * <* TABLE ( SELECT FACTOR from HPS_LABOR_FACTORS where QUOTE_TYPE='<* ProductCode *>'  and PRODUCT_TYPE='{}' ) *>".format(quoteType , product.Type.Name)
    elif product.Type.Name == "Honeywell Material" and nonPricingContainer:
        nonPricingParts = [row["Part_Number"] for row in nonPricingContainer.Rows]
        formula = "<* TABLE ( Select sum(Cost) as sumCost from SAP_Global_Services_USD_Cost_USSG_USD_L1 where PartNumber in ('{}')) *>".format("','".join(nonPricingParts))
    else:
        formula =  "<* TABLE ( SELECT Cost FROM SAP_Global_Services_USD_Cost_USSG_USD_L1 WHERE PartNumber = '<* ProductCode *>' ) *>"
    return formula

quoteType = Quote.GetCustomField("Quote Type").Content
formula = getRegionalCostFormula(Product , quoteType)

Product.CostFormula = "<*Eval( {} * <*CTX( Quote.CustomField(Exchange Rate) )*> )*>".format(formula)