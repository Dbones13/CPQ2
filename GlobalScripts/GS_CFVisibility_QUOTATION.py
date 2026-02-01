'''
New Script is created to manage the visibility of custom fields within the "QUOTATION" tab
replacing GS_Custom Field Visibilty
'''
from GS_SetEgapValues import setegapvalues
from GS_CommonConfig import CL_CommonSettings as CS
from GS_CommonModule import getCFValue,hideCF,getCF,showCF,setCFValue,setCFReadonly,getFloat
from GS_Display_Warning_Message import Laborwarningmessage

'''def checkMPAAvailable():
    MultiplePricePlanPresent = False
    if QuoteType == "Projects":
        query = TagParserQuote.ParseString(
            "select A=count(1) from MPA_PRICE_PLAN_MAPPING(NOLOCK) where Agreement_Name= '<*CTX(Quote.CustomField(MPA))*>' and Price_Plan_Status= 'Active' and Price_Plan_Systems_Discount = 'Y' and Price_Plan_Start_Date <= '<*CTX( Date.Format(MM/dd/yyyy) )*>' and Price_Plan_End_Date >= '<*CTX( Date.Format(MM/dd/yyyy) )*>'")
    else:
        query = TagParserQuote.ParseString(
            "select A=count(1) from MPA_PRICE_PLAN_MAPPING(NOLOCK) where Agreement_Name= '<*CTX(Quote.CustomField(MPA))*>' and Price_Plan_Status= 'Active' and Price_Plan_Parts_Discount = 'Y' and Price_Plan_Start_Date <= '<*CTX( Date.Format(MM/dd/yyyy) )*>' and Price_Plan_End_Date >= '<*CTX( Date.Format(MM/dd/yyyy) )*>'")
    res = SqlHelper.GetFirst(query)
    if res.A > 0:
        MultiplePricePlanPresent = True
    return MultiplePricePlanPresent'''
#MultiplePricePlanPresent = checkMPAAvailable()

# ---------------
Opportunity=Quote.GetCustomField("Opportunity Type").Content
if User.BelongsToPermissionGroup('Cyber_estimator') and str(Opportunity) in ('Contract New','Contract Renewal'):
    Quote.GetCustomField("Quote Type").Content ="Projects"
else:
    Quote.GetCustomField("Quote Type").Content = CS.getQuoteType[str(Opportunity)]

if Quote.OrderStatus.Name == 'Preparing':
    if getCFValue(Quote, "EGAP_Project_Type") == 'Time & Material Only' and not getCFValue(Quote, "MPA"):
        setegapvalues(Quote)
    Laborwarningmessage(Quote)
else:
    '''customFields = SqlHelper.GetList("SELECT distinct p.StrongName from ScParamDefnNew p join ScParamPermission pp on p.ScParamId = pp.ScParamId where pp.Permission=2 and p.StrongName like 'EGAP_%'")
    for cf in customFields:
        if Quote.GetCustomField(cf.StrongName).Editable:
            Quote.GetCustomField(cf.StrongName).Editable = False'''
    customFields = ['EGAP_CFR1_Ques', 'EGAP_CFR3_Ques', 'EGAP_Ques_CR5c', 'EGAP_Cash_Recovery_to_Margin_level', 'EGAP_PFR1_Ques_Rule', 'EGAP_Total_Sell_Price_of_HCI_Labor', 'EGAP_Total_Sell_Price_of_Third_Party_Goods', 'EGAP_IQ_Ques_12_Comment', 'EGAP_Material_Type', 'EGAP_CTFR1_Ques_Rule', 'EGAP_IQ_Ques_1', 'EGAP_Months_Negative_Cumulative_Cash_Flows', 'EGAP_Risk_Count_CR9a', 'EGAP_CAR_Ques_8', 'EGAP_Cashflow_Health', 'EGAP_Revenue_Impact_Change_in_Currency_USD', 'EGAP_IQ_Ques_7', 'EGAP_IQ_Ques_10', 'EGAP_RAFR5_Ques', 'EGAP_Ques_CR1b', 'EGAP_Milestone_Project_Duration_Months', 'EGAP_CTFR10_Ques','EGAP_CAR_Ques_1', 'EGAP_Risk_Count_CR1b', 'EGAP_IQ_Ques_5', 'EGAP_Risk_Count_CR4a', 'EGAP_RAFR2_RQUP_Number', 'EGAP_Ques_CR8a', 'EGAP_Risk_Count_CR4c', 'EGAP_Ques_CR3b', 'EGAP_CTFR3_Ques_Rule', 'EGAP_Max_Consec_Months_Neg_Cum_Cash_Flows', 'EGAP_CAR_Ques_9', 'EGAP_Risk_Count_CR3b', 'EGAP_CTFR2_Ques_Rule', 'EGAP_IQ_Ques_3', 'EGAP_MFR2_Ques_Rule', 'EGAP_MFR1_Ques_Rule', 'EGAP_IQ_Ques_10_Comment', 'EGAP_Order_Type_Obsolete', 'EGAP_Cost_Category_Type', 'EGAP_Proposal_Type', 'EGAP_Ques_CR3c', 'EGAP_Ques_CR4a', 'EGAP_Total_Sell_Price_of_Other_Goods', 'EGAP_Risk_Count_CR8a', 'EGAP_CTFR7_Ques_Rule', 'EGAP_NPV', 'EGAP_CTFR9_Ques', 'EGAP_Ques_CR5b', 'EGAP_IQ_Ques_13_Comment', 'EGAP_RAFR2_Ques', 'EGAP_CTFR3_Ques', 'EGAP_Ques_CR4c', 'EGAP_No_of_Shipment', 'EGAP_Advance_Payment_Milestone_Billing_Ques', 'EGAP_Risk_Count_CR9b', 'EGAP_HCI_SW_Milestone_Billing_Ques', 'EGAP_Lowest_Cum_CF_in_any_Single_Month_USD', 'EGAP_CTFR12_Ques_Rule', 'EGAP_Booking_Quote_Approval_Requirement', 'EGAP_CAR_Ques_2', 'EGAP_IQ_Ques_2', 'EGAP_IQ_Ques_8_Comment', 'EGAP_Do_the_Proposed_Milestones_Deviate_Negatively', 'EGAP_Ques_CR3d', 'EGAP_IQ_Ques_14', 'EGAP_Risk_Count_CR3a', 'EGAP_Contract_End_Date', 'EGAP_QT_CashOutflow_Warning', 'EGAP_RAFR2_Ques_Rule', 'EGAP_Ques_CBTPQ1', 'EGAP_Credit_Payment_Terms', 'EGAP_Risk_Count_CR4b', 'EGAP_Ques_CR7a', 'EGAP_RAFR4_Ques_Rule', 'EGAP_IS_Booking_Check_Visible', 'EGAP_Reason_For_Deviation_Milestone_Billing_Ques', 'EGAP_RAFR5_Ques_Rule', 'EGAP_CFR4_Ques_Rule', 'EGAP_Risk_Count_CR5b', 'EGAP_DCF_At_GM_Level', 'EGAP_CTFR4_Ques_Rule', 'EGAP_CFR4_Ques', 'EGAP_Total_Number_Of_Risk_Factors', 'EGAP_CTFR1_Ques', 'EGAP_IQ_Ques_9', 'EGAP_Third_Party_Goods_Milestone_Billing_Ques', 'EGAP_IQ_Ques_14_Comment', 'EGAP_CAR_Ques_6', 'EGAP_Highest_Approval_Level_for_the_Quote', 'EGAP_Total_Sell_Price_of_Subscription_SW', 'EGAP_Risk_Count_CR1a', 'EGAP_Discount_Rate', 'EGAP_Project_Labor_Milestone_Billing_Ques', 'EGAP_Non_Milestone_Billing_Total_Sell_Price', 'EGAP_IQ_Ques_8', 'EGAP_CTFR7_Ques', 'EGAP_CTFR8_Ques_Rule', 'EGAP_CFR3_Ques_Rule', 'EGAP_IQ_Ques_13', 'EGAP_Project_Duration_Months', 'EGAP_CTFR9_Ques_Rule', 'EGAP_CTFR4_Ques', 'EGAP_CAR_Ques_3', 'EGAP_Ques_CR6b', 'EGAP_CTFR12_Ques', 'EGAP_Cash_Flow_Quality', 'EGAP_Risk_Count_CR6b', 'EGAP_CFR1_Ques_Rule', 'EGAP_Milestone_Project_Duration_Weeks', 'EGAP_RAFR2_RQUP_Number_Rule', 'EGAP_IQ_Ques_7_Comment', 'EGAP_Ques_MQ8', 'EGAP_Ques_HCI_Solution_Included', 'EGAP_RAFR1_RQUP_Number_Rule', 'EGAP_CTFR2_Ques', 'EGAP_No_eGap', 'EGAP_CTFR6_Ques_Rule', 'EGAP_Milestone_Price', 'EGAP_IQ_Ques_9_Comment', 'EGAP_QT_ProjectMilestone_Warning', 'EGAP_CFD_Cashflow_Health', 'EGAP_Other_Goods_Milestone_Billing_Ques', 'EGAP_CAR_Ques_4', 'EGAP_Risk_Count_CR5a_CR5b', 'EGAP_CTFR5_Ques', 'EGAP_Credit_Terms_Months', 'EGAP_Project_Duration_Weeks', 'EGAP_CFD_Cash_Flow_Quality', 'EGAP_CTFR6_Ques', 'EGAP_HCI_Labor_Milestone_Billing_Ques', 'EGAP_Risk_Count_CR7a', 'EGAP_PFR1_Ques', 'EGAP_MFR2_Ques', 'EGAP_Approval_Level_when_Price_Discount_Exceeds_Threshold_Discount', 'EGAP_Ques_MQ4', 'EGAP_RQUP_Number', 'EGAP_Risk_Count_CR3c', 'EGAP_MFR1_Ques', 'EGAP_Approval_Level_when_Cash_Flow_negative_position_GT_100k', 'EGAP_Do_Want_to_Chanage_Ans_of_Func_Ques', 'EGAP_Contigency_Costs_USD', 'EGAP_Remaining_Milestone_Percentage', 'EGAP_CTFR11_Ques', 'EGAP_Risk_Count_CR5a', 'EGAP_IQ_Ques_6_Comment', 'EGAP_IQ_Ques_4', 'EGAP_IQ_Ques_11_Comment', 'EGAP_Total_Sell_Price_of_Project_Labor', 'EGAP_CAR_Ques_5', 'EGAP_Total_Sell_Price_of_HCI_SW', 'EGAP_Ques_CR3a', 'EGAP_Project_Type', 'EGAP_RAFR3_Ques_Rule', 'EGAP_RAFR4_Ques', 'EGAP_CFR2_Ques_Rule', 'EGAP_Ques_CR6a', 'EGAP_Cross_Margin', 'EGAP_IS_BookingGateKeeperApprovalRequired', 'EGAP_IQ_Ques_11', 'EGAP_RAFR3_Ques', 'EGAP_Subscription_SW_Milestone_Billing_Ques', 'EGAP_Ques_Manul_Cost_Entry', 'EGAP_CFR2_Ques', 'EGAP_CTFR10_Ques_Rule', 'EGAP_IQ_Ques_6', 'EGAP_Risk_Count_CR5c', 'EGAP_CTFR8_Ques', 'EGAP_Milestones_Accordance_with_the_MPA', 'EGAP_Ques_CR1a', 'EGAP_Contract_Start_Date', 'EGAP_CTFR11_Ques_Rule', 'EGAP_Risk_Count_CR3d', 'EGAP_RAFR1_RQUP_Number', 'EGAP_Risk_Count_CR6a', 'EGAP_Ques_CR5a', 'EGAP_RAFR1_Ques_Rule', 'EGAP_Highest_Price_Margin_Approval_Level', 'EGAP_Ques_CR4b', 'EGAP_IQ_Ques_12', 'EGAP_Ques_CR9a', 'EGAP_RAFR1_Ques', 'EGAP_IQ_Ques_5_Comment', 'EGAP_Highest_Cash_Risk_Approval_Level', 'EGAP_CTFR5_Ques_Rule', 'EGAP_ETR_Number_Rule', 'EGAP_Payment_Milestones', 'EGAP_CAR_Ques_7', 'EGAP_ETR_Number', 'EGAP_Ques_CR9b', 'EGAP_Ques_CBTPQ2', 'EGAP_CFR5_Ques', 'EGAP_CFR6_Ques', 'EGAP_CFR5_Ques_Rule', 'EGAP_CFR6_Ques_Rule']
    
    for cf in customFields:
        if Quote.GetCustomField(cf).Editable:
            Quote.GetCustomField(cf).Editable = False
# -------------------
# ------------------- CXCPQ-117256 -------------------
if getCFValue(Quote, "Opportunity Type") != "Change Order":
    hideCF(getCF(Quote, "EGAP_CFR6_Ques"))
    hideCF(getCF(Quote, "EGAP_CFR6_Ques_Rule"))
    setCFValue(Quote, "EGAP_CFR6_Ques", "")
# ------------------- CXCPQ-117256 -------------------
# ------------------- CXCPQ-117247 -------------------
thirdPartyMaterialTP = getFloat(getCFValue(Quote, 'TrueThirdParty_Cost_In_USD')) + getFloat(getCFValue(Quote, 'ThirdPartyHon_Cost_In_USD'))
if thirdPartyMaterialTP < 250000:
    hideCF(getCF(Quote, "EGAP_RAFR3_Ques"))
    hideCF(getCF(Quote, "EGAP_RAFR3_Ques_Rule"))
else:
    showCF(getCF(Quote, "EGAP_RAFR3_Ques"))
    showCF(getCF(Quote, "EGAP_RAFR3_Ques_Rule"))
# ------------------- CXCPQ-117247 -------------------
if getCFValue(Quote, "Quote Type") == "Projects":
    hideCF(getCF(Quote, 'Discount Request Reason'))
'''else:
    hideCF(getCF(Quote, "Recommended Discount Plan"))
    hideCF(getCF(Quote, "Selected Discount Plan"))
    hideCF(getCF(Quote, "Schedule Price Plan Updated"))

if BookingLOB in ('LSS', 'PAS') and QuoteType == "Projects":
    if MultiplePricePlanPresent:
        hideCF(getCF(Quote, "Recommended Discount Plan"))
        hideCF(getCF(Quote, "Selected Discount Plan"))
        hideCF(getCF(Quote, "Schedule Price Plan Updated"))
    else:
        showCF(getCF(Quote, "Recommended Discount Plan"))
        showCF(getCF(Quote, "Selected Discount Plan"))
        showCF(getCF(Quote, "Schedule Price Plan Updated"))
        hideCF(getCF(Quote, "MPA Price Plan"))
        hideCF(getCF(Quote, "MPA Validity"))
        hideCF(getCF(Quote, "MPA Threshold"))
        setCFValue(Quote, "Schedule Price Plan Updated", "True")
else:
    if BookingLOB != 'CCC':
        hideCF(getCF(Quote, 'Exchange Rate'))

if BookingLOB == "LSS" and QuoteType == "Parts and Spot":
    if not MultiplePricePlanPresent:
        hideCF(getCF(Quote, "MPA Threshold"))


if getCFValue(Quote, "Booking LOB") == "PMC":
    hideCF(getCF(Quote, "MPA Threshold"))
    hideCF(getCF(Quote, "MPA Price Plan"))
    hideCF(getCF(Quote, "MPA Validity"))
    setCFReadonly(getCF(Quote, "PMC Type"))
    setCFReadonly(getCF(Quote, "PMC Product Family"))
    setCFReadonly(getCF(Quote, "PMC Product Line"))
    hideCF(getCF(Quote, "MPA Honeywell Ref"))
    if getCFValue(Quote, "Quote Type") == "Projects":
        showCF(getCF(Quote, "EGAP_Proposal_Type"))
    elif getCFValue(Quote, "Quote Type") == "Parts and Spot":
        hideCF(getCF(Quote, 'Discount Request Reason'))
        if not User.BelongsToPermissionGroup('PMC WTW Cost Access Group'):
            hideCF(getCF(Quote, "TotalwtwMarginPercent"))
elif getCFValue(Quote, "Booking LOB") != "PMC":
    hideCF(getCF(Quote, "PMC Type"))
    hideCF(getCF(Quote, "PMC Product Family"))
    hideCF(getCF(Quote, "PMC Product Line"))'''

if (getCFValue(Quote, "Booking LOB") == "PMC" and getCFValue(Quote, "Quote Type") not in ("Projects")) or (getCFValue(Quote, "Booking LOB") == "LSS" and getCFValue(Quote, "Quote Type") not in ("Projects", "Contract New", "Contract Renewal")):
    Quote.CustomFields.Disallow('EGAP_Proposal_Type', 'EGAP_Project_Type')


Quote.GetCustomField('Tech/Benefit Price Factor').Visible = False
Quote.GetCustomField('Competitive Price Factor').Visible = False

if (getCFValue(Quote, "Booking LOB") in ("LSS", "PAS") and getCFValue(Quote, "Quote Type") == 'Projects') or (getCFValue(Quote, "Booking LOB") in ("CCC", "HCP")):
    if getCFValue(Quote, "EGAP_Proposal_Type") != 'Firm':
        hideCF(getCF(Quote, "Booking Revision"))
    if getCFValue(Quote, "EGAP_IS_Booking_Check_Visible") != 'Yes':
        hideCF(getCF(Quote, "Parent Firm Revision"))
        hideCF(getCF(Quote, "EGAP_Do_Want_to_Chanage_Ans_of_Func_Ques"))
    if getCFValue(Quote, "Change Proposal Type") != '1':
        hideCF(getCF(Quote, "Revised proposal type"))
    if getCFValue(Quote, "Booking LOB") == "HCP" and getCFValue(Quote, "Quote Type") == "Projects":
        Quote.GetCustomField('Tech/Benefit Price Factor').Visible = True
        Quote.GetCustomField('Competitive Price Factor').Visible = True
        Quote.GetCustomField('Competitive Price Factor').Required = True
        Quote.GetCustomField('Tech/Benefit Price Factor').Required = True
        if getCFValue(Quote, "Booking LOB") == 'HCP' and Quote.OrderStatus.Name != 'Preparing':
            setCFReadonly(getCF(Quote, "Tech/Benefit Price Factor"))
            setCFReadonly(getCF(Quote, "Competitive Price Factor"))
else:
    hideCF(getCF(Quote, "Booking Revision"))
    hideCF(getCF(Quote, "Parent Firm Revision"))
    hideCF(getCF(Quote, "EGAP_Do_Want_to_Chanage_Ans_of_Func_Ques"))
    hideCF(getCF(Quote, "Revised proposal type"))

# CXCPQ-101295
BookingCountry = getCFValue(Quote, "Booking Country").lower()
'''if getCFValue(Quote, "Quote Type") != 'Projects' or getCFValue(Quote, "Booking LOB") not in ('PAS', 'LSS') or BookingCountry != 'india':
    hideCF(getCF(Quote, "India Discounted TP Margins"))'''

#----------------
#adding Logic for CXCPQ-110966- Start
if getCFValue(Quote, "Quote Type") in ('Contract New','Contract Renewal'):
    hideCF(getCF(Quote, "Generate_document_Selection"))
    hideCF(getCF(Quote, "Document_Generation_Format"))
    hideCF(getCF(Quote, "Document_Category"))
#Logic for CXCPQ-110966- End
'''if Quote.Items.Count > 0:
    partsAvailable = ''
    if getCFValue(Quote, "Quote Type") == 'Projects':
        Quote.Messages.Remove(Translation.Get('message.UnreleasedProductRestriction').format(
            str(Quote.GetCustomField("RQUP_partList").Content)))
        #prd_List = ['C200_Migration', 'ELCN'] RITM10938438
        prd_List = ['C200_Migration']
        Partexist = []
        for prd in prd_List:
            if Quote.ContainsAnyProductByPartNumber(prd):
                Partexist.append(prd)
        Partlist = ",".join(Partexist)

        if (getCFValue(Quote, 'EGAP_RAFR1_Ques') == 'No' and CS.RQUP_Dict["PreRealseParts"] != "") or (getCFValue(Quote, 'EGAP_RAFR1_Ques') == 'Yes' and getCFValue(Quote, 'EGAP_RAFR1_RQUP_Number') == "" and Partlist != ""):
            CS.RQUP_Dict["PreRealseParts"]=''
            validParts = set([item.PartNumber for item in Quote.Items if item["QI_CrossDistributionStatus"].Value == '05 PreRelease'])
            CS.RQUP_Dict["PreRealseParts"]=str(', '.join(validParts))
            partsAvailable = CS.RQUP_Dict["PreRealseParts"] if CS.RQUP_Dict["PreRealseParts"] else Partlist
            if not Quote.Messages.Contains(Translation.Get('message.UnreleasedProductRestriction').format(partsAvailable)):
                Quote.Messages.Add(Translation.Get(
                    'message.UnreleasedProductRestriction').format(partsAvailable))
                Quote.GetCustomField("RQUP_partList").Content = str(partsAvailable)'''
#-----------------

#CXP-43972
'''import GS_Visibility_PROS_Guidance as vpg
vpg.PROS_Guidance_Visibility(Quote,User)'''

#-----------------
if getCFValue(Quote, "Booking LOB") != 'PMC' or getCFValue(Quote, "Quote Type") not in ('Projects','Parts and Spot'):
    hideCF(getCF(Quote, "Total_Tariff_Amount"))
    hideCF(getCF(Quote, "Total_Sell_Price_Incl_Tariff"))

'''if getCFValue(Quote, "Booking LOB") == 'HCP':
    hideCF(getCF(Quote, "India Discounted TP Margins"))'''
if getCFValue(Quote, "Quote Type") == 'Parts and Spot' and getCFValue(Quote, "Booking LOB") == 'LSS':
	showCF(getCF(Quote, "Total_Tariff_Amount"))
	showCF(getCF(Quote, "Total_Sell_Price_Incl_Tariff"))
if getCFValue(Quote, "Quote Type") == 'Parts and Spot':
    hideCF(getCF(Quote,"CF_ProjectId"))
if getCFValue(Quote, "Booking LOB") in ('LSS', 'PAS', 'HCP'):
    if getCFValue(Quote , "MPA") != '' and getCFValue(Quote , "MPA Price Plan") != '':
        hideCF(getCF(Quote, "Recommended Discount Plan"))
        hideCF(getCF(Quote, "Selected Discount Plan"))
        hideCF(getCF(Quote, "Schedule Price Plan Updated"))
    else:
        showCF(getCF(Quote, "Recommended Discount Plan"))
        showCF(getCF(Quote, "Selected Discount Plan"))
        showCF(getCF(Quote, "Schedule Price Plan Updated"))
        hideCF(getCF(Quote, "MPA Price Plan"))
        hideCF(getCF(Quote, "MPA Validity"))
        hideCF(getCF(Quote, "MPA Threshold"))
        hideCF(getCF(Quote, "MPA Honeywell Ref"))
        setCFValue(Quote, "Schedule Price Plan Updated", "True")
if getCFValue(Quote, "Quote Type") != "Projects":
    hideCF(getCF(Quote , "Recommended Discount Plan"))
    hideCF(getCF(Quote , "Selected Discount Plan"))
    hideCF(getCF(Quote , "Schedule Price Plan Updated"))