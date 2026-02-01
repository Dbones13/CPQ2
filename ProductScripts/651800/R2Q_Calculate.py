import GS_R2Q_FunctionalUtil
from GS_FinalizedActivities import PopulateFinalizedActivities
try:
    if Product.Attr('R2QRequest').GetValue() == 'Yes' and Quote.GetCustomField("R2Q_Save").Content == "Submit":
        SelectedProducts = Product.GetContainerByName('Cyber Configurations')
        for row in SelectedProducts.Rows:
            if row['Part Desc'] not in ['Project Management','Cyber Generic System']:
                row.Product.Attr('calculate_value_set').AssignValue('True')
                PopulateFinalizedActivities(row.Product)
                row.ApplyProductChanges()
        Product.Attr('calculate_value_set').AssignValue('True')
        Product.ApplyRules()

except Exception as ex:
	msg = 'Error Occured, {"ErrorCode": "PartsLaborConfig", "ErrorDescription": "Failed at: Add to Quote"}'
	GS_R2Q_FunctionalUtil.UpdateStatusMessage(Quote, "Error", "Notification", msg)
	raise