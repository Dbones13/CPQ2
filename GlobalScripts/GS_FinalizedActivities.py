# =========================================================================================================
#   Component: GS_FinalizedActivities
#      Author: Mangal Jagtap
#   Copyright: Honeywell Inc
#     Purpose: Finalize the activities based on selection and line items
#     Execute: Before Adding to Quote
# ========================================================================================================
def getFloat(Var):
    if Var:
        return float(Var)
    return 0

def addFinalActivities(product,final_activities):

    partsummary = product.GetContainerByName('AR_Cyber_PartsSummary')
    
    updated_item_list_dict = {}
    
    for part_row in partsummary.Rows:
        updated_item_list_dict[part_row['PartNumber']] = int(float(part_row['Final Quantity']))
    
    delete_list = []
    
    for row in final_activities.Rows:
        part_number = row.Product.PartNumber
        if part_number in updated_item_list_dict.keys() and updated_item_list_dict[part_number] >0:
            row.Product.Attr("ItemQuantity").AssignValue(str(updated_item_list_dict[part_number]))
            row.ApplyProductChanges()            
            updated_item_list_dict.pop(part_number, None)
        else:
            delete_list.append(row.RowIndex)

    if delete_list:
        for row_index in sorted(delete_list, reverse=True):
            final_activities.DeleteRow(row_index)

    if updated_item_list_dict:
        for part_number,final_quantity in updated_item_list_dict.items():
            if final_quantity>0:
                newRow = final_activities.AddNewRow(part_number, False)
                newRow.Product.Attr("ItemQuantity").AssignValue(str(final_quantity))
                newRow.ApplyProductChanges()
            
    final_activities.Calculate()
    product.ApplyRules()

def PopulateFinalizedActivities(product):
    final_activities = product.GetContainerByName('Final_Activities')
    addFinalActivities(product,final_activities)