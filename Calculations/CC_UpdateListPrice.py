#This script is applicable only for Migration - OPM / NON-SESP Exp Upgrade
if Session["prevent_execution"] != "true" and Quote.GetGlobal('PerformanceUpload') != 'Yes':
	# from GS_CommonConfig import CL_CommonSettings as CS
	from GS_ItemCalculations import CalculateListPrice
	CalculateListPrice(Quote, Item, dict(), TagParserQuote, Session)
	Item.ExtendedListPrice = Item.ListPrice * Item.Quantity
	if Item.ProductName in('OPM','Non-SESP Exp Upgrade'):
		#Session['ListPrice_WISSP'] = float(Session['ListPrice_WISSP'] or 0) + ((Item.ListPrice * 0.05) - ((Item.ListPrice * 0.05) * (Item.QI_MPA_Discount_Percent.Value / 100)))
		Session['ListPrice_WISSP'] = ((Item.ListPrice * 0.05) - ((Item.ListPrice * 0.05) * (Item.QI_MPA_Discount_Percent.Value / 100)))
		Session['WISSP_FLAG']=1
	elif not Item.IsLineItem and Item.PartNumber == "Write-in Site Support Labor" and Session['WISSP_FLAG']:
		Session['RollupValue'] = Item.RolledUpQuoteItem
	if Session['RollupValue']:
		Quote.GetItemByQuoteItem(Session['RollupValue']).ListPrice = Session['ListPrice_WISSP']