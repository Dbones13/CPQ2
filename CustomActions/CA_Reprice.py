#Log.Info(str(TagParserQuote.ParseString("<* GetFirstFromQuoteTable( Quote_Details, Total_Sell_Price_incl_appl_Fees_) *>"))+'CA_Reprice--11--' + str(TagParserQuote.ParseString("<* GetFirstFromQuoteTable( Quote_Details, Quote_Sell_Price) *>")))
def rolluupval():
	rollup = 0
	warranty_percentage = 0
	booking_country = Quote.GetCustomField('Booking Country').Content
	getWarranty = SqlHelper.GetFirst("SELECT Warranty_Percentage FROM Standard_Warranty_Percentages WHERE Country = '{}'".format(booking_country))
	if getWarranty:
		warranty_percentage = getWarranty.Warranty_Percentage
	for item in Quote.GetItemsByProductTypeSystemId('Write-In_cpq'):
		if item.Description == 'Write-In Standard Warranty System':
			item["QI_ProductLine"].Value = "7187"
			item["QI_ProductLineDesc"].Value = "Non Revenue Generating Project Cost - Warranty and Unpriced Extended Warranty"
			item["QI_PLSG"].Value = "7187-7779"
			item["QI_PLSGDesc"].Value = "Non Revenue Generating Project Cost - Warranty and Unpriced Extended Warranty"
			item["QI_UoM"].Value = "EA"
			rollup = item.RolledUpQuoteItem
			break
	return rollup,warranty_percentage

def update_or_add_warranty():
	if not Quote.ContainsAnyProductByName('Write-In Standard Warranty'):
		Quote.GetCustomField('Writein_std_wrnty').Content = ''
		warranty_add = ProductHelper.CreateProduct('Write-In_Standard_Warranty_cpq')
		warranty_add.AddToQuote()
	rollupnum,warranty_percentage = rolluupval()
	Quote.GetCustomField('Writein_std_wrnty').Content = str(rollupnum)+':'+str(warranty_percentage)
	Writein_std_wrnty = Quote.GetCustomField('Writein_std_wrnty').Content.split(":")
	if len(Writein_std_wrnty) >= 2 and float(Writein_std_wrnty[0]) > 0:
		item = Quote.GetItemByQuoteItem(str(Writein_std_wrnty[0]))
		cost = float(float(Quote.GetCustomField('Total Sell Price').Content.replace(',', '')) * float(Writein_std_wrnty[1]) / 100)
		item.Cost = cost
		query = SqlHelper.GetFirst("SELECT WTW_FACTOR from HPS_PLSG_WTW_FACTOR wtw JOIN WriteInProducts wrt on wrt.ProductLineSubGroup = wtw.PL_PLSG where wrt.Product = 'Write-In Standard Warranty'")
		wtwFac =  query.WTW_FACTOR if query else 0
		wtwCost = cost / (1 + float(wtwFac)) if cost else 0.0
		item.ExtendedCost = cost * item.Quantity
		item['QI_UnitWTWCost'].Value = wtwCost
		item['QI_ExtendedWTWCost'].Value = wtwCost * item.Quantity
		item['QI_RegionalMargin'].Value = (item.ExtendedAmount - (cost * item.Quantity))
		item['QI_WTWMargin'].Value = (item.ExtendedListPrice - (wtwCost * item.Quantity))
		if item.ExtendedAmount != 0:
			item['QI_RegionalMarginPercent'].Value = (item.ExtendedAmount - (cost * item.Quantity))/item.ExtendedAmount * 100
			item['QI_WTWMarginPercent'].Value = (item.ExtendedListPrice - (wtwCost * item.Quantity))/item.ExtendedListPrice * 100
	elif Quote.ContainsAnyProductByName('Write-In Standard Warranty') and not Quote.GetCustomField('Writein_std_wrnty').Content: #it's applicable only for existing product in the quote.
		rollupnum,warranty_percentage = rolluupval()
		quoteitem = Quote.GetItemByQuoteItem(str(rollupnum))
		quoteitem.Cost = quoteitem.ExtendedCost = float(float(Quote.GetCustomField('Total Sell Price').Content.replace(',', '')) * float(warranty_percentage) / 100)
		Quote.GetCustomField('Writein_std_wrnty').Content = str(rollupnum)+':'+str(warranty_percentage)

Qt = Quote.GetCustomField("Quote Type").Content

if Qt == "Projects" and Quote.Items.Count and Quote.GetCustomField('Booking LOB').Content != "CCC":
    update_or_add_warranty()

isR2Qquote = Quote.GetCustomField('R2QFlag').Content
BookingLOB = Quote.GetCustomField('Quote Tab Booking LOB').Content
if Qt == "Projects" and isR2Qquote == "Yes" and BookingLOB =='LSS' and Quote.ContainsAnyProductByName('Migration_New'):
    ScriptExecutor.Execute('GS_R2Q_Travel_and_living_cost')

#Log.Info(str(TagParserQuote.ParseString("<* GetFirstFromQuoteTable( Quote_Details, Total_Sell_Price_incl_appl_Fees_) *>"))+'CA_Reprice--22--' + str(TagParserQuote.ParseString("<* GetFirstFromQuoteTable( Quote_Details, Quote_Sell_Price) *>")))