def getCFValue(quote, field):
    return quote.GetCustomField(field).Content

def getPrices(quote, parts, cSign):
    response = dict()

    if not quote:
        return response

    salesOrg = getCFValue(quote , "Sales Area")
    entitlement = getCFValue(quote , "Entitlement")
    if not entitlement:
        return response

    entitlementType = 'SF' if 'flex' in entitlement.lower() else 'SP'
    currencyCode = quote.SelectedMarket.CurrencyCode
    effectiveDate = quote.EffectiveDate.ToString('MM/dd/yyyy')

    query = (
        "select * from HPS_SESP_DATA where PartNumber in ('{0}') "
        "and Price_Type = '{1}' and Sales_Org = '{2}' and Currency = '{3}' "
        "and Valid_from <= '{4}' and Valid_to >= '{4}' and coalesce(Deletion_Indicator,'') <> 'X'"
    )
    partsQuery = "','".join(parts.keys())
    query = query.format(partsQuery, entitlementType, salesOrg, currencyCode,effectiveDate)
    Trace.Write(query)

    res = SqlHelper.GetList(query)
    for r in res:
        response[str(parts[r.PartNumber])] = '{}{}'.format(cSign, UserPersonalizationHelper.ToUserFormat(r.Amount))
    return response

parts = dict(Param.Parts)
cSign = TagParserQuote.ParseString('<* CSIGN *>')
response = getPrices(Quote, parts, cSign)
Trace.Write(str(response))
ApiResponse = ApiResponseFactory.JsonResponse(response)