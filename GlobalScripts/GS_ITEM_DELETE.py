# ========================================================================================================
#   Components:
# 	1. GS_DeleteVariantsFromTable - This script is used to update VC parts details in Quote tables & containers
# 	2. GS_ETO_Del_QTable - This script is used to delete item information from Quote table when corresponding Item is removed from quote. Also used to update the item number in the quote table.
#   Copyright: Honeywell Inc
# ========================================================================================================

if Quote.GetCustomField('Booking LOB').Content == 'PMC':
	from GS_ITEM_DELETE_MOD import clear_fme_qt, update_spare_parts, qtble_row_del, qtble_row_upd
	item = sender
	guId = sender.QuoteItemGuid
	part_number = sender.PartNumber
	rolledup_num = str(sender.RolledUpQuoteItem)

	clear_fme_qt(Quote, guId)
	
	if item.QI_SparePartsFlag.Value == "Spare Part":
		update_spare_parts(part_number, item)

	# GS_ETO_Del_QTable
	del_lst = ['PMC_ETO_Selection', 'Yspecial_Selection',
             'WS_Table', 'PMC_Honeywell_Honeywell_Private_Label_Products', 'PMC_Third_Party_Buyouts']
	upd_list = ['PMC_ETO_Selection', 'Yspecial_Selection',
            'VCModelConfiguration', 'WS_Table', 'PMC_Honeywell_Honeywell_Private_Label_Products', 'PMC_Third_Party_Buyouts']

	for qt in del_lst:
		qtble_row_del(qt, part_number, guId, Quote)

	for qt in upd_list:
		qtble_row_upd(qt, part_number, guId, Quote, rolledup_num)

#Quote.GetCustomField('Reprice Flag').Content = 'True'