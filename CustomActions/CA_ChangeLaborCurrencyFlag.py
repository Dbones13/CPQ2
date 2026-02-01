Quote.GetCustomField('ChangeLaborCurrency').Content = 'False'

customFieldColumnMap = {
    "Total_Sell_Price_incl_appl_Fees_" : "Total_Sell_Price_Updated",
    "Quote_Sell_Price" : "Total Sell Price",
    "Quote_Discount_Percent" : "Total Discount Percent",
    "Quote_Regional_Margin_Percent" : "Total Regional Margin Percent",
    "Quote_WTW_Margin_Percent" : "TotalwtwMarginPercent"
}

cfValueMap = {}
qt = Quote.QuoteTables["Quote_Details"]
for row in qt.Rows:
    for cell in row.Cells:
        Trace.Write(cell.Column.Name)
        if cell.Column.Name in customFieldColumnMap:
            cfValueMap[customFieldColumnMap[cell.Column.Name]] = row[cell.Column.Name]
Trace.Write(str(cfValueMap))


for field in Quote.CustomFields:
    if field.StrongName in ["Total_Sell_Price_Updated", "Total Sell Price", "Total Discount Percent", "Total Regional Margin Percent", "TotalwtwMarginPercent"]:
        val = cfValueMap[field.StrongName]
        Log.Write("{} - {}".format(field.StrongName, str(val)))
        field.Content = str(val)