def setAccessReadonly(table):
    table.AccessLevel = table.AccessLevel.ReadOnly
    #table.Save()
    
def setAccessHidden(table):
    table.AccessLevel = table.AccessLevel.Hidden
    #table.Save()


def setAccessEditable(table):
    table.AccessLevel = table.AccessLevel.Editable
    #table.Save()

def deleteTableRows(table):
    for row in table.Rows:
        table.DeleteRow(row.Id)
    #table.Save()

def editableQuoteTableColumn(table,column):
    table.GetColumnByName(column).AccessLevel = table.AccessLevel.Editable

def readonlyQuoteTableColumn(table,column):
    table.GetColumnByName(column).AccessLevel = table.AccessLevel.ReadOnly

def hideQuoteTableColumn(table,column):
    table.GetColumnByName(column).AccessLevel = table.AccessLevel.Hidden

def getCfValue(cfName):
  return Quote.GetCustomField(cfName).Content

def checkMPAAvailable():
    MultiplePricePlanPresent = False
    if getCfValue("MPA Honeywell Ref") == '':
        return MultiplePricePlanPresent
    query = TagParserQuote.ParseString("select * from MPA_PRICE_PLAN_MAPPING where Agreement_Name= '<*CTX(Quote.CustomField(MPA))*>' and Price_Plan_Status= 'Active' and [IF]([EQ](<*CTX( Quote.CustomField(Quote Type) )*>,Projects)){Price_Plan_Systems_Discount}{Price_Plan_Parts_Discount}[ENDIF] = 'Y' and Price_Plan_Start_Date <= '<*CTX( Date.Format(MM/dd/yyyy) )*>' and Price_Plan_End_Date >= '<*CTX( Date.Format(MM/dd/yyyy) )*>'")
    res = SqlHelper.GetList(query)
    #Log.Write(query)
    if res and len(res) > 0:
        MultiplePricePlanPresent = True
    return MultiplePricePlanPresent

paymentMileStone = Quote.QuoteTables["Payment_MileStones"]

bookingLOB = getCfValue("Booking LOB")
mileStoneCategory = getCfValue("Payment Milestones Category")
if Quote.GetCustomField("Quote Tab Booking LOB").Content == "PMC":
    hideQuoteTableColumn(paymentMileStone,"PAS_Milestone_Description")
    Quote.GetCustomField('Milestone').Visible = True
    if Quote.GetCustomField("Milestone").Content == "Standard":
        deleteTableRows(paymentMileStone)
        milestone_tab = SqlHelper.GetList("select * from MILESTONETABLE where LOB = 'PMC'")
        sum = 0
        if milestone_tab is not None:
            for entry in milestone_tab:
                row = paymentMileStone.AddNewRow()
                row['Milestone'] 	= entry.MileStone
                row['_Amount'] 		= entry.Amount
                #paymentMileStone.Save()
                sum = sum + entry.Amount
            Quote.GetCustomField("Milestone_total").Content = str(sum)
        setAccessReadonly(paymentMileStone)
    elif Quote.GetCustomField("Milestone").Content == "Custom":
        setAccessEditable(paymentMileStone)
    else:
        deleteTableRows(paymentMileStone)
    paymentMileStone.Save()
elif getCfValue("Booking LOB") == "LSS" and getCfValue("Quote Type") in ('Projects') :
    hideQuoteTableColumn(paymentMileStone,"PAS_Milestone_Description")
    MultiplePricePlanPresent = checkMPAAvailable()
    Trace.Write("check1")
    if not MultiplePricePlanPresent:
        Log.Write("MPA present wrong")
        Quote.GetCustomField('Milestone').Visible = True
        Quote.GetCustomField('Payment Milestones Category').Visible = True
        if getCfValue("Milestone") in ('Standard','Custom'):
            Trace.Write("check2")
            paymentMileStone.Rows.Clear()
            mileStoneData = SqlHelper.GetList("select mt.MileStone,md.Description,mt.Amount from MILESTONETABLE mt join MILESTONE_DESCRIPTION md on mt.MileStone = md.Billing_Milestone where LOB = 'LSS' and MilestoneCategory = '{}' and md.Milestone_Category = ''".format(mileStoneCategory))
            count = 1
            if mileStoneData is not None:
                Trace.Write("check3")
                for entry in mileStoneData:
                    Trace.Write("check4")
                    row = paymentMileStone.AddNewRow()
                    row["Milestone_Number"] = "Milestone {}".format(count)
                    count = count + 1
                    row["Billing_Milestone"] = entry.MileStone
                    row["Milestone_Description"] = entry.Description
                    row["_Amount"] = entry.Amount
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
            Trace.Write("else check")
            paymentMileStone.Rows.Clear()
    else:
        Quote.GetCustomField("Milestone").Visible = False
        Quote.GetCustomField("Payment Milestones").Visible = True
        setAccessEditable(paymentMileStone)
    paymentMileStone.Save()
elif (getCfValue("Booking LOB") in ("PAS", "CCC") and getCfValue("Quote Type") in ('Projects')) or (getCfValue("Booking LOB") in ("CCC") and getCfValue("Quote Type") in ('Parts and Spot')):
    MultiplePricePlanPresent = checkMPAAvailable()
    #Trace.Write("check1")
    if not MultiplePricePlanPresent:
        Quote.GetCustomField('Milestone').Visible = True
        if getCfValue("Milestone") in ('Standard','Custom'):
            #Quote.GetCustomField('sum_of_milestone_flag').Content = '0'
            paymentMileStone.Rows.Clear()
            mileStoneData = SqlHelper.GetList("select mt.MileStone,md.Description,mt.Amount from MILESTONETABLE mt join MILESTONE_DESCRIPTION md on mt.MileStone = md.Billing_Milestone where LOB = '{}' and md.Milestone_Category = '{}' and mt.MilestoneCategory = '{}' and md.Default_Value = 'Y'".format(getCfValue("Booking LOB"), mileStoneCategory,mileStoneCategory))
            count = 1
            if mileStoneData is not None:
                Trace.Write("check3")
                for entry in mileStoneData:
                    Trace.Write("check4")
                    row = paymentMileStone.AddNewRow()
                    row["Milestone_Number"] = "Milestone {}".format(count)
                    count = count + 1
                    row["Billing_Milestone"] = entry.MileStone
                    if getCfValue("Milestone") == "Standard":
                        row["PAS_Milestone_Description"] = entry.Description
                    else:
                        row["Milestone_Description"] = row["Billing_Milestone"]
                    row["_Amount"] = entry.Amount
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
            Trace.Write("else check")
            paymentMileStone.Rows.Clear()
    else:
        Quote.GetCustomField("Milestone").Visible = False
        setAccessEditable(paymentMileStone)
    paymentMileStone.Save()
elif getCfValue("Booking LOB") in ("HCP"):
    Quote.GetCustomField('Milestone').Visible = True
    if getCfValue("Milestone") in ('Custom'):
        paymentMileStone.Rows.Clear()
        mileStoneData = SqlHelper.GetList("select mt.MileStone,md.Description,mt.Amount from MILESTONETABLE mt join MILESTONE_DESCRIPTION md on mt.MileStone = md.Billing_Milestone where LOB = '{}' and md.Milestone_Category = '{}' and mt.MilestoneCategory = '{}' and md.Default_Value = 'Y'".format(getCfValue("Booking LOB"), mileStoneCategory,mileStoneCategory))
        count = 1
        if mileStoneData is not None:
            for entry in mileStoneData:
                row = paymentMileStone.AddNewRow()
                row["Milestone_Number"] = "Milestone {}".format(count)
                count = count + 1
                row["HCP_Milestone"] = entry.MileStone
                row["Milestone_Description"] = entry.Description
                row["_Amount"] = entry.Amount if str(entry.Amount)!= '' else 0
            setAccessEditable(paymentMileStone)
            #editableQuoteTableColumn(paymentMileStone,"Milestone_Number")
            #editableQuoteTableColumn(paymentMileStone,"Billing_Milestone")
            editableQuoteTableColumn(paymentMileStone,"_Amount")
            hideQuoteTableColumn(paymentMileStone,"PAS_Milestone_Description")
            hideQuoteTableColumn(paymentMileStone,"Billing_Milestone")
            editableQuoteTableColumn(paymentMileStone,"Milestone_Description")
            paymentMileStone.CanAddRows = True
            paymentMileStone.CanDeleteRows = True
    else:
        paymentMileStone.Rows.Clear()

    paymentMileStone.Save()

else:
    setAccessHidden(paymentMileStone)
    Quote.GetCustomField('Milestone').Visible = False

Quote.GetCustomField("Milestone_total").Content = ""
qt = Quote.QuoteTables["Payment_MileStones"]
sum = 0
for row in qt.Rows:
    sum = sum + row["_Amount"]
Quote.GetCustomField("Milestone_total").Content = str(sum)
Quote.Save(False)              