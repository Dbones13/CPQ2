if Quote.GetCustomField("isR2QRequest").Content in ('yes','Yes','YES','True','true','True'):
    from CPQ_SF_IntegrationModules import CL_SalesforceIntegrationModules
    from CPQ_SF_Configuration import CL_SalesforceSettings
    class_sf_integration_modules = CL_SalesforceIntegrationModules(Quote, TagParserQuote, None, Session)

    API_VERSION = CL_SalesforceSettings.SALESFORCE_VERSION  
    INSTANCE_URL = CL_SalesforceSettings.SALESFORCE_URL 

    def query_cases():
        idval=''
        QuoteNumber=Quote.CompositeNumber
        query = "?q=SELECT+Id+FROM+Case+WHERE+Quote__r.Name='{}'".format(QuoteNumber)
        bearerToken = class_sf_integration_modules.get_auth2_token()
        headers = class_sf_integration_modules.get_authorization_header(bearerToken)
        response = class_sf_integration_modules.call_soql_api(headers, query)
        if len(response.records) != 0:
            for q in response.records:
                idval = str(q.Id)
            cases = idval
            return cases
        else:
            return ''

    # Function to Update a Case
    def update_case(case_id, sell_price_strategy, customer_budget):
        url = "{}/services/data/v{}/sobjects/Case/{}".format(INSTANCE_URL, API_VERSION, case_id)
        data = {
            "Sell_Price_Strategy__c": sell_price_strategy,
            "Customer_Budget__c": customer_budget
        }
        bearerToken = class_sf_integration_modules.get_auth2_token()
        headers = class_sf_integration_modules.get_authorization_header(bearerToken)
        headers["Sforce-Auto-Assign"] = "false"
        response = class_sf_integration_modules.call_rest_api(url, headers, data, "PATCH",None)
    cases = query_cases()
    if cases !='':
        SellPricestrategy=Quote.GetCustomField("SellPricestrategy").Content
        CustomerBudget=Quote.GetCustomField("CustomerBudget").Content
        update_case(cases, SellPricestrategy, CustomerBudget)