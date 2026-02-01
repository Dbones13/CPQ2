#------------------------------------------------------------------------------------------------
#					Change History Log
#------------------------------------------------------------------------------------------------

#Description:Added code to control visibilty of Custom fields related Service Contract Project
#Description:This is created to handle visibility of custom Quote Field.
#-------------------------------------------------------------------------------------------------
# Date 			Name					Version   Comment
# 02-11-2023	Nilesh Pingale			127		  Removed Service COntract related major codes.
# 18-10-2023	Ankit Chouhan			126		  Commented Line 293.
# 03-08-2023	Nilesh Pingale			105       Added code for Service Contract Project
# 05-07-2023	Pushpita Guru			104       Commented line 277
from GS_SetEgapValues import setegapvalues
from GS_CommonConfig import CL_CommonSettings as CS
from GS_MigrationLaborHoursModule import checkForMPACustomer
#import GS_Execution_Year_Error_Message
def getCF(quote , cfName):
	return quote.GetCustomField(cfName)

def getCFValue(quote , cfName):
	return getCF(quote , cfName).Content

def hideCF(customField):
	customField.Visible = False

def showCF(customField):
	customField.Visible = True

def setCFReadonly(customField):
	customField.Editable = False

def setCFValue(quote, cfName, Value):
	getCF(quote , cfName).Content = Value

quoteStatus=Quote.OrderStatus.Name
get_RAFR1 = getCFValue(Quote, 'EGAP_RAFR1_Ques')
get_RQUP_Number=getCFValue(Quote, 'EGAP_RAFR1_RQUP_Number')
QuoteType = getCFValue(Quote, "Quote Type")
BookingLOB = getCFValue(Quote, "Booking LOB")

def checkMPAAvailable():
	MultiplePricePlanPresent = False
	if getCFValue(Quote,"MPA Honeywell Ref") == '':
		return MultiplePricePlanPresent
	if QuoteType == "Projects":
		query = TagParserQuote.ParseString("select A=count(1) from MPA_PRICE_PLAN_MAPPING(NOLOCK) where Honeywell_Ref = '<*CTX(Quote.CustomField(MPA Honeywell Ref))*>' and Price_Plan_Status= 'Active' and Price_Plan_Systems_Discount = 'Y' and Price_Plan_Start_Date <= '<*CTX( Date.Format(MM/dd/yyyy) )*>' and Price_Plan_End_Date >= '<*CTX( Date.Format(MM/dd/yyyy) )*>'")
	else:
		query = TagParserQuote.ParseString("select A=count(1) from MPA_PRICE_PLAN_MAPPING(NOLOCK) where Honeywell_Ref = '<*CTX(Quote.CustomField(MPA Honeywell Ref))*>' and Price_Plan_Status= 'Active' and Price_Plan_Parts_Discount = 'Y' and Price_Plan_Start_Date <= '<*CTX( Date.Format(MM/dd/yyyy) )*>' and Price_Plan_End_Date >= '<*CTX( Date.Format(MM/dd/yyyy) )*>'")
	res = SqlHelper.GetFirst(query)
	if res.A > 0:
		MultiplePricePlanPresent = True
	return MultiplePricePlanPresent
MultiplePricePlanPresent = checkMPAAvailable()

def hideQuoteTableColumn(table,column):
	table.GetColumnByName(column).AccessLevel = table.AccessLevel.Hidden

def showQuoteTableColumn(table,column,isEditable):
	if isEditable:
		table.GetColumnByName(column).AccessLevel = table.AccessLevel.Editable
	else:
		table.GetColumnByName(column).AccessLevel = table.AccessLevel.ReadOnly

def hideQuoteTable(tableName):
	table = Quote.QuoteTables[tableName]
	table.AccessLevel = table.AccessLevel.Hidden

if BookingLOB != "LSS":
	hideCF(getCF(Quote , "MSID"))
	hideCF(getCF(Quote , "Customer Comment"))
	hideCF(getCF(Quote , "BOM"))
	#hideCF(getCF(Quote , "Discount Request Reason"))
'''elif getCFValue(Quote , "BookingLOB") == "LSS":
	hideCF(getCF(Quote , "PMC BOM"))'''
if BookingLOB != "PMC" or QuoteType != "Parts and Spot":
	hideQuoteTable("DCATable")
	hideCF(getCF(Quote,"Opportunity Owner Name"))
	hideCF(getCF(Quote,"Opportunity Owner Phone No"))
	hideCF(getCF(Quote,"Opportunity Owner Email"))

if QuoteType != "Projects":
	hideCF(getCF(Quote , "Recommended Discount Plan"))
	hideCF(getCF(Quote , "Selected Discount Plan"))
	hideCF(getCF(Quote , "Schedule Price Plan Updated"))

if QuoteType != "Parts and Spot" or BookingLOB == "PMC":
	hideCF(getCF(Quote , "System Number"))
else:
	showCF(getCF(Quote,"System Number"))


'''if not getCFValue(Quote , "Expedite Fee"):
	setCFReadonly(getCF(Quote , "Expedite Reason"))
	setCFReadonly(getCF(Quote , "Expedite Fee Waiver Reason")) commented by Chirag, will activate it in the next sprint'''

'''if not getCFValue(Quote , "Minimum Order Fee"):
	setCFReadonly(getCF(Quote , "Minimum Order fee Waiver reason"))'''

Customfields = ['Warranty','Published Lead Time','Customer Requested Date','Document Format','Expedite Fee','Expedite Fee Waiver Reason','Minimum Order Fee','Minimum Order fee Waiver reason','Expedite Reason','Expedite Fee Waiver','Access to Inventory','Minimum Order Fee Waiver','Entitlement','Opp Prod Desc','BOM','Discount Request Reason']
if BookingLOB == "PMC" and QuoteType == "Parts and Spot":
	for field in Customfields:
		hideCF(getCF(Quote , field))
	if not User.BelongsToPermissionGroup('PMC WTW Cost Access Group'):
		hideCF(getCF(Quote,"TotalwtwMarginPercent"))
	if getCFValue(Quote, "Global Major Project") == 'False':
		hideCF(getCF(Quote, "Global Major Project"))
elif BookingLOB == "LSS" and QuoteType == "Parts and Spot":
																		 
	if not MultiplePricePlanPresent:
		hideCF(getCF(Quote,"MPA Threshold"))
	showCF(getCF(Quote,"Does Quote include Labor Services"))
else:
	hideCF(getCF(Quote,"Does Quote include Labor Services"))

'''salesStage = getCFValue(Quote,"Sales Stage")
if salesStage[0] == '3':
	setCFValue(Quote, "EGAP_Proposal_Type","Budgetary")
elif salesStage[0] == '4':
	setCFValue(Quote, "EGAP_Proposal_Type","Firm")
elif int(salesStage[0]) >= 5:
	setCFValue(Quote, "EGAP_Proposal_Type","Booking")'''

if QuoteType != "Projects":
	hideCF(getCF(Quote,"Recommended Discount Plan"))
	hideCF(getCF(Quote,"Selected Discount Plan"))
	hideCF(getCF(Quote,"Schedule Price Plan Updated"))
	hideCF(getCF(Quote,"Systems Price List"))
else:
	hideCF(getCF(Quote,"Parts Price List"))

fieldsToHideShow = ['AM Name','Backlog Flag','Booking Account','Booking Info Business Model','Booking Info Milestone Category','Contractor/ Partner(C/P)','Drop Shipment','End User','Estimator Name','Exchange Rate','PO Amount','Project Comments','Project Owner Name','Quote and Po Currency','Quote Sell price','SAP Project Number','Legacy CRM ID_Booking Info Tab','Account Siebel Id','Opportunity Siebel Id']
if BookingLOB in ('LSS','PAS') and QuoteType == "Projects":
	#MultiplePricePlanPresent = checkMPAAvailable()
	if MultiplePricePlanPresent:
		hideCF(getCF(Quote,"Recommended Discount Plan"))
		hideCF(getCF(Quote,"Selected Discount Plan"))
		#setCFValue(Quote,"Schedule Price Plan Updated","True")
		hideCF(getCF(Quote,"Schedule Price Plan Updated"))
	else:
		showCF(getCF(Quote,"Recommended Discount Plan"))
		showCF(getCF(Quote,"Selected Discount Plan"))
		showCF(getCF(Quote,"Schedule Price Plan Updated"))
		hideCF(getCF(Quote,"MPA Price Plan"))
		hideCF(getCF(Quote,"MPA Validity"))
		hideCF(getCF(Quote,"MPA Threshold"))
		setCFValue(Quote,"Schedule Price Plan Updated","True")
else:
	if BookingLOB == 'CCC':
 		fieldsToHideShow.remove('Exchange Rate')
	for field in fieldsToHideShow:
		hideCF(getCF(Quote , field))

CfNames = ['MSID','Published Lead Time','Customer Requested Date','Customer Comment']

paymentMileStone = Quote.QuoteTables["Payment_MileStones"]
																	 
												  
															
if BookingLOB == "LSS" and QuoteType in ('Projects'):
	showQuoteTableColumn(paymentMileStone,"Billing_Milestone",True)
	showQuoteTableColumn(paymentMileStone,"Milestone_Description",True)
	showQuoteTableColumn(paymentMileStone,"Milestone_Number",False)
	hideQuoteTableColumn(paymentMileStone,"Milestone")
	ScriptExecutor.Execute('GS_PopulateMileStoneTable')
	for field in CfNames:
		hideCF(getCF(Quote , field))
	if getCFValue(Quote , "EGAP_Proposal_Type") != 'Firm':
		hideCF(getCF(Quote,"Booking Revision"))

	if getCFValue(Quote , "EGAP_IS_Booking_Check_Visible") != 'Yes':
		hideCF(getCF(Quote,"Parent Firm Revision"))
		hideCF(getCF(Quote,"EGAP_Do_Want_to_Chanage_Ans_of_Func_Ques"))
	if getCFValue(Quote , "Change Proposal Type") != '1':
		hideCF(getCF(Quote,"Revised proposal type"))
	attValues = Quote.GetCustomField("Milestone").AttributeValues
	Quote.GetCustomField("Milestone").Label = "Payment Milestones"
	for value in attValues:
		if value.DisplayValue == "Exclude":
			value.Allowed = False
	MultiplePricePlanPresent = checkMPAAvailable()
	if MultiplePricePlanPresent:
		hideCF(getCF(Quote,"Payment Milestones Category"))
		hideCF(getCF(Quote,"Milestone"))
	else:
		attValues2 = Quote.GetCustomField("Payment Milestones Category").AttributeValues
		hideValues = ['Base Project - Preferred','GMP Project - Preferred','Base Project - Alternative','GMP Project - Alternative','New Construction and Retrofit projects','Upgrade and Migration Project','Non-project engineering design and optimization services','Standard Small','Standard Large']
		for value in attValues2:
			if value.DisplayValue in hideValues:
				value.Allowed = False
		hideCF(getCF(Quote,"Payment Milestones"))
elif BookingLOB in("PAS") and QuoteType == "Projects":
	showQuoteTableColumn(paymentMileStone,"Billing_Milestone",True)
	showQuoteTableColumn(paymentMileStone,"Milestone_Description",True)
	showQuoteTableColumn(paymentMileStone,"Milestone_Number",False)
	hideQuoteTableColumn(paymentMileStone,"Milestone")
	mpaAvailable = checkForMPACustomer(TagParserQuote)
	if mpaAvailable:
		hideQuoteTableColumn(paymentMileStone,"PAS_Milestone_Description")
	ScriptExecutor.Execute('GS_PopulateMileStoneTable')
	
	if getCFValue(Quote , "EGAP_Proposal_Type") != 'Firm':
		hideCF(getCF(Quote,"Booking Revision"))
	
	
	if getCFValue(Quote , "EGAP_IS_Booking_Check_Visible") != 'Yes':
		hideCF(getCF(Quote,"Parent Firm Revision"))
		hideCF(getCF(Quote,"EGAP_Do_Want_to_Chanage_Ans_of_Func_Ques"))
	if getCFValue(Quote , "Change Proposal Type") != '1':
		hideCF(getCF(Quote,"Revised proposal type"))
	attValues = Quote.GetCustomField("Milestone").AttributeValues
	Quote.GetCustomField("Milestone").Label = "Payment Milestones"
	for value in attValues:
		if value.DisplayValue == "Exclude":
			value.Allowed = False
	MultiplePricePlanPresent = checkMPAAvailable()
	
	
	if MultiplePricePlanPresent:
		hideCF(getCF(Quote,"Payment Milestones Category"))
		hideCF(getCF(Quote,"Milestone"))
		showCF(getCF(Quote,"Payment Milestones"))

	else:
		attValues2 = Quote.GetCustomField("Payment Milestones Category").AttributeValues
		hideValues = ['Lump Sum Small','Ex-Works Small','Lump Sum Large','Ex-Works Large','New Construction and Retrofit projects','Upgrade and Migration Project','Non-project engineering design and optimization services','Standard Small','Standard Large']
		for value in attValues2:
			if value.DisplayValue in hideValues:
				value.Allowed = False
		hideCF(getCF(Quote,"Payment Milestones"))

elif BookingLOB in ("CCC") and QuoteType in("Projects","Parts and Spot"):
	showQuoteTableColumn(paymentMileStone,"Billing_Milestone",True)
	showQuoteTableColumn(paymentMileStone,"Milestone_Description",True)
	showQuoteTableColumn(paymentMileStone,"Milestone_Number",False)
	hideQuoteTableColumn(paymentMileStone,"Milestone")
	ScriptExecutor.Execute('GS_PopulateMileStoneTable')
	#for field in CfNames:
	#	hideCF(getCF(Quote , field))
	if getCFValue(Quote , "EGAP_Proposal_Type") != 'Firm':
		hideCF(getCF(Quote,"Booking Revision"))
	#if getCFValue(Quote , "EGAP_Proposal_Type") != 'Booking':
		#hideCF(getCF(Quote,"Parent Firm Revision"))
	if getCFValue(Quote , "EGAP_IS_Booking_Check_Visible") != 'Yes':
		hideCF(getCF(Quote,"Parent Firm Revision"))
		hideCF(getCF(Quote,"EGAP_Do_Want_to_Chanage_Ans_of_Func_Ques"))
	if getCFValue(Quote , "Change Proposal Type") != '1':
		hideCF(getCF(Quote,"Revised proposal type"))
	attValues = Quote.GetCustomField("Milestone").AttributeValues
	Quote.GetCustomField("Milestone").Label = "Payment Milestones"
	for value in attValues:
		if value.DisplayValue == "Exclude":
			value.Allowed = False
	MultiplePricePlanPresent = checkMPAAvailable()
	if MultiplePricePlanPresent and BookingLOB == "LSS" :
		hideCF(getCF(Quote,"Payment Milestones Category"))
		hideCF(getCF(Quote,"Milestone"))
	elif MultiplePricePlanPresent and BookingLOB == "PAS":
		hideCF(getCF(Quote,"Payment Milestones Category"))
		hideCF(getCF(Quote,"Milestone"))
		showCF(getCF(Quote,"Payment Milestones"))

	else:
		attValues2 = Quote.GetCustomField("Payment Milestones Category").AttributeValues
		hideValues = ['Base Project - Preferred','GMP Project - Preferred','Base Project - Alternative','GMP Project - Alternative','Lump Sum Small','Ex-Works Small','Lump Sum Large','Ex-Works Large','Standard Small','Standard Large']
		for value in attValues2:
			if value.DisplayValue in hideValues:
				value.Allowed = False
		hideCF(getCF(Quote,"Payment Milestones"))



else:
	hideCF(getCF(Quote,"Pricing Summary Type"))
	hideCF(getCF(Quote,"NewMigration_Pricing_Summary"))
	hideCF(getCF(Quote,"BOM Type"))
	hideCF(getCF(Quote,"Booking Revision"))
	hideCF(getCF(Quote,"Parent Firm Revision"))
	hideCF(getCF(Quote,"Payment Milestones Category"))
	hideCF(getCF(Quote,"Payment Milestones"))
	hideCF(getCF(Quote,"Revised proposal type"))
	hideQuoteTableColumn(paymentMileStone,"Billing_Milestone")
	hideQuoteTableColumn(paymentMileStone,"Milestone_Description")
	#hideQuoteTableColumn(paymentMileStone,"Milestone_Number")
	hideCF(getCF(Quote,"EGAP_Do_Want_to_Chanage_Ans_of_Func_Ques"))
	
CfNames = ['Document Format','Holding charges/Order change fee','BOM','Discount Request Reason','PMC BOM','Final Destination','Warranty']

if QuoteType == "Projects":
	for field in CfNames:
		hideCF(getCF(Quote , field))
	hideQuoteTable("Country_of_Origin")

if QuoteType == "Projects":
	productcheck = []
	for item in Quote.MainItems:
		if item.PartNumber in ("Migration","PRJT",'IAA -Project','Trace Software'):
			productcheck.append(item.PartNumber)

	if "Migration" in productcheck and "PRJT" in productcheck:
		hideCF(getCF(Quote,"BOM Type"))
		showCF(getCF(Quote,"Pricing Summary Type"))
		showCF(getCF(Quote,"NewMigration_Pricing_Summary"))
	elif "Migration" in productcheck or "IAA -Project" in productcheck or "Trace Software" in productcheck:
		showCF(getCF(Quote,"Pricing Summary Type"))
		showCF(getCF(Quote,"BOM Type"))
		hideCF(getCF(Quote,"NewMigration_Pricing_Summary"))
	else:
		hideCF(getCF(Quote,"Pricing Summary Type"))
		hideCF(getCF(Quote,"BOM Type"))
		showCF(getCF(Quote,"NewMigration_Pricing_Summary"))


'''Change all editable custom fields as readonly when the quote status is not preparing'''
if Quote.OrderStatus.Name != 'Preparing':
	customFields = SqlHelper.GetList("SELECT distinct p.StrongName from ScParamDefnNew p join ScParamPermission pp on p.ScParamId = pp.ScParamId where pp.Permission=2 and p.StrongName like 'EGAP_%'")
	for cf in customFields:
		if Quote.GetCustomField(cf.StrongName).Editable:
			Quote.GetCustomField(cf.StrongName).Editable = False

if getCFValue(Quote,'Quote Tab Booking LOB') == 'LSS' and QuoteType == 'Parts and Spot':
	exchangeRate = getCFValue(Quote,'Exchange Rate') if getCFValue(Quote,'Exchange Rate').strip() !='' else 1.0
																																			  
	sellPrice	 = float(UserPersonalizationHelper.ConvertToNumber(getCFValue(Quote,"Total Sell Price"))) / float(exchangeRate) if getCFValue(Quote,"Total Sell Price").strip() else 0
	getCF(Quote,'Minimum Order Fee').Visible = True
	if  ((sellPrice > 600 )or getCFValue(Quote,'Minimum Order fee Waiver reason') or getCFValue(Quote,'Minimum Order Fee Waiver')== 'True'):
		setCFValue(Quote, 'Minimum Order Fee', '0')
	elif ((sellPrice < 600 )or not(getCFValue(Quote,'Minimum Order fee Waiver reason') or getCFValue(Quote,'Minimum Order Fee Waiver')== 'True')):
		getCF(Quote,'Minimum Order Fee').Visible = True

getCF(Quote,'LOB_Approver_Name').Visible = False
if (getCFValue(Quote,'Minimum Order fee Waiver reason') or getCFValue(Quote, 'Expedite Fee Waiver Reason') ):
	getCF(Quote,'LOB_Approver_Name').Visible = True

if BookingLOB != "PMC":
	hideCF(getCF(Quote,"Sub-LOB"))
	hideCF(getCF(Quote,"Proposal Template Type"))
	hideCF(getCF(Quote,"ApprovedControlNumber"))
	hideCF(getCF(Quote,"PMC Type")) #----> H541049 (start)
	hideCF(getCF(Quote,"PMC Product Family"))
	hideCF(getCF(Quote,"PMC Product Line")) #----> H541049 (end)
elif BookingLOB == "PMC" :
									
	paymentMileStonetable = Quote.QuoteTables["Payment_MileStones"]
	hideCF(getCF(Quote,"ProfitCentre"))
	#hideCF(getCF(Quote,"Profit Centre Description"))
	hideCF(getCF(Quote,"MPA")) #----> H541049 (start)
	hideCF(getCF(Quote,"MPA Price Plan"))
	hideCF(getCF(Quote,"MPA Threshold"))
	hideCF(getCF(Quote,"MPA Validity"))
	hideCF(getCF(Quote,"MPA Commercial"))
	hideCF(getCF(Quote,"MPA Price Plan Commercial"))
	hideCF(getCF(Quote,"MPA Customer Reference No"))
	hideCF(getCF(Quote,"MPA Honeywell Ref"))
	hideQuoteTableColumn(paymentMileStonetable,"_Amount_text")
	hideQuoteTable("EGAP_Cash_Inflow_Calculations")
	setCFReadonly(getCF(Quote ,"PMC Type"))
	setCFReadonly(getCF(Quote ,"PMC Product Family"))
	setCFReadonly(getCF(Quote ,"PMC Product Line")) #----> H541049 (end)
	# CXCPQ-73072 - show the following fields for LOB = PMC & Quote Type = Projects --- H542832 || Start
	if QuoteType == "Projects":
		showCF(getCF(Quote , "EGAP_Proposal_Type")) # H542832 || end


if QuoteType == "Projects" and getCFValue(Quote , "Booking Country") == "united states":
	showCF(getCF(Quote,"CF_US_TAX1"))
	showCF(getCF(Quote,"CF_US_TAX2"))
else:
	hideCF(getCF(Quote,"CF_US_TAX1"))
	hideCF(getCF(Quote,"CF_US_TAX2"))

if QuoteType == 'Parts and Spot':
	hideCF(getCF(Quote,"CF_ProjectId"))
	hideCF(getCF(Quote,"Project_Release_Flag"))
	hideCF(getCF(Quote,"System Number"))

#For hiding custom fields for booking LOB PMC and quote type Projects/Parts and Spot. ------> H541049 (start)
if BookingLOB == "PMC" and QuoteType == "Parts and Spot":
	hideCF(getCF(Quote,"EGAP_Contigency_Costs_USD"))
	hideCF(getCF(Quote,"EGAP_Highest_Price_Margin_Approval_Level"))
	hideCF(getCF(Quote,"EGAP_Highest_Cash_Risk_Approval_Level"))
	hideCF(getCF(Quote,"EGAP_Approval_Level_when_Cash_Flow_negative_position_GT_100k"))
	hideCF(getCF(Quote,"EGAP_Approval_Level_when_Price_Discount_Exceeds_Threshold_Discount"))
elif BookingLOB == "PMC" and QuoteType == "Projects":
	setCFValue(Quote, "EGAP_Highest_Price_Margin_Approval_Level","N/A")
	setCFValue(Quote, "EGAP_Highest_Cash_Risk_Approval_Level","N/A")
	setCFValue(Quote, "EGAP_Approval_Level_when_Cash_Flow_negative_position_GT_100k","N/A")
	setCFValue(Quote, "EGAP_Approval_Level_when_Price_Discount_Exceeds_Threshold_Discount","N/A") #------> H541049 (end)
	#hiding Quetions from financial summary for PMC
	hideCF(getCF(Quote,"EGAP_Cash_Flow_Quality"))
	hideCF(getCF(Quote,"EGAP_Lowest_Cum_CF_in_any_Single_Month_USD"))
	hideCF(getCF(Quote,"EGAP_Months_Negative_Cumulative_Cash_Flows"))
	hideCF(getCF(Quote,"EGAP_Cashflow_Health"))
	hideCF(getCF(Quote,"EGAP_Max_Consec_Months_Neg_Cum_Cash_Flows"))
	hideCF(getCF(Quote,"EGAP_Revenue_Impact_Change_in_Currency_USD"))


#Quote.Save(False)----Commented as part of CXCPQ-59424

# CXCPQ-63377 hiding multiyear customFields for Booking LOB other than ("Quote Type -"Projects")
if not (QuoteType == "Projects") :
	setCFValue(Quote, "CF_Multiyear_Project","No")
	hideCF(getCF(Quote,"CF_Multiyear_Project"))
	hideCF(getCF(Quote,"CF_LCM_Year_1_to_be_Escalated")) #--> CXCPQ-71723
#- start-> CXCPQ-71723
elif getCFValue(Quote,"CF_Multiyear_Project")=='Yes':
	showCF(getCF(Quote,"CF_LCM_Year_1_to_be_Escalated"))
else:
	setCFValue(Quote, "CF_LCM_Year_1_to_be_Escalated","No")
	hideCF(getCF(Quote,"CF_LCM_Year_1_to_be_Escalated"))
#- End-> CXCPQ-71723
if getCFValue(Quote , "Quote Type") not in ("Contract New","Contract Renewal", "Projects") and getCFValue(Quote , "Booking LOB") in ("PMC", "LSS"):

	hideCF(getCF(Quote , "EGAP_Project_Type"))
	hideCF(getCF(Quote , "Functional Currency of Entity"))


if getCFValue(Quote , "MPA") in (None, '') and getCFValue(Quote , 'Milestone') in ['Custom'] and getCFValue(Quote , 'Booking LOB') in ['LSS']:
	#Quote.GetCustomField("do_proposed_milestones_deviate_negatively").Content = 'Yes'
	Quote.GetCustomField('do_proposed_milestones_deviate_negatively').Visible = True
else:
	Quote.GetCustomField('do_proposed_milestones_deviate_negatively').Visible = False

if Quote.OrderStatus.Name == 'Preparing':
    Quote.GetCustomField("Quote Expiration Date").Content = TagParserQuote.ParseString("<*CTX(Date.AddDays(1000))*>") if getCFValue(Quote , "Quote Type") == 'Projects' else TagParserQuote.ParseString("<*CTX(Date.AddDays(30))*>")
    # if QuoteType not in ("Contract New","Contract Renewal"):
    if BookingLOB == 'CCC':
        res = SqlHelper.GetFirst("SELECT Exchange_Rate FROM CURRENCY_EXCHANGERATE_MAPPING_CCC WHERE From_Currency = 'USD' AND To_Currency = '"+str(Quote.GetCustomField('Currency').Content)+"'")
    else:
        res = SqlHelper.GetFirst("SELECT Exchange_Rate FROM Currency_ExchangeRate_Mapping WHERE From_Currency = 'USD' AND To_Currency = '"+str(Quote.GetCustomField('Currency').Content)+"'")
    Quote.GetCustomField('Exchange Rate').Content = res.Exchange_Rate
    if Quote.GetCustomField('MPA Price Plan').Content == '':
        from GS_SetDefaultPricePlan import setDefaultMpa
        setDefaultMpa(Quote,TagParserQuote)
	if getCFValue(Quote , "EGAP_Project_Type") == 'Time & Material Only' and not getCFValue(Quote , "MPA"):
		setegapvalues(Quote)
#if BookingLOB in ["LSS","PAS"] and Quote.GetCustomField('Quote Type').Content=="Projects" and quoteStatus in ['Preparing','Ready for Approval','Rejected']:
#	GS_Execution_Year_Error_Message.Quote_Items(CS, Quote)
partsAvailable=''
if QuoteType == 'Projects':
    Quote.Messages.Remove(Translation.Get('message.UnreleasedProductRestriction').format(str(Quote.GetCustomField("RQUP_partList").Content)))
    #Quote.Messages.Clear()
    #prd_List=['C200_Migration','ELCN']
    prd_List=['C200_Migration']
    Partexist=[]
    for prd in prd_List:
        if Quote.ContainsAnyProductByPartNumber(prd):
            Partexist.append(prd)
    Partlist=",".join(Partexist)
    if (get_RAFR1 == 'Yes' and get_RQUP_Number=="" and Partlist!=""):
        partsAvailable= Partlist
        if not Quote.Messages.Contains(Translation.Get('message.UnreleasedProductRestriction').format(partsAvailable)):
            Quote.Messages.Add(Translation.Get('message.UnreleasedProductRestriction').format(partsAvailable))
            Quote.GetCustomField("RQUP_partList").Content=str(partsAvailable)
	Quote.RefreshActions()