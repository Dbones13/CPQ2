try:
	cf_salesarea = Quote.GetCustomField('Sales Area').Content
	QueryData = SqlHelper.GetFirst("Select Salesorg,Plant_Oil_Terminal_Default from PLANT_SALESORG_MAPPING where Salesorg  = '"+cf_salesarea+"'")
	QueryData1 = QueryData.Plant_Oil_Terminal_Default
	Product.Attr('Plant (Own or External)').AssignValue(str(QueryData1))
except:
	Trace.Write("GS_SetVcSoPlant------>" + " "+str(Product.Id) +" = "+ str(Product.PartNumber))