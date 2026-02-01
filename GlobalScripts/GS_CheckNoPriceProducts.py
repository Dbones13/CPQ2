import GS_CommonModule as cm
# Moved this session storage from Gs_BeforeRendering to this script - starts
if Session["prevent_execution"] == "true":
    Session["prevent_execution"] = "false"
# Ends
def checkNoPriceProducts(Quote):
    itemsToBeDeleted = []
    for item in Quote.MainItems:
        #if item.PartNumber not in ("PRJT","Migration") or '.' not in item.RolledUpQuoteItem:
        #	continue
        if item.VCItemPricingPayload.Conditions:
            x = item.VCItemPricingPayload.Conditions[0]
            #CXCPQ-68375: 10/13/2023: Added VA00
            if x.ConditionType not in ('ZP00','ZQ00','VA00') and float(item.ListPrice) <= float(0):
                itemsToBeDeleted.append(item.PartNumber)
    #Trace.Write(str(itemsToBeDeleted))
    return itemsToBeDeleted

if Session["IsHCIUpload"] in (None, ""):
    Quote.SetGlobal('PerformanceUpload', '')
    if Quote.GetCustomField('Booking LOB').Content == 'PMC':
        itemsToBeDeleted = [item.PartNumber for item in Quote.MainItems if str(item.ListPrice) in ('0.00','0.0000000000')]
    else:
        itemsToBeDeleted = checkNoPriceProducts(Quote)
    cm.setCFValue(Quote,"NoPriceParts",'')
    if len(itemsToBeDeleted) > 0:
        cm.setCFValue(Quote,"NoPriceParts",str(itemsToBeDeleted))
        if not Quote.Messages.Contains(Translation.Get('message.pricenotavailable').format("','".join(itemsToBeDeleted))):
            Quote.Messages.Add(Translation.Get('message.pricenotavailable').format("','".join(itemsToBeDeleted)))