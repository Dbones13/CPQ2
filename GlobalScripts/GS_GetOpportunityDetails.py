def GetOpportunityDetails(Quote,TagParserQuote,Session):
    #Getting all SFDC information and assign into CPQ fields and tables.
    from System import Array
    from CPQ_SF_FunctionModules import get_quote_opportunity_id
    from CPQ_SF_IntegrationModules import CL_SalesforceIntegrationModules
    def getCFValue(Quote, CF_Name):
        return Quote.GetCustomField(CF_Name).Content
    def setCFValue(Quote, CF_Name, CF_Value):
        Quote.GetCustomField(CF_Name).Content = CF_Value
    def getCountryCodeMap():
        query = "select COUNTRY_NAME , COUNTRY_ABREV3 from V_COUNTRY"
        countryCodeMap = dict()
        for res in SqlHelper.GetList(query):
            countryCodeMap[res.COUNTRY_NAME.lower()] = res.COUNTRY_ABREV3
        return countryCodeMap
    def getCustomerDetails(headers , id , customerRole , countryCodeMap):
        typeList = ["RE","WE","EN"]
        Trace.Write(typeList[int(customerRole) - 1])
        query = "?q="+"select+Id,System_ID_Type__c,System_ID__c,IsActive__c,Address_Line_1__c,Address_Line_2__c,City__c,State__c,Postal_Code__c,Country__c+from+Account_Xref__c+where+id+=+'{}'".format(id)
        response = class_sf_integration_modules.call_soql_api(headers, query)
        cutomerRecords = response.records
        #cutomerRecords = salesforceProxy.Binding.query(query).records
        if cutomerRecords:
            customer = Quote.NewCustomer(customerRole)
            for item in cutomerRecords:
                customer.Active = True
                customer.CustomerType = typeList[int(customerRole) - 1]
                customer.CustomerCode = str(item["System_ID__c"] if item["IsActive__c"] == 'true' else '')
                if customer.CustomerType=="WE" and  Quote.GetCustomField('IsDropShip').Content=="True":
                    customer.Address1               = str(Quote.GetCustomField("DropShipAddress1").Content)
                    customer.Address2               = str(Quote.GetCustomField("DropShipAddress2").Content)
                    customer.City                   = str(Quote.GetCustomField("DropShipCity").Content)
                    customer.Province               = str(Quote.GetCustomField("DropShipState").Content)
                    customer.ZipCode                = str(Quote.GetCustomField("DropShipZipCode").Content)
                    customer.CountryAbbreviation    = str(Quote.GetCustomField("DropShipCountry").Content)
                else:
                    customer.Address1               = str(item["Address_Line_1__c"] if item["IsActive__c"] == 'true' else '')
                    customer.Address2               = str(item["Address_Line_2__c"] if item["IsActive__c"] == 'true' else '')
                    customer.City                   = str(item["City__c"] if item["IsActive__c"] == 'true' else '')
                    customer.Province               = str(item["State__c"] if item["IsActive__c"] == 'true' else '')
                    customer.ZipCode                = str(item["Postal_Code__c"] if item["IsActive__c"] == 'true' else '')
                    if str(item["Country__c"])=="south korea (republic of korea":
                        customer.CountryAbbreviation    = "KOR"
                    else:
                        customer.CountryAbbreviation    = str(item["Country__c"] if item["IsActive__c"] == 'true' else '')
            return customer
        return None
    def getOpportunityDetails(headers, OppId):
        #OppInfo = SalesforceProxy.Binding.query("SELECT AccountId, Name, CurrencyIsoCode, Partner_Account__c, Partner_Contact__c FROM Opportunity WHERE Id = '"+str(OppId)+"'")
        query = "?q="+"SELECT+AccountId,+Name,+CurrencyIsoCode,+Partner_Account__c,+Partner_Contact__c,+Type,+Id+FROM+Opportunity+WHERE+Id+=+'"+str(OppId)+"'"
        OppInfo = class_sf_integration_modules.call_soql_api(headers, query)
        return OppInfo.records
    def getQuoteDetails(headers):
        quoteId = Quote.QuoteId
        userId = Quote.UserId
        query = "?q="+"SELECT+Status,+Primary_Quote__c,+ContactId,+Project_Manager__r.name,+ERP_Reference__c+,+Sold_To__c+,+Id+FROM+Quote+WHERE+Quote_ID__c+=+{}+and+Owner_ID__c+=+{}".format(quoteId,userId)
        QuoteInfo = class_sf_integration_modules.call_soql_api(headers, query)
        #QuoteInfo = SalesforceProxy.Binding.query("SELECT Primary_Quote__c,ContactId FROM Quote WHERE Quote_ID__c = {} and Owner_ID__c = {}".format(quoteId,userId))
        return QuoteInfo.records
    def getprimaryQuoteStatus(headers, OppId):
        query = "?q="+"SELECT+Status+FROM+Quote+WHERE+OpportunityId+=+'"+str(OppId)+"'+and+Primary_Quote__c+=+true"
        QuoteInfo = class_sf_integration_modules.call_soql_api(headers, query)
        #QuoteInfo = SalesforceProxy.Binding.query("SELECT Status FROM Quote WHERE OpportunityId = '"+str(OppId)+"' and Primary_Quote__c = true")
        return QuoteInfo.records
    def getAccountDetails(headers, Id):
        query = "?q="+"select+id,+CurrencyIsoCode,+Name,+Site,+OwnerId,+ParentId,+Phone,+billingstreet,+billingcity,+billingstate,+billingcountry,+billingPostalCode+,+Type+from+Account+WHERE+Id+=+'"+str(Id)+"'"
        AccountInfo = class_sf_integration_modules.call_soql_api(headers, query)
        #AccountInfo = SalesforceProxy.Binding.query("select id, CurrencyIsoCode, Name, Site, OwnerId, Phone, billingstreet, billingcity, billingstate, billingcountry, billingPostalCode , Type from Account WHERE Id = '"+str(Id)+"'")
        return AccountInfo.records
    def getManagerDetails(headers, Id):
        # query = "?q="+"SELECT+User__c,+User__r.Name,+User__r.Phone,+User__r.Email+FROM+Account_Team__c+WHERE+Account__c+=+'"+str(Id)+"'+and+Primary_Flag__c+=+true"
        query = "?q="+"SELECT+User__c+FROM+Account_Team__c+WHERE+Account__c+=+'"+str(Id)+"'+and+Primary_Flag__c+=+true"
        OwnerMngr = class_sf_integration_modules.call_soql_api(headers, query)
        #OwnerMngr = SalesforceProxy.Binding.query("SELECT User__c FROM Account_Team__c WHERE Account__c = '"+str(Id)+"' and Primary_Flag__c = true")
        userRec=None
        if OwnerMngr is not None:
            for item in OwnerMngr.records:
                userID=str(item["User__c"])
                userRec=getUserDetails(headers, userID)
                return userRec
        else:
            return None
    def getUserDetails(headers, Id):
        query = "?q="+"SELECT+Name,Phone,email+FROM+User+WHERE+Id+=+'"+str(Id)+"'"
        OppOwner = class_sf_integration_modules.call_soql_api(headers, query)
        #OppOwner = SalesforceProxy.Binding.query("SELECT Name,Phone,email FROM User WHERE Id = '"+str(Id)+"'")
        return OppOwner.records
    def getContactDetails(headers, Id):
        Quote.GetCustomField('ContactId').Content=str(Id)
        query = "?q="+"SELECT+Name,Phone,email,Type__c+FROM+Contact+WHERE+Id+=+'"+str(Id)+"'"
        ContactDetails = class_sf_integration_modules.call_soql_api(headers, query)
        #ContactDetails = SalesforceProxy.Binding.query("SELECT Name,Phone,email,Type__c FROM Contact WHERE Id = '"+str(Id)+"'")
        return ContactDetails.records
    def getProposalRequestDetails(headers, Id):
        query = "?q="+"select+Id,Createddate,Due_Date__c,Pricing_Type__c+from+Case+where+Opportunity__c+=+'"+str(Id)+"'+order+by+Createddate+desc+limit+1"
        ProposalRequestInfo = class_sf_integration_modules.call_soql_api(headers, query)
        return ProposalRequestInfo.records
    def getMPA(AccountId):
        MPA = SqlHelper.GetFirst("SELECT AgreementName, PricePlanName from MPA(nolock) where AccountId = '"+str(AccountId)+"'")
        return MPA
    def updateCFValue( Quote, CustomFields):
        for Name, Value in CustomFields.items():
            setCFValue(Quote, Name, Value)
    def fetch_LeapContract_details(headers,Id):
        query = "?q="+"Select+(+select+Leap_Contract_Number__c+,+Incoterms__c+,+Leap_Payment_Terms__c+,+Status+from+Contracts__r+where+status+=+'Active'+Order+BY+CreatedDate+Desc+Limit+1)+from+Opportunity+where+id+=+'"+str(Id)+"'"
        return class_sf_integration_modules.call_soql_api(headers, query)

    def fetch_customerprice_details(headers,Org,Id):
        # query = "?q="+"select+id,+Price_Group__c,+Price_List__c,+ERP_ID_SoldTo__c,+Sales_ORG__c+from+Source_System__c+where+Sales_ORG__c+=+'"+str(Org)+"'+and+ERP_ID_SoldTo__c+=+true+and+Account__c+=+'"+str(Id)+"'"
        # query = "?q="+"select+id,+Customer_Price_Group__c,+Price_List__c,+ERP_ID_SoldTo__c,+Source_Organization__c+from+Account_Xref__c+where+Source_Organization__c +=+'"+str(Org)+"'+and+ERP_ID_SoldTo__c+=+true+and+Customer_Account__c+=+'"+str(Id)+"'"
        query = "?q="+"select+id,+System_ID__c,+Customer_Price_Group__c,+Price_List__c,+ERP_ID_SoldTo__c,+Source_Organization__c+from+Account_Xref__c+where+Source_Organization__c +=+'"+str(Org)+"'+and+System_ID_Type__c+=+'SAP Sold To'+and+Customer_Account__c+=+'"+str(Id)+"'"
        Log.Info(query)
        return class_sf_integration_modules.call_soql_api(headers, query)

    def getLSSActiveServiceContract(headers, Id):
        cont = "False"
        query = "?q=SELECT+Id,+name,+AccountId+FROM+ServiceContract+WHERE+Line_of_Business__c ='LSS'+and+status='Active'+and+AccountId+IN+(SELECT+AccountId+FROM+opportunity+WHERE+Id+=+'{}')".format(Id)
        lssActiveRecords = class_sf_integration_modules.call_soql_api(headers, query)
        if lssActiveRecords and lssActiveRecords.totalSize > 0:
            cont = "True"
        return cont

    # Get Authorization Token
    class_sf_integration_modules = CL_SalesforceIntegrationModules(Quote, TagParserQuote, None, Session)
    bearerToken = class_sf_integration_modules.get_auth2_token()
    headers = class_sf_integration_modules.get_authorization_header(bearerToken)
    # Get Opportunity Id from Quote
    oppId = get_quote_opportunity_id(Quote)
    if not oppId:
    # Get Opportunity Id from Session
        oppId = Session["OpportunityId"]
    if oppId:
    #if SFEnvironment.Opportunity is not None:
        countryCodeMap = getCountryCodeMap()
        customerFields = {'1':'BillToId' , '2':'ShipToId' , '3':'EndCustomerId'}
        bookingtab_visibility = TagParserQuote.ParseString('[IF]([EQ](<* QuoteProperty (Quote Type) *>,Projects)){[EQ](<* QuoteProperty (EGAP_Proposal_Type) *>,Booking)}{[IN](<*CTX( Quote.Status.Name )*>,Pending Order Confirmation,Booked,Accepted by Customer,Order Confirmation Pending,Pending Project Creation,Project Created,GCC Handover,ERP Contract Created)}[ENDIF]')
        if int(bookingtab_visibility) == 1:
            for role , field in customerFields.items():
                id = getCFValue(Quote , field)
                if id:
                    customer = getCustomerDetails(headers , id , role , countryCodeMap)
                    if customer:
                        Quote.SaveCustomer(customer)
                else:
                    customer = Quote.NewCustomer(role)
                    Quote.SaveCustomer(customer)
        #Get the Opportunity Id
        #OppId = SFEnvironment.Opportunity.Id
        OppId = oppId
        quoteNumber = quoteNumber = Quote.CompositeNumber
        contactId = ''
        CustomFields = {}
        CustomFields["OpportunityId"] = str(OppId)
        CustomFields["IsPrimaryAllowed"] = "1"
        sfdcDetails = getQuoteDetails(headers)
        #Trace.Write("DS CHECK: " + str(sfdcDetails))
        if sfdcDetails is not None:
            for i in sfdcDetails:
                if Quote.GetCustomField('Quote Type').Content in ['Contract New']:
                    CustomFields['SC_CF_ERPREFNO'] = str(i["ERP_Reference__c"])
                #Defect CXCPQ-63326 : Addition of "True" in below if check
                if str(i["Primary_Quote__c"]) in ("true","True"):
                    CustomFields["IsPrimary"] = "1"
                else:
                    CustomFields["IsPrimary"] = "0"
                if str(i["ContactId"]) != "":
                    contactId = str(i["ContactId"])
                if i["Project_Manager__r"] != None:
                    CustomFields["Project_Manager"] = str(i["Project_Manager__r"].Name) #throwing error no attr name.
        #contactId = getCFValue(Quote,"ContactId")
        cfFields = ['Account Contact Name','Account Contact Phone','Account Contact Email','Partner Account Contact Name','Partner Account Contact Phone','Partner Account Contact Email']
        for field in cfFields:
            CustomFields[field] = ''
            
        if contactId:
            contactDetails = getContactDetails(headers, contactId)
            #Trace.Write("DS CHECK: " + str(contactDetails))
            if contactDetails is not None:
                for item in contactDetails:
                    if getCFValue(Quote,"Opportunity Sales Type").startswith('Direct'):
                        CustomFields[cfFields[0]] = str(item["Name"])
                        CustomFields[cfFields[1]] = str(item["Phone"])
                        CustomFields[cfFields[2]] = str(item["Email"])
                    else:
                        CustomFields[cfFields[3]] = str(item["Name"])
                        CustomFields[cfFields[4]] = str(item["Phone"])
                        CustomFields[cfFields[5]] = str(item["Email"])
                        CustomFields[cfFields[0]] = str(item["Name"]) # CXCPQ-111147 R2Q first edit to load the value
                        CustomFields[cfFields[1]] = str(item["Phone"]) # CXCPQ-111147 R2Q first edit to load the value
                        CustomFields[cfFields[2]] = str(item["Email"]) # CXCPQ-111147 R2Q first edit to load the value
        #quoteStatus = getprimaryQuoteStatus(headers, OppId)
        #if quoteStatus is not None:
        #    Trace.Write(quoteStatus[0].Any[0].InnerText)
        #    if quoteStatus[0].Any[0].InnerText in ('Accepted by Customer','Pending Order Confirmation','Order Failed','Booked'):
        #        CustomFields["IsPrimaryAllowed"] = "0"

        Opprecords1 = getOpportunityDetails(headers, OppId)
        if Opprecords1:
            #Get the MPA from custom table
            for item in Opprecords1:
                CustomFields["PartnerAccountID"] = str(item["AccountId"])
                accountID = str(item["AccountId"])
                partnerAcc = str(item["Partner_Account__c"])
                opportunityType = str(item["Type"])
                Mngrrecords = getManagerDetails(headers, accountID)
                CheckR2q = Quote.GetCustomField('IsR2QRequest').Content
                Account_Manager = Quote.GetCustomField('Account Manager Email').Content
                if Mngrrecords is not None and CheckR2q != 'Yes' and Account_Manager == "":
                    for item in Mngrrecords:
                        CustomFields["Account Manager"] = str(item["Name"])
                        CustomFields["Account Manager Phone No"] = str(item["Phone"])
                        CustomFields["Account Manager Email"] = str(item["Email"])
            #Get the Account Details
            quoterecords2 = getAccountDetails(headers, accountID)
            if quoterecords2 is not None:
                for item in quoterecords2:
                    OwnerId = str(item["OwnerId"])
                    ParentId = str(item["ParentId"])
                    CustomFields["AccountId"] = str(item["Id"])
                    CustomFields["Account Name"] = str(item["Name"])
                    CustomFields["Account Site"] = str(item["Site"])
                    #CustomFields["Account Contact Phone"] = quoterecords2[0].Any[5].InnerText
                    CustomFields["Account Address Line 1"] = str(item["BillingStreet"])
                    CustomFields["Account Address City"] = str(item["BillingCity"])
                    CustomFields["Account Address State"] = str(item["BillingState"])
                    CustomFields["Account Address Country"] = str(item["BillingCountry"])
                    CustomFields["Account Address Zip Code"] = str(item["BillingPostalCode"])
                    # Mngrrecords = None #getManagerDetails(headers, Opprecords1[0].Any[0].InnerText)
                '''if Mngrrecords is not None:
                    ALGet = getUserDetails(headers, Mngrrecords[0].Any[0].InnerText)
                    Trace.Write("DS getUserDetails: " + str(ALGet))
                    if ALGet is not None:
                        CustomFields["Account Manager"] = ALGet[0].Any[0].InnerText
                        CustomFields["Account Manager Phone No"] = ALGet[0].Any[1].InnerText
                        CustomFields["Account Manager Email"] = ALGet[0].Any[2].InnerText'''
                OwnerRecords = getUserDetails(headers, OwnerId)
                if OwnerRecords is not None:
                    for item in OwnerRecords:
                        CustomFields["Account Owner Name"] = str(item["Name"])
                        CustomFields["Account Owner Phone No"] = str(item["Phone"])
                        CustomFields["Account Owner Email"] = str(item["Email"])
                #For Service Quotes 
                #Get Parent Account Name and Proposal Request Due Date form SFDC
                if opportunityType is not None and opportunityType in ("Contract New", "Contract Renewal") and ParentId is not None:
                    ParentRecords = getAccountDetails(headers, ParentId)
                    if ParentRecords and ParentRecords.Count>0 and str(ParentRecords[0]["Name"]) != '':
                        CustomFields["SC_CF_PARENT_ACCOUNT_NAME"] = str(ParentRecords[0]["Name"])
                    #CXCPQ-61385 - Jagruti Chandratre - 21/9/23 (No integration required from SFDC)
                    '''
                    ProposalRecords = getProposalRequestDetails(headers, OppId)
                    if ProposalRecords is not None:
                        for item in ProposalRecords:
                            CustomFields["SC_CF_DUEDATE"] = DateTime.Parse(str(item["Due_Date__c"])).ToString("dd/MM/yyyy")
                            CustomFields["EGAP_Proposal_Type"] = str(item["Pricing_Type__c"])
                    '''
            #Get the Partner Account Details
            quoterecords3 = getAccountDetails(headers, partnerAcc)
            if quoterecords3 is not None:
                for item in quoterecords3:
                    CustomFields["Partner Account Name"] = str(item["Name"])
                    CustomFields["Partner Account Site"] = str(item["Site"])
                    CustomFields["Partner Account Address (Site) Line 1"] = str(item["BillingStreet"])
                    CustomFields["Partner Account Address City"] = str(item["BillingCity"])
                    CustomFields["Partner Account Address State"] = str(item["BillingState"])
                    CustomFields["Partner Account Address Country"] = str(item["BillingCountry"])
                    CustomFields["Partner Account Address Zip Code"] = str(item["BillingPostalCode"])
                    CustomFields["Partner Account Type"] = str(item["Type"])
                '''PartnerContactRecords = getContactDetails(headers, Opprecords1[0].Any[3].InnerText)
                if PartnerContactRecords is not None:
                    CustomFields["Partner Account Contact Name"] = PartnerContactRecords[0].Any[0].InnerText
                    CustomFields["Partner Account Contact Phone"] = PartnerContactRecords[0].Any[1].InnerText
                    CustomFields["Partner Account Contact Email"] = PartnerContactRecords[0].Any[2].InnerText'''
            #Jagruti (H543314) -> Added condition such that below code block should not execute for Service contract quotes.
            if Quote.GetCustomField('Quote Type').Content not in ['Contract New','Contract Renewal']:
                #Get Leap Details - Q2C - Digital Threads
                Leapresponse = fetch_LeapContract_details(headers,OppId)
                if Leapresponse and Leapresponse.totalSize>0 and str(Leapresponse.records[0]["Contracts__r"]) != '':
                    CustomFields["Leap_Contract_Number"] = str(Leapresponse.records[0]["Contracts__r"].records[0]["Leap_Contract_Number__c"])
                    CustomFields["Delivery Terms"] = str(Leapresponse.records[0]["Contracts__r"].records[0]["Incoterms__c"])
                    Quote.CustomFields.SelectValueByValueCode("NetTerms",str(Leapresponse.records[0]["Contracts__r"].records[0]["Leap_Payment_Terms__c"]))
            #Get Customer Price Group & Price List from SalesForce
            if getCFValue(Quote, 'Quote Tab Booking LOB') == 'PMC':
                Custresponse = fetch_customerprice_details(headers,getCFValue(Quote, 'Sales Area'),accountID)
                # Log.Info(str(Custresponse))
                if Custresponse and int(Custresponse.totalSize)>0:
                    CustomFields["Customer Price Group"] = str(Custresponse.records[0]["Customer_Price_Group__c"])
                    CustomFields["Customer Price List"] = str(Custresponse.records[0]["Price_List__c"])
                    if str(Quote.OrderStatus.Name) in('Preparing'):
                        i=0
                        if sfdcDetails and str(sfdcDetails[0]["Sold_To__c"]):
                            for item in Custresponse.records:
                                if str(item["Id"]) ==  str(sfdcDetails[0]["Sold_To__c"]):
                                    break
                                i+=1
                            if i>int(Custresponse.totalSize)-1:
                                i=0
                        CustomFields["SoldToCustomerId"] = str(Custresponse.records[i]["System_ID__c"])
                        CustomFields["SoldToId"] = str(Custresponse.records[i]["Id"])

        #update custom fields value
        if Quote.GetCustomField("isR2QRequest").Content == 'Yes':
            CustomFields["Check_LSS_Rec_Count"] = getLSSActiveServiceContract(headers, oppId)
        updateCFValue(Quote, CustomFields)
        Quote.Save(False)
        if sfdcDetails:
            Session['SFDC_Quote_ID'] = sfdcDetails[0]["Id"]
            if (str(sfdcDetails[0]["Status"]) in('Approved','Rejected') and str(Quote.OrderStatus.Name) in('Ready for Approval','Awaiting Approval')) or (str(sfdcDetails[0]["Status"]) in('Project Created') and str(Quote.OrderStatus.Name) in('Pending Project Creation') and getCFValue(Quote, 'CF_ProjectId') != '') or (str(sfdcDetails[0]["Status"]) in('Booked') and str(Quote.OrderStatus.Name) in('Pending Order Confirmation') and getCFValue(Quote, 'CF_ProjectId') != '' and Quote.OrderId != ''):
                Quote.ChangeQuoteStatus(str(sfdcDetails[0]["Status"])) #SFDC to CPQ Update
            elif (str(sfdcDetails[0]["Status"]) in('Pending Project Creation') and str(Quote.OrderStatus.Name) in('Project Created') and getCFValue(Quote, 'CF_ProjectId') != '') or (str(sfdcDetails[0]["Status"]) in('Pending Order Confirmation') and str(Quote.OrderStatus.Name) in('Booked') and getCFValue(Quote, 'CF_ProjectId') != '' and Quote.OrderId != ''):
                ScriptExecutor.Execute('CPQ_SF_CreateUpdateOpportunity') #CPQ to SFDC update