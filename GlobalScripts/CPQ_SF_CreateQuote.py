from CPQ_SF_Configuration import CL_CPQSettings
from CPQ_SF_IntegrationModules import CL_SalesforceIntegrationModules
from CPQ_SF_IntegrationSettings import CL_SalesforceIntegrationParams, CL_GeneralIntegrationSettings, CL_SalesforceQuoteParams
from CPQ_SF_FunctionModules import set_quote_opportunity_id, set_quote_multiple_params
from CPQ_SF_CpqHelper import EVENT_CREATE
from CPQ_SF_IntegrationReferences import CL_CompositeRequestReferences as REF, CL_SalesforceApis as API, CL_IntegrationReferences as INT_REF
import CPQ_SF_OpportunityMapping as OpportunityMapping
from CPQ_SF_CustomerModules import CL_CustomerModules
from CPQ_SF_ContactModules import CL_ContactIntegrationModules
from CPQ_SF_CustomObjectModules import CL_CustomObjectModules
from CPQ_SF_IntegrationMessages import CL_MessageHandler, CL_IntegrationMessages
from GS_MarketModule import marketinit

def main(Param, quote):
	editQuoteURl = "/cart/edit?cartcompositenumber={quoteNumber}"
	externalParameters = Param.externalParameters
	# Get Opportunity Id
	opportunityId = externalParameters["opportunityid"]
	productType = externalParameters["productType"]
	action = externalParameters["action"]
	r2qRequest=0
	Entitlement = ''
	try:
		r2qRequest=externalParameters["IsR2QRequest"]
	except:
		Log.Info("Normal Quote")

	try:
		customerBudget=externalParameters["budget"]
	except:
		customerBudget = ''
	try:
		Entitlement=externalParameters["Entitlement"]
	except:
		Log.Info("Entitlement Error")
		Entitlement = ''
	if opportunityId:
		# Create New Quote
		if Param.createQuote:
			quoteNumber = QuoteHelper.CreateNewQuote()
			Quote = QuoteHelper.Edit(quoteNumber)
		# Get current Quote
		else:
			Quote = quote
			quoteNumber = Quote.CompositeNumber
		if Quote:
			# Set redirection URL
			redirectionUrl = CL_CPQSettings.CPQ_URL + editQuoteURl.format(quoteNumber=quoteNumber)
			if r2qRequest == 'Yes' and action == 'create':
				productname = {'New/Expansion':'R2Q New / Expansion Project','Migration':'Migration_New','HCI':'R2Q HCI','Cyber':'Cyber'}
				base_query = """ SELECT PA.PRODUCT_ID, PA.PRODUCT_NAME FROM products PA INNER JOIN product_versions PV ON PV.product_id = PA.PRODUCT_ID WHERE PA.PRODUCT_NAME = '{}' AND PV.is_active = 'True' AND PA.IsSimple = 'False' """.format(productname[productType])
				if productType == 'Cyber':
					base_query += " AND PA.SYSTEM_ID = 'Cyber__cpq'"
				getPrd = SqlHelper.GetFirst(base_query)
				prd_id = int(getPrd.PRODUCT_ID)
				editQuoteURl = "/Configurator.aspx?pid="+str(prd_id)+""

				redirectionUrl = CL_CPQSettings.CPQ_URL + editQuoteURl
			class_sf_integration_modules = CL_SalesforceIntegrationModules(Quote, TagParserQuote, None, Session)
			class_customer_modules = CL_CustomerModules(Quote, TagParserQuote, None, Session)
			class_contact_modules = CL_ContactIntegrationModules(Quote, TagParserQuote, None, Session)
			class_custom_object_modules = CL_CustomObjectModules(Quote, TagParserQuote, None, Session)
			class_msg_handler = CL_MessageHandler(Quote, TagParserQuote, None, Session)
			#############################################
			# 1. AUTHORIZATION
			#############################################
			bearerToken = class_sf_integration_modules.get_auth2_token()
			adminToken = class_sf_integration_modules.get_admin_auth2_token()
			# GET other quotes linked to opportunity
			compositePayload = list()
			compositeRequest = class_sf_integration_modules.build_cr_get_opp_quotes(opportunityId)
			compositePayload.append(compositeRequest)
			# Call REST API
			response = class_sf_integration_modules.post_composite_request(adminToken, compositePayload, INT_REF.REF_GET_QUOTES_LINKED_TO_OPPORTUNITY)
			linkedQuotesResp = next((resp for resp in response["compositeResponse"] if resp["referenceId"] == REF.GET_OPP_QUOTES_REFID), None)
			# Only one quote can be linked to SF opportunity
			if CL_GeneralIntegrationSettings.ONLY_ONE_QUOTE_LINKED_TO_OPPORTUNITY and CL_GeneralIntegrationSettings.ATTACH_TO_OPP_IMMEDIATELY_ON_QUOTE_CREATED:
				if linkedQuotesResp:
					if linkedQuotesResp["body"]["totalSize"] > 0:
						# STOP PROCESSING
						class_msg_handler.add_message(CL_IntegrationMessages.ONLY_ONE_QUOTE_E_MSG)
						# Log Error
						Log.Error("CPQ-SFDC: Create Quote", str(CL_IntegrationMessages.ONLY_ONE_QUOTE_E_MSG))
						return None, class_msg_handler
			##############################################################
			# 2. COLLECT OPPORTUNITY INFORMATION & CREATE QUOTE & PRIMARY
			##############################################################
			# Attach Opportunity Id to Quote
			set_quote_opportunity_id(Quote, opportunityId)
			# Attach msid, contactid, egapproposaltype, entitlementselectedvalue parameters to Quote ||| Daniel S. ||| 08.05.2023
			set_quote_multiple_params(Quote, externalParameters)

			compositePayload = list()
			# Opportunity
			compositeRequest = class_sf_integration_modules.build_cr_sobject_get_opportunity(opportunityId)
			compositePayload.append(compositeRequest)
			
			# Make Quote Primary - Set other Quotes Primary Flag to False
			if CL_GeneralIntegrationSettings.ATTACH_TO_OPP_IMMEDIATELY_ON_QUOTE_CREATED:
				if linkedQuotesResp:
					if linkedQuotesResp["body"]["totalSize"] > 0:
						records = list()
						for linkedQuote in linkedQuotesResp["body"]["records"]:
							record = dict()
							record[CL_SalesforceQuoteParams.SF_PRIMARY_QUOTE_FIELD] = False
							record["Id"] = str(linkedQuote["Id"])
							record["attributes"] = {"type": CL_SalesforceQuoteParams.SF_QUOTE_OBJECT}
							records.append(record)
						if records:
							compositeRequest = class_sf_integration_modules.get_cr_sobjectcollection_payload_header(API.PATCH, REF.UPDATE_PRIMARY_REFID, None)
							compositeRequest["body"] = {"records": records}
							compositePayload.append(compositeRequest)
			
			# Opportunity Partners
			compositeRequest = class_sf_integration_modules.build_cr_sobject_get_opportunity_partners(opportunityId)
			compositePayload.append(compositeRequest)

			# Attach quote to opportunity immediately upon quote is created
			if CL_GeneralIntegrationSettings.ATTACH_TO_OPP_IMMEDIATELY_ON_QUOTE_CREATED:
				# Quote
				records = list()
				record = class_sf_integration_modules.build_cr_record_create_quote(opportunityId)
				records.append(record)
				compositeRequest = class_sf_integration_modules.get_cr_sobjectcollection_payload_header(API.POST, CL_SalesforceQuoteParams.SF_QUOTE_OBJECT, None)
				compositeRequest["body"] = {"records": records}
				compositePayload.append(compositeRequest)

			if compositePayload:
				# Check Create/Update Quote Permissions
				permissionList = [class_sf_integration_modules.build_permission_checklist(CL_SalesforceQuoteParams.SF_QUOTE_OBJECT, True, True)]
				# Call API
				response = class_sf_integration_modules.post_composite_request(bearerToken, compositePayload, INT_REF.REF_UPDATE_OPP_MAKE_PRIMARY, permissionList)

			if response:
				# Set header fields in Quote
				# Get Opportunity info
				opportunityResponse = next((resp for resp in response["compositeResponse"] if str(resp["referenceId"]) == CL_SalesforceIntegrationParams.SF_OPPORTUNITY_OBJECT), None)
				if opportunityResponse:
					OpportunityMapping.on_quote_create_inbound_opportunity_integration_mapping(Quote, opportunityResponse["body"])
					OpportunityMapping.on_quote_createupdate_inbound_opportunity_integration_mapping(Quote, opportunityResponse["body"])
					if r2qRequest == 'Yes':
						marketinit(Quote)

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
						class_customer_modules.process_customers_contacts(response, CustomerHelper, EVENT_CREATE)
			#############################################
			# 4. CUSTOM OBJECTS
			#############################################
			class_custom_object_modules.process_inbound_custom_object_mappings(adminToken, EVENT_CREATE) 
		if Quote.GetCustomField('IsR2QRequest').Content=="No":
			Quote.Save(False)
		else:
			Quote.GetCustomField('IsR2QRequest').Content=externalParameters["IsR2QRequest"]
			Quote.GetCustomField('R2QFlag').Content=externalParameters["IsR2QRequest"]
			#Quote.GetCustomField('SellPricestrategy').Content = externalParameters["sellpricestrategy"]
			#Quote.GetCustomField('CustomerBudget').Content = customerBudget
			Quote.GetCustomField('Account Manager').Content = externalParameters["accountManager"]
			Quote.GetCustomField('Quote Record Type').Content=externalParameters["quoterecordtype"]
			Quote.GetCustomField('Quote Comment').Content=externalParameters["description"]
			Quote.GetCustomField('EGAP_Proposal_Type').Content=externalParameters["quoteType"]
			Quote.GetCustomField('ProductType').Content = externalParameters["productType"]
			Quote.GetCustomField("Account Name").Content = str(opportunityResponse['body']['T_Account_Name__c'])
			Quote.GetCustomField("AccountId").Content = str(opportunityResponse['body']['AccountId'])
			if Entitlement != '':
				Quote.GetCustomField('Entitlement').Content = '' if externalParameters["Entitlement"] == 'No SESP' else externalParameters["Entitlement"]
			#cfFields = ['Account Contact Name','Account Contact Phone','Account Contact Email','Partner Account Contact Name','Partner Account Contact Phone','Partner Account Contact Email']
			try:
				class_sf_integration_modules = CL_SalesforceIntegrationModules(Quote, TagParserQuote, None, Session)
				bearerToken = class_sf_integration_modules.get_auth2_token()
				headers = class_sf_integration_modules.get_authorization_header(bearerToken)
				query = "?q="+"SELECT+Name,Phone,email+FROM+User+WHERE+Id+=+'"+str(externalParameters["accountManager"])+"'"
				OppOwner = class_sf_integration_modules.call_soql_api(headers, query)
				#OppOwner = SalesforceProxy.Binding.query("SELECT Name,Phone,email FROM User WHERE Id = '"+str(Id)+"'")
				Mngrrecords= OppOwner.records
				if Mngrrecords is not None:
					for item in Mngrrecords:
						Log.Write("Account Manager="+str(item["Name"]))
						#Log.Write("Account Manager phone="+str(item["Phone"]))
						Log.Write("Account Manager Mail="+str(item["Email"]))
						Quote.GetCustomField("Account Manager").Content = str(item["Name"])
						Quote.GetCustomField("Account Manager Phone No").Content = str(item["Phone"])
						Quote.GetCustomField("Account Manager Email").Content = str(item["Email"])
				else:
					 Log.Write("Account Manager No Records")

				polequery = "?q="+"SELECT+Booking_Country__r.Pole__c+FROM+Opportunity+WHERE+Id+=+'"+str(externalParameters["opportunityId"])+"'"
				poleInfo = class_sf_integration_modules.call_soql_api(headers, polequery)
				polerec= poleInfo.records
				if polerec is not None:
					for item in polerec:
						Quote.GetCustomField("R2Q_Booking_Pole").Content = str(item["Booking_Country__r"]["Pole__c"])
			except:
				Log.Info("Account Manager")
			Quote.GetCustomField('ContactId').Content=externalParameters["contactid"]
			ScriptExecutor.Execute('CPQ_SF_CreateUpdateOpportunity')
		return redirectionUrl, class_msg_handler


# Execute Main and return redirect URL
if Param is not None:
	quote = None
	if "Quote" in globals():
		quote = Quote
	Result, class_msg_handler = main(Param, quote)
	# Display Messages
	if class_msg_handler:
		if class_msg_handler.messages:
			class_msg_handler.show_messages()