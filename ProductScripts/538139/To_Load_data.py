#reference_number1=Quote.GetCustomField("SC_CF_PREVIOUS_QUOTE_NO").Content
SC_Product_Type=Product.Attr('SC_Product_Type').GetValue()

    
if SC_Product_Type=='Renewal':
    reference_number=Quote.GetCustomField("SC_CF_PREVIOUS_QUOTE_NO").Content
    query = SqlHelper.GetFirst("Select Product,ProductDetails from SC_RENEWAL_TABLE where Product = '{}' and QuoteID = '{}'".format("BGP inc Matrikon",reference_number))
    l=[]
    if query is not None:

        var = eval(query.ProductDetails)
        for i in var:
            if i['Type'] == 'ListBoxMultipleSelect' and i["Name"]=="SC_BGP_Serv_Product":
                l.append(i['Value'])
                Product.Attr('Service_product_Test').AssignValue(str(i['Value']))
    summary=Product.GetContainerByName('SC_BGP_Models_Cont')
    summary.Rows.Clear()
    #inValidModelCont = Product.GetContainerByName("SC_BGP_Invalid_Cont")
   # inValidModelCont.Rows.Clear()
    Product.Attr('Service_Product_Test1').AssignValue('Test')