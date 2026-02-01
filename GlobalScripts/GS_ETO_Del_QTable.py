# ========================================================================================================
#   Component: GS_ETO_Del_QTable
#   Copyright: Honeywell Inc
#   Purpose: - This script is used to delete item information from Quote table when corresponding Item is removed from quote. Also used to update the item number in the quote table.
# ========================================================================================================

item=sender
if Quote.GetCustomField('Booking LOB').Content == "PMC":
	def qtble_row_del(in_quote_table):
		lv_qtable=''
		if in_quote_table=='PMC_ETO_Selection':
			lv_qtable='QT__PMC_ETO_Selection'
		elif in_quote_table=='Yspecial_Selection':
			lv_qtable='QT__Yspecial_Selection'
		elif in_quote_table=='WS_Table':
			lv_qtable='QT__WS_Table'
		elif in_quote_table == 'PMC_Honeywell_Honeywell_Private_Label_Products':
			lv_qtable = 'QT__PMC_Honeywell_Honeywell_Private_Label_Products'
		elif in_quote_table =='PMC_Third_Party_Buyouts':
			lv_qtable = 'QT__PMC_Third_Party_Buyouts'
		qtable = Quote.QuoteTables[in_quote_table]
		if qtable.Rows.Count>0 and  lv_qtable !='' :
			if lv_qtable=='QT__WS_Table':
				remain_data = SqlHelper.GetList("SELECT * FROM {} WHERE  PartNumber = '{}' AND cartid = '{}' AND Item_Guid = '{}'".format(str(lv_qtable),str(item.PartNumber),str(Quote.QuoteId),str(item.QuoteItemGuid)))
			elif lv_qtable=='QT__Yspecial_Selection':
				remain_data = SqlHelper.GetList("SELECT * FROM {} WHERE  MainPart = '{}' AND cartid = '{}' AND CartItemGUID = '{}'".format(str(lv_qtable),str(item.PartNumber),str(Quote.QuoteId),str(item.QuoteItemGuid)))
			else:            
				remain_data = SqlHelper.GetList("SELECT * FROM {} WHERE  PartNumber = '{}' AND cartid = '{}' AND CartItemGUID = '{}'".format(str(lv_qtable),str(item.PartNumber),str(Quote.QuoteId),str(item.QuoteItemGuid)))
			for rw in remain_data:
				qtable.DeleteRow(rw.Id)
			qtable.Save()

	def qtble_row_upd(in_quote_table):
		lv_qtable=''
		if in_quote_table=='PMC_ETO_Selection':
			lv_qtable='QT__PMC_ETO_Selection'
		elif in_quote_table=='Yspecial_Selection':
			lv_qtable='QT__Yspecial_Selection'
		elif in_quote_table=='WS_Table':
			lv_qtable='QT__WS_Table'
		elif in_quote_table=='VCModelConfiguration':
			lv_qtable='QT__VCModelConfiguration'
		elif in_quote_table == 'PMC_Honeywell_Honeywell_Private_Label_Products':
			lv_qtable = 'QT__PMC_Honeywell_Honeywell_Private_Label_Products'
		elif in_quote_table =='PMC_Third_Party_Buyouts':
			lv_qtable ='QT__PMC_Third_Party_Buyouts'
		qtable = Quote.QuoteTables[in_quote_table]
		if qtable.Rows.Count>0:
			for j in qtable.Rows:
				if lv_qtable=='QT__WS_Table':
					q_data = SqlHelper.GetList("SELECT * FROM {} WHERE  PartNumber = '{}' AND cartid = '{}' AND Item_Guid = '{}'".format(str(lv_qtable),str(item.PartNumber),str(Quote.QuoteId),str(item.QuoteItemGuid)))
					for k in q_data:
						if j['Item_Guid']==k.Item_Guid:
							j['ItemNumberSr']=str(item.RolledUpQuoteItem)
					qtable.Save()

				elif lv_qtable=='QT__Yspecial_Selection':
					q_data = SqlHelper.GetList("SELECT * FROM {} WHERE  MainPart = '{}' AND cartid = '{}' AND CartItemGUID = '{}'".format(str(lv_qtable),str(item.PartNumber),str(Quote.QuoteId),str(item.QuoteItemGuid)))
					for k in q_data:
						if j['CartItemGUID']==k.CartItemGUID:
							j['ItemNumber']=str(item.RolledUpQuoteItem)
					qtable.Save()

				else:
					q_data = SqlHelper.GetList("SELECT * FROM {} WHERE  PartNumber = '{}' AND cartid = '{}' AND CartItemGUID = '{}'".format(str(lv_qtable),str(item.PartNumber),str(Quote.QuoteId),str(item.QuoteItemGuid)))
					for k in q_data:
						if j['CartItemGUID']==k.CartItemGUID:
							j['ItemNumber']=str(item.RolledUpQuoteItem)
					qtable.Save()
							
						  
							

	qtble_row_del('PMC_ETO_Selection')
	qtble_row_del('Yspecial_Selection')
	qtble_row_del('VCModelConfiguration')
	qtble_row_del('WS_Table')
	qtble_row_del('PMC_Honeywell_Honeywell_Private_Label_Products')
	qtble_row_del('PMC_Third_Party_Buyouts')
	#Quote.Save()
	qtble_row_upd('PMC_ETO_Selection')
	qtble_row_upd('Yspecial_Selection')
	qtble_row_upd('VCModelConfiguration')
	qtble_row_upd('WS_Table')
	qtble_row_upd('PMC_Honeywell_Honeywell_Private_Label_Products')
	qtble_row_upd('PMC_Third_Party_Buyouts')