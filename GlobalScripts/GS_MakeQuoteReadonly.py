def getCFValue(quote , field):
    return quote.GetCustomField(field).Content

def setQuoteTableReadonly(quote):
    for quoteTable in quote.QuoteTables:
        quoteTable.AccessLevel = quoteTable.AccessLevel.ReadOnly
        quoteTable.CanAddRows = quoteTable.CanCopyRows = quoteTable.CanDeleteRows = False

def setCustomFieldsReadonly(quote):
    for cf in quote.CustomFields:
        if cf.Editable:
            quote.GetCustomField(cf.StrongName).Editable = False

Quote.SetGlobal('PerformanceUpload', '')
newCurrency = getCFValue(Quote , 'CF_NewCurrency')
oldCurrency = getCFValue(Quote , 'Currency')
message = Translation.Get("message.new.currency").format(newCurrency)
ignoredStatus = ['Accepted by Customer']

if not Quote.Messages.Contains(message):
    if newCurrency != '' and newCurrency != oldCurrency:
        setQuoteTableReadonly(Quote)
    	setCustomFieldsReadonly(Quote)
        if Quote.OrderStatus.NameTranslated not in ignoredStatus:
            Quote.Messages.Add(message)