if sender.PartNumber == "Winest Labor Import" :
    from GS_Display_Warning_Message import Laborwarningmessage

    Quote_Guid = dict()
    quoteTotalTable = Quote.QuoteTables["Quote_Details"]
    if quoteTotalTable.Rows.Count > 0:
        row = quoteTotalTable.Rows[0]
        Quote_Guid = eval(row['Labor_Execution_Year']) if row['Labor_Execution_Year'] != '' else dict()

    validParts = Product.GetContainerByName('Winest Labor Container')
    Guid = TagParserQuote.ParseString('<*CTX( Quote.CurrentItem.CartItemGuid )*>')

    Execution_Year_list = []
    for row in validParts.Rows:
        if row["Execution Year"] != '' and row["Final Hrs"] != '' and float(row["Final Hrs"]) > 0:
            Execution_Year_list.append(row["Execution Year"])

    if quoteTotalTable.Rows.Count > 0 and len(Execution_Year_list) > 0:
        row = quoteTotalTable.Rows[0]
        Quote_Guid[Guid] = (',').join(set(Execution_Year_list))
        row['Labor_Execution_Year'] = str(Quote_Guid)
        Trace.Write("Execution year passed1")
    elif quoteTotalTable.Rows.Count > 0:
        if Guid in Quote_Guid:
            Quote_Guid.pop(Guid)
        row = quoteTotalTable.Rows[0]
        row['Labor_Execution_Year'] = str(Quote_Guid)
    quoteTotalTable.Save()

    Laborwarningmessage(Quote)