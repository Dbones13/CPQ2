#import GS_APIGEE_Integration_Util

#Generate the document, BOM and send it to SFDC
if Quote.GetCustomField("R2Q_Save").Content == "Submit":
    import GS_APIGEE_Integration_Util
    import GS_R2Q_FunctionalUtil
    import GS_Populate_PAS_DocumentTable
    import GS_PAS_Pricing_Summary
    import GS_CyberGenerateDocument
    import GS_R2Q_Migration_BOM_Parts
    import GS_R2Q_DocumentTable_PLC
    import time
    try:
        checkCount =SqlHelper.GetFirst("SELECT count(*) as cnt FROM CART_ITEM  where  (CATALOGCODE LIKE 'hps_%' OR CATALOGCODE LIKE 'SVC_%')   and cost = 0 and CART_ID = '"+str(Quote.QuoteId)+"' AND USERID = '"+str(Quote.UserId)+"'")
        if checkCount.cnt==0:
            Log.Info("document generation started")
            approval =  Quote.GetCustomField("EGAP_Highest_Approval_Level_for_the_Quote").Content
            Log.Info("approval----> " +str(approval))
            saveAction = Quote.GetCustomField("R2Q_Save").Content
            if Quote.GetCustomField('Honeywell Entity Name').Content == '':
                bookingCountry = Quote.GetCustomField("Booking Country").Content
                query = "select Entity_Name,Default_Entity from Country_Entity_Mapping where Country='{}'".format(bookingCountry)
                res = SqlHelper.GetList(query)
                if res:
                    #Log.Info("res[0].Default_Entity" + str(res[0].Default_Entity))
                    Quote.CustomFields.SelectValueByValueCode("Honeywell Entity Name" , res[0].Default_Entity)
                    Quote.CustomFields.DisallowAllValuesExceptByValueCodes("Honeywell Entity Name" , Array[type('str')]([r.Entity_Name for r in res]))
            #Insert data to quote table and generate documents and excel
            Product_flag = ''
            Messagetext = ''
            lisy_plc_uoc=["ControlEdge UOC System Migration","ControlEdge PLC System Migration","CE PLC Control Group","UOC Control Group","CE PLC Remote Group","UOC Remote Group"]
            # Initializing Data for Third party PLC/UOC product
            final_msidAttributeDict = dict()
            final_RacksList = dict()
            final_unitlist_cg = dict()
            final_unitlist_rg = dict()
            uoc_unit = 0
            plc_unit = 0
            last_plc_unit_name = ""
            last_uoc_unit_name = ""
            plc_control_group_name = ""
            uoc_control_group_name = ""
            migration_quote_table_update = False
            
            for item in Quote.MainItems:
                GS_R2Q_Migration_BOM_Parts.sellprice_proposal(item,Quote)
                if item.ProductName in lisy_plc_uoc:
                    GS_R2Q_Migration_BOM_Parts.thirdpartyprop(item,Quote)
                    msidAttributeDict, RacksList, unitlist_cg, unitlist_rg, uoc_unit, plc_unit, last_plc_unit_name, last_uoc_unit_name, plc_control_group_name, uoc_control_group_name = GS_R2Q_DocumentTable_PLC.thirdparty_units(item,Quote,uoc_unit,plc_unit,last_plc_unit_name,last_uoc_unit_name,plc_control_group_name,uoc_control_group_name)
                    final_msidAttributeDict.update(msidAttributeDict)
                    final_RacksList.update(RacksList)
                    final_unitlist_cg.update(unitlist_cg)
                    final_unitlist_rg.update(unitlist_rg)
                    migration_quote_table_update = True
                #GS_R2Q_DocumentTable_PLC.thirdparty_units(item,Quote)
                #Log.Info("Execution of GS_R2Q_DocumentTable_PLC End")
                if str(item.ParentRolledUpQuoteItem) == '' and str(item.PartNumber) =='CYBER':
                    Product_flag = 'Cyber'
                    break
                elif str(item.ParentRolledUpQuoteItem) == '' and str(item.PartNumber).find('HCI') != -1:
                    Product_flag = 'HCI'
                elif item.ProductName == "MSID_New":
                    Product_flag = 'Migration'
                    GS_R2Q_Migration_BOM_Parts.bom_migration(item,Quote)
            # Populating Data of Third party PLC/UOC product to Quote Table
            if migration_quote_table_update:
                table = Quote.QuoteTables["Migration_Document_Data"]
                if final_RacksList:
                    GS_R2Q_DocumentTable_PLC.populateQuoteTable(final_RacksList, table)
                if final_unitlist_cg:
                    GS_R2Q_DocumentTable_PLC.populateQuoteTable_groupdata(final_unitlist_cg, table, "cg_group")
                if final_unitlist_rg:
                    GS_R2Q_DocumentTable_PLC.populateQuoteTable_groupdata(final_unitlist_rg, table, "rg_group")
                table.Save()

            if str(Product_flag) =='Cyber':
                #response = RestClient.Get("https://non-existing-url.com")
                GS_CyberGenerateDocument.cyber_proposal(Quote)
                templateName = 'R2Q Cyber Budgetary Proposal'
            elif str(Product_flag) =='HCI':
                language_dict = {
                    "English": "102",
                    "Spanish": "107"
                }

                # Retrieve the content of the "Language" custom field
                qt_lang = Quote.GetCustomField("R2Q_PRJT_Proposal Language").Content
                # Set the "Customer's Language" custom field based on the lookup
                Quote.GetCustomField("Customer's Language").Content = language_dict.get(qt_lang, language_dict['English'])
                ScriptExecutor.Execute('GS_HCI_Firm_and_Budgetary_Report')
                templateName = 'R2Q HCI Budgetary Proposal'
            else:
                language_dict = {
                    "English": "102",
                    "French": "108",
                    "German": "103",
                    "Spanish": "107",
                    "Portuguese": "106",
                    "Korean": "105",
                    "Chinese": "104"
                }

                # Retrieve the content of the "Language" custom field
                qt_lang = Quote.GetCustomField("R2Q_PRJT_Proposal Language").Content
                # Set the "Customer's Language" custom field based on the lookup
                Quote.GetCustomField("Customer's Language").Content = language_dict.get(qt_lang, language_dict['English'])
                GS_PAS_Pricing_Summary.PAS_Pricing_Summary(Quote,TagParserQuote)
                GS_Populate_PAS_DocumentTable.PAS_DocumentTable(Quote,TagParserQuote)
                #Log.Info("document Honeywell Entity--->"+str(Quote.GetCustomField('Honeywell Entity Name').Content)+"<------Proposal Validity------>"+str(Quote.GetCustomField('Proposal Validity').Content))
                if str(Product_flag) == 'Migration':
                    templateName = 'R2Q Migration (Multilanguage)'

                else:
                    templateName = 'R2Q New/Expansion Project'
            #if approval in ['','NA','0','No Approval']:
            APIGEEHeader=GS_APIGEE_Integration_Util.GetAPIGEEAuthHeader()
            APIGEEURL=GS_APIGEE_Integration_Util.GetAPIGEEBaseURL()
            APIGEEDocurl='{APIGEEURL}/hps/cpq/proposal-doc/v1/get-attachment'.format(APIGEEURL = str(APIGEEURL))

            #Fetch QuoteID from APIGEE
            cartId = Quote.QuoteId
            ownerId = Quote.UserId
            APIGEEQuoteURL="{APIGEEURL}/hps/cpq/line-items/{ver}/get-line-item?q=select+Id+from+Quote+where+Quote_ID__c={cartId}+and+Owner_ID__c={ownerId}".format(APIGEEURL = str(APIGEEURL), ver = "v1",cartId = str(cartId),ownerId = str(ownerId))
            quoteID=RestClient.Get(APIGEEQuoteURL,APIGEEHeader)
            if len(quoteID.records) != 0:
                for q in quoteID.records:
                    SFQuoteID = str(q.Id)

            #Generate pdf document
            pdf_doc=Quote.GenerateDocument(templateName,GenDocFormat.PDF)
            if approval in ['','NA','0','No Approval']:
                pdfName=Quote.GetLatestGeneratedDocumentFileName()
                PdfBytes=Quote.GetLatestGeneratedDocumentInBytes()
                pdf_64bit=Convert.ToBase64String(PdfBytes)
                parampdf={'ParentId' : SFQuoteID ,'Name' : pdfName, 'body' : pdf_64bit,'ContentType': 'application/pdf'}
                pdfPost=RestClient.Post(APIGEEDocurl,parampdf,APIGEEHeader)

            #Generate docx document
            docx_doc=Quote.GenerateDocument(templateName,GenDocFormat.DOCX)
            if approval in ['','NA','0','No Approval']:
                docName=Quote.GetLatestGeneratedDocumentFileName()
                docBytes=Quote.GetLatestGeneratedDocumentInBytes()
                doc_64bit=Convert.ToBase64String(docBytes)
                paramdoc={'ParentId' : SFQuoteID ,'Name' : docName, 'body' : doc_64bit,'ContentType': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'}
                docpost=RestClient.Post(APIGEEDocurl,paramdoc,APIGEEHeader)


            Messagetext = ''
            if approval in ['','NA','0','No Approval']:
                if str(Product_flag) in ['Migration','Cyber','HCI']:
                    product_type_map = {"Honeywell Material": "Honeywell Hardware", "Other": "Travel & Living", "Honeywell Labor": "Engineering Service"}
                    if str(Product_flag) in ('Migration'):
                        productTypes = ('Honeywell Material', 'Honeywell Software', 'Third-Party Material', 'Honeywell Labor', 'Other')
                    elif str(Product_flag) in ('Cyber','HCI'):
                        productTypes = ('Honeywell Material', 'Honeywell Software', 'Third-Party Material', 'Honeywell Labor', 'Write-In')
                    query = "select Product_Type, Sell_Price from QT__Product_Type_Details where cartId ='" + str(Quote.QuoteId) + "' and ownerId = '" + str(Quote.UserId) + "' and product_type in {}".format(productTypes)
                    query_result = SqlHelper.GetList(query)

                    if query_result:
                        if str(Product_flag) in ('Migration','HCI'):
                            #order = ["Honeywell Material", "Honeywell Software", "Third-Party Material", "Honeywell Labor", "Other"]
                            order = ["Honeywell Hardware", "Honeywell Software", "Third-Party Material", "Engineering Service", "Travel & Living"]
                        elif str(Product_flag) == 'Cyber':
                            order = ["Honeywell Hardware", "Honeywell Software", "Third-Party Material", "Engineering Service", "Write-In"]
                        order_index = {product: idx for idx, product in enumerate(order)}
                        for item in query_result:
                            if item.Product_Type in product_type_map:
                                item.Product_Type = product_type_map[item.Product_Type]
                        query_result_sorted = sorted(query_result, key=lambda x: order_index.get(x.Product_Type, float('inf')))
                        parts = {}
                        sum_eng = 0
                        for index, val in enumerate(query_result_sorted, start=1):
                            try:
                                selling_price = float(str(val.Sell_Price).replace(',', '').strip())
                                if str(Product_flag) == "HCI" and str(val.Product_Type) in ('Honeywell Software','Write-In'):
									sum_eng += selling_price
                                else:
									parts["{}.{}".format(index, val.Product_Type)] = "{:,.2f}".format(selling_price)
                            except ValueError:
                                parts["{}.{}".format(index, val.Product_Type)] = "0.00"
                        #Log.Info(str()+"-----email---parts--111-->"+str(parts))
                        if str(Product_flag) == "HCI":
                            parts["{}.{}".format(1, 'Honeywell Software')] = "{:,.2f}".format(sum_eng)
                            #Log.Info(str(sum_eng)+"-----email---parts--222-->"+str(parts))
                        total_raw = Quote.GetCustomField('Total Sell Price').Content
                        try:
                            total = float(str(total_raw).replace(',', '').strip())
                        except ValueError:
                            total = 0.0
                        parts["{}.Project Total".format(len(parts) + 1)] = "{:,.2f}".format(total)
                        #total = sum(float(val.Sell_Price) for val in query_result_sorted)
                        #parts[str(len(parts) + 1) + ".Grand Total"] = "{:,.2f}".format(total)
                        parts_as_str = '{' + ', '.join(['"{}": "{}"'.format(k, v) for k, v in parts.items()]) + '}'
                        Messagetext = "Proposal document has been generated successfully., Parts: " + parts_as_str
                    else:
                        Messagetext = "Proposal document has been generated successfully."
                else:
                    product_type_map = {"Hardware and Software": "Hardware and Software", "Project Management and Engineering Services": "Project Management and Engineering Services"}
                    productTypes = ('Hardware and Software', 'Project Management and Engineering Services')
                    newexp_query = "select Product_Type, SELLING_PRICE from QT__PAS_DCS_Pricing_Summary where cartId ='" + str(Quote.QuoteId) + "' and ownerId = '" + str(Quote.UserId) + "' and product_type in {}".format(productTypes)
                    NE_query_result = SqlHelper.GetList(newexp_query)
                    if NE_query_result:
                        project_total_raw = Quote.GetCustomField('Total Sell Price').Content
                        project_total_str = str(project_total_raw).replace(',', '').strip()
                        project_total = float(project_total_str) if project_total_str.replace('.', '', 1).isdigit() else 0.0
                        proposal_parts = {}
                        counter = 1
                        for item in NE_query_result:
                            product_type = item.Product_Type
                            selling_price_str = str(item.SELLING_PRICE).replace(',', '').strip()
                            selling_price = float(selling_price_str) if selling_price_str.replace('.', '', 1).isdigit() else 0.0
                            proposal_parts[str(counter) + "." + product_type] = "{:,.2f}".format(selling_price)
                            counter += 1
                        proposal_parts[str(counter) + ".Project Total"] = "{:,.2f}".format(project_total)
                        parts_as_str = "{" + ", ".join(['"' + str(k) + '": "' + str(v) + '"' for k, v in proposal_parts.items()]) + "}"
                        Messagetext = "Proposal document has been generated successfully., Parts: " + parts_as_str
                    else:
                        Messagetext = "Proposal document has been generated successfully."

                Quote.ChangeQuoteStatus('Submitted to Customer')
                Quote.ExecuteAction(3116)
                ScriptExecutor.Execute('CPQ_SF_CreateUpdateOpportunity')
                #Log.Info(str(TagParserQuote.ParseString("<* GetFirstFromQuoteTable( Quote_Details, Total_Sell_Price_incl_appl_Fees_) *>"))+'---Sell_Price__c = BHC163-->check--1---GS_R2Q_CPQ_TO_SFDC_DOC ---->' + str(TagParserQuote.ParseString("<* GetFirstFromQuoteTable( Quote_Details, Quote_Sell_Price) *>")))
                #Added a 60-second delay (time.sleep(60)) as per Pameer's request to send the final CPQ payload to SFDC - START
                if str(Product_flag) =='':
                    time.sleep(180)
                    pass
                else:
                    GS_R2Q_FunctionalUtil.UpdateStatusMessage(Quote, "Final", "Action", Messagetext)
                #Log.Info(str(TagParserQuote.ParseString("<* GetFirstFromQuoteTable( Quote_Details, Total_Sell_Price_incl_appl_Fees_) *>"))+'---Sell_Price__c = BHC163-->check--2---GS_R2Q_CPQ_TO_SFDC_DOC ---->' + str(TagParserQuote.ParseString("<* GetFirstFromQuoteTable( Quote_Details, Quote_Sell_Price) *>")))
                #Added a 60-second delay (time.sleep(60)) as per Pameer's request to send the final CPQ payload to SFDC - END
                 #GS_R2Q_FunctionalUtil.UpdateStatusMessage(Quote, "Final", "Action", Messagetext)
            else:
                if Quote.GetCustomField("EGAP_Highest_Approval_Level_for_the_Quote").Content not in ['','NA','0','No Approval'] and Quote.GetCustomField("R2Q_Save").Content != 'Save':
                    if str(Product_flag) !='':
                        GS_R2Q_FunctionalUtil.UpdateStatusMessage(Quote, "Egap Initiation", "Action", 'Quote submitted but egap approval required, {"ApprovalLevel": "'+Quote.GetCustomField("EGAP_Highest_Approval_Level_for_the_Quote").Content+'"}')
                        Log.Info(str(Quote.GetCustomField("EGAP_Highest_Approval_Level_for_the_Quote").Content)+"-EGAPIssue--111-->"+str(Product_flag))
                    else:
                        Messagetext = 'Quote submitted but egap approval required, {"ApprovalLevel": "'+Quote.GetCustomField("EGAP_Highest_Approval_Level_for_the_Quote").Content+'"}'
                        Log.Info(str(Quote.GetCustomField("EGAP_Highest_Approval_Level_for_the_Quote").Content)+"-EGAPIssue--222-->"+str(Product_flag))
                Log.Info("ApprovalApprovalApprovalApprovalApproval  "+str(approval))
            #Generate the BOM and send the details to SFDC
            if str(Product_flag) =='':
                QuoteNumber=Quote.CompositeNumber
                templateNameexcel = 'R2Q Excel pull doc'
                xl_doc=Quote.GenerateDocument(templateNameexcel,GenDocFormat.EXCEL)
                #if approval in ['','NA','0','No Approval']:
                xlName=Quote.GetLatestGeneratedDocumentFileName()
                xlBytes=Quote.GetLatestGeneratedDocumentInBytes()
                excelbit=Convert.ToBase64String(xlBytes)
                #paramexcel={'ParentId' : SFQuoteID ,'Name' : xlName, 'body' : excelbit,'ContentType': 'application/EXCEL'}
                #pdfPost=RestClient.Post(APIGEEDocurl,paramexcel,APIGEEHeader)
                APIGEE_Credentials = SqlHelper.GetFirst("Select Value from HPS_INTEGRATION_PARAMS Where [Key]='APIGEE_Credentials'").Value
                APIGEE_R2Q_URL = SqlHelper.GetFirst("Select Value from HPS_INTEGRATION_PARAMS Where [Key]='APIGEE_URL'").Value
                tokenUrl = "{}/v2/oauth/accesstoken".format(APIGEE_R2Q_URL)
                responseToken=AuthorizedRestClient.GetClientCredentialsGrantOAuthToken(APIGEE_Credentials,tokenUrl)
                Req_Token = "{} {}".format(responseToken["token_type"] , responseToken["access_token"])
                excel_Url="https://it.api-beta.honeywell.com/cpq/r2q/sfdc/v1/cpqtor2q/bom-generator"
                header = {"Content-Type" : "application/json","Authorization" : "{}".format(Req_Token),"HON-Org-Id" : "PMT-HPS" }
                final_request_body={'base64String':str(excelbit),'CPQQuoteNumber':str(QuoteNumber),'SFQuoteID':SFQuoteID,'Messagetext':Messagetext}
                RestClient.Post(excel_Url, RestClient.SerializeToJson(str(final_request_body)),header)
                Log.Info("Bom Sent to R2Q: {}".format(str(final_request_body)))

            Log.Info("document sent tO SFDC")
        else:
            msg = ('Error Occurred, ''{"ErrorCode": "PartsLaborConfig", ''"ErrorDescription": "Failed at: LaborCostMissing.<br>''<span style='color: #4C9AFF;'>Please contact P&E team to fix the missing labor cost error in this quote manually</span>"}')
            GS_R2Q_FunctionalUtil.UpdateStatusMessage(Quote, "Error", "Notification", msg)
    except Exception as ex:
        Log.Write("GS_R2Q_CPQ_TO_SFDC_DOC Fail-->>"+str(ex))
        ProductType = Quote.GetCustomField('ProductType').Content
        excel_Url, header = GS_APIGEE_Integration_Util.GetR2QAPIGEEAuthDetails()
        final_request_body={'QuoteNumber':str(Quote.CompositeNumber),'CartId':str(Quote.QuoteId),'RevisionNumber': str(Quote.RevisionNumber),'UserName':str(User.UserName),'Module':str(ProductType),'Action':'Update','Status':'Fail','Action_List':[{'ActionName':'Reprice','ScriptName':'GS_R2QPRJT_Reprice_Documentations','ErrorMessage':'GS_R2Q_CPQ_TO_SFDC_DOC'+str(ex)}]}
        msg = 'Error Occured, {"ErrorCode": "PartsLaborConfig", "ErrorDescription": "Failed at: DocumentGeneration"}'
        GS_R2Q_FunctionalUtil.UpdateStatusMessage(Quote, "Error", "Notification", msg)
        RestClient.Post(excel_Url, RestClient.SerializeToJson(str(final_request_body)),header)