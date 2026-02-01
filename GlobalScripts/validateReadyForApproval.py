def getCfValue(cf):
    return Quote.GetCustomField(cf).Content

from datetime import datetime

def getobsoletePartList(Quote):
    partsList = []
    obsoleteParts = dict()
    obsoletePartList = []
    parts = SqlHelper.GetList("SELECT DISTINCT(CATALOGCODE) from CART_ITEM where CART_ID = '" +
                              str(Quote.QuoteId)+"' and USERID  = '"+str(Quote.UserId)+"'")

    daystoCompare = DateTime.Now.Subtract(DateTime(1899 , 12 , 31)).Days
    query = ("select p.* from Products p join product_versions pv on p.Product_ID = pv.Product_ID where System_ID in ('{}') and pv.Is_Active = 1 ").format("','".join(i.CATALOGCODE for i in parts))
    res = SqlHelper.GetList(query)
    for i in res:
        d1 = i.D1 if i.D1 else 0
        d2 = i.D2 if i.D2 else 99999999999999999999999999
        if d1 <= daystoCompare <= d2:
            pass
        else:
            obsoletePartList.append(i.PRODUCT_CATALOG_CODE)
    return obsoletePartList

fieldsToCheck1 = ['Proposal Validity' , 'Payment Terms','Discount Request Reason']
fieldsToCheck2 = ['Proposal Validity' , 'Payment Terms']
isValid = True

if getCfValue("Quote Type") != "Projects" :
    #SFDC Redirection for PMC Quotes || CXCPQ-78576
    if getCfValue("Booking LOB") == "PMC":
        for field in fieldsToCheck2:
            if getCfValue(field):
                continue
            isValid = False
            Trace.Write("check0")
            break
    if getCfValue("Booking LOB") in ('LSS','PAS'):
        for field in fieldsToCheck1:
            if getCfValue(field):
                continue
            isValid = False
            Trace.Write("check0")
            break
else:
    for field in fieldsToCheck2:
        if getCfValue(field):
            continue
        isValid = False
        Trace.Write("check0")
        break
if getCfValue("Quote Type") == "Projects":
	projectFieldCheck = ['EGAP_Contract_Start_Date','EGAP_Contract_End_Date','Payment Terms']
	for field in projectFieldCheck:
		if getCfValue(field):
			continue
		isValid = False
		break
	if getCfValue("EGAP_CFR4_Ques") == "Yes" and getCfValue("EGAP_ETR_Number") == '':
		isValid = False

	if getCfValue("EGAP_RAFR1_Ques") == "Yes" and getCfValue("EGAP_RAFR1_RQUP_Number") == '' and Quote.GetCustomField('EGAP_Proposal_Type').Content != 'Budgetary':
		isValid = False

	# if getCfValue("EGAP_RAFR2_Ques") == "Yes" and getCfValue("EGAP_RAFR2_RQUP_Number") == '':
		# isValid = False

	if getCfValue("EGAP_Cashflow_Health") == "Out of Balance":
		isValid = False

	if getCfValue("EGAP_Project_Type") == '':
		isValid = False

	projectDuration = getCfValue('EGAP_Project_Duration_Months')
	projectDuration = int(projectDuration) if projectDuration != '' else 0
	sqlQuery = "Select count(Month_ARO) as ct from QT__Cash_Outflow where ownerid={} and cartid={} and Row_Type='{}' and (Month_ARO <= {} or Month_ARO > {} )"
	sqlResult = SqlHelper.GetFirst(sqlQuery.format(Quote.UserId, Quote.QuoteId, 'Item', 0, projectDuration))
	if sqlResult is not None and sqlResult.ct > 0:
		isValid = False

	cdsflag = Quote.GetGlobal('CDSFlag')
	if cdsflag == 'Yes':
		isValid = False

	regional_cost = 0
	exchRate = 0
	if getCfValue("Booking LOB") in ("LSS","PAS","HCP") and Quote.GetCustomField('EGAP_Proposal_Type').Content != 'Budgetary':
		product_type = Quote.QuoteTables["Product_Type_Details"]
		if product_type.Rows.Count > 0:
			for row in product_type.Rows:
				if row["Product_Type"] == "Third-Party Material":
					regional_cost = row["Regional_Cost"]
					exchRate = float(getCfValue("Exchange Rate"))
					if regional_cost/exchRate > 250000 and getCfValue("EGAP_RAFR3_Ques") == "No":
						isValid = False

UserID = Quote.UserId
CartID = TagParserQuote.ParseString('<*CTX( Quote.Revision.MasterId )*>')
query = SqlHelper.GetList('''SELECT cr.*, cart.ACTIVE_REV, cart.DATE_CREATED, cart.DATE_MODIFIED, cart.ORDER_STATUS, (osd.ORDER_STATUS_NAME) as OrderStatusName
FROM CART_REVISIONS cr 
JOIN CART cart ON cr.VISITOR_ID=cart.USERID AND cr.CART_ID=cart.CART_ID
JOIN ORDER_STATUS_DEFN osd ON cart.ORDER_STATUS = osd.ORDER_STATUS_ID
WHERE VISITOR_ID={} AND MASTER_ID={}'''.format(UserID,CartID))

for i in query:
	if i.REVISION_ID != Quote.RevisionNumber and i.OrderStatusName in ('Ready for Approval','Awaiting Approval'):
		Trace.Write("check1")
		isValid = False

#SFDC Redirection for PMC Quotes || CXCPQ-78576
if getCfValue("Booking LOB") in ('LSS','PAS'):
	query = TagParserQuote.ParseString("select * from MPA_PRICE_PLAN_MAPPING where Agreement_Name= '<*CTX(Quote.CustomField(MPA))*>' and Price_Plan_Status= 'Active' and [IF]([EQ](<*CTX( Quote.CustomField(Quote Type) )*>,Projects)){Price_Plan_Systems_Discount}{Price_Plan_Parts_Discount}[ENDIF] = 'Y' and Price_Plan_Start_Date <= '<*CTX( Date.Format(MM/dd/yyyy) )*>' and Price_Plan_End_Date >= '<*CTX( Date.Format(MM/dd/yyyy) )*>'")
	res = SqlHelper.GetList(query)
	if res and len(res) > 0 and getCfValue("MPA Price Plan") == '':
		Trace.Write("check2")
		isValid = False

obsoletePartList = getobsoletePartList(Quote)
if len(obsoletePartList) >= 1:
	isValid = False

invaildParts =Quote.GetCustomField("Unreleased_partList").Content
if invaildParts and getCfValue('EGAP_RAFR1_Ques') == 'No' and Quote.GetCustomField('EGAP_Proposal_Type').Content != 'Budgetary':
    isValid = False

Log.Info("Is Valid --------------> "+str(isValid))
ApiResponse = ApiResponseFactory.JsonResponse({"valid":True if isValid else False})