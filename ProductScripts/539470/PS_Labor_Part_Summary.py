#PS_Labor_Part_Summary
Checkproduct = Product.ParseString('<*CTX(Product.RootProduct.PartNumber)*>')
if Checkproduct != "PRJT R2Q":
    if Product.Name == "Digital Video Manager":
        from Update_System_Labor_Cost_Price import updateLaborCostPrice
        Log.Info('Product_name' + str(Product.Name))
        gesLocation = Product.Attr("DVM_GES_Location").GetValue()
        gesMapping = {'GES India':'IN','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','None':'None','GES Egypt':'EG'}
        gesLocationVC = gesMapping.get(gesLocation)
        cont = Product.GetContainerByName('Labor_PriceCost_Cont')
        if Quote:
            contList = ['DVM_Engineering_Labor_Container','DVM_Additional_Labour_Container']
            foEngColumn = {'DVM_Engineering_Labor_Container':'DVM_FOENG','DVM_Additional_Labour_Container':'DVM_Additional_Project_FOENG_Deliverables'}
            updateLaborCostPrice(Product, Quote, TagParserQuote, contList, foEngColumn, gesLocationVC, True, Session)
            cont.Calculate()

        Product.Attr('PERF_ExecuteScripts').AssignValue('')