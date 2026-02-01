def setAccessReadonly(table):
    table.AccessLevel = table.AccessLevel.ReadOnly

def setAccessHidden(table):
    table.AccessLevel = table.AccessLevel.Hidden

def setAccessEditable(table):
    table.AccessLevel = table.AccessLevel.Editable

def deleteTableRows(table):
    table.Rows.Clear()

def editableQuoteTableColumn(table,column):
    table.GetColumnByName(column).AccessLevel = table.AccessLevel.Editable

def readonlyQuoteTableColumn(table,column):
    table.GetColumnByName(column).AccessLevel = table.AccessLevel.ReadOnly

def hideQuoteTableColumn(table,column):
    table.GetColumnByName(column).AccessLevel = table.AccessLevel.Hidden

def getCfValue(cfName):
    return Quote.GetCustomField(cfName).Content

def update_payment_milestones(lob, payment_milestone, milestone_data):
    if milestone_data:
        sum = 0
        count = 1
        for entry in milestone_data:
            row = payment_milestone.AddNewRow()
            row["Milestone_Number"] = "Milestone {}".format(count)
            count += 1
            row["_Amount"] = entry.Amount
            sum = sum + entry.Amount
            if lob == "LSS":
                row["Billing_Milestone"] = entry.MileStone
                row["Milestone_Description"] = entry.Description               
            elif lob == "PAS":
                row["Billing_Milestone"] = entry.MileStone
                if getCfValue("Milestone") == "Standard":
                    row["PAS_Milestone_Description"] = entry.Description
                else:
                    row["Milestone_Description"] = row["Billing_Milestone"]
            elif lob == "HCP":
                row["HCP_Milestone"] = entry.MileStone
                row["Milestone_Description"] = entry.Description
            else:
                row['PMC_Milestone'] 	= entry.MileStone
                row['Milestone'] 	= entry.MileStone
        Quote.GetCustomField("Milestone_total").Content = str(sum)
        Trace.Write("total amount : "+str(sum))

def checkMPAAvailable():
    MultiplePricePlanPresent = False
    if getCfValue("MPA Honeywell Ref") == '':
        return MultiplePricePlanPresent
    query = TagParserQuote.ParseString("select A=1 from MPA_PRICE_PLAN_MAPPING(nolock) where Honeywell_Ref = '<*CTX(Quote.CustomField(MPA Honeywell Ref))*>' and Price_Plan_Status= 'Active' and [IF]([EQ](<*CTX( Quote.CustomField(Quote Type) )*>,Projects)){Price_Plan_Systems_Discount}{Price_Plan_Parts_Discount}[ENDIF] = 'Y' and Price_Plan_Start_Date <= '<*CTX( Date.Format(MM/dd/yyyy) )*>' and Price_Plan_End_Date >= '<*CTX( Date.Format(MM/dd/yyyy) )*>'")
    res = SqlHelper.GetFirst(query)
    if res and len(res) > 0:
        MultiplePricePlanPresent = True
    return MultiplePricePlanPresent

paymentMileStone = Quote.QuoteTables["Payment_MileStones"]

bookingLOB = getCfValue("Booking LOB")
mileStoneCategory = getCfValue("Payment Milestones Category")
MultiplePricePlanPresent = checkMPAAvailable()
Trace.Write("Bookign Lob Change ===== "+str(getCfValue("Booking LOB")))
if bookingLOB == "PMC":
    hideQuoteTableColumn(paymentMileStone,"PAS_Milestone_Description")
    Quote.GetCustomField('Milestone').Visible = True

    if getCfValue("Milestone") == 'Standard':
        deleteTableRows(paymentMileStone)
        if paymentMileStone.Rows.Count == 0:
            milestone_tab = SqlHelper.GetList("select MileStone,Amount from MILESTONETABLE(nolock) where LOB = 'PMC'")
            update_payment_milestones(bookingLOB,paymentMileStone, milestone_tab)
            readonlyQuoteTableColumn(paymentMileStone,"PMC_Milestone")
            readonlyQuoteTableColumn(paymentMileStone,"Milestone")
            readonlyQuoteTableColumn(paymentMileStone,"_Amount")
            setAccessReadonly(paymentMileStone)
            paymentMileStone.CanAddRows = False
            paymentMileStone.CanDeleteRows = False
        else:
            setAccessEditable(paymentMileStone)
            #readonlyQuoteTableColumn(paymentMileStone,"Milestone_Number")
            editableQuoteTableColumn(paymentMileStone,"PMC_Milestone")
            editableQuoteTableColumn(paymentMileStone,"Milestone")
            editableQuoteTableColumn(paymentMileStone,"_Amount")
            paymentMileStone.CanAddRows = True
            paymentMileStone.CanDeleteRows = True
        Quote.GetCustomField('CF_PMC_MilestoneCustom_NewMode').Content = "1"
    elif getCfValue("Milestone") == 'Custom' and getCfValue("CF_PMC_MilestoneCustom_NewMode") == "1":
        deleteTableRows(paymentMileStone)
        if paymentMileStone.Rows.Count == 0:
            milestone_tab = SqlHelper.GetList("select MileStone,Amount from MILESTONETABLE(nolock) where LOB = 'PMC'")
            update_payment_milestones(bookingLOB,paymentMileStone, milestone_tab)
            Quote.GetCustomField('CF_PMC_MilestoneCustom_NewMode').Content = "0"
            setAccessEditable(paymentMileStone)
            #readonlyQuoteTableColumn(paymentMileStone,"Milestone_Number")
            editableQuoteTableColumn(paymentMileStone,"PMC_Milestone")
            editableQuoteTableColumn(paymentMileStone,"Milestone")
            editableQuoteTableColumn(paymentMileStone,"_Amount")
            paymentMileStone.CanAddRows = True
            paymentMileStone.CanDeleteRows = True
    elif getCfValue("Milestone") != 'Custom':
        deleteTableRows(paymentMileStone)
        paymentMileStone.CanAddRows = True
        paymentMileStone.CanDeleteRows = True
        Quote.GetCustomField('CF_PMC_MilestoneCustom_NewMode').Content = "1"
    paymentMileStone.Save()
elif bookingLOB == "LSS" and getCfValue("Quote Type") in ('Projects') :
    hideQuoteTableColumn(paymentMileStone,"PAS_Milestone_Description")
    hideQuoteTableColumn(paymentMileStone,"PMC_Milestone")
    MultiplePricePlanPresent = checkMPAAvailable()
    if not MultiplePricePlanPresent:
        Quote.GetCustomField('Milestone').Visible = True
        Quote.GetCustomField('Payment Milestones Category').Visible = True
        if getCfValue("Milestone") in ('Standard','Custom'):
            if paymentMileStone.Rows.Count == 0:                    
                mileStoneData = SqlHelper.GetList("select mt.MileStone,md.Description,mt.Amount from MILESTONETABLE mt(nolock) join MILESTONE_DESCRIPTION md(nolock) on mt.MileStone = md.Billing_Milestone where LOB = 'LSS' and MilestoneCategory = '{}' and md.Milestone_Category = ''".format(mileStoneCategory))
                update_payment_milestones(bookingLOB,paymentMileStone, mileStoneData)
            if getCfValue("Milestone") == "Standard":
                #readonlyQuoteTableColumn(paymentMileStone,"Milestone_Number")
                readonlyQuoteTableColumn(paymentMileStone,"Billing_Milestone")
                readonlyQuoteTableColumn(paymentMileStone,"Milestone_Description")
                readonlyQuoteTableColumn(paymentMileStone,"_Amount")
                setAccessReadonly(paymentMileStone)
                paymentMileStone.CanAddRows = False
                paymentMileStone.CanDeleteRows = False
            else:
                setAccessEditable(paymentMileStone)
                #editableQuoteTableColumn(paymentMileStone,"Milestone_Number")
                editableQuoteTableColumn(paymentMileStone,"Billing_Milestone")
                editableQuoteTableColumn(paymentMileStone,"Milestone_Description")
                editableQuoteTableColumn(paymentMileStone,"_Amount")
                paymentMileStone.CanAddRows = True
                paymentMileStone.CanDeleteRows = True
        else:
            paymentMileStone.Rows.Clear()
    else:
        Quote.GetCustomField("Milestone").Visible = False
        setAccessEditable(paymentMileStone)
    paymentMileStone.Save()
elif (bookingLOB in("PAS","CCC") and getCfValue("Quote Type") in ('Projects')) or (bookingLOB in("CCC") and getCfValue("Quote Type") in ('Parts and Spot')):
    hideQuoteTableColumn(paymentMileStone,"PMC_Milestone")
    MultiplePricePlanPresent = checkMPAAvailable()
    if not MultiplePricePlanPresent:
        Quote.GetCustomField('Milestone').Visible = True
        Quote.GetCustomField('Payment Milestones Category').Visible = True
        if getCfValue("Milestone") in ('Standard','Custom'):
            if paymentMileStone.Rows.Count == 0:
                mileStoneData = SqlHelper.GetList("select mt.MileStone,md.Description,mt.Amount from MILESTONETABLE mt(nolock) join MILESTONE_DESCRIPTION md(nolock) on mt.MileStone = md.Billing_Milestone where LOB = '{}' and md.Milestone_Category = '{}' and mt.MilestoneCategory = '{}' and md.Default_Value = 'Y'".format(bookingLOB, mileStoneCategory,mileStoneCategory))
                update_payment_milestones(bookingLOB,paymentMileStone, mileStoneData)
            if getCfValue("Milestone") == "Standard":
                #setAccessReadonly(paymentMileStone)
                #setAccessEditable(paymentMileStone)
                hideQuoteTableColumn(paymentMileStone,"Milestone_Description")
                #readonlyQuoteTableColumn(paymentMileStone,"Milestone_Number")
                readonlyQuoteTableColumn(paymentMileStone,"Billing_Milestone")
                readonlyQuoteTableColumn(paymentMileStone,"_Amount")
                editableQuoteTableColumn(paymentMileStone,"PAS_Milestone_Description")
                paymentMileStone.CanAddRows = False
                paymentMileStone.CanDeleteRows = False
            else:
                setAccessEditable(paymentMileStone)
                #editableQuoteTableColumn(paymentMileStone,"Milestone_Number")
                editableQuoteTableColumn(paymentMileStone,"Billing_Milestone")
                editableQuoteTableColumn(paymentMileStone,"_Amount")
                hideQuoteTableColumn(paymentMileStone,"PAS_Milestone_Description")
                editableQuoteTableColumn(paymentMileStone,"Milestone_Description")
                paymentMileStone.CanAddRows = True
                paymentMileStone.CanDeleteRows = True
        else:
            paymentMileStone.Rows.Clear()
    else:
        Quote.GetCustomField("Milestone").Visible = False
        setAccessEditable(paymentMileStone)
    paymentMileStone.Save()
elif bookingLOB in("HCP"):
    Trace.Write('hcp quote rows-'+str(mileStoneCategory))
    hideQuoteTableColumn(paymentMileStone,"PMC_Milestone")
    hideQuoteTableColumn(paymentMileStone,"PAS_Milestone_Description")
    hideQuoteTableColumn(paymentMileStone,"Billing_Milestone")
    Quote.GetCustomField('Milestone').Visible = True
    Quote.GetCustomField('Milestone').Label = 'Payment Milestones'
    Quote.GetCustomField('Payment Milestones Category').Visible = True
    #Quote.GetCustomField('Payment Milestones Category').Content = 'Standard Small' if getCfValue("Payment Milestones Category") == '' else getCfValue("Payment Milestones Category")
    if getCfValue("Milestone") == "Custom":
        if paymentMileStone.Rows.Count == 0:
            mileStoneData = SqlHelper.GetList("select mt.MileStone,md.Description,mt.Amount from MILESTONETABLE mt(nolock) join MILESTONE_DESCRIPTION md(nolock) on mt.MileStone = md.Billing_Milestone where LOB = '{}' and md.Milestone_Category = '{}' and mt.MilestoneCategory = '{}' and md.Default_Value = 'Y'".format(bookingLOB,mileStoneCategory,mileStoneCategory))
            Trace.Write("select mt.MileStone,md.Description,mt.Amount from MILESTONETABLE mt(nolock) join MILESTONE_DESCRIPTION md(nolock) on mt.MileStone = md.Billing_Milestone where LOB = '{}' and md.Milestone_Category = '{}' and mt.MilestoneCategory = '{}' and md.Default_Value = 'Y'".format(bookingLOB,mileStoneCategory,mileStoneCategory))
            Trace.Write('--hcp miles--'+str(len(mileStoneData)))
            update_payment_milestones(bookingLOB,paymentMileStone, mileStoneData)
            setAccessEditable(paymentMileStone)
            #editableQuoteTableColumn(paymentMileStone,"Milestone_Number")
            editableQuoteTableColumn(paymentMileStone,"_Amount")
            editableQuoteTableColumn(paymentMileStone,"Milestone_Description")
            paymentMileStone.CanAddRows = True
            paymentMileStone.CanDeleteRows = True
    paymentMileStone.Save()
else:
    Trace.Write("Hidden Inside ==== ")
    setAccessHidden(paymentMileStone)
    Quote.GetCustomField('Milestone').Visible = False

Quote.GetCustomField("Milestone_total").Content = ""
qt = Quote.QuoteTables["Payment_MileStones"]
sum = 0
for row in qt.Rows:
    sum = sum + row["_Amount"]
if bookingLOB in ("CCC","HCP") and sum == 100:
    Quote.Messages.Remove('Sum of % milestone payment is not equal to 100%')
    Quote.GetCustomField('sum_of_milestone_flag').Content = '0'
    # Quote.GetCustomField('EGAP_Cashflow_Health').Content = 'In Balance' 
Quote.GetCustomField("Milestone_total").Content = str(sum)
Quote.Save(False)