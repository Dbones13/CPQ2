def clear_fme_qt(quote, guId):
	# CXCPQ-90702 - The invalid parts table is not being erased
	quote.QuoteTables['FME_Invalid_Parts'].Rows.Clear()

	VariantTable = quote.QuoteTables["VCModelConfiguration"]
	rows_to_delete = [
		row.Id for row in VariantTable.Rows if row["CartItemGUID"] == guId]
	for row_id in rows_to_delete:
		VariantTable.DeleteRow(row_id)
	VariantTable.Save()

def Vf_AddedVCParts(product, container, part_number):
    vfaddedVCParts = product.GetContainerByName(container)
    if vfaddedVCParts.Rows.Count > 0:
        for row in vfaddedVCParts.Rows:
            if row["VC Model Number"] == part_number:
                row.IsSelected = False
            product.UpdateQuote()


def qtble_row_del(in_quote_table, part_number, guId, quote):
    quote_id = str(quote.QuoteId)
    lv_qtable = ''
    if in_quote_table == 'PMC_ETO_Selection':
        lv_qtable = 'QT__PMC_ETO_Selection'
    elif in_quote_table == 'Yspecial_Selection':
        lv_qtable = 'QT__Yspecial_Selection'
    elif in_quote_table == 'WS_Table':
        lv_qtable = 'QT__WS_Table'
    elif in_quote_table == 'PMC_Honeywell_Honeywell_Private_Label_Products':
        lv_qtable = 'QT__PMC_Honeywell_Honeywell_Private_Label_Products'
    elif in_quote_table == 'PMC_Third_Party_Buyouts':
        lv_qtable = 'QT__PMC_Third_Party_Buyouts'
    qtable = quote.QuoteTables[in_quote_table]
    if qtable.Rows.Count > 0 and lv_qtable != '':
        if lv_qtable == 'QT__WS_Table':
            remain_data = SqlHelper.GetList("SELECT * FROM {} WHERE  PartNumber = '{}' AND cartid = '{}' AND Item_Guid = '{}'".format(
                str(lv_qtable), str(part_number), quote_id, str(guId)))
        elif lv_qtable == 'QT__Yspecial_Selection':
            remain_data = SqlHelper.GetList("SELECT * FROM {} WHERE  MainPart = '{}' AND cartid = '{}' AND CartItemGUID = '{}'".format(
                str(lv_qtable), str(part_number), quote_id, str(guId)))
        else:
            remain_data = SqlHelper.GetList("SELECT * FROM {} WHERE  PartNumber = '{}' AND cartid = '{}' AND CartItemGUID = '{}'".format(
                str(lv_qtable), str(part_number), quote_id, str(guId)))
        for rw in remain_data:
            qtable.DeleteRow(rw.Id)
        qtable.Save()


def qtble_row_upd(in_quote_table, part_number, guId, quote, rolledup_num):
    quote_id = str(quote.QuoteId)
    lv_qtable = ''
    if in_quote_table == 'PMC_ETO_Selection':
        lv_qtable = 'QT__PMC_ETO_Selection'
    elif in_quote_table == 'Yspecial_Selection':
        lv_qtable = 'QT__Yspecial_Selection'
    elif in_quote_table == 'WS_Table':
        lv_qtable = 'QT__WS_Table'
    elif in_quote_table == 'VCModelConfiguration':
        lv_qtable = 'QT__VCModelConfiguration'
    elif in_quote_table == 'PMC_Honeywell_Honeywell_Private_Label_Products':
        lv_qtable = 'QT__PMC_Honeywell_Honeywell_Private_Label_Products'
    elif in_quote_table == 'PMC_Third_Party_Buyouts':
        lv_qtable = 'QT__PMC_Third_Party_Buyouts'
    qtable = quote.QuoteTables[in_quote_table]
    if qtable.Rows.Count > 0:
        for j in qtable.Rows:
            if lv_qtable == 'QT__WS_Table':
                q_data = SqlHelper.GetList("SELECT * FROM {} WHERE  PartNumber = '{}' AND cartid = '{}' AND Item_Guid = '{}'".format(
                    str(lv_qtable), str(part_number), quote_id, str(guId)))
                for k in q_data:
                    if j['Item_Guid'] == k.Item_Guid:
                        j['ItemNumberSr'] = rolledup_num

            elif lv_qtable == 'QT__Yspecial_Selection':
                q_data = SqlHelper.GetList("SELECT * FROM {} WHERE  MainPart = '{}' AND cartid = '{}' AND CartItemGUID = '{}'".format(
                    str(lv_qtable), str(part_number), quote_id, str(guId)))
                for k in q_data:
                    if j['CartItemGUID'] == k.CartItemGUID:
                        j['ItemNumber'] = rolledup_num

            else:
                q_data = SqlHelper.GetList("SELECT * FROM {} WHERE  PartNumber = '{}' AND cartid = '{}' AND CartItemGUID = '{}'".format(
                    str(lv_qtable), str(part_number), quote_id, str(guId)))
                for k in q_data:
                    if j['CartItemGUID'] == k.CartItemGUID:
                        j['ItemNumber'] = rolledup_num
            qtable.Save()


def update_spare_parts(part_number, item):
    vfdquery = SqlHelper.GetFirst(
        "Select VFD_VC_Model from VFD_VC_Models(nolock) where VFD_VC_Model = '{}'".format(item.QI_ParentVcModel.Value))
    product = item.EditConfiguration()
    if vfdquery:
        Vf_AddedVCParts(product, "VFD_Add_Recommended_VC_PartCont", part_number)
    else:
        Vf_AddedVCParts(product, "Add_Recommended_VC_PartCont", part_number)

