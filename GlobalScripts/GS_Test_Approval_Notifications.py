ListPrice_Discount_check = False
for item in Quote.Items:
    if item['QI_Additional_Discount_Percent'].Value > 0: #Sell Price Discount % value from dictionary
        ListPrice_Discount_check = True
        break

Trace.Write(ListPrice_Discount_check)

'''"

fetch_result=SqlHelper.GetFirst(query_retrieve_data)
query_composite_number=QuoteHelper.Edit(119,10).CompositeNumber'''

query_retrieve_data="SELECT * FROM QT__Quote_Details WHERE MPA_Discount_Amount>0 and Quote_Discount_Percent=0"
fetch_result=SqlHelper.GetFirst(query_retrieve_data)
quoteDetails = Quote.QuoteTables["Quote_Details"]
row = quoteDetails.Rows[0]
QLP = float(row["Quote_List_Price"])
MPA = float(row["MPA_Discount_Amount"])
QDA = float(row["Quote_Discount_Amount"])

'''QLP = float(fetch_result.Quote_List_Price)
MPA = float(fetch_result.MPA_Discount_Amount)
QDA = float(fetch_result.Quote_Discount_Amount)
QSP = float(fetch_result.Quote_Sell_Price)'''
QSP = QLP - MPA - QDA #new formula CXCPQ-118744

if QLP > 0 and ListPrice_Discount_check:
	TDP = UserPersonalizationHelper.ConvertToNumber(str(((QLP - QSP) / QLP) * 100))
else:
    TDP = 0