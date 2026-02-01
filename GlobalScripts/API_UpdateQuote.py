data         = RestClient.DeserializeJson(RequestContext.Body)
Log.Write(str(data))
if data is not None:
    if data["ProjectId"] is not None and data["ReleaseFlag"] is None:
        Log.Write("productID present")
        Quote.GetCustomField("CF_ProjectId").Content = str(data["ProjectId"])
        Quote.Save(False)
        query = SqlHelper.GetFirst("Select max(CpqTableEntryId)as x from PROJECTCREATION_BOOKING_IDHOCS where QuoteNumber = '{}'".format(Quote.CompositeNumber))
        tableId = query.x
        tableInfo = SqlHelper.GetTable("PROJECTCREATION_BOOKING_IDHOCS")
        tablerow = { "CpqTableEntryId" :tableId, "SAPProjectID" :str(data["ProjectId"])}
        tableInfo.AddRow(tablerow)
        upsertResult = SqlHelper.Upsert(tableInfo)
    #Code change for Order Booking - H122094 - Start Here
                                                             
    if data["Status"] is not None and data["ReleaseFlag"] is None:
        Quote.ChangeQuoteStatus(str(data["Status"]))
        if str(data["Status"]) == 'Project Created' and Quote.GetCustomField("CF_ProjectId").Content != "":
            # QuoteHelper.Edit(Quote.CompositeNumber)
            ActIdQry = SqlHelper.GetFirst("SELECT ACTION_ID FROM ACTIONS WHERE ACTION_NAME = 'Place order to ERP' ")
            try:
                Log.Write("Try Block exec")
                Quote.ExecuteAction(ActIdQry.ACTION_ID)
            except Exception as e:
                Log.Write("except Block exec=>"+str(e.message)+':'+str(e.args))
                Quote.GetCustomField("Q_CF_PROJFLAG").Content = "TRUE"
        else:
			Quote.Messages.Add(Translation.Get('message.ProjectIDnotset'))
        Quote.Save(False)
      #Code change for Order Booking - H122094 - End Here
    if data["ReleaseFlag"] is not None and data["ProjectId"] is not None:
        Log.Write("inside release flag1")
        query = SqlHelper.GetFirst("select QuoteNumber from PROJECTCREATION_BOOKING_IDHOCS where SAPProjectID = '{}'".format(data["ProjectId"]))
        if query is not None and query.QuoteNumber != '':
            Log.Write("inside release flag2")
            quote = QuoteHelper.Edit(query.QuoteNumber)
            quote.GetCustomField("Project_Release_Flag").Content = str(data["ReleaseFlag"])
            quote.Save(False)
ScriptExecutor.Execute('CPQ_SF_CreateUpdateOpportunity')