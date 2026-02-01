''' New Script is created to manage the visibility of custom fields within the "COMMERCIAL INFO" tab replacing GS_Custom Field Visibilty '''

from GS_CommonModule import hideQuoteTable,hideQuoteTableColumn,showQuoteTableColumn,getCF,getCFValue,hideCF,setCFValue,setCFReadonly,showCF
from GS_MigrationLaborHoursModule import checkForMPACustomer
booking_lob = getCFValue(Quote, "Booking LOB")
quote_type = getCFValue(Quote, "Quote Type")

if booking_lob != "LSS":
	hideCF(getCF(Quote , "MSID"))
	hideCF(getCF(Quote , "Customer Comment"))
	hideCF(getCF(Quote , "BOM"))

if quote_type != "Parts and Spot" or booking_lob == "PMC":
	hideCF(getCF(Quote , "System Number"))
else:
	showCF(getCF(Quote,"System Number"))

if quote_type == "Parts and Spot" and booking_lob == "HCP":
	hideCF(getCF(Quote , "EGAP_Contract_Start_Date"))
	hideCF(getCF(Quote , "EGAP_Contract_End_Date"))

Customfields = ['Warranty','Published Lead Time','Customer Requested Date','Document Format','Expedite Fee','Expedite Fee Waiver Reason','Minimum Order Fee','Minimum Order fee Waiver reason','Expedite Reason','Expedite Fee Waiver']

if booking_lob == "LSS" and quote_type == "Parts and Spot":
	showCF(getCF(Quote,"Does Quote include Labor Services"))
else:
	hideCF(getCF(Quote,"Does Quote include Labor Services"))

if booking_lob == "PMC":
	hideCF(getCF(Quote,"MPA Commercial"))
	hideCF(getCF(Quote,"MPA Price Plan Commercial"))
	hideCF(getCF(Quote,"MPA Customer Reference No"))
	hideCF(getCF(Quote,"MPA Honeywell Ref"))
	hideCF(getCF(Quote,"ProfitCentre"))
	if quote_type == "Parts and Spot":
		for field in Customfields:
			hideCF(getCF(Quote , field))
else:
	hideCF(getCF(Quote,"Proposal Template Type"))
	hideCF(getCF(Quote,"Sub-LOB"))

getCF(Quote,'LOB_Approver_Name').Visible = False
if (getCFValue(Quote,'Minimum Order fee Waiver reason') or getCFValue(Quote, 'Expedite Fee Waiver Reason') ):
	getCF(Quote,'LOB_Approver_Name').Visible = True

CfNames = ['Holding charges/Order change fee','PMC BOM','Final Destination']
if quote_type == "Projects":
	for field in CfNames:
		hideCF(getCF(Quote , field))
	prd_data = {
		"Migration": Quote.ContainsAnyProductByPartNumber("Migration"),
		"PRJT": Quote.ContainsAnyProductByPartNumber("PRJT"),
		"IAA -Project": Quote.ContainsAnyProductByPartNumber("IAA -Project"),
		"Trace Software": Quote.ContainsAnyProductByPartNumber("Trace Software")
	}
	'''for item in Quote.MainItems:
		if item.PartNumber in ("Migration","PRJT",'IAA -Project','Trace Software'):
			productcheck.append(item.PartNumber)'''


	if prd_data["Migration"] and prd_data["PRJT"]:
		hideCF(getCF(Quote,"BOM Type"))
		showCF(getCF(Quote,"Pricing Summary Type"))
		showCF(getCF(Quote,"NewMigration_Pricing_Summary"))
	elif prd_data["Migration"] or prd_data["IAA -Project"] or prd_data["Trace Software"]:
		showCF(getCF(Quote,"Pricing Summary Type"))
		showCF(getCF(Quote,"BOM Type"))
		hideCF(getCF(Quote,"NewMigration_Pricing_Summary"))
	else:
		hideCF(getCF(Quote,"Pricing Summary Type"))
		hideCF(getCF(Quote,"BOM Type"))
		showCF(getCF(Quote,"NewMigration_Pricing_Summary"))

if booking_lob not in ("LSS","PAS","CCC","HCP") and quote_type in ('Projects'):
	hideCF(getCF(Quote,"NewMigration_Pricing_Summary"))

if booking_lob == "HCP":
	if Quote.GetCustomField('Payment Milestones as per Standard/MPA?').Content == '':
		Quote.GetCustomField('Payment Milestones as per Standard/MPA?').Content = 'Yes'
	if Quote.GetCustomField('Payment Milestones as per Standard/MPA?').Content == 'Yes':
		Quote.CustomFields.Disallow( 'Is Payment milestones are negatively deviating from standard milestone?')
	elif Quote.GetCustomField('Payment Milestones as per Standard/MPA?').Content == 'No':
		Quote.CustomFields.Allow( 'Is Payment milestones are negatively deviating from standard milestone?')
		if Quote.GetCustomField('Is Payment milestones are negatively deviating from standard milestone?').Content == '':
			Quote.GetCustomField('Is Payment milestones are negatively deviating from standard milestone?').Content = 'Yes'
else:
	Quote.CustomFields.Disallow( 'Is Payment milestones are negatively deviating from standard milestone?','Is Payment milestones are negatively deviating from standard milestone?')
	Quote.CustomFields.Disallow( 'Payment Milestones as per Standard/MPA?','Payment Milestones as per Standard/MPA?')

def milestone_exclude():
	attValues = Quote.GetCustomField("Milestone").AttributeValues
	Quote.GetCustomField("Milestone").Label = "Payment Milestones"
	for value in attValues:
		if value.DisplayValue == "Exclude":
			value.Allowed = False

if booking_lob in ("LSS","PAS", "CCC") and quote_type in ('Projects'):
	milestone_exclude()
	if getCFValue(Quote , "MPA") and getCFValue(Quote , "MPA Price Plan") and booking_lob == "LSS" :
		hideCF(getCF(Quote,"Payment Milestones Category"))
		hideCF(getCF(Quote,"Milestone"))
	elif getCFValue(Quote , "MPA") and getCFValue(Quote , "MPA Price Plan") and booking_lob == "PAS":
		hideCF(getCF(Quote,"Payment Milestones Category"))
		hideCF(getCF(Quote,"Milestone"))
		showCF(getCF(Quote,"Payment Milestones"))
	elif getCFValue(Quote , "MPA") == '' and getCFValue(Quote , "MPA Price Plan") == '' and booking_lob == "PAS":
		hideCF(getCF(Quote,"Payment Milestones"))
if booking_lob == "CCC":
	milestone_exclude()

# CXCPQ-63377 hiding multiyear customFields for Booking LOB other than ("Quote Type -"Projects")
if not (quote_type == "Projects") :
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


CfNames = ['MSID','Published Lead Time','Customer Requested Date','Customer Comment']

paymentMileStone = Quote.QuoteTables["Payment_MileStones"]
hideQuoteTableColumn(paymentMileStone,"HCP_Milestone")
if booking_lob == "LSS" and quote_type in ('Projects'):
    showQuoteTableColumn(paymentMileStone,"Billing_Milestone",True)
    showQuoteTableColumn(paymentMileStone,"Milestone_Description",True)
    showQuoteTableColumn(paymentMileStone,"Milestone_Number",False)
    hideQuoteTableColumn(paymentMileStone,"Milestone")
    ScriptExecutor.Execute('GS_PopulateMileStoneTable')
    for field in CfNames:
        hideCF(getCF(Quote , field))
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
    # MultiplePricePlanPresent = checkMPAAvailable()
    MultiplePricePlanPresent = checkForMPACustomer(TagParserQuote)
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
elif booking_lob in("PAS") and quote_type == "Projects":
    showQuoteTableColumn(paymentMileStone,"Billing_Milestone",True)
    showQuoteTableColumn(paymentMileStone,"Milestone_Description",True)
    showQuoteTableColumn(paymentMileStone,"Milestone_Number",False)
    hideQuoteTableColumn(paymentMileStone,"Milestone")
    mpaAvailable = checkForMPACustomer(TagParserQuote)
    if mpaAvailable:
        hideQuoteTableColumn(paymentMileStone,"PAS_Milestone_Description")
    ScriptExecutor.Execute('GS_PopulateMileStoneTable')
    #showCF(getCF(Quote,"PROS Guidance Recommendation"))
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
    # MultiplePricePlanPresent = checkMPAAvailable()
    MultiplePricePlanPresent = checkForMPACustomer(TagParserQuote)
    hideCF(getCF(Quote,'Published Lead Time'))
    hideCF(getCF(Quote,'Customer Requested Date'))    
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

elif booking_lob in ("CCC") and quote_type in("Projects","Parts and Spot"):
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
    # MultiplePricePlanPresent = checkMPAAvailable()
    MultiplePricePlanPresent = checkForMPACustomer(TagParserQuote)
    if MultiplePricePlanPresent and booking_lob == "LSS" :
        hideCF(getCF(Quote,"Payment Milestones Category"))
        hideCF(getCF(Quote,"Milestone"))
    elif MultiplePricePlanPresent and booking_lob == "PAS":
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
elif booking_lob == "CCC":
    showQuoteTableColumn(paymentMileStone,"Billing_Milestone",True)
    showQuoteTableColumn(paymentMileStone,"Milestone_Description",True)
    showQuoteTableColumn(paymentMileStone,"Milestone_Number",False)
    hideQuoteTableColumn(paymentMileStone,"Milestone")
    #mpaAvailable = checkForMPACustomer(TagParserQuote)
    #if mpaAvailable:
    #    hideQuoteTableColumn(paymentMileStone,"PAS_Milestone_Description")
    ScriptExecutor.Execute('GS_PopulateMileStoneTable')
    #showCF(getCF(Quote,"PROS Guidance Recommendation"))
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
    for value in attValues:
        if value.DisplayValue == "Exclude":
            value.Allowed = False
    #MultiplePricePlanPresent = checkMPAAvailable()
    hideCF(getCF(Quote,'Published Lead Time'))
    hideCF(getCF(Quote,'Customer Requested Date'))    
    #if MultiplePricePlanPresent:
    #    hideCF(getCF(Quote,"Payment Milestones Category"))
    #    hideCF(getCF(Quote,"Milestone"))
    #    showCF(getCF(Quote,"Payment Milestones"))
    #else:
    attValues2 = Quote.GetCustomField("Payment Milestones Category").AttributeValues
    hideValues = ['Lump Sum Small','Ex-Works Small','Lump Sum Large','Ex-Works Large','Base Project - Preferred','GMP Project - Preferred','Base Project - Alternative','GMP Project - Alternative','Standard Small', 'Standard Large']
    for value in attValues2:
        if value.DisplayValue in hideValues:
            value.Allowed = False
    showCF(getCF(Quote,"Milestone"))
    #Quote.GetCustomField("Milestone").Label = "Payment Milestones"
elif getCFValue(Quote , "Booking LOB") == "HCP":
    if quote_type != "Projects":
        Quote.CustomFields.Disallow( 'Tech/Benefit Price Factor','Tech/Benefit Price Factor')
        Quote.CustomFields.Disallow( 'Competitive Price Factor','Competitive Price Factor')
    #elif quote_type == "Projects":
    if Quote.GetCustomField('Payment Milestones as per Standard/MPA?').Content == '':
        Quote.GetCustomField('Payment Milestones as per Standard/MPA?').Content = 'Yes'
    if Quote.GetCustomField('Payment Milestones as per Standard/MPA?').Content == 'Yes':
        Quote.CustomFields.Disallow( 'Is Payment milestones are negatively deviating from standard milestone?')
    elif Quote.GetCustomField('Payment Milestones as per Standard/MPA?').Content == 'No':
        Quote.CustomFields.Allow( 'Is Payment milestones are negatively deviating from standard milestone?')
        if Quote.GetCustomField('Is Payment milestones are negatively deviating from standard milestone?').Content == '':
            Quote.GetCustomField('Is Payment milestones are negatively deviating from standard milestone?').Content = 'Yes'
    attValues2 = Quote.GetCustomField("Payment Milestones Category").AttributeValues
    showQuoteTableColumn(paymentMileStone,"HCP_Milestone",True)
    hideQuoteTableColumn(paymentMileStone,"Billing_Milestone")
    showvalues = ['Standard Small', 'Standard Large']
    for value in attValues2:
        if value.DisplayValue not in showvalues:
            value.Allowed = False
    Quote.GetCustomField('Milestone').Content = 'Custom'
    attValues2 = Quote.GetCustomField("Milestone").AttributeValues
    for value in attValues2:
        if value.DisplayValue!= 'Custom':
            value.Allowed = False
    showQuoteTableColumn(paymentMileStone,"Milestone_Description",True)
    showQuoteTableColumn(paymentMileStone,"Milestone_Number",False)
    hideQuoteTableColumn(paymentMileStone,"Milestone")
    #mpaAvailable = checkForMPACustomer(TagParserQuote)
    #if mpaAvailable:
    #    hideQuoteTableColumn(paymentMileStone,"PAS_Milestone_Description")
    ScriptExecutor.Execute('GS_PopulateMileStoneTable')
    #showCF(getCF(Quote,"PROS Guidance Recommendation"))
    if getCFValue(Quote , "EGAP_Proposal_Type") != 'Firm':
        hideCF(getCF(Quote,"Booking Revision"))
    #if getCFValue(Quote , "EGAP_Proposal_Type") != 'Booking':
        #hideCF(getCF(Quote,"Parent Firm Revision"))
    if getCFValue(Quote , "EGAP_IS_Booking_Check_Visible") != 'Yes':
        hideCF(getCF(Quote,"Parent Firm Revision"))
        hideCF(getCF(Quote,"EGAP_Do_Want_to_Chanage_Ans_of_Func_Ques"))
    if getCFValue(Quote , "Change Proposal Type") != '1':
        hideCF(getCF(Quote,"Revised proposal type"))
    #MultiplePricePlanPresent = checkMPAAvailable()
    hideCF(getCF(Quote,'Published Lead Time'))
    hideCF(getCF(Quote,'Customer Requested Date'))
    hideCF(getCF(Quote,"Payment Milestones")) 
    #if MultiplePricePlanPresent:
    #    hideCF(getCF(Quote,"Payment Milestones Category"))
    #    hideCF(getCF(Quote,"Milestone"))
    #    showCF(getCF(Quote,"Payment Milestones"))
    #else:
    showCF(getCF(Quote,"Milestone"))
    #Quote.GetCustomField("Milestone").Label = "Payment Milestones"
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


paymentMileStone = Quote.QuoteTables["Payment_MileStones"]
hideQuoteTableColumn(paymentMileStone,"HCP_Milestone")
if (booking_lob in ("LSS","PAS") and quote_type in ('Projects')) or (booking_lob in ("CCC","HCP")):
	showQuoteTableColumn(paymentMileStone,"Billing_Milestone",True)
	showQuoteTableColumn(paymentMileStone,"Milestone_Description",True)
	showQuoteTableColumn(paymentMileStone,"Milestone_Number",False)
	hideQuoteTableColumn(paymentMileStone,"Milestone")
	if booking_lob in("PAS"):
		mpaAvailable = checkForMPACustomer(TagParserQuote)
		if mpaAvailable:
			hideQuoteTableColumn(paymentMileStone,"PAS_Milestone_Description")
	elif booking_lob == 'HCP':
		attValues2 = Quote.GetCustomField("Payment Milestones Category").AttributeValues
		showQuoteTableColumn(paymentMileStone,"HCP_Milestone",True)
		hideQuoteTableColumn(paymentMileStone,"Billing_Milestone")
		showvalues = ['Standard Small', 'Standard Large']
		for value in attValues2:
			if value.DisplayValue not in showvalues:
				value.Allowed = False
		Quote.GetCustomField('Milestone').Content = 'Custom'
		if Quote.GetCustomField("Payment Milestones Category").Content not in ('Standard Small','Standard Large'):
			Quote.GetCustomField('Payment Milestones Category').Content = 'Standard Small'
		attValues2 = Quote.GetCustomField("Milestone").AttributeValues
		for value in attValues2:
			if value.DisplayValue!= 'Custom':
				value.Allowed = False
		showQuoteTableColumn(paymentMileStone,"Milestone_Description",True)
		showQuoteTableColumn(paymentMileStone,"Milestone_Number",False)
		hideQuoteTableColumn(paymentMileStone,"Milestone")
else:
	hideQuoteTableColumn(paymentMileStone,"Billing_Milestone")
	hideQuoteTableColumn(paymentMileStone,"Milestone_Description")

if quote_type in ('Projects','Contract New','Contract Renewal'):
	hideQuoteTable(Quote,"Country_of_Origin")
	hideQuoteTable(Quote,"DCATable")
elif booking_lob == "PMC" and quote_type == "Parts and Spot":
    CountryofOriginTable=Quote.QuoteTables["Country_of_Origin"]
    hideQuoteTableColumn(CountryofOriginTable,"Country_of_Origin")
    hideQuoteTableColumn(CountryofOriginTable,"Product_Line_Sub_Group")
    hideQuoteTableColumn(CountryofOriginTable,"PLSG_Desc")