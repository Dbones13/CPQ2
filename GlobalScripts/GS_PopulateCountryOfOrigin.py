def getCfValue(cfName):
    return Quote.GetCustomField(cfName).Content

def getUniquePLSG(plsgTable):
    plsgData = []
    if plsgTable.Rows.Count > 0:
        for row in plsgTable.Rows:
            if row["Product_Line_Sub_Group"] not in plsgData:
                plsgData.append(row["Product_Line_Sub_Group"])
    Trace.Write(str(plsgData))
    return plsgData

def getPLSGCTData(plsgData):
    defaultCountry = dict()
    query = "Select PLSG,Country_of_Origin,Is_Default_Country,PL_SubGroup from COUNTRY_OF_ORIGIN_PLSG_MAPPING where PLSG in ('{}') and Is_Default_Country = 'Yes'".format("','".join(plsgData))
    res = SqlHelper.GetList(query)
    if res is not None:
        for row in res:
            defaultCountry[row.PLSG] = [row.Country_of_Origin,row.PL_SubGroup]
    Trace.Write(str(defaultCountry))
    return defaultCountry

if getCfValue("Booking LOB") == "PMC":
    plsgTable = Quote.QuoteTables["Product_Line_Sub_Group_Details"]
    CountryofOriginTable = Quote.QuoteTables["Country_of_Origin"]
    #CountryofOriginTable.Rows.Clear()
    plsgData  = getUniquePLSG(plsgTable)
    defaultCountry = getPLSGCTData(plsgData)
    plsgList = []
    if defaultCountry:
        if CountryofOriginTable.Rows.Count > 0:
            for row in CountryofOriginTable.Rows:
                plsgList.append(row["Product_Line_Sub_Group"])
            for row in CountryofOriginTable.Rows:
                if row["Product_Line_Sub_Group"] not in plsgData:
                    CountryofOriginTable.DeleteRow(row.Id)
        for key in defaultCountry:
            if key not in plsgList:
                addNewRow = CountryofOriginTable.AddNewRow()
                addNewRow["Product_Line_Sub_Group"] = key
                addNewRow["PLSG_Desc"] = str(defaultCountry[key][1])
                addNewRow.SetColumnValue('Country_of_Origin',str(defaultCountry[key][0]))