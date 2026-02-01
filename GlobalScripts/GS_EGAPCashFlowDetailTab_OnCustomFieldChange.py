import GS_EGAPCashFlowDetail as CFD

cashOutflow =  CFD.GetQuoteTable(Quote, "Cash_Outflow")
newRecord = {'Cost_Category_Type':'','Shipment_Number':'','Shipment_Description':'','Cost':0.00,'Month_ARO':0,'P3_Product_Type':'','Vendor_Payment_Term':'','HW_SW_Labor_Type':'','Adj_Month_ARO':0,'Labor_Cost':0.00,'ARO_Labor':0,'Burden_Cost':0.00,'ARO_Burden':0,'Material_Cost':0.00,'ARO_Material':0,'Purchasing_Cost':0.00,'ARO_Purchasing':0,'Freight_Cost':0.00,'ARO_Freight':0,'Row_Type':'Item','Adj_Month_Price':0, 'Price_Receipt':0.00}
columns = ['Shipment_Number', 'Shipment_Description', 'Cost', 'Month_ARO', 'Vendor_Payment_Term','P3_Product_Type']#Added by abhijeet
if Quote.GetCustomField('EGAP_No_of_Shipment').Label == sender.Label:
    if Quote.GetCustomField('EGAP_No_of_Shipment').Content.strip() != '':
        noOfNewRecords = int(Quote.GetCustomField('EGAP_No_of_Shipment').Content)
        if Quote.GetCustomField('EGAP_Material_Type').Content.strip() != '' and noOfNewRecords > 0:
            materialType = Quote.GetCustomField('EGAP_Material_Type').Content.strip()
            if noOfNewRecords:
                #cashOutflow = Quote.QuoteTables["Cash_Outflow"]
                items = []
                for row in cashOutflow.Rows:
                    rowDict = dict()
                    for key in newRecord.keys():
                        rowDict[key] = row[key]
                    items.append(rowDict)
                maxIndex = len(items)
                if maxIndex:
                    resultArray = []
                    newRecordAdded = 0
                    shipmentNumber = 1
                    previousMaterialType = currentMaterialType = ''
                    for index, item in enumerate(items):
                        if item['Row_Type'] == 'Header':
                            previousMaterialType = currentMaterialType
                            currentMaterialType = item['Cost_Category_Type']
                        if item['Row_Type'] == 'Item' and currentMaterialType == materialType:
                            shipmentNumber += 1
                        if previousMaterialType == materialType and newRecordAdded < 1:
                            totalRow = resultArray.pop()
                            resultArray, newRecordAdded = CFD.addNewRecords(newRecord, noOfNewRecords, resultArray, shipmentNumber)
                            resultArray.append(totalRow)
                        resultArray.append(item)
                    if len(resultArray) == len(items):
                        totalRow = resultArray.pop()
                        resultArray, newRecordAdded = CFD.addNewRecords(newRecord, noOfNewRecords, resultArray, shipmentNumber)
                        resultArray.append(totalRow)
                    #cashOutflow = Quote.QuoteTables["Cash_Outflow"]
                    cashOutflow.Rows.Clear()
                    for data in resultArray:
                        row = cashOutflow.AddNewRow()
                        for key in data.keys():
                            row[key] = data[key]
                        if row['Row_Type'] in ['Header', 'Total']:
                            if row['Row_Type'] == 'Header':
                                currentMaterialType = row['Cost_Category_Type']
                            for col in columns:
                                row.Cells.Item[col].AccessLevel = cashOutflow.AccessLevel.ReadOnly
                        elif currentMaterialType not in ['Third Party Goods & Services','Other Goods & Services', 'Third Party Buyout']:
                            row.Cells.Item['Vendor_Payment_Term'].AccessLevel = cashOutflow.AccessLevel.ReadOnly
                    #cashOutflow.Save()
        Quote.GetCustomField('EGAP_No_of_Shipment').Content = ''
        Quote.GetCustomField('EGAP_Material_Type').Content = ''
elif Quote.GetCustomField('EGAP_Subscription_SW_Milestone_Billing_Ques').Label == sender.Label:
    if arg.NewValue in ['Yes','No']:
        Quote.CustomFields.Allow('EGAP_Total_Sell_Price_of_Subscription_SW')
    else:
        Quote.CustomFields.Disallow('EGAP_Total_Sell_Price_of_Subscription_SW')
elif Quote.GetCustomField('EGAP_Project_Labor_Milestone_Billing_Ques').Label == sender.Label:
    if arg.NewValue in ['Yes','No']:
        Quote.CustomFields.Allow('EGAP_Total_Sell_Price_of_Project_Labor')
    else:
        Quote.CustomFields.Disallow('EGAP_Total_Sell_Price_of_Project_Labor')
elif Quote.GetCustomField('EGAP_Third_Party_Goods_Milestone_Billing_Ques').Label == sender.Label:
    if arg.NewValue in ['Yes','No']:
        Quote.CustomFields.Allow('EGAP_Total_Sell_Price_of_Third_Party_Goods')
    else:
        Quote.CustomFields.Disallow('EGAP_Total_Sell_Price_of_Third_Party_Goods')
elif Quote.GetCustomField('EGAP_Other_Goods_Milestone_Billing_Ques').Label == sender.Label:
    if arg.NewValue in ['Yes','No']:
        Quote.CustomFields.Allow('EGAP_Total_Sell_Price_of_Other_Goods')
    else:
        Quote.CustomFields.Disallow('EGAP_Total_Sell_Price_of_Other_Goods')
elif Quote.GetCustomField('Payment Terms').Label == sender.Label:
    '''Refresh Cash outflow Calculation'''
    CFD.updateCashOutflowCalculation(Quote, cashOutflow, TagParserQuote)
    #cashOutflow.Save()
    '''Refresh Project Milestone Quote table'''
    cf_milestonePrice = float(Quote.GetCustomField('EGAP_Milestone_Price').Content)
    cf_creditTerms = CFD.getCreditTermsMonths(Quote)
    projectMilestone = Quote.QuoteTables["EGAP_Project_Milestone"]
    CFD.updateProjectMilestone(Quote, projectMilestone, cf_creditTerms, cf_milestonePrice, TagParserQuote)
    '''Validating Project Milestone Data '''
    maxMonthARO = CFD.getMaxMonthARO(Quote)
    Quote.GetCustomField('EGAP_QT_ProjectMilestone_Warning').Content = CFD.validateProjectMilestoneData(projectMilestone, maxMonthARO)
    #projectMilestone.Save()
elif Quote.GetCustomField('EGAP_Ques_Manul_Cost_Entry').Label == sender.Label:
    honeywellLaborCostCurve =  CFD.GetQuoteTable(Quote, "EGAP_Honeywell_Labor_Cost_Curve")
    cf_CostCategoryType = Quote.GetCustomField('EGAP_Cost_Category_Type')
    costCategoryTypeList = []
    if cf_CostCategoryType.Content != '':
        costCategoryTypeList = cf_CostCategoryType.Content.replace("'",'').split(', ')
    WTWCost,sellPrice_p = CFD.getWTWCost_sellprice(Quote, 'Honeywell Labor')
    if arg.NewValue == 'No':
        '''Remove Honeywell Labor from Cash_Outflow'''
        CFD.removeCostCategory(cashOutflow, 'Honeywell Labor')
        '''Standard timleine for the Cost curve calculcation'''
        projectDurationMonths = 0
        if Quote.GetCustomField('EGAP_Milestone_Project_Duration_Months').Content:
            projectDurationMonths = float(Quote.GetCustomField('EGAP_Milestone_Project_Duration_Months').Content)
        #CFD.standardCostCurveCalculation(Quote, honeywellLaborCostCurve, projectDurationMonths, WTWCost)
        '''Remove the Honeywell Labor from material type drop down'''
        if 'Honeywell Labor' in costCategoryTypeList:
            costCategoryTypeList.remove('Honeywell Labor')
            cf_CostCategoryType.Content = ', '.join("'{}'".format(category) for category in costCategoryTypeList)
    elif arg.NewValue == 'Yes':
        '''Add Honeywell Labor to the material type drop down'''
        if cf_CostCategoryType.Content != '':
            cf_CostCategoryType.Content = cf_CostCategoryType.Content.join(", 'Honeywell Labor'")
        #CFD.updateCashOutflowCalculation(Quote, cashOutflow)
        row = cashOutflow.AddNewRow()
        row['Cost_Category_Type']     = 'Honeywell Labor'
        row['Shipment_Description'] = ''
        row['Cost'] = WTWCost
        row['Row_Type'] = 'Header'
        '''Readonly Columns'''
        for col in columns:
            row.Cells.Item[col].AccessLevel = cashOutflow.AccessLevel.ReadOnly
        defaultRows = [{'Shipment_Number':'Shipment 1','Row_Type':'Item'}, {'Shipment_Number':'Total of Entered Shipment','Row_Type':'Total'}]
        CFD.addDefaultRows(Quote, cashOutflow, defaultRows, 'Honeywell Labor', columns,{})
        honeywellLaborCostCurve.Rows.Clear()
	#honeywellLaborCostCurve.Save()
    '''Update Total of shipment cost and cash outflow Warning message'''
    #Quote.GetCustomField('EGAP_QT_CashOutflow_Warning').Content = CFD.updateTotalCost(Quote, cashOutflow)
    CFD.populateCashOutflowCalculation(Quote, TagParserQuote)
elif Quote.GetCustomField('EGAP_Milestone_Price').Label == sender.Label:
    '''Refresh Project Milestones Quote table'''
    milestonePrice = float(arg.NewValue)
    cf_creditTerms = CFD.getCreditTermsMonths(Quote)
    projectMilestone = Quote.QuoteTables["EGAP_Project_Milestone"]
    CFD.updateProjectMilestone(Quote, projectMilestone, cf_creditTerms, milestonePrice, TagParserQuote)
if sender.Label in [Quote.GetCustomField('EGAP_Ques_CBTPQ1').Label, Quote.GetCustomField('EGAP_Ques_CBTPQ2').Label, Quote.GetCustomField('EGAP_Third_Party_Goods_Milestone_Billing_Ques').Label,Quote.GetCustomField('EGAP_Other_Goods_Milestone_Billing_Ques').Label]:
    '''Refresh Cash outflow Calculation'''
    CFD.updateCashOutflowCalculation(Quote, cashOutflow, TagParserQuote)
#cashOutflow.Save()