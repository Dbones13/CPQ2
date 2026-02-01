if Product.Attr('isProductLoaded').GetValue() == 'True':
    import GS_Labor_Utils
    import GS_Pouplate_UOC_Labor_Price_Cost

    checkMPA = GS_Labor_Utils.checkForMPACustomer(Quote, TagParserQuote)
    LOB = Quote.GetCustomField("Booking LOB").Content
    salesOrg = Quote.SelectedMarket.MarketCode.split('_')[0]
    parts_dict = {}

    Product.ExecuteRulesOnce = True

    laborCont = Product.GetContainerByName('System_Network_Engineering_Labor_Container')
    row0 = laborCont.Rows[0]
    fo_dict = dict()
    fo_ld = row0.Product.Attr('Additional_CustomDev_FO_Eng')
    fo_dict = GS_Pouplate_UOC_Labor_Price_Cost.buildDict(fo_ld)

    for row in laborCont.Rows:
        #salesOrg = GS_Labor_Utils.getSalesOrg(row['Execution Country'])
        try:
            parts_dict = GS_Pouplate_UOC_Labor_Price_Cost.populateListPrice(Quote,row, salesOrg, LOB, parts_dict,TagParserQuote, fo_dict)
        except Exception,e:
            msg = "Error when Calculating ListPice: {0}".format(e)
            Product.ErrorMessages.Add(msg)
            Trace.Write(msg)
        try:
            parts_dict = GS_Pouplate_UOC_Labor_Price_Cost.populateCost(Quote, row, parts_dict, fo_dict)
            if checkMPA:
                parts_dict = GS_Pouplate_UOC_Labor_Price_Cost.populate_MPA_Price(row, Product, Quote, parts_dict, fo_dict)
        except Exception,e:
            msg = "Error when Calculating Pricing Error: {0}".format(e)
            Product.ErrorMessages.Add(msg)
            Trace.Write(msg)
    laborCont.Calculate()

    laborContSIE = Product.GetContainerByName('System_Interface_Engineering_Labor_Container')
    for row in laborContSIE.Rows:
        #salesOrg = GS_Labor_Utils.getSalesOrg(row['Execution Country'])
        try:
            parts_dict = GS_Pouplate_UOC_Labor_Price_Cost.populateListPrice(Quote,row, salesOrg, LOB, parts_dict,TagParserQuote, fo_dict)
        except Exception,e:
            msg = "Error when Calculating ListPice: {0}".format(e)
            Product.ErrorMessages.Add(msg)
            Trace.Write(msg)
        try:
            parts_dict = GS_Pouplate_UOC_Labor_Price_Cost.populateCost(Quote, row, parts_dict, fo_dict)
            if checkMPA:
                parts_dict = GS_Pouplate_UOC_Labor_Price_Cost.populate_MPA_Price(row, Product, Quote, parts_dict, fo_dict)
        except Exception,e:
            msg = "Error when Calculating Pricing Error: {0}".format(e)
            Product.ErrorMessages.Add(msg)
            Trace.Write(msg)
    laborContSIE.Calculate()

    laborContHEL = Product.GetContainerByName('Hardware Engineering Labour Container')
    for row in laborContHEL.Rows:
        #salesOrg = GS_Labor_Utils.getSalesOrg(row['Execution Country'])
        try:
            parts_dict = GS_Pouplate_UOC_Labor_Price_Cost.populateListPrice(Quote,row, salesOrg, LOB, parts_dict,TagParserQuote, fo_dict)
        except Exception,e:
            msg = "Error when Calculating ListPice: {0}".format(e)
            Product.ErrorMessages.Add(msg)
            Trace.Write(msg)
        try:
            parts_dict = GS_Pouplate_UOC_Labor_Price_Cost.populateCost(Quote, row, parts_dict, fo_dict)
            if checkMPA:
                parts_dict = GS_Pouplate_UOC_Labor_Price_Cost.populate_MPA_Price(row, Product, Quote, parts_dict, fo_dict)
        except Exception,e:
            msg = "Error when Calculating Pricing Error: {0}".format(e)
            Product.ErrorMessages.Add(msg)
            Trace.Write(msg)
    laborContHEL.Calculate()

    laborCont = Product.GetContainerByName('HMI_Engineering_Labor_Container')
    row0 = laborCont.Rows[0]
    fo_dict = dict()
    fo_ld = row0.GetColumnByName("FO Eng 1").ReferencingAttribute
    fo_dict = GS_Pouplate_UOC_Labor_Price_Cost.buildDict(fo_ld)

    for row in laborCont.Rows:
        #salesOrg = GS_Labor_Utils.getSalesOrg(row['Execution Country'])
        try:
            parts_dict = GS_Pouplate_UOC_Labor_Price_Cost.populateListPrice(Quote,row, salesOrg, LOB, parts_dict,TagParserQuote, fo_dict)
        except Exception,e:
            msg = "Error when Calculating ListPice for HMI: {0}".format(e)
            Product.ErrorMessages.Add(msg)
            Trace.Write(msg)
        try:
            parts_dict = GS_Pouplate_UOC_Labor_Price_Cost.populateCost(Quote, row, parts_dict, fo_dict)
            if checkMPA:
                parts_dict = GS_Pouplate_UOC_Labor_Price_Cost.populate_MPA_Price(row, Product, Quote, parts_dict, fo_dict)
        except Exception,e:
            msg = "Error when Calculating Pricing Error for HMI: {0}".format(e)
            Product.ErrorMessages.Add(msg)
            Trace.Write(msg)
    laborCont.Calculate()

    laborCont = Product.GetContainerByName('Additional_CustomDev_Labour_Container')
    row0 = laborCont.Rows[0]
    fo_dict = dict()
    fo_ld = row0.GetColumnByName("FO Eng").ReferencingAttribute
    fo_dict = GS_Pouplate_UOC_Labor_Price_Cost.buildDict(fo_ld)

    for row in laborCont.Rows:
        #salesOrg = GS_Labor_Utils.getSalesOrg(row['Execution Country'])
        try:
            parts_dict = GS_Pouplate_UOC_Labor_Price_Cost.populateListPrice(Quote,row, salesOrg, LOB, parts_dict,TagParserQuote, fo_dict)
        except Exception,e:
            msg = "Error when Calculating ListPice for Additional Custom Deliverable: {0}".format(e)
            Product.ErrorMessages.Add(msg)
            Trace.Write(msg)
        try:
            parts_dict = GS_Pouplate_UOC_Labor_Price_Cost.populateCost(Quote, row, parts_dict, fo_dict)
            if checkMPA:
                parts_dict = GS_Pouplate_UOC_Labor_Price_Cost.populate_MPA_Price(row, Product, Quote, parts_dict, fo_dict)
        except Exception,e:
            msg = "Error when Calculating Pricing Error for Additional Custom Deliverable: {0}".format(e)
            Product.ErrorMessages.Add(msg)
            Trace.Write(msg)
    laborCont.Calculate()

    if '' in parts_dict.keys():
        del parts_dict['']
    Product.ExecuteRulesOnce = False
    GS_Labor_Utils.populatePriceCost(Product, parts_dict)