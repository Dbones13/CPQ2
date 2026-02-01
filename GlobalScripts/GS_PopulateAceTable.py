def PopulateAceTable(item,tableInfo):
    if item.QI_Ace_Quote_Number.Value != "":
        query = SqlHelper.GetFirst("Select CpqTableEntryId FROM PMC_ACE_QUOTE WHERE PartNumber='{}' AND AceQuoteReferenceNumber = '{}'".format(str(item.PartNumber),str(item.QI_Ace_Quote_Number.Value)))
        if query is None:
            tablerow = {
                "AceQuoteReferenceNumber" : str(item.QI_Ace_Quote_Number.Value), 
                "AceQuoteDescription" : item.QI_Ace_Description.Value, 
                "PartNumber" : str(item.PartNumber), 
                "FME" : item.QI_FME.Value, 
                "ExtendedDescription" : item.QI_ExtendedDescription.Value, 
                "UnitListPrice" : str(round(item.QI_AceQuote_ListPrice.Value,2))
            }

        else:
            entryID = query.CpqTableEntryId
            tablerow = {
                "CpqTableEntryId": entryID ,
                "AceQuoteReferenceNumber" : str(item.QI_Ace_Quote_Number.Value), 
                "AceQuoteDescription" : item.QI_Ace_Description.Value, 
                "PartNumber" : str(item.PartNumber), 
                "FME" : item.QI_FME.Value, 
                "ExtendedDescription" : item.QI_ExtendedDescription.Value, 
                "UnitListPrice" : str(round(item.QI_AceQuote_ListPrice.Value,2))
            }
        tableInfo.AddRow(tablerow)
        SqlHelper.Upsert(tableInfo)
