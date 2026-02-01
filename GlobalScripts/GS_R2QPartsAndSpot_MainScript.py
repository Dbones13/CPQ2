#---------------------------------------------------------------------------------------------------------
#					Change History Log
#---------------------------------------------------------------------------------------------------------
# Description: Main script for R2Q Parts and Spot Quote product addition
#----------------------------------------------------------------------------------------------------------
# Date 			Name					    Version   Comment
# 05-12-2023	Sourav Kumar Samal			176		  Applied fix for CXCPQ-72938

import GS_R2Q_FunctionalUtil
from GS_R2Q_Integration_Messages import CL_R2Q_Integration_ErrorMessages as Error, CL_R2Q_Integration_SuccessMessages as Success

try:
	#Get Quote context
	bodyData         = RestClient.DeserializeJson(RequestContext.Body)
	quoteNumber     = str(bodyData["QuoteNumber"])
	Quote = QuoteHelper.Edit(quoteNumber)
	responseBody = {"Status": "Success","ErrorMessage": ""}

	if Quote.GetCustomField("CF_R2Q_AutomationFlag").Content != 'Y':
		responseBody = {"Status": "Error", "ErrorMessage": Error.InvalidQuote}
	elif Quote.GetCustomField("CF_R2Q_QuoteRef").Content == '':
		responseBody = {"Status": "Error", "ErrorMessage": Error.InvalidQuote}
	elif Quote.GetCustomField("CF_R2Q_FirstEdit").Content == '0':
		responseBody = {"Status": "Error", "ErrorMessage": Error.MultiExecutionError}
	else:

		# Check the quote is of type 'Parts and Spot', R2Q Automation flag is true and 1st edit is true -- H542832 : CXCPQ-51857 :start
		if Quote.GetCustomField("Quote Type").Content == 'Parts and Spot' and Quote.GetCustomField("CF_R2Q_AutomationFlag").Content == 'Y' and Quote.GetCustomField("CF_R2Q_FirstEdit").Content == '1':
			ScriptExecutor.ExecuteGlobal('GS_GetOpportunityDetails')
			ScriptExecutor.ExecuteGlobal('GS_Set Quote Reprice Date')
			res = SqlHelper.GetFirst("SELECT Exchange_Rate FROM Currency_ExchangeRate_Mapping WHERE From_Currency = 'USD' AND To_Currency = '"+str(Quote.GetCustomField('Currency').Content)+"'")
			Quote.GetCustomField('Exchange Rate').Content = res.Exchange_Rate
			# Upon 1st time execution set the field to 0
			Quote.GetCustomField("CF_R2Q_FirstEdit").Content = '0' #-- H542832 : CXCPQ-51857 :end
			# If MPA Price Plan is not filled in then add the field value -- H542831 : CXCPQ-53006 :start
			if Quote.GetCustomField("MPA Price Plan").Content == "" and Quote.GetCustomField("MPA").Content != "":
				# fetch MPA Price Plan from database
				#ScriptExecutor.ExecuteGlobal('GS_SetDefaultPricePlan')
				from GS_SetDefaultPricePlan import setDefaultMpa
				setDefaultMpa(Quote,TagParserQuote)
			# Fetch the R2Q quote line items from SFDC -- H542832 : CXCPQ-51857 :start
			products = GS_R2Q_FunctionalUtil.getItem(Quote.GetCustomField("CF_R2Q_QuoteRef").Content)
			# Add the Quote line items to CPQ Quote
			productsAdded = GS_R2Q_FunctionalUtil.AddProducts(Quote, TagParserQuote, products)  #-- H542832 : CXCPQ-51857 :end
			if productsAdded and Quote.Items.Count < len(products): #-- H541049 : CXCPQ-52047 :start
				GS_R2Q_FunctionalUtil.UpdateStatusMessage(Quote, "Error", "Notification", Error.ProductAdditionError)
			elif productsAdded and Quote.Items.Count >= len(products):
				# Execute the approval script
				Quote.CalculateAndSaveCustomFields()
				ScriptExecutor.ExecuteGlobal('GS_ApprovalMessage')
				# Check if approval is required
				isAprovalRequired = TagParserQuote.ParseString("[AND]([NEQ](<*CTX( Quote.CustomField(IsApprovalNotRequired) )*>,1), [OR]([NEQ](<*CTX( Quote.CustomField(CF_MaxApprovalLevel) )*>,),[GT](<* TABLE ( SELECT count(*) FROM QT__EGAP_Approvers WHERE cartid = '<*CTX( Quote.CartId )*>' and ownerid = '<*CTX( Quote.OwnerId )*>') *>,0)),[NEQ](<*CTX(Quote.CustomField(EGAP_Highest_Price_Margin_Approval_Level))*>,No Approval))")
				if int(isAprovalRequired):
					# If the CPQ quote requires approval, then populate "Discount Request Reason" on CPQ Quote Info tab as "Sales Manager Discretion"
					Quote.GetCustomField("Discount Request Reason").Content = "Sales Manager Discretion"
					Quote.Save()
					# Execute the 'Request for Approval' custom action
					for action in Quote.Actions:
						if action.Name == "Request for Approval":
							Quote.ExecuteAction(action.Id)
							break
					if Quote.OrderStatus.Name == "Ready for Approval":
						ScriptExecutor.Execute('CPQ_SF_CreateUpdateOpportunity')
						GS_R2Q_FunctionalUtil.calculateQuoteDetails(Quote, TagParserQuote, StreamReader)
						GS_R2Q_FunctionalUtil.UpdateStatusMessage(Quote, "Approval Initiation", "Action", Success.ApprovalInitiated)
					else:
						GS_R2Q_FunctionalUtil.UpdateStatusMessage(Quote, "Error", "Notification", "Error occured during approval initiation.")
				else:
					# Generate and send Quote documents to SFDC
					ScriptExecutor.Execute('CPQ_SF_CreateUpdateOpportunity')
					GS_R2Q_FunctionalUtil.calculateQuoteDetails(Quote, TagParserQuote, StreamReader)
					if Quote.GetCustomField('Total_Sell_Price_Updated').Content in ["0", "", "0.0"]:
						import GS_CalculateTotals

						totalDict = GS_CalculateTotals.calculateQuoteTotals(Quote)
						Quote.GetCustomField('Total_Sell_Price_Updated').Content = str(totalDict.get('totalExtendedAmount',0))
					Quote.Save()
					genDoc = GS_R2Q_FunctionalUtil.R2QDocumentGeneration(Quote)
					if genDoc:
						# Change the staus to 'Submitted to Customer'
						Quote.ChangeQuoteStatus('Submitted to Customer')
						for action in Quote.Actions:
							if action.Name == "Make Quote Primary":
								Quote.ExecuteAction(action.Id)
								break
						Quote.Save()
						ScriptExecutor.Execute('CPQ_SF_CreateUpdateOpportunity')
						GS_R2Q_FunctionalUtil.calculateQuoteDetails(Quote, TagParserQuote, StreamReader)
						if Quote.OrderStatus.Name == "Submitted to Customer":
							GS_R2Q_FunctionalUtil.UpdateStatusMessage(Quote, "Final", "Action", Success.Submitted)
						else:
							GS_R2Q_FunctionalUtil.UpdateStatusMessage(Quote, "Error", "Notification", "Error occured during changing the status to Submitted to Customer.") #-- H541049 : CXCPQ-52047 : end

	ApiResponse=ApiResponseFactory.JsonResponse(responseBody)

except Exception as e:
	Log.Write("Exception occured as follows:
{0}".format(e))
	GS_R2Q_FunctionalUtil.UpdateStatusMessage(Quote, "Error", "Notification", str(e))
	Quote.Save()