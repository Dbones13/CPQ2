import GS_APIGEE_Integration_Util

excel_Url, header = GS_APIGEE_Integration_Util.GetR2QAPIGEEAuthDetails()
try:
    QuoteNumber = Param.QuoteNumber
    Quote = QuoteHelper.Edit(QuoteNumber)
    c300 = Quote.GetCustomField('C300 Cabinet Count').Content
    fgs = Quote.GetCustomField('SM FGS Cabinet Count').Content
    esd = Quote.GetCustomField('SM ESD Cabinet Count').Content
    cabinetcheck = False
    Quote.SetGlobal('PerformanceUpload', "Yes")
    for item in Quote.MainItems:
        if item.PartNumber == 'PRJT':
            Product = item.EditConfiguration()
            sysCont = Product.GetContainerByName('CE_SystemGroup_Cont')

            for row in sysCont.Rows:
                '''selected_products = row['Selected_Products']
                if selected_products not in ('C300 System', 'Safety Manager FGS', 'Safety Manager ESD'):
                    break'''

                # Define a mapping for product names, attributes, and values
                product_mappings = {
                    'C300 System': ('C300_Marshalling_cabinet_count (0-500)', c300, 'CE_System_Cont'),
                    'Safety Manager FGS': ('Marshalling_cabinet_count', fgs, 'SM_Labor_Cont'),
                    'Safety Manager ESD': ('Marshalling_cabinet_count', esd, 'SM_Labor_Cont')
                }

                for product_name, (attribute, value, container_name) in product_mappings.items():
                    if product_name and value != '0':  
                        for row1 in row.Product.GetContainerByName('CE_System_Cont').Rows:
                            if row1['Product Name'] == product_name:
                                if product_name == 'C300 System':
                                    row1.Product.Attr(attribute).AssignValue(value)
                                if product_name in ('Safety Manager FGS', 'Safety Manager ESD'):
                                    for sub_row in row1.Product.GetContainerByName(container_name).Rows:
                                        sub_row[attribute] = value
                                cabinetcheck = True
            if cabinetcheck:
                Product.UpdateQuote()
    Log.Info('GS_R2Q_Cabinet_Count Success-->>')
    Quote.SetGlobal('PerformanceUpload', "")
    final_request_body={'QuoteNumber':str(Param.QuoteNumber),'CartId':str(Param.CartId),'RevisionNumber': str(Param.RevisionNumber),'UserName':str(User.UserName),'Module':'New/Expansion','Action':'Update','Status':'Success','Action_List':[{'ActionName':str(Param.ActionName),'ScriptName':'GS_R2Q_Cabinet_Count'}]}
    RestClient.Post(excel_Url, RestClient.SerializeToJson(str(final_request_body)),header)
except Exception as ex:
	Log.Info('GS_R2Q_Cabinet_Count Error-->>'+str(ex))
	final_request_body={'QuoteNumber':str(Param.QuoteNumber),'CartId':str(Param.CartId),'RevisionNumber': str(Param.RevisionNumber),'UserName':str(User.UserName),'Module':'New/Expansion','Action':'Update','Status':'Fail','Action_List':[{'ActionName':str(Param.ActionName),'ScriptName':'GS_R2Q_Cabinet_Count','ErrorMessage':str(ex)}]}
	RestClient.Post(excel_Url, RestClient.SerializeToJson(str(final_request_body)),header)