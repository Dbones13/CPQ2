import GS_R2Q_FunctionalUtil

Log.Info('GS_R2Q_Error_Notification Param-->>' + str(JsonHelper.Serialize(Param).encode("ascii", "replace").replace('?','')).strip())

actionName = Param.ActionName
FailureMessage = Param.FailureMessage

Quote = QuoteHelper.Edit(Param.QuoteNumber)

errorCodeMap = {
    "R2Q_Gs_PartsummaryforPrjt": "PartsLaborConfig",
    "Cabinet Count": "DiscountPricing",
    "Experion Calculation": "DiscountPricing",
    "WriteIn": "PartsLaborConfig",
    "System Architecture": "DocumentGeneration",
    "Reprice": "DocumentGeneration"
}

if actionName in errorCodeMap:
    errCode = "PartsLaborConfig" if FailureMessage == 'Quote has incomplete products' else errorCodeMap[actionName]
    errorDescription = "Failed at: " + ("Parts & Labor Configuration" if FailureMessage == 'Quote has incomplete products' else actionName) + ". Error Message: " + FailureMessage if FailureMessage else ""
elif FailureMessage == 'Wait time exceeded 20 mins':
    errCode = "PartsLaborConfig"
    errorDescription = "Failed at: " + actionName + " - Waiting Time Exceeded"
else:
    errCode = "PartsLaborConfig"
    errorDescription = "Failed at: " + FailureMessage + " " + actionName

msg = 'Error Occurred, {"ErrorCode": "' + errCode + '", "ErrorDescription": "' + errorDescription + '"}'

Log.Info('GS_R2Q_Error_Notification msg-->>' + msg)

GS_R2Q_FunctionalUtil.UpdateStatusMessage(Quote, "Error", "Notification", msg)