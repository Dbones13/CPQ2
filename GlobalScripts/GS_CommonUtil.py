def getCFValue(quote, cfName):
    return quote.GetCustomField(cfName).Content

def setCFValue(quote, cfName, cfValue):
    quote.GetCustomField(cfName).Content = cfValue


def getFloat(Var):
    if Var:
        return float(Var)
    return 0


def log_dict(dictionary):
    Trace.Write(RestClient.SerializeToJson(dictionary))


def queryToCsv(queryRes):
    columns = []
    rows = []
    for row in queryRes:
        for col in row:
            columns.append(col.Key)
        break

    for resRow in queryRes:
        row = list()
        for col in resRow:
            row.append(str(col.Value))
        rows.append("","".join(row))

    csv = ""{}"
"{}"".format("","".join(columns) , ""
"".join(rows))
    return csv


def queryToDict(queryRes , arrayKey = 'Rows'):
    resDict = dict()
    rows = list()
    for resRow in queryRes:
        rowDict = dict()
        for col in resRow:
            rowDict[col.Key] = col.Value
        rows.append(rowDict)
    resDict[arrayKey] = rows
    return resDict

#Function to retrive custom parameter value from CT_CUSTOM_PARAMETER table
def GetCustomParamValue(*args):
    arg_count=len(args)
    if arg_count==1:
        SqlQuery="Select NUMERIC_VALUE,STRING_VALUE from CT_CUSTOM_PARAMETER where PARAM_NAME='"+str(args[0])+"'"
    elif arg_count==2:
        SqlQuery="Select NUMERIC_VALUE,STRING_VALUE from CT_CUSTOM_PARAMETER where PARAM_NAME='"+str(args[0])+"'"
    elif arg_count==3:
        SqlQuery="Select NUMERIC_VALUE,STRING_VALUE from CT_CUSTOM_PARAMETER where PARAM_NAME='"+str(args[0])+"' AND FUNC_IND1='"+str(args[1])+"'"
    elif arg_count==4:
        SqlQuery="Select NUMERIC_VALUE,STRING_VALUE from CT_CUSTOM_PARAMETER where PARAM_NAME='"+str(args[0])+"' AND FUNC_IND1='"+str(args[1])+"' AND FUNC_IND1='"+str(args[2])+"'"
    else:
        SqlQuery="Select STRING_VALUE from CT_CUSTOM_PARAMETER where PARAM_NAME='"+str(args[0])+"'"
    Res=SqlHelper.GetFirst(SqlQuery)
    if arg_count==2:
        if args[1]=='R_DEC':
            return Res.NUMERIC_VALUE
        else:
            return Res.STRING_VALUE
    else:
    	return Res.STRING_VALUE