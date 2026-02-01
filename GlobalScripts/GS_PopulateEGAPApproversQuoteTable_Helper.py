#------------------------------------------------------------------------------------------------
#					Change History Log
#------------------------------------------------------------------------------------------------
#Description:This helper utility is created to handle the logical operation of egap approval table.
# 			 (EGAP_APPROVAL_TITLE_REASON_MAPPING)
#-------------------------------------------------------------------------------------------------
# Date 			Name					Version   Comment
# 14-04-2023	Pallavi Sharma			1		  Initial Creation

from System import DBNull
def addToTotal(totalDict , key , value):
    totalDict[key] = totalDict.get(key , 0) + value
def getQuoteTableData(Quote, column, quoteTableName, condition):
    query = "Select {} as output from {} where ownerid={} and cartid={} {} ".format(column, quoteTableName, Quote.UserId, Quote.QuoteId, condition)
    qtResult = SqlHelper.GetFirst(query)
    output = 0
    if qtResult is not None and len(qtResult) > 0:
        output = qtResult.output if qtResult.output != DBNull.Value else 0
    return output
def operate(operator , operand1 , operand2):
    res = 0
    if operator == '/':
        return operand1 / operand2
    if operator == '%':
        return operand1 % operand2
    if operator == '//':
        return operand1 // operand2
    if operator == '+':
        return round(float(operand1) + float(operand2))
    if operator == '-':
        return round(float(operand1) - float(operand2))
    if operator == '*':
        return round(float(operand1) * float(operand2),2)
    if operator == '>':
        res = bool(float(operand1) > float(operand2))
        return res
    if operator == '<':
        return bool(float(operand1) < float(operand2))
    if operator == '>=':
        operand1=0 if operand1 =='No Approval' else operand1
        return bool(float(operand1) >= float(operand2))
    if operator == '<=':
        return bool(float(operand1) <= float(operand2))
    if operator == 'and':
        return bool(operand1) and bool(operand2)
    if operator == 'or':
        return bool(operand1) or bool(operand2)
    if operator == '!=':
        return bool(operand1 != operand2)
    if operator == '==':
        if operand1 == 'HGR' or operand2 == 'HGR':
            operand = operand1 if operand2 == 'HGR' else operand2
            sqlQuery = "Select Count(*) as Count from EGAP_HGR_Countries Where Country_Name = '{}'".format(operand.lower())
            sqlResult = SqlHelper.GetFirst(sqlQuery)
            return bool(sqlResult.Count > 0)
        elif type(operand1) == str and type(operand2) == str:
            return bool(operand1.lower() == operand2.lower())
        else:
            operand2 = int(operand2)
            return bool(operand1 == operand2)
    return 0
def calc(expression, inputArguments):
    resultantValue = []
    preResult = operator = None
    logicalCondition = False
    for var in expression:
        if var not in [ '+', '>','>=','<','<=', '==','!=','-', '*','/','//', '&&', '||']:
            resultantValue.append(inputArguments.get(var, var))
        elif var == '&&':
            logicalCondition = True
            preResult = resultantValue.pop()
            operator = 'and'
        elif var == '||':
            logicalCondition = True
            preResult = resultantValue.pop()
            operator = 'or'
        elif var in [ '+', '>','>=','<','<=', '==','!=','-', '*','/','//']:
            y = resultantValue.pop()
            x = resultantValue.pop()
            res = operate(var , x , y)
            if logicalCondition and bool == type(preResult) and bool == type(res):
                x = preResult
                y = res
                res = operate(operator , x , y)
                logicalCondition = False
            resultantValue.append(res)
    return resultantValue
def populateLabor_and_Engineering_Service(Quote):
    laboHours={}
    laborFields = ['Local Labor','Cross Border Labor','GES - Work @ GES Location','GES - Work @ Non GES Location','Total GES Hours','Total Labor']
    laborGESTable = Quote.QuoteTables["EGAP_Labor_and_Engineering_Service"]
    local_labor = cross_border = ges_at_ges_location = ges_at_non_ges = 0
    laborGESTable.Rows.Clear()
    for item in Quote.MainItems:
        local_labor = local_labor + int(item["QI_Local_Labor"].Value)
        cross_border = cross_border + int(item["QI_Cross_Border_Labor"].Value) 
        ges_at_ges_location = ges_at_ges_location + int(item["QI_GES_Work_GES_Location"].Value) 
        ges_at_non_ges = ges_at_non_ges + int(item["QI_GES_Work_Non_GES_Location"].Value) 
    laboHours['Local Labor'] = local_labor; laboHours['Cross Border Labor'] = cross_border; laboHours['GES - Work @ GES Location'] = ges_at_ges_location; laboHours['GES - Work @ Non GES Location']=ges_at_non_ges
    totalLabor = laboHours.get("Local Labor",0) + laboHours.get("Cross Border Labor",0) + laboHours.get("GES - Work @ GES Location",0) + laboHours.get("GES - Work @ Non GES Location",0)
    for field in laborFields:
        addRow = laborGESTable.AddNewRow()
        if field == "Total GES Hours":
            addRow["EGAP_Labor_Field_Details"] = field
            addRow["EGAP_Labor_Hours"] = laboHours.get("GES - Work @ GES Location",0) + laboHours.get("GES - Work @ Non GES Location",0)
            if totalLabor != 0:
                addRow["EGAP_Labor_Pct"] = round(((float(laboHours.get("GES - Work @ GES Location",0)) + float(laboHours.get("GES - Work @ Non GES Location",0))) / totalLabor * 100) ,2)
        elif field == "Total Labor":
            addRow["EGAP_Labor_Field_Details"] = field
            addRow["EGAP_Labor_Hours"] = totalLabor
            addRow["EGAP_Labor_Pct"] = 100
        else:
            addRow["EGAP_Labor_Field_Details"] = field
            addRow["EGAP_Labor_Hours"] = laboHours.get(field,0)
            if totalLabor != 0:
                addRow["EGAP_Labor_Pct"] = round(((float(laboHours.get(field,0)) / totalLabor) * 100),2)
    laborGESTable.Save()

def BGP(Quote):
	pLSGDetails = Quote.QuoteTables['Product_Line_Sub_Group_Details']
	BGP_PLSG_Code =['7242-7990','7242-7990','7246-7998','7249-7A05','7243-7992','7245-7996','7247-7A01','7688-7B50','7248-7A03','7686-7B48']
	BGP_SELL=''
	BGP_MPA =''
	for row in pLSGDetails.Rows:
		if row['Product_Line_Sub_Group'] in BGP_PLSG_Code and  (int(row['Sell_Price_Discount_Percent'])):
			BGP_SELL='True'
			BGP_MPA= 'True'
			break
		elif row['Product_Line_Sub_Group'] in BGP_PLSG_Code and int(row['MPA_Discount_Percent']) >0 :
			BGP_MPA = 'True'
	return([BGP_SELL,BGP_MPA])
  
def conditionVariables(Quote):
    getVariables = {
        'Q16':Quote.GetCustomField('EGAP_IQ_Ques_16').Content,
        'CTFR10':Quote.GetCustomField('EGAP_CTFR10_Ques').Content,
        'CTFR11':Quote.GetCustomField('EGAP_CTFR11_Ques').Content,
        'CR3d':Quote.GetCustomField('EGAP_Ques_CR3d').Content,
        'EgapNegativeCashflow':(Quote.GetCustomField('EGAP_Max_Consec_Months_Neg_Cum_Cash_Flows').Content or 0),
        'advPaymentmilestone':Quote.GetCustomField('EGAP_Advance_Payment_Milestone_Billing_Ques').Content,
        'CFR1':Quote.GetCustomField('EGAP_CFR1_Ques').Content,
        'CFR2':Quote.GetCustomField('EGAP_CFR2_Ques').Content,
        'CFR4':Quote.GetCustomField('EGAP_CFR4_Ques').Content,
        'CFR5':Quote.GetCustomField('EGAP_CFR5_Ques').Content,
        'CFR6':Quote.GetCustomField('EGAP_CFR6_Ques').Content,
        'MFR1':Quote.GetCustomField('EGAP_MFR1_Ques').Content,
        'CTFR3':Quote.GetCustomField('EGAP_CTFR3_Ques').Content,
        'CTFR4':Quote.GetCustomField('EGAP_CTFR4_Ques').Content,
        'RAFR5':Quote.GetCustomField('EGAP_RAFR5_Ques').Content,
        'RAFR2':Quote.GetCustomField('EGAP_RAFR2_Ques').Content,
        'CTFR1':Quote.GetCustomField('EGAP_CTFR1_Ques').Content,
        'CTFR2':Quote.GetCustomField('EGAP_CTFR2_Ques').Content,
        'CTFR6':Quote.GetCustomField('EGAP_CTFR6_Ques').Content,
		'CTFR5':Quote.GetCustomField('EGAP_CTFR5_Ques').Content,
        'cf_RAFR4Ques':Quote.GetCustomField('EGAP_RAFR4_Ques').Content,
        'cf_RAFR1Ques':Quote.GetCustomField('EGAP_RAFR1_Ques').Content,
        'CTFR12':Quote.GetCustomField('EGAP_CTFR12_Ques').Content,
        'quoteDiscount':float(Quote.QuoteTables["Quote_Details"].Rows[0]["Quote_Discount_Percent"]),
        'MPADiscount': float(Quote.QuoteTables["Quote_Details"].Rows[0]["MPA_Discount_Percent"]),
        'BGP_SELL': BGP(Quote)[0],
        'BGP_MPA':BGP(Quote)[1],
        'NegativePayment':Quote.GetCustomField('Is Payment milestones are negatively deviating from standard milestone?').Content,
        'CR3A':Quote.GetCustomField('EGAP_Ques_CR3a').Content
    }
    return getVariables

# Added this function for the quote exemption scenario in HCP
def check_swbgp(Quote):
    getValues = SqlHelper.GetList("SELECT Software_PLSG_Code,BGP_PLSG_Code FROM HCI_SOFTWARE_BGP (NOLOCK)")
    #Software and BGP dict
    sw_to_bgp_map = {i.Software_PLSG_Code: i.BGP_PLSG_Code for i in getValues}
    #PLSG codes and quantities
    plsg_qty = {}
    BGP_PLSG = []
    Software_PLSG = []
    for item in Quote.Items:
        plsg_code = item.QI_PLSG.Value
        quantity = item.Quantity
        if(plsg_code in sw_to_bgp_map.Keys):
            Software_PLSG.append(plsg_code)
        if(plsg_code in sw_to_bgp_map.Values):
            BGP_PLSG.append(plsg_code)
        if plsg_code in Software_PLSG or plsg_code in BGP_PLSG:
            if plsg_code in plsg_qty:
                plsg_qty[plsg_code] += quantity
            else:
                plsg_qty[plsg_code] = quantity
    for pl in Software_PLSG:
        if sw_to_bgp_map[pl] not in BGP_PLSG or (sw_to_bgp_map[pl] in BGP_PLSG and plsg_qty[sw_to_bgp_map[pl]] <= 0 and plsg_qty[pl] != 0):
            return "false"
    return "true"


def Hgr_data(calc,inputArguments,bookingCountry,bookingLOB,approvalData,uniqueApprover):
	sql_HGR = SqlHelper.GetList("SELECT  HGR.Dep_CF_Name, HGR.Dep_CF_Value,HGR.Approver_Title, HGR.Approver_Reason FROM EGAP_HGR_COUNTRIES_TITLE_REASONS HGR join EGAP_HGR_Countries country on HGR.Country_Name = country.Country_Name Where HGR.Country_Name = '{}' and LOB = '{}' ".format(bookingCountry,bookingLOB.Content))
	Trace.Write(("SELECT  HGR.Dep_CF_Name, HGR.Dep_CF_Value,HGR.Approver_Title, HGR.Approver_Reason FROM EGAP_HGR_COUNTRIES_TITLE_REASONS HGR join EGAP_HGR_Countries country on HGR.Country_Name = country.Country_Name Where HGR.Country_Name = '{}' and LOB = '{}' ".format(bookingCountry,bookingLOB.Content)))
	if sql_HGR is not None:
		for row in sql_HGR:
			approverTitle = row.Approver_Title
			approverReason = row.Approver_Reason
			depCFName = row.Dep_CF_Name
			depCFValue = row.Dep_CF_Value
			approverTitleReason = approverReason
			depFlag = False
			if depCFName == 'Multiple Conditions' and depCFValue.strip() != '':
				expression = depCFValue.split(",")
				resultantValue = calc(expression, inputArguments)
				depFlag = resultantValue[0] if resultantValue[0] else False
			if depFlag == True and approverTitleReason:
				rec = {'EGAP_Approver_Title':'', 'EGAP_Reason':''}
				rec['EGAP_Approver_Title'] = approverTitle
				rec['EGAP_Reason'] = approverReason
				approvalData.append(rec)
				uniqueApprover.append(approverTitleReason)