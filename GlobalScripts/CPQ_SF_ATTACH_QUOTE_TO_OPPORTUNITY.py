responseDictionary={}
responseDictionary["ActionResult"]="OK"
responseDictionary["Message"] = "Successfully"

# To be used after NewQuoteApi
# Replicate Apply CRM Mappings functionality
from CPQ_SF_FunctionModules import get_quote_opportunity_id
oppId = get_quote_opportunity_id(Quote)

listoferrors = []

if oppId:
    # Build Params
    # Uncomment once recieved from Parameter
    externalParameters = dict()
    externalParameters["opportunityid"] = oppId
    # Set User Session
    Session["apiSessionID"] = Quote.GetCustomField("CPQ_SF_SESSION_ID").Content
    # Trigger Create Quote Flow
    result = ScriptExecutor.Execute("CPQ_SF_CreateQuote_Attach", {"externalParameters": externalParameters, "createQuote": False})
    if result == "False":
        responseDictionary["ActionResult"]="NOK"
        responseDictionary["Message"] = "Quote is not created on SFDC side. CPQ_SF_SESSION_ID script error."
        Log.Error("Quote is not created on SFDC side. CPQ_SF_SESSION_ID script error.")
    if Quote.Messages:
        for err in Quote.Messages:
            listoferrors.append(err)
        responseDictionary["ActionResult"]="NOK"
        responseDictionary["Message"] = {"Info": listoferrors}
        try:
            responseDictionary["ErrorQuote"] = Quote.CompositeNumber
            Log.Error("Error Quote: " + Quote.CompositeNumber + "
 Message: " + str(listoferrors))
        except:
            responseDictionary["ErrorQuote"] = "No quote"
            Log.Error("Error Quote: No quote")
else:
    responseDictionary["ActionResult"]="NOK"
    responseDictionary["Message"] = "Opportunity ID is missing."
    Log.Error("Opportunity ID is missing.")

ApiResponse = ApiResponseFactory.JsonResponse(responseDictionary)