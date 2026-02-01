# ========================================================================================================
#   Component: GS_PMC_ETOInfo
#   Copyright: Honeywell Inc
#   Purpose: - This script is used to fetch ETO information based on ETO ref number.
# ========================================================================================================

def fet_Qtrows(yetotable,lv_ETO_Ref):
    final_list = []
    queryObj = SqlHelper.GetFirst("SELECT * FROM Reference_Number_Price_Mapping where ReferenceNumber = '{}'".format(lv_ETO_Ref))
    if queryObj:
		try:
			price = float(queryObj.Price)
		except:
			price = 1
		quoteCurrency = Quote.SelectedMarket.CurrencyCode
		exchangeObj = SqlHelper.GetFirst("select Exchange_Rate from Currency_ExchangeRate_Mapping where From_Currency = 'USD' and To_Currency = '{}'".format(quoteCurrency))
		Exchange_Rate = float(exchangeObj.Exchange_Rate)
		price = price * Exchange_Rate
		final_list.append([lv_ETO_Ref, queryObj.YDescription, '', '', price, ''])
		return final_list
    if yetotable=='QT__PMC_ETO_Selection':
        re_data = SqlHelper.GetList("SELECT TOP(100) * FROM QT__PMC_ETO_Selection WHERE ETO_Ref_No = '{}' AND PartNumber = '{}' order by cartID desc,ID desc".format(lv_ETO_Ref,Product.PartNumber))
        for rw in re_data:
            final_list.append([rw.ETO_Ref_No,rw.ETO_Proposal_Notes,rw.ETO_Production_Notes,rw.ETO_Manufacturing_Notes,rw.ETO_Price,rw.ETO_Cost])
    return final_list


lv_FamilyCode = Param.FamilyCode
lv_ETO_Ref    = Param.ETO_ref
yetotable = "QT__PMC_ETO_Selection"
ApiResponse = ApiResponseFactory.JsonResponse(fet_Qtrows(yetotable,lv_ETO_Ref))