if Quote.GetGlobal('PerformanceUpload') != 'Yes':
	from GS_CommonConfig import CL_CommonSettings as CS
	from GS_GetPriceFromCPS import getCYBERPrice
	if len(CS.cyberProductfromtable) == 0:
		part_number_list = SqlHelper.GetList('SELECT Part_Number FROM CT_CYBER_PRICINGLISTTYPE')
		CS.cyberProductfromtable = [i.Part_Number for i in part_number_list]
	if Item.PartNumber in CS.cyberProductfromtable and Item.ListPrice == 0:
		Item.ListPrice = float(getCYBERPrice(Quote,dict(),Item.PartNumber,TagParserQuote, dict()) or 0)