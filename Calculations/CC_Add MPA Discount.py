if Quote.GetGlobal('PerformanceUpload') != 'Yes':

	import GS_ItemCalculations as ic

	import GS_ItemCalculationsUpdated as ic_upd

	import GS_CalculateTotals as ct



	booking_country = Quote.GetCustomField('Booking Country').Content

	honeywellRef = Quote.GetCustomField('MPA Honeywell Ref').Content

	addList = []

	ProductList = []



	## Prevent execution in certain conditions

	if (Session["prevent_execution"] != "true" and

		(Quote.GetCustomField('CF_Plant_Prevent_Calc').Content != 'true' or Quote.GetCustomField('Booking LOB').Content != 'PMC') and

		Quote.GetCustomField('Quote Type').Content not in ("Contract New", "Contract Renewal")):



		MPA = Quote.GetCustomField('MPA').Content

		quoteCurrency = Quote.SelectedMarket.CurrencyCode

		total = ct.calculateTotalListPrice(Quote)

		Quote.GetCustomField('Total List Price').Content = str(total)



		totalLaborHours = 0.0

		RolledUpQuoteItem = ""



		#return a list from sql calls

		#get a list of part numbers on the quote

		full_part_list = "'{0}'".format("','".join(str(item.PartNumber) for item in Quote.Items))

		category_query = SqlHelper.GetList("SELECT PL.Cost_Category,PM.PartNumber FROM HPS_PRODUCTS_MASTER PM JOIN SAP_PLSG_LOB_MAPPING PL ON PM.PLSG=PL.SAP_PL_PLSG WHERE PM.PartNumber IN ({0})".format(full_part_list))

		for item in Quote.Items:        

			if item.ProductTypeName == 'Write-In':

				query = SqlHelper.GetFirst("SELECT ProductCategory FROM WRITEINPRODUCTS WHERE Product= '{}'".format(item.PartNumber))

				if query:

					item["QI_ProductCostCategory"].Value = query.ProductCategory

			else:

				#query = SqlHelper.GetFirst("SELECT PL.Cost_Category FROM HPS_PRODUCTS_MASTER PM JOIN SAP_PLSG_LOB_MAPPING PL ON PM.PLSG=PL.SAP_PL_PLSG WHERE PM.PartNumber = '{}'".format(item.PartNumber))

				#if query:

					#item["QI_ProductCostCategory"].Value = query.Cost_Category

				if category_query:

					for item_material in category_query:

						if item.PartNumber == item_material.PartNumber.strip():

							item["QI_ProductCostCategory"].Value = item_material.Cost_Category

							#Trace.Write(str(item_material.Cost_Category))

			if item["QI_ProductCostCategory"].Value == "Honeywell Labor":

				totalLaborHours += float(item.Quantity)

				ProductList.append(item)



			if item.ProductName in ('HCI Labor Upload', 'HCI Labor Config'):

				RolledUpQuoteItem = str(item.RolledUpQuoteItem)



			if RolledUpQuoteItem and str(item.RolledUpQuoteItem).startswith(RolledUpQuoteItem):

				if item.ProductTypeName == "Honeywell Labor":

					addList.append(item)

			else:

				RolledUpQuoteItem = ""



	## Proceed if booking_country and honeywellRef exist

	if booking_country and honeywellRef:

		part_numbers = set(val.PartNumber for val in ProductList + addList)

		if part_numbers:

			## Batch Query to fetch MPA Prices for all items at once

			query = """

				SELECT Service_Material, Unit_MPA_Price, Currency 

				FROM GES_MPA_PRICE (NOLOCK) 

				WHERE Booking_Country = '{}' 

				AND HoneywellRef = '{}'

				AND CAST({} AS FLOAT) BETWEEN Minimum_MH AND Maximum_MH

				AND Service_Material IN ({})

			""".format(

				booking_country, honeywellRef, totalLaborHours,

				", ".join("'{}'".format(pn) for pn in part_numbers)

			)



			mpa_prices = {row.Service_Material: (row.Unit_MPA_Price, row.Currency) for row in SqlHelper.GetList(query)}



			## Handle currency conversion

			unique_currencies = set(row[1] for row in mpa_prices.values() if row[1] != quoteCurrency)

			exchange_rates = {}

			if unique_currencies:

				exchange_query = """

					SELECT From_Currency, Exchange_Rate 

					FROM CURRENCY_EXCHANGERATE_MAPPING 

					WHERE From_Currency IN ({}) AND To_Currency = '{}'

				""".format(", ".join("'{}'".format(c) for c in unique_currencies), quoteCurrency)

				exchange_rates = {row.From_Currency: row.Exchange_Rate for row in SqlHelper.GetList(exchange_query)}



			## Function to update MPA price for items

			def update_mpa_price(item):

				if item.PartNumber in mpa_prices:

					unit_price, currency = mpa_prices[item.PartNumber]

					if quoteCurrency != currency and currency in exchange_rates:

						item.QI_MPA_Price.Value = str(float(unit_price) * float(exchange_rates[currency]))

					else:

						item.QI_MPA_Price.Value = str(unit_price)



			## Apply updates in bulk

			for val in ProductList + addList:

				update_mpa_price(val)

	if (Session["prevent_execution"] != "true" and

		(Quote.GetCustomField('CF_Plant_Prevent_Calc').Content != 'true' or Quote.GetCustomField('Booking LOB').Content != 'PMC') and

		Quote.GetCustomField('Quote Type').Content not in ("Contract New", "Contract Renewal")):

		ic_upd.applyMPA(Quote)