def PopulateOrderBookingErrorQuoteTable(Quote):
	query = ("SELECT Top 1000 ERROR_TEXT,ROW_NUMBER, ROW_TEXT, Convert (varchar(20), CpqTableEntryDateModified, 101) as CpqTableEntryDateModified from ORDER_BOOKING_ERROR_LOG(nolock) where QUOTE_ID ='{}' Order by CpqTableEntryDateModified Desc, ROW_TEXT,ROW_NUMBER").format(Quote.CompositeNumber)
	orderBookingErrorLog = SqlHelper.GetList(query)
	if orderBookingErrorLog is not None:
		orderBookingError = Quote.QuoteTables["Order_Booking_Error"]
		#Trace.Write(orderBookingError.Rows.Count)
		orderBookingError.Rows.Clear()
		#if orderBookingError.Rows.Count == 0:
		idx = 1
		tableData = {}
		orderableItemList = []
		previous_date = ''
		for row in orderBookingErrorLog:
			if previous_date == '' or previous_date == row.CpqTableEntryDateModified:
				tableData[idx] = {"errorMessage" : row.ERROR_TEXT , "orderableItemId" : row.ROW_NUMBER , "rowText" : row.ROW_TEXT}
				previous_date = row.CpqTableEntryDateModified
				if row.ROW_NUMBER not in orderableItemList:
					orderableItemList.append(row.ROW_NUMBER)
				idx += 1
			else:
				break
		qry = "select c.CATALOGCODE, cf.Orderable_ItemId from cartitemcustomfields(nolock) cf inner join cart_item(nolock) as c on c.cart_id = cf.cart_id and c.userid = cf.userid and c.cart_item = cf.cart_item where c.cart_id = {} and c.userid = {} and cf.Orderable_ItemId in ('{}')"
		cartItem=SqlHelper.GetList(qry.format(Quote.QuoteId, Quote.UserId, "','".join(orderableItemList)))
		if cartItem is not None:
			partNumberData = {}
			cartOrderableItemList = []
			for row in cartItem:
				cartOrderableItemList.append(row.Orderable_ItemId)
				#Trace.Write("pno: {} {}".format(row.CATALOGCODE, row.Orderable_ItemId))
				partNumberData[row.Orderable_ItemId] = row.CATALOGCODE

		for key , data in tableData.items():
			newRow = orderBookingError.AddNewRow()
			orderableItemId = data['orderableItemId']
			if orderableItemId in cartOrderableItemList:
				newRow['Part_Number']   = partNumberData[orderableItemId]
			else:
				newRow['Part_Number']   = ''
			#Trace.Write("Part_Number: {}, Orderable_ItemId: {}".format(newRow['Part_Number'], orderableItemId))
			newRow['Item_Number']   = orderableItemId if int(orderableItemId) > 0 else ''
			newRow['Error_Message'] = data['errorMessage']
			newRow['Error_Level']   = data['rowText']
		orderBookingError.Save()
#PopulateOrderBookingErrorQuoteTable(Quote)