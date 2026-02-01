final_rows=[]
headers = []
rows = []
bookingLOB = Quote.GetCustomField("Booking LOB").Content
quoteType = Quote.GetCustomField("Quote Type").Content
userBelongs = User.BelongsToPermissionGroup('Estimator-ProsGuidanceAccess')
#Param = {"tableName":"EGAP_Revenue_Margin", "isQuoteTable":True,"condition":""}
if (Param is not None and Param.tableName is not None):
    tableName = Param.tableName
    isQuoteTable = Param.isQuoteTable
    if tableName == 'EGAP_Revenue_Margin':
        headers = ['','Quote Currency','USD Currency']
    if isQuoteTable:
        quoteTable = Quote.QuoteTables[tableName]
        if quoteTable.Rows.Count > 0:
            '''firstRow = quoteTable.Rows[0]
            for cell in firstRow.Cells:
                headers.append(cell.ColumnName)'''
            for row in quoteTable.Rows:
                rowData = {}
                for cell in row.Cells:
                    columnValue = row[cell.ColumnName]
                    if tableName == 'EGAP_Revenue_Margin':
                        info_note = "&nbsp;<span class="tooltip-trigger" data-bind=" tooltip: { title: 'Calculated based on Walk-away Sell Price', placement: 'top auto' }"><a href="#" title="Calculated based on Walk-away Sell Price"  class="sap-icon"><span>&#xe289;</span></a></span>"
                        if columnValue in ['Regional Margin', 'Regional Margin %', 'WTW Margin','WTW Margin %']:
                            columnValue = columnValue + info_note
                            #Trace.Write(columnValue)
                    rowData[cell.ColumnName] = columnValue
                    #Trace.Write("{}:{}".format(cell.ColumnName,rowData[cell.ColumnName]))
                rows.append(rowData)
    	#Trace.Write("------rows {}".format(rows))
		final_rows = rows[:]
		'''if userBelongs==False or quoteType!='Projects' or bookingLOB not in ['LSS','PAS','HCP','CCC']:
			for indx in range(len(rows)):
				if rows[indx]['EGAP_Field_Details']=='PROS Recommended Price':
					final_rows.pop(indx)
		else:
			pass'''

		#Trace.Write("------rows-updated {}".format(final_rows))

    else:
        pass
        '''condition = Param.condition.strip()
        sqlQuery = "Select * From {} {}"
        sqlQuery = sqlQuery.format(tableName, condition)
        sqlResult = SqlHelper.GetList(sqlQuery)
        if sqlResult is not None:
            for column in list[0]:
                headers.append(column.Key)
            for row in sqlResult:
                rowData = {}
                for column in row:
                    rowData[column.Key] = str(column.Value)
                rows.append(rowData)'''
Model = {"headers":headers,"rows":final_rows}
ApiResponse = ApiResponseFactory.JsonResponse(Model)