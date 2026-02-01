#PS_PLC_Calculate_Labor_Hours
Checkproduct = Product.ParseString('<*CTX(Product.RootProduct.PartNumber)*>')
if Checkproduct != "PRJT R2Q":
    if Product.Attr('isProductLoaded').GetValue() == 'True':
        Log.Info(str(Quote.GetCustomField("Booking LOB").Content))
        # PLC Labor Container Populate - NEW
        import GS_Labor_Engineering_Calcs, GS_Labor_Functional_Calcs, GS_Labor_Procure_Calcs, GS_Labor_Detail_Calcs, GS_Labor_Procedure_Calcs, GS_Labor_Hardware_Calcs, GS_Labor_Software_Calcs, GS_Labor_Integration_Calcs, GS_Labor_Factory_Calcs, GS_Labor_Installation_Calcs, GS_Labor_Acceptance_Calcs, GS_Labor_Cutover_Calcs, GS_Labor_Operation_Calcs, GS_Labor_Training_Calcs, GS_Labor_Close_Calcs
        import GS_PLC_Labor_Parameters
        import GS_Labor_Utils

        checkMPA = GS_Labor_Utils.checkForMPACustomer(Quote, TagParserQuote)
        laborCont = Product.GetContainerByName('CE PLC Engineering Labor Container')
        Booking_LOB = TagParserQuote.ParseString('<* QuoteProperty (Booking LOB) *>')
        Query=''
        if Booking_LOB=="LSS":
            Query='select Deliverable,Calculated_Hrs,LSS_GES_Eng_NoGES as GES_Eng_NoGES,LSS_GES_Eng_GES as GES_Eng_GES,LSS_FO_Eng_1 as FO_Eng_1,LSS_FO1_Eng_NoGES as FO1_Eng_NoGES,LSS_FO1_Eng_GES as FO1_Eng_GES,LSS_FO_Eng_2 as FO_Eng_2,LSS_FO2_Eng_NoGES as FO2_Eng_NoGES,LSS_FO2_Eng_GES as FO2_Eng_GES,Rank,Execution_Country from CE_PLC_Engineering_Deliverables'
        else:
            Query='select Deliverable,Calculated_Hrs,GES_Eng_NoGES,GES_Eng_GES,FO_Eng_1,FO1_Eng_NoGES,FO1_Eng_GES,FO_Eng_2,FO2_Eng_NoGES,FO2_Eng_GES,Rank,Execution_Country from CE_PLC_Engineering_Deliverables'
        tableLabor = SqlHelper.GetList(Query)
        calc_name_dict = {} #This is a mapping of deliverable name to script calculation name
        for x in tableLabor:
            calc_name_dict[x.Deliverable] = x.Calculated_Hrs
        try:
            attrs = GS_PLC_Labor_Parameters.AttrStorage(Product)
        except Exception,e:
            attrs = None
            Product.ErrorMessages.Add("Error when Cacluating PLC System Labor Parameters: " + str(e))
            Trace.Write("Error when Cacluating PLC System Labor Parameters: " + str(e))
            Log.Error("Error when Cacluating PLC System Labor Parameters: " + str(e))
        if attrs:
            LOB = Quote.GetCustomField("Booking LOB").Content
            try:
                Pricebook1, Pricebook2 = GS_Labor_Utils.getPriceBookName(Quote)
                Trace.Write("PB1 {} :: PB2 {}".format(Pricebook1, Pricebook2))
            except:
                msg = 'No Pricebook found on Quote for labor calculations.'
                Product.ErrorMessages.Add(msg)
                Trace.Write(msg)
                Log.Info(msg)
                Pricebook1 = Pricebook2 = None
            parts_dict = {}
            for row in laborCont.Rows:
                calc_name = calc_name_dict[row.GetColumnByName("Deliverable").Value]
                Trace.Write("calc name: {0}".format(calc_name))
                if row.GetColumnByName("Deliverable").Value != 'CE PLC Customer Training' and row.GetColumnByName("Deliverable").Value != 'CE PLC Cut Over Procedure':
                    try:
                        row.GetColumnByName("Calculated Hrs").Value = str(getattr(globals()[calc_name], calc_name)(attrs)) #dynamically calls the function within the calculation module
                    except Exception,e:
                        msg = "Error when Calculating Hours for: {0}, Error: {1}".format(calc_name, e)
                        Product.ErrorMessages.Add(msg)
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
                    Product.ErrorMessages.Add(msg)
                    Trace.Write(msg)
                try:
                    parts_dict = GS_Labor_Utils.populateListPrice(Quote,row, salesOrg, LOB, parts_dict,TagParserQuote,Session)
                except Exception,e:
                    msg = "Error when Calculating ListPice: {0}".format(e)
                    Product.ErrorMessages.Add(msg)
                    Trace.Write(msg)

            #Price/Cost calculations for custom deliverables
            laborCont_custom = Product.GetContainerByName('CE PLC Additional Custom Deliverables')
            for row in laborCont_custom.Rows:
                salesOrg = GS_Labor_Utils.getSalesOrg(row['Execution Country'])
                try:
                    parts_dict = GS_Labor_Utils.populateCost(Quote, row, parts_dict)
                    if checkMPA:
                        parts_dict = GS_Labor_Utils.populate_MPA_Price(row, Product, Quote, parts_dict)
                except Exception,e:
                    msg = "Error when Additional Custom Deliverables Calculating Pricing Error: {0}".format(e)
                    Product.ErrorMessages.Add(msg)
                try:
                    parts_dict = GS_Labor_Utils.populateListPrice(Quote,row, salesOrg, LOB, parts_dict,TagParserQuote,Session)
                except Exception,e:
                    msg = "Error when Additional Custom Deliverables Calculating ListPice: {0}".format(e)
                    Product.ErrorMessages.Add(msg)
                    Trace.Write(msg)
            laborCont_custom.Calculate()

            Trace.Write("parts_dict: {0}".format(parts_dict))
            Trace.Write("-parts_dict-->"+str(parts_dict))
            GS_Labor_Utils.populatePriceCost(Product, parts_dict)
            cont_name = "Labor_PriceCost_Cont"
            cont = Product.GetContainerByName(cont_name)
            Trace.Write("row count : - {}".format(cont.Rows.Count))
            Trace.Write("AI-> {0}, AO-> {1}, DI-> {2}, DO-> {3}".format(attrs.AI, attrs.AO, attrs.DI, attrs.DO))
            #C = attrs.AI + attrs.AO + attrs.DI + attrs.DO
            #if C > 5000:
                #Product.Messages.Add('Hours for Engineering Plan needs to be entered manually for more than 5000 IOs. (Read item info for more detail)')
                
                
'''if Product.Attr("CE_Scope_Choices").GetValue() == 'HW/SW':
    Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Hidden) )*>'.format('PLC_Labour_Details','PLC_Process_Type'))
elif Product.Attr("CE_Scope_Choices").GetValue() == 'HW/SW + LABOR':
    Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Editable) )*>'.format('PLC_Labour_Details','PLC_Process_Type'))'''

if Checkproduct == "PRJT":
    Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Hidden) )*>'.format('PLC_Labour_Details','PLC_Process_Type'))
else:
    Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Hidden) )*>'.format('PLC_Labour_Details','PLC_Number_of_Sequences'))
    Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Hidden) )*>'.format('PLC_Labour_Details','PLC_3rd_Party_Communication_Signals'))
    Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Hidden) )*>'.format('PLC_Labour_Details','PLC_Hardware_Design_Drawing_Complexity'))
    if Product.Attr("CE_Scope_Choices").GetValue() == 'HW/SW':
        Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Hidden) )*>'.format('PLC_Labour_Details','PLC_Process_Type'))
    elif Product.Attr("CE_Scope_Choices").GetValue() == 'HW/SW + LABOR':
        Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Editable) )*>'.format('PLC_Labour_Details','PLC_Process_Type'))