#CXCPQ-86942
import GS_GetPriceFromCPS as cps
def reset_values(Product):
    Product.Attr('CBM_REMOTE_TIME').AssignValue('0.00')
    Product.Attr('CBM_LOCAL_TIME').AssignValue('0.00')
    Product.Attr('CBM_TASK_PERCENTAGE').AssignValue('0.00 %')
    Product.Attr('CBM_PER_TIME').AssignValue('0.00')
    Product.Attr('CBM_REMOTE_TASKS').AssignValue('0')
    Product.Attr('CBM_LOCAL_TASKS').AssignValue('0')
    Product.Attr('CBM_LIST_PRICE_PER_CYCLE').AssignValue('0.00')
    Product.Attr('CBM_ANNUAL_PRICE').AssignValue('0.00')
    Product.Attr('CBM_LPM_TASK').AssignValue('')
########## All Pricing Calc ##################
def pricing_calc(level,getPricingDetails,count,cycles,Quote,TagParserQuote,Session):
    returnDict = {}
    ########## Remote Time and Remote Task Calc ################## 
    Trace.Write('Remote_TT_NC_Quarterly:' + str(getPricingDetails.Remote_TT_NC_Quarterly))
    Trace.Write('Remote_TT_NC Annually:' + str(getPricingDetails.Remote_TT_NC))
    Trace.Write('Remote_TT_C_Quarterly:' + str(getPricingDetails.Remote_TT_C_Quarterly))
    Trace.Write('Remote_TT_C Annually:' + str(getPricingDetails.Remote_TT_C))
    Trace.Write('cycles:' + str(cycles))

    if level in ["1", "3"]:
        remoteTime = float(getPricingDetails.Remote_TT_NC_Quarterly) + (float(getPricingDetails.Remote_TT_NC)/int(cycles))
        remoteTask = getPricingDetails.Remote_T_NC
    else:
        remoteTime = float(getPricingDetails.Remote_TT_C_Quarterly) + (float(getPricingDetails.Remote_TT_C)/int(cycles))
        remoteTask = getPricingDetails.Remote_T_C
    returnDict["RemoteTime"] = str(remoteTime)
    returnDict["RemoteTask"] = str(remoteTask)
    ########## Local Time and Local Task Calc ################### 
    if int(level) < 3:
        localTime = 0.00
        localTask = 0
    else:
        localTime = (float(getPricingDetails.STD_Hours_LT_Quarterly) +(float(getPricingDetails.STD_Hours_LT)/int(cycles)))- float(remoteTime)
        localTask = int(getPricingDetails.Total_Tasks) - int(remoteTask)
    returnDict["LocalTime"] = str(localTime)
    returnDict["LocalTask"] = str(localTask)
    Trace.Write('STD_Hours_LT_Quarterly:' + str(getPricingDetails.STD_Hours_LT_Quarterly))
    Trace.Write('STD_Hours_LT Annually:' + str(getPricingDetails.STD_Hours_LT))
    Trace.Write('localTime:' + str(localTime))
    Trace.Write('remoteTime:' + str(remoteTime))
    ########## Time Percent Calc #################
    #%Time= (Local Time + Remote Time)/(StandardHours_LT_Q+(StandardHours_LT/cycles))
    if float(getPricingDetails.STD_Hours_LT) > 0.00:
        timePercent = round(((float(localTime) + float(remoteTime))/  (float(getPricingDetails.STD_Hours_LT_Quarterly) +(float(getPricingDetails.STD_Hours_LT)/int(cycles))))*100,2)
    else:
        timePercent = 0.00
    timePercent=0.00
    returnDict["PerTime"] = str(timePercent)
    ########## Unit List Calc ###################
    #unitPrice=(Labour List Price (Hourly)based on country * Local Time) +  Labour List Price (Hourly)based on country  * "REMOTE Time" M16 * (1-"Remote Factor %") 
    # Remote Factor is 20%
    priceDict = dict()
    laborPart = 'SVC-ESSS-FD'
    priceDict = cps.getPrice(Quote,priceDict,[laborPart],TagParserQuote,Session)
    laborPrice = float(priceDict.get(laborPart,0))/8.0
    Trace.Write('price from SAP:' + str(float(priceDict.get(laborPart,0))))
    unitPrice = (float(laborPrice) * float(localTime)) + (float(remoteTime)*float(laborPrice)*(1-0.2)) 
    returnDict["ListPricePerCycle"] = str(unitPrice)
    Trace.Write('laborPrice:' + str(laborPrice))
    Trace.Write('unitPrice:' + str(unitPrice))
    ########## Annual Price Calc ################
    # AnnualPrice=((Full PM unit price averaged per cycle + (Full PM unit price averaged per cycle* "Admin factor %" ) )*  "PM/CBM Cycles")* Qty
    #Admin factor is 10%
    admin_factor=0.1
    annualPrice = round((unitPrice + (unitPrice*admin_factor))*int(cycles) * int(count),2)
    returnDict["AnnualPrice"] = str(annualPrice)
    Trace.Write('annualPrice:' + str(annualPrice))
    ########## Task Percent Calc #################
    #%Tasks = (Local Task + Remote Task)/Total Tasks
    if int(getPricingDetails.Total_Tasks) > 0:
        taskPrecent = round(((float(localTask) + float(remoteTask)) / float(getPricingDetails.Total_Tasks))*100,2)
    else:
        taskPrecent = 0
    returnDict["Tasks"] = str(taskPrecent) + " %"
    return returnDict