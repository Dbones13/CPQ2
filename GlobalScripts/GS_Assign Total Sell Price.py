quoteTotalTable = Quote.QuoteTables["Quote_Details"]

minOrderFee = UserPersonalizationHelper.ConvertToNumber(Quote.GetCustomField('Minimum Order Fee').Content) if Quote.GetCustomField('Minimum Order Fee').Content else 0.0
totalExpediteFee = 0.0
if quoteTotalTable.Rows.Count > 0:#--Added due to exception on SaveQuote
    row = quoteTotalTable.Rows[0]

    for item in Quote.Items:
        if item['QI_Expedite_Fees'].Value:
            totalExpediteFee = totalExpediteFee + UserPersonalizationHelper.ConvertToNumber(str(item['QI_Expedite_Fees'].Value))

    row['Total_Sell_Price_incl_appl_Fees_'] = row['Quote_Sell_Price'] + minOrderFee + totalExpediteFee
    Trace.Write('row = ' +str(row['Total_Sell_Price_incl_appl_Fees_'] ))
    quoteTotalTable.Save()


if Quote.GetCustomField('Total_Sell_Price_Updated').Content in ["0", "", "0.0"]:
    Quote.CalculateAndSaveCustomFields()