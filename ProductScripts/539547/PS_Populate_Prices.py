if Product.Attr('isProductLoaded').GetValue() == 'True' and Product.Attr('CE_Scope_Choices').GetValue() == "HW/SW + LABOR":
    #import sys
    import GS_Labor_Utils
    import GS_Pouplate_UOC_Labor_Price_Cost
    
    checkMPA = GS_Labor_Utils.checkForMPACustomer(Quote, TagParserQuote)
    LOB = Quote.GetCustomField("Booking LOB").Content
    parts_dict = {}
    
    Product.ExecuteRulesOnce = True
    
    #salesOrg = Quote.SelectedMarket.MarketCode.split('_')[0]
    salesOrg = Quote.GetCustomField('Sales Area').Content
    laborCont = Product.GetContainerByName('SCADA_Engineering_Labor_Container')
    row0 = laborCont.Rows[0]
    fo_dict = dict()
    fo_ld = row0.Product.Attr('SCADA_Labor_FO_Eng')
    fo_dict = GS_Pouplate_UOC_Labor_Price_Cost.buildDict(fo_ld)
    
    for row in laborCont.Rows:
        #salesOrg = GS_Labor_Utils.getSalesOrg(row['Execution Country'])
        try:
            parts_dict = GS_Pouplate_UOC_Labor_Price_Cost.populateListPrice(Quote,row, salesOrg, LOB, parts_dict,TagParserQuote, fo_dict, Session)
        except Exception,e:
            msg = "Error when Calculating ListPice: {0}, Line Number: {1}".format(e, exc_traceback.tb_next.tb_lineno)
            Product.ErrorMessages.Add(msg)
            Trace.Write(msg)
        try:
            parts_dict = GS_Pouplate_UOC_Labor_Price_Cost.populateCost(Quote, row, parts_dict, fo_dict)
            if checkMPA:
                parts_dict = GS_Pouplate_UOC_Labor_Price_Cost.populate_MPA_Price(row, Product, Quote, parts_dict, fo_dict)
        except Exception,e:
            msg = "Error when Calculating Pricing Error: {0}, Line Number: {1}".format(e, exc_traceback.tb_lineno)
            Product.ErrorMessages.Add(msg)
            Trace.Write(msg)
    laborCont.Calculate()
 
    laborCont_custom = Product.GetContainerByName('SCADA_Additional_Custom_Deliverables_Container')
    row0 = laborCont_custom.Rows[0]
    fo_dict = dict()
    fo_ld = row0.Product.Attr('SCADA_Labor_FO_Eng')
    fo_dict = GS_Pouplate_UOC_Labor_Price_Cost.buildDict(fo_ld)
    
    for row in laborCont_custom.Rows:
        #salesOrg = GS_Labor_Utils.getSalesOrg(row['Execution Country'])
        try:
            parts_dict = GS_Pouplate_UOC_Labor_Price_Cost.populateListPrice(Quote,row, salesOrg, LOB, parts_dict,TagParserQuote, fo_dict, Session)
        except Exception,e:
            msg = "Error when Calculating ListPice: {0}, Line Number: {1}".format(e, exc_traceback.tb_next.tb_lineno)
            Product.ErrorMessages.Add(msg)
            Trace.Write(msg)
        try:
            parts_dict = GS_Pouplate_UOC_Labor_Price_Cost.populateCost(Quote, row, parts_dict, fo_dict)
            if checkMPA:
                parts_dict = GS_Pouplate_UOC_Labor_Price_Cost.populate_MPA_Price(row, Product, Quote, parts_dict, fo_dict)
        except Exception,e:
            msg = "Error when Calculating Pricing Error: {0}, Line Number: {1}".format(e, exc_traceback.tb_lineno)
            Product.ErrorMessages.Add(msg)
            Trace.Write(msg)
    laborCont_custom.Calculate()
    if '' in parts_dict.keys():
        del parts_dict['']
    Product.ExecuteRulesOnce = False
    Trace.Write("parts_dict------>"+str(parts_dict))
    GS_Labor_Utils.populatePriceCost(Product, parts_dict)
    Product.GetContainerByName('Labor_PriceCost_Cont').Calculate()