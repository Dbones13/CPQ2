if Product.Attr('isProductLoaded').GetValue() == 'True':
    # PMD Labor Container Populate - NEW
    import GS_Labor_Engineering_Calcs, GS_Labor_Functional_Calcs, GS_Labor_Procure_Calcs, GS_Labor_Detail_Calcs, GS_Labor_Procedure_Calcs, GS_Labor_Hardware_Calcs, GS_Labor_Software_Calcs, GS_Labor_Integration_Calcs, GS_Labor_Factory_Calcs, GS_Labor_Installation_Calcs, GS_Labor_Acceptance_Calcs, GS_Labor_Cutover_Calcs, GS_Labor_Operation_Calcs, GS_Labor_Training_Calcs, GS_Labor_Close_Calcs
    import GS_PMD_ReadAttrs
    import GS_PMD_Labor_Parameters
    import GS_Labor_Utils

    checkMPA = GS_Labor_Utils.checkForMPACustomer(Quote, TagParserQuote)

    call_module = GS_Labor_Utils
    get_attrs = GS_PMD_ReadAttrs.AttrStorage(Product)
    laborCont = Product.GetContainerByName('PMD Engineering Labor Container')
    tableLabor = SqlHelper.GetList('select * from CE_PMD_ENGINEERING_DELIVERABLES')
    calc_name_dict = {} #This is a mapping of deliverable name to script calculation name
    for x in tableLabor:
        calc_name_dict[x.Deliverable] = x.Calculated_Hrs
    try:
        attrs = GS_PMD_Labor_Parameters.AttrStorage(Product, get_attrs)
    except Exception,e:
        attrs = None
        Product.Messages.Add("Error when Cacluating PMD System Labor Parameters: " + str(e))
        Trace.Write("Error when Cacluating PMD System Labor Parameters: " + str(e))
        Log.Error("Error when Cacluating PMD System Labor Parameters: " + str(e))
    if attrs:
        LOB = Quote.GetCustomField("Booking LOB").Content
        try:
            Pricebook1, Pricebook2 = GS_Labor_Utils.getPriceBookName(Quote)
            Trace.Write("PB1 {} :: PB2 {}".format(Pricebook1, Pricebook2))
        except:
            msg = 'No Pricebook found on Quote for labor calculations.'
            Product.Messages.Add(msg)
            Trace.Write(msg)
            Log.Info(msg)
            Pricebook1 = Pricebook2 = None
        parts_dict = {}
        for row in laborCont.Rows:
            calc_name = calc_name_dict[row.GetColumnByName("Deliverable").Value]
            Trace.Write("calc name: {0}".format(calc_name))
            if row.GetColumnByName("Deliverable").Value not in ['PMD Customer Training', 'CE PLC Cut Over Procedure']:
                try:
                    row.GetColumnByName("Calculated Hrs").Value = str(getattr(globals()[calc_name], calc_name)(attrs)) #dynamically calls the function within the calculation module
                except Exception,e:
                    msg = "Error when Calculating Hours for: {0}, Error: {1}".format(calc_name, e)
                    Product.Messages.Add(msg)
                    Trace.Write(msg)
                    Log.Error(msg)

            #Begin labor Price/Cost calculations
            salesOrg = GS_Labor_Utils.getSalesOrg(row['Execution Country'])
            try:
                parts_dict = GS_Labor_Utils.populateCost(Quote, row, parts_dict)
                if checkMPA:
                    parts_dict = GS_Labor_Utils.populate_MPA_Price(row, Product, Quote, parts_dict)
            except Exception,e:
                msg = "Error when Calculating Pricing Error: {0}".format(e)
                Product.Messages.Add(msg)
                Trace.Write(msg)
            try:
                parts_dict = GS_Labor_Utils.populateListPrice(Quote,row, salesOrg, LOB, parts_dict,TagParserQuote)
            except Exception,e:
                msg = "Error when Calculating ListPice: {0}".format(e)
                Product.Messages.Add(msg)
                Trace.Write(msg)

        #Price/Cost calculations for custom deliverables
        laborCont_custom = Product.GetContainerByName('PMD Labor Additional Custom Deliverable')
        for row in laborCont_custom.Rows:
            salesOrg = GS_Labor_Utils.getSalesOrg(row['Execution Country'])
            try:
                parts_dict = GS_Labor_Utils.populateCost(Quote, row, parts_dict)
                if checkMPA:
                    parts_dict = GS_Labor_Utils.populate_MPA_Price(row, Product, Quote, parts_dict)
            except Exception,e:
                msg = "Error when Additional Custom Deliverables Calculating Pricing Error: {0}".format(e)
                Product.Messages.Add(msg)
            try:
                parts_dict = GS_Labor_Utils.populateListPrice(Quote,row, salesOrg, LOB, parts_dict,TagParserQuote)
            except Exception,e:
                msg = "Error when Additional Custom Deliverables Calculating ListPice: {0}".format(e)
                Product.Messages.Add(msg)
                Trace.Write(msg)
        laborCont_custom.Calculate()

        Trace.Write("parts_dict: {0}".format(parts_dict))
        GS_Labor_Utils.populatePriceCost(Product, parts_dict)