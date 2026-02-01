
from datetime import datetime, timedelta
import math
costCurveTable = Quote.QuoteTables['Honeywell_HCI_Labor_BGP_Cost_Curve']
projectDurationMonths = 0
if Quote.GetCustomField('EGAP_Milestone_Project_Duration_Months').Content:
    projectDurationMonths = int(Quote.GetCustomField('EGAP_Milestone_Project_Duration_Months').Content)
cf_contractStartDate = Quote.GetCustomField('EGAP_Contract_Start_Date').Content
cf_contractEndDate = Quote.GetCustomField('EGAP_Contract_End_Date').Content
contractStartDate =TagParserQuote.ParseString("<*CTX( Quote.CustomField(EGAP_Contract_Start_Date).Format(dd.MM.yy))*>")
contractEndDate = TagParserQuote.ParseString("<*CTX( Quote.CustomField(EGAP_Contract_End_Date).Format(dd.MM.yy))*>")
changedCellIndex = len(EventArgs.Cells) - 1
changedCell = EventArgs.Cells[changedCellIndex]
changedRow = changedCell.Row
newValue = changedCell.Value
changedColumn = changedCell.ColumnName

def calculate_roundup(startDate, result_date, newValue):
    if int(newValue) > 0:
        result = int(newValue)
    else:
        days_difference = (result_date - startDate).days+1
        value = days_difference / 30
        result = 0 if value < 0 else value

    return int(-(-result // 1))

if changedColumn == "Starting_Month" and newValue != '' and int(newValue)>0:
    if int(newValue)> int(projectDurationMonths):
        changedRow['Starting_Month'] = 0
        curveDeleteList = [rows.Id for rows in costCurveTable.Rows if rows['PLSG_Code'] == changedRow['PLSG_Code']]
        curveDeleteList.reverse()
        for delrow in curveDeleteList:
            costCurveTable.DeleteRow(delrow)
    elif int(newValue)<= int(projectDurationMonths):
        getTimeLine = SqlHelper.GetList("SELECT Product_Description, Standard_Timeline, Cost_Per FROM Cost_Curve_timeline_laborBGP(NOLOCK) WHERE PLSG_Code = '"+str(changedRow['PLSG_Code'])+"' ")  
        try:  
            startDate = datetime.strptime(str(contractStartDate), '%d.%m.%Y')
            endDate = datetime.strptime(str(contractEndDate), '%d.%m.%Y')
        except:
            startDate = datetime.strptime(str(contractStartDate), '%d.%m.%y')
            endDate = datetime.strptime(str(contractEndDate), '%d.%m.%y')
        monthARO = int(changedRow['Starting_Month'])
        #Trace.Write(str(startDate)+'-startDate--'+str(monthARO * 30 - (30 - 15)))
        startDateDCSCompletion = startDate + timedelta(days=monthARO * 30 - (30 - 15))
        durationAdvsolEnd = round(((endDate - startDateDCSCompletion).days+1) / 30.00)
        durationStartAdvsols = round(((startDateDCSCompletion - startDate).days+1) / 30.00)
        #Trace.Write('startDateDCSCompletion-'+str(startDateDCSCompletion))
        curveUpdateList = [rows for rows in costCurveTable.Rows if rows['PLSG_Code'] == changedRow['PLSG_Code']]
        result_date = startDate + timedelta(days=int(newValue) * 30 - (30 - 15))
        for timelines in getTimeLine:
            timeCost = str(timelines.Cost_Per).replace('%','')
            #Trace.Write(str(durationAdvsolEnd)+'---------'+str(durationStartAdvsols))
            calculatedARO = float(timelines.Standard_Timeline)*durationAdvsolEnd+durationStartAdvsols
            resultantMonthARO = math.ceil(round(calculatedARO,5))
            timeCost = float(timeCost)/100
            #Trace.Write(str(row['Cost'])+'--timeCost-'+str(timeCost))
            costCurve = float(timeCost)*float(changedRow['Cost'])
            #Trace.Write('costCurve---'+str(costCurve))
            if len(curveUpdateList) == 0:
                addRow = costCurveTable.AddNewRow()
                addRow['PLSG_Code'] = changedRow['PLSG_Code']
                addRow['Product_Description'] = changedRow['Product_Description']
                #addRow['Month_ARO'] = changedRow['Starting_Month']
                addRow['Month_ARO'] = str(int(resultantMonthARO))
                addRow['Cost_Curve'] = costCurve
                addRow['DCSCompletion'] = str(startDateDCSCompletion)
                addRow['Standard_Timeline'] = str(timelines.Standard_Timeline)
            else:
                for rows in curveUpdateList:
                    if rows['Standard_Timeline'] == str(timelines.Standard_Timeline):
                        rows['Month_ARO'] = str(int(resultantMonthARO))
                        rows['Cost_Curve'] = costCurve
                        rows['DCSCompletion'] = str(startDateDCSCompletion)
        if len(getTimeLine) == 0:
            if len(curveUpdateList) == 0:
                addRow = costCurveTable.AddNewRow()
                addRow['PLSG_Code'] = changedRow['PLSG_Code']
                addRow['Product_Description'] = changedRow['Product_Description']
                #addRow['Month_ARO'] = changedRow['Starting_Month']
                addRow['Month_ARO'] = str(int(calculate_roundup(startDate, result_date, newValue)))
                addRow['Cost_Curve'] = float(changedRow['Cost'])
                addRow['DCSCompletion'] = str(startDateDCSCompletion)
                #addRow['Standard_Timeline'] = str(timelines.Standard_Timeline)
            elif len(curveUpdateList)>0:
                for rows in curveUpdateList:
                    rows['Month_ARO'] = str(int(calculate_roundup(startDate, result_date, newValue)))
                    rows['Cost_Curve'] = float(changedRow['Cost'])
                    rows['DCSCompletion'] = str(startDateDCSCompletion)

elif int(newValue)==0:
    curveDeleteList = [rows.Id for rows in costCurveTable.Rows if rows['PLSG_Code'] == changedRow['PLSG_Code']]
    curveDeleteList.reverse()
    for delrow in curveDeleteList:
        costCurveTable.DeleteRow(delrow)