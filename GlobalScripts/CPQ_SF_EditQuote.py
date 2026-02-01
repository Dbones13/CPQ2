from CPQ_SF_Configuration import CL_CPQSettings
from CPQ_SF_IntegrationModules import CL_SalesforceIntegrationModules
from CPQ_SF_IntegrationSettings import CL_GeneralIntegrationSettings, CL_SalesforceIntegrationParams
from CPQ_SF_FunctionModules import set_quote_opportunity_id, set_quote_multiple_params
from CPQ_SF_CpqHelper import EVENT_UPDATE
from CPQ_SF_IntegrationReferences import CL_CompositeRequestReferences as REF, CL_IntegrationReferences as INT_REF
import CPQ_SF_OpportunityMapping as OpportunityMapping
from CPQ_SF_CustomerModules import CL_CustomerModules
from CPQ_SF_ContactModules import CL_ContactIntegrationModules
from CPQ_SF_CustomObjectModules import CL_CustomObjectModules

if Param is not None:
    externalParameters = Param.externalParameters
    redirectionUrl = CL_CPQSettings.CPQ_URL
    # Get Opportunity Id
    opportunityId = externalParameters["opportunityid"]
    quoteNumber = externalParameters["quotenumber"]
    quoteId = externalParameters["quoteId"]
    ownerId = externalParameters["ownerId"]
    Quote = Param.quote # SAP Case ref. 790977/2024 and 1140590/2024
    r2qRequest=0
    try:
        r2qRequest=externalParameters["IsR2QRequest"]
    except:
        Log.Info("Normal Quote")

    editR2Q = externalParameters["editR2Q"] if "editR2Q" in externalParameters else 'False'

    if editR2Q == 'True' and (Quote.GetCustomField('R2QFlag').Content == 'Yes' or Quote.GetCustomField('R2QFlag').Content == ''):
        Quote.GetCustomField('IsR2QRequest').Content = 'Yes'
    else:
        Quote.GetCustomField('IsR2QRequest').Content = ''

    if opportunityId and quoteId and ownerId:
        if Quote: # SAP Case ref. 790977/2024 and 1140590/2024
            # Open active revision
            if CL_GeneralIntegrationSettings.ALL_REV_ATTACHED_TO_SAME_OPPORTUNITY:
                editQuoteURl = "/cart/edit?cartcompositenumber={quoteNumber}".format(quoteNumber=str(quoteNumber))
                # SAP Case ref. 790977/2024 and 1140590/2024
                # Quote = QuoteHelper.Edit(quoteNumber)
            elif int(r2qRequest) == 1: #R2Q
                #editQuoteURl = "/quotation/QuoteProperty.aspx?TabId=19797"
                #editQuoteURl = "/configurator.aspx?pid=209839"
                editQuoteURl = "/Configurator.aspx?pid=300994"
                # SAP Case ref. 790977/2024 and 1140590/2024
                # Quote = QuoteHelper.Edit(float(ownerId), float(quoteId))
            elif editR2Q == 'True':
                editQuoteURl = "/Configurator.aspx"
                if Quote.Items.Count > 0:
                    Quote.MainItems[0].EditConfiguration()
                else:
                    productType = Quote.GetCustomField('ProductType').Content
                    productname = {'New/Expansion':'R2Q New / Expansion Project','Migration':'Migration_New','HCI':'R2Q HCI','Cyber':'Cyber'}
                    base_query = """ SELECT PA.PRODUCT_ID, PA.PRODUCT_NAME FROM products PA INNER JOIN product_versions PV ON PV.product_id = PA.PRODUCT_ID WHERE PA.PRODUCT_NAME = '{}' AND PV.is_active = 'True' AND PA.IsSimple = 'False' """.format(productname[productType])
                    if productType == 'Cyber':
                        base_query += " AND PA.SYSTEM_ID = 'Cyber__cpq'"
                    getPrd = SqlHelper.GetFirst(base_query)
                    prd_id = int(getPrd.PRODUCT_ID)
                    editQuoteURl = "/Configurator.aspx?pid="+str(prd_id)+""
            else:
                editQuoteURl = "/quotation/Cart.aspx"
                #editQuoteURl = "/cart/edit?ownerId={ownerId}&quoteId={quoteId}".format(ownerId=str(ownerId), quoteId=str(quoteId))
                # SAP Case ref. 790977/2024 and 1140590/2024
                # Quote = QuoteHelper.Edit(float(ownerId), float(quoteId))

            # Attach Opportunity Id to Quote
            set_quote_opportunity_id(Quote, opportunityId)
            # Attach msid, contactid, egapproposaltype, entitlementselectedvalue parameters to Quote ||| Daniel S. ||| 08.05.2023
            set_quote_multiple_params(Quote, externalParameters)

            class_sf_integration_modules = CL_SalesforceIntegrationModules(Quote, TagParserQuote, None, Session)
            class_customer_modules = CL_CustomerModules(Quote, TagParserQuote, None, Session)
            class_contact_modules = CL_ContactIntegrationModules(Quote, TagParserQuote, None, Session)
            class_custom_object_modules = CL_CustomObjectModules(Quote, TagParserQuote, None, Session)
            #############################################
            # 1. AUTHORIZATION
            #############################################
            bearerToken = class_sf_integration_modules.get_auth2_token()
            headers = class_sf_integration_modules.get_authorization_header(bearerToken) #pole on edit R2Q
            adminToken = class_sf_integration_modules.get_admin_auth2_token()
            ######################################################
            # 2. COLLECT OPPORTUNITY INFORMATION & CREATE QUOTE
            ######################################################
            compositePayload = list()
            # Opportunity
            compositeRequest = dict()
            compositeRequest = class_sf_integration_modules.build_cr_sobject_get_opportunity(opportunityId)
            compositePayload.append(compositeRequest)

            # Opportunity Partners
            compositeRequest = dict()
            compositeRequest = class_sf_integration_modules.build_cr_sobject_get_opportunity_partners(opportunityId)
            compositePayload.append(compositeRequest)
            
            #pole on edit R2Q
            if Quote.GetCustomField('IsR2QRequest').Content == 'Yes':
                polequery = "?q="+"SELECT+Booking_Country__r.Pole__c+FROM+Opportunity+WHERE+Id+=+'"+str(externalParameters["opportunityId"])+"'"
                poleInfo = class_sf_integration_modules.call_soql_api(headers, polequery)
                polerec= poleInfo.records
                if polerec is not None:
                    for item in polerec:
                        Quote.GetCustomField("R2Q_Booking_Pole").Content = str(item["Booking_Country__r"]["Pole__c"])
            #pole on edit R2Q

            # Call API
            response = class_sf_integration_modules.post_composite_request(bearerToken, compositePayload, INT_REF.REF_GET_OPP)
            if response:
                # Set opportunity fields in Quote
                # Get Opportunity info
                opportunityResponse = next((resp for resp in response["compositeResponse"] if str(resp["referenceId"]) == CL_SalesforceIntegrationParams.SF_OPPORTUNITY_OBJECT), None)
                if opportunityResponse:
                    OpportunityMapping.on_quote_update_inbound_opportunity_integration_mapping(Quote, opportunityResponse["body"])
                    OpportunityMapping.on_quote_createupdate_inbound_opportunity_integration_mapping(Quote, opportunityResponse["body"])

                # Get Opportunity Partners info
                opportunityPartnersResp = next((resp for resp in response["compositeResponse"] if str(resp["referenceId"]) == REF.GET_OPP_PARTNERS_REFID), None)

                if opportunityResponse:
                    # Set Market on quote
                    class_sf_integration_modules.set_market_on_quote(opportunityResponse)
                    ######################################################
                    # 3. COLLECT ADDITIONAL INFORMATION
                    ######################################################
                    response = class_customer_modules.get_customer_details(bearerToken, class_contact_modules, opportunityId, opportunityResponse, opportunityPartnersResp)
                    if response:
                        # Process Customers and Contacts
                        class_customer_modules.process_customers_contacts(response, CustomerHelper, EVENT_UPDATE)
            #############################################
            # 4. CUSTOM OBJECTS
            #############################################
            class_custom_object_modules.process_inbound_custom_object_mappings(adminToken, EVENT_UPDATE)
        Quote.Save(False)
        # Return redirect URL
        redirectionUrl = CL_CPQSettings.CPQ_URL + editQuoteURl
    Result = str(redirectionUrl)