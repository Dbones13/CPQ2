def getCfValue(cf):
    return Quote.GetCustomField(cf).Content

requiredFields = []

restrictApproval = False
projectFieldCheck = ['EGAP_Contract_Start_Date','EGAP_Contract_End_Date','Payment Terms']
for field in projectFieldCheck:
    if getCfValue(field):
        continue
    restrictApproval = True
    if field == "EGAP_Contract_Start_Date":
        requiredFields.append("Contract Start Date")
    elif field == "EGAP_Contract_End_Date":
        requiredFields.append("Contract End Date")
    elif field == "Payment Terms":
        requiredFields.append("Payment Terms")

    break

if getCfValue("EGAP_CFR4_Ques") == "Yes" and getCfValue("EGAP_ETR_Number") == '':
    restrictApproval = True
    requiredFields.append("ETR Number")

if getCfValue("Quote Type") == "Projects" and getCfValue("EGAP_Project_Type") == '':
    restrictApproval = True
    requiredFields.append("Project Type")

if getCfValue("EGAP_RAFR1_Ques") == "Yes" and getCfValue("EGAP_RAFR1_RQUP_Number") == '' and Quote.GetCustomField('EGAP_Proposal_Type').Content != 'Budgetary':
    restrictApproval = True
    requiredFields.append("RQUP Number")

# if getCfValue("EGAP_RAFR2_Ques") == "Yes" and getCfValue("EGAP_RAFR2_RQUP_Number") == '':
    # restrictApproval = True
    # requiredFields.append("RQUP Number")

if getCfValue("Booking LOB") == "CCC" and getCfValue("sum_of_milestone_flag") == '1':
    restrictApproval = True
    requiredFields.append("Sum of % milestone payment is not equal to 100%")

if getCfValue("EGAP_Cashflow_Health") == "Out of Balance":
    restrictApproval = True
    requiredFields.append("Cashflow Health is Out of Balance")

projectDuration = getCfValue('EGAP_Project_Duration_Months')
projectDuration = int(projectDuration) if projectDuration != '' else 0
sqlQuery = "Select count(Month_ARO) as ct from QT__Cash_Outflow where ownerid={} and cartid={} and Row_Type='{}' and (Month_ARO <= {} or Month_ARO > {} )"
sqlResult = SqlHelper.GetFirst(sqlQuery.format(Quote.UserId, Quote.QuoteId, 'Item', 0, projectDuration))

if sqlResult is not None and sqlResult.ct > 0:
    restrictApproval = True
    requiredFields.append("Month ARO is either less than or equal to 0 Or it does not fall under project duration")

if not Quote.GetCustomField("EGAP_Reason_For_Deviation_Milestone_Billing_Ques").Content:
   requiredFields.append("Reason for Deviation")

if getCfValue("Booking LOB") in ("LSS","PAS","HCP") and getCfValue("Quote Type") == "Projects" and Quote.GetCustomField('EGAP_Proposal_Type').Content != 'Budgetary':
    ThirdPartycontent = float(getCfValue("TrueThirdParty_Cost_In_USD"))
    #regional_cost = 0
    if ThirdPartycontent > 250000 and getCfValue("EGAP_RAFR3_Ques") == "No":
        Quote.Messages.Add(Translation.Get("error.message.rafr3"))
        restrictApproval = True
                    
                    

if restrictApproval and getCfValue("Quote Type") == "Projects" and getCfValue("Booking LOB") != "PMC":
    WorkflowContext.BreakWorkflowExecution = True
    if 'Reason for Deviation' in requiredFields and not Quote.Messages.Contains(Translation.Get("error.message.ReasonForDeviation")):
        Quote.Messages.Add(Translation.Get("error.message.ReasonForDeviation"))
        requiredFields.remove('Reason for Deviation')
    if requiredFields:
        Quote.Messages.Add(Translation.Get("error.message.egapapproval").format(",".join(requiredFields)))