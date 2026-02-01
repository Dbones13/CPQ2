from GS_PopulateEGAPApproversQuoteTable_Helper import *
from GS_CommonUtil import GetCustomParamValue
def EGAP_aprover_module(Quote,quoteType,TagParserQuote):
	getCF = Quote.GetCustomField
	SFDCQuotetype = getCF("SFDC_Quote_Type").Content
	HCP_paymentmil = getCF('Payment Milestones as per Standard/MPA?').Content
	HCP_d_negative =getCF('Is Payment milestones are negatively deviating from standard milestone?').Content
	marketSeg = getCF("Market Segment").Content
	SC_AGREE = 'empty' if getCF('SC_CF_AGREEMENT_TYPE').Content in ('','None') else ''
	Ques_CTFR1 = getCF("EGAP_CTFR1_Ques").Content
	RAFR3 = getCF("EGAP_RAFR3_Ques").Content
	isMilestoneNeg=getCF('Is Payment milestones are negatively deviating from standard milestone?').Content
	populateLabor_and_Engineering_Service(Quote)
	bookingLOB = getCF("CF_ApprovalTabBookingLOB")
	oppCategory = getCF("CF_ApprovalTabOpportunityCategory")
	agreement_type = getCF('SC_CF_AGREEMENT_TYPE').Content
	Ques_PFR1 = getCF('EGAP_PFR1_Ques').Content
	SC_PFR1 = 'change' if SC_AGREE!='empty' and Ques_PFR1=='Yes' else ''
	HoneywellControlMilestone = float(sum(row['EGAP_Pct_of_Total_Milestone_Payment'] for row in Quote.QuoteTables["EGAP_Project_Milestone"].Rows if row['EGAP_Customer_Signoff_Required'] != 'Yes'))
	walkAwayPrice = TagParserQuote.ParseString('<*CTX( Number(<*Round (<* GetFirstFromQuoteTable(Quote_Details,Walk_away_Sales_Price) *>,0)*>).Format )*>')
	walkAwayPrice = walkAwayPrice.replace(',','')
	exchangeRate = float(getCF('Exchange Rate').Content) if getCF('Exchange Rate').Content else 0.0
	if quoteType in ('Contract New','Contract Renewal'):
		exchangeRate = float(getCF('SC_CF_EXCHANGE_RATE').Content)
	walkAwayPriceinUSD = round(float(walkAwayPrice)/exchangeRate) if exchangeRate > 0 else walkAwayPrice
	recommendedTargetPrice = TagParserQuote.ParseString('<*CTX( Number(<*Round (<* GetFirstFromQuoteTable(Quote_Details,Recommended_Target_Price) *>,0)*>).Format )*>')
	recommendedTargetPrice = recommendedTargetPrice.replace(',','')
	recommendedTargetPriceinUSD = round(float(recommendedTargetPrice)/exchangeRate) if exchangeRate > 0 else recommendedTargetPrice
	proposalType = getCF('EGAP_Proposal_Type').Content if getCF('EGAP_Proposal_Type').Content.strip() !='' else ''
	projectDuration = int(Quote.GetCustomField('EGAP_Project_Duration_Months').Content) if Quote.GetCustomField('EGAP_Project_Duration_Months').Content.strip() != '' else 0
	IsCARQuestionsVisible = getCF('IsCARQuestionsVisible')
	IsCARQuestionsVisible.Content = '1'
	if proposalType == 'Budgetary':
		IsCARQuestionsVisible.Content = '0'
		USDSellPrice = 0
		controllershipQ2, controllershipQ3, controllershipQ4, controllershipQ5, controllershipQ6, controllershipQ7, controllershipQ8, controllershipQ9 = ('',) * 8
	else:
		USDSellPrice = float(getCF('EGAP_CAR_Ques_1').Content.replace(',','')) if getCF('EGAP_CAR_Ques_1').Content.strip() !='' else 0
		controllershipQ2, controllershipQ3, controllershipQ4, controllershipQ5, controllershipQ6, controllershipQ7, controllershipQ8, controllershipQ9 = [getCF('EGAP_CAR_Ques_{0}'.format(i)).Content.strip() or '' for i in range(2, 10)]
	controllershipReview = 'No'
	if controllershipQ2 == 'Yes' or controllershipQ3 == 'Yes' or controllershipQ4 == 'Yes' or controllershipQ5 == 'Yes' or controllershipQ6 == 'Yes' or controllershipQ7 == 'Yes' or controllershipQ8 == 'Yes' or controllershipQ9 == 'Yes':
		controllershipReview = 'Yes'
	bookingCountry = getCF('Booking Country').Content if getCF('Booking Country').Content.strip() !='' else ''
	petrofac = getCF('Opportunity for Petrofac').Content
	getVariables = conditionVariables(Quote)
	cf_MaxApprovalLevel = int(getCF('CF_MaxApprovalLevel').Content.replace('L','').replace('C','').replace('NA','0')) if getCF('CF_MaxApprovalLevel').Content.strip() !='' and getCF('CF_MaxApprovalLevel').Content != 'No Approval' else 0
	if getCF('CF_MaxApprovalLevel').Content == 'No Approval':
		cf_MaxApprovalLevel = getCF('CF_MaxApprovalLevel').Content
	totalNoOfRiskFactors = 0
	riskCountFields = ['EGAP_Risk_Count_CR1a','EGAP_Risk_Count_CR3a','EGAP_Risk_Count_CR4a','EGAP_Risk_Count_CR5a','EGAP_Risk_Count_CR6a','EGAP_Risk_Count_CR7a','EGAP_Risk_Count_CR8a','EGAP_Risk_Count_CR9a']
	for riskCountField in riskCountFields:
		riskCount = int(getCF(riskCountField).Content) if getCF(riskCountField).Content.strip() !='' else 0
		totalNoOfRiskFactors += riskCount
	IsCashRiskQuestionsVisible = getCF('IsCashRiskQuestionsVisible')
	cf_highestCashRiskApprovalLevel =  getCF('EGAP_Highest_Cash_Risk_Approval_Level')
	if IsCashRiskQuestionsVisible.Content == '0' or totalNoOfRiskFactors <=2:
		cf_highestCashRiskApprovalLevel.Content = '0'
	elif totalNoOfRiskFactors == 3:
		cf_highestCashRiskApprovalLevel.Content = '3'
	elif totalNoOfRiskFactors > 3:
		cf_highestCashRiskApprovalLevel.Content = '4'
	else:
		cf_highestCashRiskApprovalLevel.Content = '0'
	highestCashRiskApprovalLevel = int(cf_highestCashRiskApprovalLevel.Content)
	if getCF('EGAP_No_eGap').Content == 'No eGap':
		highestPriceMarginApprovalLevel = 'No P&M Approval'
		if bookingLOB.Content in('LSS','PAS','CCC') and proposalType == 'Budgetary':
			highestPriceMarginApprovalLevel = 'No Approval'
		elif bookingLOB.Content in('PAS','CCC') and proposalType in ['Firm', 'Booking']:
			highestPriceMarginApprovalLevel = 'Functional Approvals Only'
		getCF('EGAP_Highest_Price_Margin_Approval_Level').Content = highestPriceMarginApprovalLevel
		highestPriceMarginApprovalLevel_int = 0
	else:
		if cf_MaxApprovalLevel == 'No Approval':
			getCF('EGAP_Highest_Price_Margin_Approval_Level').Content = 'No Approval'
			highestPriceMarginApprovalLevel_int = 0
		else:
			highestPriceMarginApprovalLevel = cf_MaxApprovalLevel
			getCF('EGAP_Highest_Price_Margin_Approval_Level').Content = str(highestPriceMarginApprovalLevel) if int(highestPriceMarginApprovalLevel) > 0 else ''
			highestPriceMarginApprovalLevel_int = highestPriceMarginApprovalLevel if int(highestPriceMarginApprovalLevel) > 0 else 0
	cf_highestPriceMarginApprovalLevel = getCF('EGAP_Highest_Price_Margin_Approval_Level').Content
	IsApprovalNotRequired_FQ = getCF('IsApprovalNotRequired_FQ').Content
	if bookingLOB.Content == 'CCC' and cf_highestPriceMarginApprovalLevel == 'No Approval' and getCF('EGAP_Highest_Approval_Level_for_the_Quote').Content == 'Functional Approvals Only' and float(Quote.QuoteTables["Quote_Details"].Rows[0]["Quote_Discount_Percent"]) in(0,0.0):
		getCF('IsApprovalNotRequired').Content = '0'
	elif quoteType in ['Projects'] and bookingLOB.Content in('LSS','PAS','HCP') and (cf_highestPriceMarginApprovalLevel == 'No Approval' or IsApprovalNotRequired_FQ == '1'):
		getCF('IsApprovalNotRequired').Content = '1'
	elif quoteType == 'Parts and Spot' and bookingLOB.Content == 'HCP' and (cf_highestPriceMarginApprovalLevel == 'No Approval' or IsApprovalNotRequired_FQ == '1'):
		getCF('IsApprovalNotRequired').Content = '1'
	elif cf_highestPriceMarginApprovalLevel == 'No Approval':
		getCF('IsApprovalNotRequired').Content = '1'
	else:
		getCF('IsApprovalNotRequired').Content = '0'
	thresholdDiscount	= 20.0 if bookingLOB.Content == 'LSS' else 30.0
	salesPriceThreshold = 50000
	approvalLevelwhenPriceDiscountExceedsThresholdDiscount = 0
	if recommendedTargetPriceinUSD > salesPriceThreshold and cf_highestPriceMarginApprovalLevel not in ('No P&M Approval', 'No Approval'):
		excessDiscount = 0 if recommendedTargetPriceinUSD <= 1 else (recommendedTargetPriceinUSD-walkAwayPriceinUSD)/recommendedTargetPriceinUSD
		excessDiscount = float(excessDiscount) * 100
		if excessDiscount > thresholdDiscount:
			approvalLevelwhenPriceDiscountExceedsThresholdDiscount = 2
	getCF('EGAP_Approval_Level_when_Price_Discount_Exceeds_Threshold_Discount').Content = str(approvalLevelwhenPriceDiscountExceedsThresholdDiscount)
	MPA = getCF('MPA Price Plan').Content if getCF('MPA Price Plan').Content.strip() !='' else 'None'
	paymentMilestones = getCF('Payment Milestones').Content if getCF('Payment Milestones').Content.strip() !='' else ''
	do_proposed_milestones_deviate_negatively = getCF('do_proposed_milestones_deviate_negatively').Content
	if MPA != 'None':
		Milestone = ''
		pass
	else:
		paymentMilestones = getCF('Milestone').Content if getCF('Milestone').Content.strip() !='' else ''
		Milestone = getCF('Milestone').Content if getCF('Milestone').Content.strip() !='' else ''
	CFQ = getCF('EGAP_Cash_Flow_Quality').Content.replace('%','') if getCF('EGAP_Cash_Flow_Quality').Content.strip() !='' else 0
	cashFlowModelRequired = 'No'
	projectType = getCF("EGAP_Project_Type").Content.strip()
	paymentTerms = getCF("Payment Terms").Content.strip()
	cf_creditTermsMonths = getCF("EGAP_Credit_Terms_Months")
	if paymentTerms != '' and paymentTerms != 'COD' and paymentTerms != 'Due Immediately' and paymentTerms != 'Other' :
		cf_creditTermsMonths.Content = '0'
		if ' ' not in paymentTerms:
			cf_creditTermsMonths.Content = str(int(round(int(paymentTerms)/30.0)))
	else:
		paymentTerms = 0
		cf_creditTermsMonths.Content = '0'
	if (paymentTerms > 30 or walkAwayPriceinUSD > 100000) and projectType != 'Time & Material only':
		cashFlowModelRequired = 'Yes'
	approvalLevelCashFlowNegative = getCF('EGAP_Approval_Level_when_Cash_Flow_negative_position_GT_100k')
	lowestCumCashFlow = float(getCF('EGAP_Lowest_Cum_CF_in_any_Single_Month_USD').Content) if getCF('EGAP_Lowest_Cum_CF_in_any_Single_Month_USD').Content.strip() !='' else 0
	if projectType == 'Time & Material only':
		approvalLevelCashFlowNegative.Content = '0'
	elif MPA != 'None' and MPA != '' and paymentMilestones == 'As per MPA':
		approvalLevelCashFlowNegative.Content = '0'
	elif (MPA == 'None' or paymentMilestones == 'Deviate from MPA' ) and lowestCumCashFlow < -100000:
		approvalLevelCashFlowNegative.Content = '4'
	else:
		approvalLevelCashFlowNegative.Content = '0'
	if bookingLOB.Content != "PMC":
		cf_highestApprovalLevel = getCF('EGAP_Highest_Approval_Level_for_the_Quote')
		if (quoteType == 'Projects') or (quoteType in ['Parts and Spot', 'Software Only'] and bookingLOB.Content == 'HCP') or (quoteType in ['Contract New','Contract Renewal'] and bookingLOB.Content == 'LSS'):
			levelCounts = [highestPriceMarginApprovalLevel_int]
		else :
			levelCounts = [highestPriceMarginApprovalLevel_int, highestCashRiskApprovalLevel, int(approvalLevelCashFlowNegative.Content), int(approvalLevelwhenPriceDiscountExceedsThresholdDiscount),int(getCF('Petrofac Opportunity Approval Escalation').Content)]
		if max(levelCounts) > 0 and IsApprovalNotRequired_FQ != '1':
			cf_highestApprovalLevel.Content = str(max(levelCounts))
		else:
			cf_highestApprovalLevel.Content = 'Functional Approvals Only' if getCF('EGAP_Highest_Price_Margin_Approval_Level').Content == 'Functional Approvals Only' else 'No Approval'
	honeywellLaborTP, thirdPartyMaterialTP, preSaleinUSD, pMCContentSellPriceinUSD, PASContentSellPriceinUSD, lSSContentSellPriceinUSD, cYBContentSellPriceinUSD, cYBContentTransferPriceinUSD, hCIContentSellPriceinUSD, HCIConnectedOfferingSellPriceinUSD, HCIConnectedOfferingW2WCostinUSD = (0,) * 11
	HCISolutionIncludedWithSubscription = 'No'
	if Quote.Items.Count > 0:
		preSalesPLSG = []
		honeywellLaborPLSG = []
		pmcPLSG =[]
		cYBPLSG =[]
		lSSPLSG =[]
		pASPLSG=[]
		hCIPLSG = []
		Q_PLSG_List = []
		sqlResult = None
		hCIConnectedOfferingPLSG = []
		HCI_Sub_LOB = GetCustomParamValue("HCI_Connected_Offering_SubLOB").split(',')
		plsgquery=SqlHelper.GetList("SELECT Product_Line_Sub_Group as PLSG FROM {} WHERE cartid = {} AND ownerId ={}".format('QT__Product_Line_Sub_Group_Details',Quote.QuoteId, Quote.UserId))
		if len(plsgquery):
			Q_PLSG_List = ', '.join("'{}'".format(x.PLSG) for x in plsgquery)
			sqlResult = SqlHelper.GetList("Select distinct SAP_PL_PLSG, Cost_Category, LOB, Sub_LOB from SAP_PLSG_LOB_Mapping where SAP_PL_PLSG in ({})".format(Q_PLSG_List))
		if sqlResult is not None:
			for row in sqlResult:
				if row.Cost_Category == 'Pre-Sales':
					preSalesPLSG.append(row.SAP_PL_PLSG)
				elif row.Cost_Category == 'Honeywell Labor':
					honeywellLaborPLSG.append(row.SAP_PL_PLSG)
				if row.LOB == 'PAS':
					pASPLSG.append(row.SAP_PL_PLSG)
				if row.LOB == 'PMC':
					pmcPLSG.append(row.SAP_PL_PLSG)
				if row.LOB == 'CYB':
					cYBPLSG.append(row.SAP_PL_PLSG)
				if row.LOB == 'LSS':
					lSSPLSG.append(row.SAP_PL_PLSG)
				if row.LOB == 'AS' and row.Sub_LOB in HCI_Sub_LOB:
					hCIConnectedOfferingPLSG.append(row.SAP_PL_PLSG)
				if row.LOB == 'AS':
					hCIPLSG.append(row.SAP_PL_PLSG)
		pLSGDetails = Quote.QuoteTables['Product_Line_Sub_Group_Details']
		for row in pLSGDetails.Rows:
			pLSG = row['Product_Line_Sub_Group']
			if pLSG in preSalesPLSG:
				preSaleinUSD += float(row['PLSG_Regional_Cost'])
			elif pLSG in honeywellLaborPLSG:
				honeywellLaborTP += float(row['PLSG_Regional_Cost'])
			if pLSG in pmcPLSG:
				pMCContentSellPriceinUSD += float(row['PLSG_Sell_Price'])
			if pLSG in pASPLSG:
				PASContentSellPriceinUSD += float(row['PLSG_Sell_Price'])
			if pLSG in lSSPLSG:
				lSSContentSellPriceinUSD += float(row['PLSG_Sell_Price'])
			if pLSG in cYBPLSG:
				cYBContentSellPriceinUSD += float(row['PLSG_Sell_Price'])
				cYBContentTransferPriceinUSD += float(row['PLSG_Regional_Cost'])
			if pLSG in hCIConnectedOfferingPLSG:
				HCISolutionIncludedWithSubscription = 'Yes'
				HCIConnectedOfferingSellPriceinUSD += float(row['PLSG_Sell_Price'])
				HCIConnectedOfferingW2WCostinUSD += float(row['PLSG_WTW_Cost'])
			if pLSG in hCIPLSG:
				hCIContentSellPriceinUSD += float(row['PLSG_Sell_Price'])
		preSaleinUSD = round(float(preSaleinUSD)/exchangeRate) if exchangeRate > 0 else preSaleinUSD
		pMCContentSellPriceinUSD = round(float(pMCContentSellPriceinUSD)/exchangeRate) if exchangeRate > 0 else pMCContentSellPriceinUSD
		PASContentSellPriceinUSD = round(float(PASContentSellPriceinUSD)/exchangeRate) if exchangeRate > 0 else PASContentSellPriceinUSD
		cYBContentSellPriceinUSD = round(float(cYBContentSellPriceinUSD)/exchangeRate) if exchangeRate > 0 else cYBContentSellPriceinUSD
		cYBContentTransferPriceinUSD = round(float(cYBContentTransferPriceinUSD)/exchangeRate) if exchangeRate > 0 else cYBContentTransferPriceinUSD
		lSSContentSellPriceinUSD = round(float(lSSContentSellPriceinUSD)/exchangeRate) if exchangeRate > 0 else lSSContentSellPriceinUSD
		hCIContentSellPriceinUSD = round(float(hCIContentSellPriceinUSD)/exchangeRate) if exchangeRate > 0 else hCIContentSellPriceinUSD
		HCIConnectedOfferingSellPriceinUSD = round(float(HCIConnectedOfferingSellPriceinUSD)/exchangeRate) if exchangeRate > 0 else HCIConnectedOfferingSellPriceinUSD
		HCIConnectedOfferingW2WCostinUSD = round(float(HCIConnectedOfferingW2WCostinUSD)/exchangeRate) if exchangeRate > 0 else HCIConnectedOfferingW2WCostinUSD
	thirdPartyHoninUSD = 0
	trueThirdPartyinUSD = 0
	query=SqlHelper.GetList("Select SAP_PLSG_Description,Third_Party_Category,SAP_PL_PLSG from SAP_PLSG_LOB_MAPPING where Third_Party_Category = 'True Third Party' or Third_Party_Category ='Third Party Hon'")
	PLSG_TP_Categor_Map={}
	for i in query:
		PLSG_TP_Categor_Map[i.SAP_PL_PLSG]= str(i.Third_Party_Category)
	for item in Quote.MainItems:
		if(item['QI_PLSG'].Value):
			if item['QI_PLSG'].Value and str(item['QI_PLSG'].Value) in PLSG_TP_Categor_Map.keys():
				if PLSG_TP_Categor_Map[str(item['QI_PLSG'].Value)] == 'True Third Party':
					trueThirdPartyinUSD = trueThirdPartyinUSD + item.ExtendedCost
				else:
					thirdPartyHoninUSD= thirdPartyHoninUSD + item.ExtendedCost
	trueThirdPartyinUSD = round(float(trueThirdPartyinUSD)/exchangeRate) if exchangeRate > 0 else trueThirdPartyinUSD
	thirdPartyHoninUSD = round(float(thirdPartyHoninUSD)/exchangeRate) if exchangeRate > 0 else thirdPartyHoninUSD
	thirdPartyMaterialTP = thirdPartyHoninUSD + trueThirdPartyinUSD
	getCF('TrueThirdParty_Cost_In_USD').Content = str(trueThirdPartyinUSD)
	getCF('ThirdPartyHon_Cost_In_USD').Content = str(thirdPartyHoninUSD)
	inputArguments = {'PASContentSellPriceinUSD':PASContentSellPriceinUSD,'WalkAwayPriceinUSD':walkAwayPriceinUSD,'ProposalType':proposalType,'USDSellPrice':USDSellPrice,'ControllershipQ2':controllershipQ2,'ControllershipQ3':controllershipQ3,'ControllershipQ4':controllershipQ4,'ControllershipQ5':controllershipQ5,'ControllershipQ6':controllershipQ6,'ControllershipQ7':controllershipQ7,'ControllershipQ8':controllershipQ8,'ControllershipQ9':controllershipQ9,'ControllershipReview':controllershipReview,'Booking Country': bookingCountry,'CF_MaxApprovalLevel':cf_MaxApprovalLevel,'EGAP_Highest_Cash_Risk_Approval_Level':highestCashRiskApprovalLevel,'EGAP_Highest_Price_Margin_Approval_Level':highestPriceMarginApprovalLevel,'EGAP_Approval_Level_when_Price_Discount_Exceeds_Threshold_Discount':approvalLevelwhenPriceDiscountExceedsThresholdDiscount,'EGAP_Payment_Milestones':paymentMilestones,'EGAP_Highest_Price_Margin_Approval_Level':highestPriceMarginApprovalLevel_int,'MPA':MPA,'HoneywellControlMilestone':HoneywellControlMilestone,'projectDuration':projectDuration,'CFQ':CFQ,'CashFlowModelRequired':cashFlowModelRequired,'ThirdPartyHoninUSD':thirdPartyHoninUSD,'TrueThirdPartyinUSD':trueThirdPartyinUSD,'PreSaleinUSD':preSaleinUSD,'HoneywellLaborTP':honeywellLaborTP,'ThirdPartyMaterialTP':thirdPartyMaterialTP,'BookingLOB':bookingLOB.Content,'PMCContentSellPriceinUSD':pMCContentSellPriceinUSD,'CreditTerm':paymentTerms,'Market Segment':marketSeg,'SC_AGREE':SC_AGREE,'SC_PFR1':SC_PFR1,'CYBContentSellPriceUSD':cYBContentSellPriceinUSD,'CYBContentTransferPriceUSD':cYBContentTransferPriceinUSD,'EGAP_RAFR4_Ques':getVariables['cf_RAFR4Ques'], 'LSSContentSellPriceinUSD': lSSContentSellPriceinUSD,'HCIContentSellPriceinUSD':hCIContentSellPriceinUSD, 'HCIConnectedOfferingSellPriceinUSD':HCIConnectedOfferingSellPriceinUSD,'HCIConnectedOfferingW2WCostinUSD':HCIConnectedOfferingW2WCostinUSD,'do_proposed_milestones_deviate_negatively':do_proposed_milestones_deviate_negatively,'HCP_d_negative':HCP_d_negative,'HCP_paymentmil':HCP_paymentmil,'HCISolutionIncludedWithSubscription':HCISolutionIncludedWithSubscription,'Opportunity for Petrofac':petrofac,'EGAP_IQ_Ques_16':getVariables['Q16'],'QuoteType':quoteType,'SFDCQuotetype':SFDCQuotetype,'AgreementType':agreement_type,'ProjectType':projectType,'EGAP_PFR1_Ques':Ques_PFR1,'EGAP_Ques_CR3d':getVariables['CR3d'],'EGAP_Max_Consec_Months_Neg_Cum_Cash_Flows':getVariables['EgapNegativeCashflow'],'EGAP_Approval_Level_when_Cash_Flow_negative_position_GT_100k':approvalLevelCashFlowNegative.Content,'EGAP_Advance_Payment_Milestone_Billing_Ques':getVariables['advPaymentmilestone'],'EGAP_CFR1_Ques':getVariables['CFR1'],'EGAP_CFR5_Ques':getVariables['CFR5'],'EGAP_CFR6_Ques':getVariables['CFR6'],'EGAP_CFR2_Ques':getVariables['CFR2'],'EGAP_CFR4_Ques':getVariables['CFR4'],'EGAP_MFR1_Ques':getVariables['MFR1'],'CR3A':getVariables['CR3A'],'CTFR1':getVariables['CTFR1'],'EGAP_RAFR1_Ques':getVariables['cf_RAFR1Ques'],'CTFR12':getVariables['CTFR12'],'NegativePayment':getVariables['NegativePayment'],'quoteDiscount':int(getVariables['quoteDiscount']),'MPADiscount':int(getVariables['MPADiscount']),'RAFR2':getVariables['RAFR2'],'BGP_SELL':getVariables['BGP_SELL'],'BGP_MPA':getVariables['BGP_MPA'],'EGAP_CTFR1_Ques':Ques_CTFR1,'Is Payment milestones are negatively deviating from standard milestone?':isMilestoneNeg,'RAFR3':RAFR3,"Milestone":Milestone,"EGAP_CTFR5_Ques":getVariables['CTFR5']}
	countryVpGmReason = 'L3 and China, Hong Kong, Taiwan, or India-Price Discount Exceeds Threshold Discount'
	poleGmReason = 'Price Discount Exceeds Threshold Discount'
	countryVpGmReasons = []
	poleGmReasons = []
	countryVpGmFlag = 0
	poleGmFlag = 0
	if bookingLOB.Content in("LSS", "PAS", "HCP", "PMC", "CCC"):
		approvalData = []
		sqlRes = SqlHelper.GetList("SELECT TOP 1000 CF_Selected_Ques_Name, CF_Selected_Value, Dep_CF_Name, Dep_CF_Value,Dep_CF_Value_1,Dep_CF_Value_2, Dep_CF_MinLimit, Dep_CF_MaxLimit, Approver_Title, Approver_Reason FROM EGAP_Approval_Title_Reason_Mapping Where LOB = '{}' ORDER BY Approver_Title ".format(bookingLOB.Content))
		uniqueApprover = []
		if sqlRes is not None:
			for row in sqlRes:
				cfSelectedQuesName = row.CF_Selected_Ques_Name
				cfSelectedValue = row.CF_Selected_Value
				if quoteType in ('Contract New','Contract Renewal') and row.Approver_Title == 'Project Manager':
					continue
				approverTitle = 'Legal Contract Manager' if quoteType in ('Contract New','Contract Renewal') and row.Approver_Title == 'Contract Manager' else row.Approver_Title 
				approverReason = row.Approver_Reason
				if approverReason.Contains('{0}'):
					deviation = getCF("EGAP_Reason_For_Deviation_Milestone_Billing_Ques").Content
					approverReason = approverReason.format(deviation)
				depCFName = row.Dep_CF_Name
				depCFValue = row.Dep_CF_Value
				depCFValue1 = row.Dep_CF_Value_1
				depCFValue2 = row.Dep_CF_Value_2
				depCFMinLimit = row.Dep_CF_MinLimit
				approverTitleReason = approverTitle+'_'+approverReason
				depFlag = False
				depResultantValue_1 = True
				depResultantValue_2 = True
				if cfSelectedQuesName.strip() != '' and getCF(cfSelectedQuesName).Content is not None:
					if getCF(cfSelectedQuesName).Content == cfSelectedValue:
						depFlag = True
						if cfSelectedQuesName == 'EGAP_Approval_Level_when_Price_Discount_Exceeds_Threshold_Discount':
							poleGmReasons.append(approverReason)
						if depCFName != '' and depCFName != 'Multiple Conditions':
							pos = depCFValue.find("!")
							if pos != -1:
								depCFValue = depCFValue.replace('!=', '')
								depFlag = False
								if getCF(depCFName).Content.strip() != '' and getCF(depCFName).Content != depCFValue:
									depFlag = True
							elif getCF(depCFName).Content != depCFValue and depCFValue != '':
								depFlag = False
							elif depCFMinLimit.strip() != '':
								intVal = int(getCF(depCFName).Content) if getCF(depCFName).Content.strip() != '' else 0

								if intVal >= int(depCFMinLimit):
									depFlag = True
						elif depCFName == 'Multiple Conditions' and depCFValue != '':
							try:
								expression = depCFValue.split(",")
								resultantValue = calc(expression, inputArguments)
								if depCFValue1 != '':
									expression_1 = depCFValue1.split(",")
									resultantValue_1 = calc(expression_1, inputArguments)
									depResultantValue_1 = resultantValue_1[0]
								if depCFValue2 != '':
									expression_2 = depCFValue2.split(",")
									resultantValue_2 = calc(expression_2, inputArguments)
									depResultantValue_2 = resultantValue_2[0]
							except:
								Trace.Write("depCFValue:{}".format(depCFValue))
							depFlag = resultantValue[0] if resultantValue[0] and depResultantValue_1 and depResultantValue_2 else False
				elif depCFName != '' and depCFName != 'Multiple Conditions' and depCFValue.strip() != '':
					if getCF(depCFName).Content == depCFValue:
						depFlag = True
				elif depCFName != '' and depCFName != 'Multiple Conditions' and depCFMinLimit.strip() != '':
					if depCFName == 'Proposal Validity':
						intVal = getCF(depCFName).Content if getCF(depCFName).Content.strip() != '' else 0
						intVal = int(intVal.replace('days','').replace(' ',''))
					else:
						intVal = int(getCF(depCFName).Content.replace('L','')) if getCF(depCFName).Content.strip() not in ['','No Approval'] else 0
					if intVal >= int(depCFMinLimit):
						depFlag = True
						if approverTitle == 'Regional Business Leader' and  int(depCFMinLimit) == 3:
							poleGmReasons.append(approverReason)
				elif depCFName == 'Multiple Conditions' and depCFValue.strip() != '':
					try:
						expression = depCFValue.split(",")
						resultantValue = calc(expression, inputArguments)
						if str(depCFValue1) != '':
							expression_1 = depCFValue1.split(",")
							resultantValue_1 = calc(expression_1, inputArguments)
							depResultantValue_1 = resultantValue_1[0]
						if str(depCFValue2) != '':
							expression_2 = depCFValue2.split(",")
							resultantValue_2 = calc(expression_2, inputArguments)
							depResultantValue_2 = resultantValue_2[0]
					except:
						Trace.Write("depCFValue:{}".format(depCFValue))
					depFlag = resultantValue[0] if resultantValue[0] and depResultantValue_1 and depResultantValue_2 else False
				if depFlag == True and approverTitleReason not in uniqueApprover:
					rec = {'Ques':cfSelectedQuesName,'Ans':cfSelectedValue,'EGAP_Approver_Title':'', 'EGAP_Reason':''}
					rec['EGAP_Approver_Title'] = approverTitle
					rec['EGAP_Reason'] = approverReason
					approvalData.append(rec)
					uniqueApprover.append(approverTitleReason)
		if quoteType in ('Contract New','Contract Renewal'):
			SESP_Flag = False
			Total_Discount = 0
			Total_Discount_Flag = False
			for item in Quote.MainItems:
				if item.PartNumber == "SESP":
					Total_Discount = str(item.QI_SC_Total_Discount_Percent.Value)
				if float(Total_Discount) >= 20:
					Total_Discount_Flag = True
					SESP_Flag = True
					break
			if SESP_Flag == True and Total_Discount_Flag == True:
					rec = {'Ques':'','Ans':'','EGAP_Approver_Title':'Service Director', 'EGAP_Reason':'SESP Total discount >= 20%'}
					approvalData.append(rec)
		if recommendedTargetPriceinUSD > 50000 and highestPriceMarginApprovalLevel != 'No P&M Approval' and bookingLOB.Content == 'LSS':
			targetRatio = (recommendedTargetPriceinUSD - walkAwayPriceinUSD)/recommendedTargetPriceinUSD
			if (targetRatio > 0.2 and highestPriceMarginApprovalLevel >= 1):
				rec = {'Ques':'','Ans':'','EGAP_Approver_Title':'Branch Business Leader', 'EGAP_Reason':'Price Discount Exceeds Threshold Discount'}
				approvalData.append(rec)
		qt = Quote.QuoteTables['EGAP_Approvers'].Rows
		if qt.Count > 0:
			for i in qt:
				if i['EGAP_Approver_Title'] == 'Regional Business Leader':
					val = i['EGAP_Reason'].replace('(Notification) ', '')
					poleGmReasons.append(val)
		poleGmReasons = list(dict.fromkeys(poleGmReasons))
		if len(poleGmReasons) == 1 and poleGmReason in poleGmReasons:
			poleGmFlag = 1
		countGuarantee = getQuoteTableData(Quote, 'Count(*)', 'QT__EGAP_Project_Milestone', " and (EGAP_Customer_Signoff_Required = 'Yes' or EGAP_Milestone_with_Bank_Guarantee = 'Yes')")
		if countGuarantee > 0 and (bookingLOB.Content in ("LSS","PAS","HCP")) and quoteType not in ('Contract New','Contract Renewal'):
			approvalData.append({'Ques':'','Ans':'','EGAP_Approver_Title':'Project Manager', 'EGAP_Reason':'Milestones include Customer Approval or Bank Guarantees'})
		if bookingLOB.Content in ("HCP"):
			#if '7222-7772' in Q_PLSG_List:
				#if SFDCQuotetype!='Software Only':
					#if getVariables['Q16'] == 'No':
					#	approvalData.append({'Ques':'','Ans':'','EGAP_Approver_Title':'Branch Business Leader', 'EGAP_Reason':'Corrosion to COE'})
					#elif getVariables['Q16'] == 'Yes':
					#	approvalData.append({'Ques':'','Ans':'','EGAP_Approver_Title':'Service Business Leader', 'EGAP_Reason':'Corrosion to COE'})
				#elif SFDCQuotetype=='Software Only' or SFDCQuotetype=='Spot Service':
				#	approvalData.append({'Ques':'','Ans':'','EGAP_Approver_Title':'Branch Business Leader', 'EGAP_Reason':'Corrosion to COE'})
			BGPzeroQuantity = check_swbgp(Quote)
			if BGPzeroQuantity== 'false':
				approvalData.append({'Ques':'','Ans':'','EGAP_Approver_Title':'Branch Business Leader', 'EGAP_Reason':'BGP/Software Support is not included'})
		qt = Quote.QuoteTables["EGAP_Approvers"]
		qt.Rows.Clear()
		qt.Save()
		if len(approvalData) > 0 and bookingLOB.Content != "PMC":
			quote_exempted_MPA=Quote.GetCustomField('Is_Quote_Approval_Exempted_due_to_MPA').Content
			cf_highestApprovalLevel = getCF('EGAP_Highest_Approval_Level_for_the_Quote')
			quote_exempted = getCF('Is_Quote_Approval_Exempted').Content
			if bookingLOB.Content=="LSS" and quote_exempted_MPA=="Yes" and quote_exempted!='Yes':
				cf_highestApprovalLevel.Content='0'
			elif bookingLOB.Content=="PAS" and quote_exempted_MPA=="Yes" and quote_exempted!='Yes':
				cf_highestApprovalLevel.Content='2'
			elif quote_exempted =='Yes':
				cf_highestApprovalLevel.Content='No Approval'
			titlearray=[]
			count_vpgm = sum(1 for record in approvalData if record.get('EGAP_Approver_Title') == 'BU Regional Leader')
			count_polegm = sum(1 for record in approvalData if record.get('EGAP_Approver_Title') == 'Regional Business Leader')
			for rec in approvalData:
				row = qt.AddNewRow()
				row['EGAP_Approver_Title'] = rec['EGAP_Approver_Title']
				row['EGAP_Reason']		   = rec['EGAP_Reason']
				isNotificationAllowed = False
				if rec['EGAP_Approver_Title'] == 'Regional Business Leader' and poleGmFlag == 1 and bookingLOB.Content != "HCP":
					isNotificationAllowed = True
				if rec['EGAP_Approver_Title'] == 'BU Regional Leader' and count_vpgm == 1 and rec['EGAP_Reason'].strip() == 'Contains HCI Solutions' and bookingLOB.Content == "HCP":
					isNotificationAllowed = True
				if rec['EGAP_Approver_Title'] == 'Regional Business Leader' and count_polegm == 1 and rec['EGAP_Reason'].strip() == 'Contains HCI Solutions' and bookingLOB.Content == "HCP":
					isNotificationAllowed = True
				if rec['EGAP_Approver_Title'].strip() in ['HCI BU Regional Leader', 'HCI Regional Business Leader'] and rec['EGAP_Reason'].strip() == 'Contains HCI Connected Offerings':
					isNotificationAllowed = True
				if rec['EGAP_Approver_Title'].strip() in ['HCI RSL', 'RSL']:
					isNotificationAllowed = True
				if "Sales Price/Margin" in rec['EGAP_Reason'] and quote_exempted_MPA=="Yes":
					isNotificationAllowed = True
				row['EGAP_IsNotificationAllowed'] = isNotificationAllowed
				if isNotificationAllowed and quote_exempted_MPA=="Yes" and quote_exempted!='Yes' and bookingLOB.Content in ('PAS','LSS'): #AutoApproved - MPA standard quote
					row['EGAP_Reason'] = "(AutoApproved - MPA standard quote) {}".format(row['EGAP_Reason'])
				elif isNotificationAllowed :
					row['EGAP_Reason'] = "(Notification) {}".format(row['EGAP_Reason'])
				else:
					titlearray.append(rec['EGAP_Approver_Title'].strip())
			qt.Save()
			titlearray=set(sorted(titlearray))
			qt = Quote.QuoteTables["EGAP_Approvers"]
			for row in qt.Rows:
				title = str(row['EGAP_Approver_Title']).strip()
				if row['EGAP_IsNotificationAllowed'] == True and title in titlearray:
					row['EGAP_Reason'] = str(row['EGAP_Reason']).replace('(Notification) ','')
					row['EGAP_IsNotificationAllowed'] = False
			qt.Save()
		revenueMarginQT = Quote.QuoteTables["EGAP_Revenue_Margin"]
		quoteDetailsQT	= Quote.QuoteTables["Quote_Details"]
		quoteDetails	= quoteDetailsQT.Rows[0]
		sellPrice = quoteDetails['Quote_Sell_Price_Incl_Tariff']
		negotiationLimit = quoteDetails['Negotiation_Limit']
		walkAwaySellPrice = sellPrice - negotiationLimit
		transferPrice = quoteDetails['Quote_Regional_Cost']
		PROSRecommendedPrice = quoteDetails['PROS_Guidance_Recommended_Price']
		regionalMargin = walkAwaySellPrice - transferPrice
		regionalMarginPercent = wtwMarginPercentage = 0
		quoteWTWCost = quoteDetails['Quote_WTW_Cost']
		wtwMargin = walkAwaySellPrice - quoteWTWCost
		thresholdDiscount	= 20.0 if bookingLOB.Content == 'LSS' else 30.0
		salesPriceThreshold = 50000
		localSalesPriceThreshold = salesPriceThreshold * exchangeRate
		Regional_price = float(getCF('EGAP_Contigency_Costs_USD').Content) if getCF('EGAP_Contigency_Costs_USD').Content else 0
		if walkAwaySellPrice >0:
			regionalMarginPercent = (regionalMargin/walkAwaySellPrice)*100
			wtwMarginPercentage = (wtwMargin/walkAwaySellPrice)*100
		NPV = float(getCF('EGAP_NPV').Content) if getCF('EGAP_NPV').Content != '' else 0
		sumOfDiscountedMonthlyOutflow = getQuoteTableData(Quote, 'Sum(Cash_Outflow_Discounted_Monthly_Outflows)', 'QT__EGAP_Cash_Outflow_Calculations', '')
		sumOfDiscountedMonthlyInflow = getQuoteTableData(Quote, 'Sum(Cash_Inflow_Discounted_Monthly_Inflows)', 'QT__EGAP_Cash_Inflow_Calculations', '')
		effectiveGrossMargin = 0
		if sumOfDiscountedMonthlyInflow > 0:
			effectiveGrossMargin = round(((sumOfDiscountedMonthlyOutflow + sumOfDiscountedMonthlyInflow)*100)/sumOfDiscountedMonthlyInflow, 2)
		recommendedTargetPrice = quoteDetails['Recommended_Target_Price']
		recommendedTargetPriceUSD = recommendedTargetPrice/exchangeRate
		walkAwaySellPriceUSD = walkAwaySellPrice/exchangeRate
		MPA = getCF('MPA Price Plan').Content if getCF('MPA Price Plan').Content.strip() !='' else 'None'
		excessDiscount = 0 if recommendedTargetPrice <= 1 else (recommendedTargetPriceUSD-walkAwaySellPriceUSD)/recommendedTargetPriceUSD
		excessDiscount *= 100
		revenueField = [
{
'Field':'Going in Sell Price',
'QuoteCurrency':"{:,.2f}".format(round(sellPrice,2)),
'USD': "{:,.2f}".format(round(sellPrice/exchangeRate,2))
},
{
'Field':'Walk-away Sell Price',
'QuoteCurrency':"{:,.2f}".format(round(walkAwaySellPrice,2)),
'USD':"{:,.2f}".format(round(walkAwaySellPrice/exchangeRate,2))
},
{
'Field':'Regional Margin',
'QuoteCurrency':"{:,.2f}".format(round(regionalMargin,2)),
'USD':"{:,.2f}".format(round(regionalMargin/exchangeRate,2))
},
{
'Field':'Regional Margin %',
'QuoteCurrency':str(round(regionalMarginPercent,2))+'%',
'USD': str(round(regionalMarginPercent,2))+'%'
},
{'Field':'WTW Margin',
'QuoteCurrency':"{:,.2f}".format(round(wtwMargin,2)),
'USD': "{:,.2f}".format(round(wtwMargin/exchangeRate,2))
},
{
'Field':'WTW Margin %',
'QuoteCurrency':str(round(wtwMarginPercentage,2))+'%',
'USD':str(round(wtwMarginPercentage,2))+'%'
},
{
'Field':'Net Present Value (NPV)',
'QuoteCurrency':"{:,.2f}".format(round(NPV,2)),
'USD': "{:,.2f}".format(round(NPV/exchangeRate,2))
},
{
'Field':'Effective Gross Margin %',
'QuoteCurrency':str(round(effectiveGrossMargin,2))+'%',
'USD': str(round(effectiveGrossMargin,2))+'%'
},
{
'Field':'Recommended Target Price',
'QuoteCurrency':"{:,.2f}".format(round(recommendedTargetPrice,2)),
'USD': "{:,.2f}".format(round(recommendedTargetPrice/exchangeRate,2))
},
{
'Field':'PROS Recommended Price',
'QuoteCurrency':"{:,.2f}".format(round(PROSRecommendedPrice,2)),
'USD': "{:,.2f}".format(round(PROSRecommendedPrice/exchangeRate,2))
},
{
'Field':'Excess Discount %',
'QuoteCurrency':str(round(excessDiscount,2))+'%',
'USD': str(round(excessDiscount,2))+'%'
},
{
'Field':'Threshold Discount %',
'QuoteCurrency':str(round(thresholdDiscount,2))+'%',
'USD': str(round(thresholdDiscount,2))+'%'
},
{
'Field':'Sales Price Threshold',
'QuoteCurrency':"{:,}".format(round(localSalesPriceThreshold,2)),
'USD': "{:,}".format(salesPriceThreshold)
},
{
'Field':'Contingency costs',
'QuoteCurrency':"{:,}".format(round(Regional_price,2)),
'USD': "{:,}".format(round(Regional_price/exchangeRate,2))
}
]
		if revenueMarginQT.Rows.Count > 0:
			idx = 0
			for row in revenueMarginQT.Rows:
				for latestData in revenueField:
					if row['EGAP_Field_Details']  == latestData['Field']:
						row['EGAP_Quote_Currency'] = latestData['QuoteCurrency']
						row['EGAP_USD_Currency']   = latestData['USD']
		else:
			for row in revenueField:
				r = revenueMarginQT.AddNewRow()
				r['EGAP_Field_Details']	 = row['Field']
				r['EGAP_Quote_Currency'] = row['QuoteCurrency']
				r['EGAP_USD_Currency']	 = row['USD']
		revenueMarginQT.Save()
		thirdPartyContentQT = Quote.QuoteTables["EGAP_Third_Party_Content"]
		sellPriceDict = dict()
		costCategory = []
		sellPriceWithHoneywellPartNumber, sellPriceWithHoneywellPartNumberUSD, sellPriceWithoutHoneywellPartNumber, sellPriceWithoutHoneywellPartNumberUSD, totalSellPrice = (0,) * 5
		for item in Quote.Items:
			if item.AsMainItem and len(list(item.AsMainItem.Children)):
				if quoteType in ('Contract New','Contract Renewal') and float(item.ExtendedAmount) >= 0:
					addToTotal(sellPriceDict, item.QI_PLSG.Value,  round(item.ExtendedAmount,2))
				else:
					continue
			if float(item.ExtendedAmount) >= 0:
				addToTotal(sellPriceDict, item.QI_PLSG.Value,  round(item.ExtendedAmount,2))
			if not item.QI_PLSG.Value in costCategory:
				costCategory.append(item.QI_PLSG.Value)
		if len(costCategory):
			costCategoryList = ', '.join("'{}'".format(category) for category in costCategory)
			SqlQuery = "SELECT SAP_PL_PLSG, Cost_Category, Third_Party_Category FROM SAP_PLSG_LOB_Mapping WHERE SAP_PL_PLSG in ({}) and Third_Party_Category in ({})"
			SqlResult = SqlHelper.GetList(SqlQuery.format(costCategoryList, "'Third Party Hon','True Third Party'"))
			if SqlResult is not None and len(SqlResult) > 0:
				for row in SqlResult:
					sapPLSG = row.SAP_PL_PLSG
					costCategory = row.Cost_Category
					thirdPartCategory = row.Third_Party_Category
					sellPrice = sellPriceDict[sapPLSG]
					totalSellPrice += sellPrice
					if thirdPartCategory == 'True Third Party':
						sellPriceWithoutHoneywellPartNumber += sellPrice
					else:
						sellPriceWithHoneywellPartNumber += sellPrice
			if totalSellPrice > 0:
				sellPriceWithHoneywellPartNumberUSD = sellPriceWithHoneywellPartNumber/exchangeRate
				sellPriceWithoutHoneywellPartNumberUSD = sellPriceWithoutHoneywellPartNumber/exchangeRate
				if thirdPartyContentQT.Rows.Count == 0:
					row = thirdPartyContentQT.AddNewRow()
					row['Product_Details'] = 'Third Party content with HON Part #'
					row['Sell_Price'] = sellPriceWithHoneywellPartNumber
					row['Sell_Price_in_USD'] = sellPriceWithHoneywellPartNumberUSD
					row = thirdPartyContentQT.AddNewRow()
					row['Product_Details'] = 'Third Party content without HON Part #'
					row['Sell_Price'] = sellPriceWithoutHoneywellPartNumber
					row['Sell_Price_in_USD'] = sellPriceWithoutHoneywellPartNumberUSD
					row = thirdPartyContentQT.AddNewRow()
					row['Product_Details'] = 'Total Third Party Content'
					row['Sell_Price'] = totalSellPrice
					row['Sell_Price_in_USD'] = totalSellPrice/exchangeRate
				else:
					for row in thirdPartyContentQT.Rows:
						if row['Product_Details'] == 'Third Party content with HON Part #':
							row['Sell_Price']  = sellPriceWithHoneywellPartNumber
							row['Sell_Price_in_USD'] = sellPriceWithHoneywellPartNumberUSD
						elif row['Product_Details'] == 'Third Party content without HON Part #':
							row['Sell_Price'] = sellPriceWithoutHoneywellPartNumber
							row['Sell_Price_in_USD'] = sellPriceWithoutHoneywellPartNumberUSD
						else:
							row['Sell_Price'] = totalSellPrice
							row['Sell_Price_in_USD'] = totalSellPrice/exchangeRate
			else:
				thirdPartyContentQT.Rows.Clear()
		else:
			thirdPartyContentQT.Rows.Clear()
		thirdPartyContentQT.Save()
		cf_cashflowHealth = getCF('EGAP_Cashflow_Health')
		quoteWTWCost =	getQuoteTableData(Quote, 'Quote_WTW_Cost', 'QT__Quote_Details', '')
		walkawaySalesPrice = getQuoteTableData(Quote, 'Walk_away_Sales_Price', 'QT__Quote_Details', '')
		totalCashInflow = getQuoteTableData(Quote, 'Sum(Cash_Inflow_Total)', 'QT__EGAP_Cash_Inflow_Calculations', '')
		totalCashOutflow = getQuoteTableData(Quote, 'Sum(Cash_Outflow_Total)', 'QT__EGAP_Cash_Outflow_Calculations', '')
		remainingCashOutflow = totalCashOutflow + quoteWTWCost
		remainingCashInflow = totalCashInflow - walkawaySalesPrice
		absNet = abs(round(remainingCashInflow+remainingCashOutflow))