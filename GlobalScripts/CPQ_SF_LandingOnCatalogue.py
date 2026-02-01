from CPQ_SF_Configuration import CL_CPQSettings

redirectionUrl = CL_CPQSettings.CPQ_URL + "/quotation/Cart.aspx"
ScriptExecutor.Execute("CPQ_SF_ATTACH_QUOTE_TO_OPPORTUNITY")
Result = str(redirectionUrl)