#CA_FPWorkSheet_Populate_QTables: This script is called as a pre-action while generating proposal document.
bookingLOB = Quote.GetCustomField("Booking LOB").Content
quoteType = Quote.GetCustomField('Quote Type').Content
if bookingLOB == "PMC" and quoteType in ['Parts and Spot', 'Projects']:
    quote = Quote
    import GS_Populate_WS_Table as gpws
    #import GS_Populate_Optional_FP_ItemsTable as gpof #CXCPQ-46820: commented: 06/02/2023
    import GS_Populate_VASTable as gpvas
    import GS_Populate_FP_ProjSynTables as gpjs
    #import GS_populate_BOMSpares_table as gpbs #CXCPQ-46820: commented: 06/02/2023

    gpws.populateWSTable(quote)
    #gpof.populateOptional(Quote) #CXCPQ-46820: commented: 06/02/2023
    gpvas.populateVAS(quote)
    gpjs.populateProjSynTables(quote)
    #gpbs.populateBOMSpares(Quote) #CXCPQ-46820: commented: 06/02/2023
    #ScriptExecutor.ExecuteGlobal('GS_FP_WORKSHEET_BOM_TAB') #CXCPQ-46820: commented: 06/02/2023
    ScriptExecutor.ExecuteGlobal('GS_Populate_ModelDecodeTable')
