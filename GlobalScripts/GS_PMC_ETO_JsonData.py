# ========================================================================================================
#   Component: GS_PMC_ETO_JsonData
#   Copyright: Honeywell Inc
#   Purpose: - This script is used to display (view) the ETO information from quote table to configurator. Also when action is add, it sets the ETO global variables which will be used in GS_Add_ETO_QTable global script.
# ========================================================================================================

#Gets the information from quote table
def fet_Qtrows(PMC_ETO_Selection):
	Eto_data_Lookedup=Quote.GetGlobal('Eto_data_Lookedup')
	final_list = []
	if Eto_data_Lookedup != 'Yes':
		remain_data = SqlHelper.GetList("SELECT * FROM QT__PMC_ETO_Selection WHERE cartid = '{}' AND CartItemGUID = '{}'".format(str(Quote.QuoteId),TagParserProduct.ParseString("<*CTX( Quote.CurrentItem.CartItemGuid )*>")))
		for rw in remain_data:
			final_list.append([rw.ETO_Ref_No,rw.ETO_Proposal_Notes,rw.ETO_Production_Notes,rw.ETO_Manufacturing_Notes,rw.ETO_Price,rw.ETO_Cost])
		Quote.SetGlobal('Eto_data_Lookedup', 'Yes')
	return final_list

action = Param.action
if action == "view":
    #CXCPQ-44061 Below function used to display ETO or Yspec table on product configurator. This script is called from header template. When a new Gas/Marine product is created, add the product to PMC_GASETO_YSPEC_MARINE_PRODUCTS table.
    pf_res = SqlHelper.GetFirst("select PartNumber,family_code from PMC_GASETO_YSPEC_MARINE_PRODUCTS where PartNumber = '{}'".format(TagParserProduct.ParseString("<*CTX( Quote.CurrentItem.PartNumber)*>")))
    if pf_res is not None:
        PMC_ETO_Selection = Quote.QuoteTables["PMC_ETO_Selection"]
        ApiResponse = ApiResponseFactory.JsonResponse(fet_Qtrows(PMC_ETO_Selection))
                
if action == "add":
	ETO_json_Data=str(Param.ETO_json_Data)
	ETO_Row_CNT=str(Param.ETO_Row_CNT)
	Quote.SetGlobal('G_ETO_json_Data', ETO_json_Data)
	Quote.SetGlobal('G_ETO_Row_CNT', ETO_Row_CNT)
	Log.Info("In GS ETO jsondata ETO_json_Data:"+ str(ETO_json_Data))
	Log.Info("In GS ETO jsondata ETO_Row_CNT:"+ str(ETO_Row_CNT))