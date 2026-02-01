headers=[]
rows=[]
report=[]
Model={}
if (Param is not None and Param.tableName is not None):
    Trace.Write(str(Param))
    tableName = Param.tableName
    cartId = Param.cartId
    ownerId = Param.ownerId
    labor_report = Param.Report
    if tableName != '':
        sqlQuery = "Select * From {} WHERE cartId='{}' AND ownerId='{}'"
        sqlQuery = sqlQuery.format(tableName, cartId,ownerId)
        sqlResult = SqlHelper.GetList(sqlQuery)
        if sqlResult is not None:
            for column in sqlResult[0]:
                headers.append(column.Key)
            for row in sqlResult:
                rowData = {}
                for column in row:
                    rowData[column.Key] = str(column.Value)
                rows.append(rowData)
    if labor_report is not None and labor_report != '':
        Quote = QuoteHelper.Edit(int(ownerId),int(cartId))
        getpartsitems =SqlHelper.GetList("SELECT CART_ITEM FROM CART_ITEM  WHERE CATALOGCODE = 'PRJT' AND CART_ID = '"+str(Quote.QuoteId)+"' AND USERID = '"+str(Quote.UserId)+"'")
        rowData = {}
        for item in getpartsitems:
            row=Quote.GetItemByQuoteItem(item.CART_ITEM).SelectedAttributes.GetContainerByName(labor_report).Rows[0].Columns
            for column in row:
                rowData[column.Name] = str(int(column.Value)+int(rowData.get(column.Name) or 0))
            report.append(rowData)
    Model = {"headers":headers,"rows":rows,"laborReport":report}
ApiResponse = ApiResponseFactory.JsonResponse(Model)