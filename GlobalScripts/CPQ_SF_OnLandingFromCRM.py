from CPQ_SF_FunctionModules import is_action_allowed
from CPQ_SF_IntegrationSettings import CL_GeneralIntegrationSettings # SAP Case ref. 790977/2024 and 1140590/2024

# Constants
CREATE = "create"
EDIT = "edit"
NEW = "new"
VIEW = "view"
# action Edit -> Id = 13
EDIT_ACTION_ID = 13

# Get paramters
externalParameters = context.ExternalParameters
#Log.Info('External Parameters----'+str(externalParameters))
# Create Quote or Edit Quote
action = externalParameters["action"]
#Log.Info('Action1 ----'+str(action))

# Set SF User Session Token
Session["apiSessionID"] = externalParameters["apiSessionID"]
# Set Opportunity Id in Session
Session["OpportunityId"] = externalParameters["opportunityid"]

# Clear Session OnLandingFromCRM # SAP Case ref. 790977/2024 and 1140590/2024
Session["OpportunityId"] = None
Session["Query"] = None

# Dispose Quote from Session (If Quote was opened previously)
if Quote is not None:
    Quote.Dispose()

# Refresh Market Visibility
User.RefreshMarkets()

if action == CREATE:
    redirectionUrl = ScriptExecutor.Execute("CPQ_SF_CreateQuote", {"externalParameters": externalParameters, "createQuote": True})
elif action == EDIT: # SAP Case ref. 790977/2024 and 1140590/2024
    # Open active revision
    if CL_GeneralIntegrationSettings.ALL_REV_ATTACHED_TO_SAME_OPPORTUNITY:
        quoteNumber = externalParameters["quotenumber"]
        Quote = QuoteHelper.Edit(quoteNumber)
    # Open chosen revision
    else:
        quoteId = externalParameters["quoteId"]
        ownerId = externalParameters["ownerId"]
        Quote = QuoteHelper.Edit(float(ownerId), float(quoteId))

    if is_action_allowed(Quote, User, externalParameters, EDIT_ACTION_ID) == True:
        redirectionUrl = ScriptExecutor.Execute("CPQ_SF_EditQuote", {"externalParameters": externalParameters, "quote": Quote})
    else:
        redirectionUrl = ScriptExecutor.Execute("CPQ_SF_ViewQuote", {"externalParameters": externalParameters})
elif action == NEW:
    quoteId = externalParameters["quoteId"]
    ownerId = externalParameters["ownerId"]
    QuoteHelper.Edit(float(ownerId), float(quoteId))
    redirectionUrl = ScriptExecutor.Execute("CPQ_SF_LandingOnCatalogue")
elif action == VIEW:
    redirectionUrl = ScriptExecutor.Execute("CPQ_SF_ViewQuote", {"externalParameters": externalParameters})