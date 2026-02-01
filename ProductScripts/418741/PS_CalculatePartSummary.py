iaa_container = Product.GetContainerByName("IAA Inputs_Cont")
iaa_container_2 = Product.GetContainerByName("IAA Inputs_Cont_2")
part_number_cont = Product.GetContainerByName("Pricing Parts")
assessments = dict()
total_qty = 0
def populateContainerQuantity(quantity):
    for partrow in part_number_cont.Rows:
        partrow["ItemQuantity"] = str(quantity)
        partrow.Product.Attributes.GetByName("ItemQuantity").AssignValue(str(quantity))
#        partrow.Product.ApplyRules() #Commented  ApplyRules on 11/7/2023: CXCPQ-70447
        partrow.ApplyProductChanges()

for row in iaa_container.Rows:
    assessments[row["IAA_Assessment_Type"]] = int(row['IAA_Quantity']) if row['IAA_Quantity'] != '' else 0
for row in iaa_container_2.Rows:
    assessments["IAA_How_many_SPBs_did_the_customer_purchase_in_the_last_12_months"] = int(row['Quantity']) if row['Quantity'] != '' else 0

entitlement = Quote.GetCustomField("Entitlement").Content
if entitlement in  ['K&E Pricing Plus', 'K&E Pricing Flex']:
    qty1 = assessments["Experion Standard IAA (0-200)"] + assessments["LCN/TPS Standard IAA (0-200)"] + assessments["Experion with TPS Standard IAA (0-200)"]
    qty2 = assessments["Experion System Performance Baseline (0-200)"] + assessments["LCN/TPS System Performance Baseline (0-200)"]
    total_qty = qty1 * 23 + qty2 * 8
else:
    qty1 = assessments["Experion Standard IAA (0-200)"] + assessments["LCN/TPS Standard IAA (0-200)"] + assessments["Experion with TPS Standard IAA (0-200)"] - assessments["IAA_How_many_SPBs_did_the_customer_purchase_in_the_last_12_months"]
    qty2 = assessments["Experion System Performance Baseline (0-200)"] + assessments["LCN/TPS System Performance Baseline (0-200)"]
    qty3 = assessments["IAA_How_many_SPBs_did_the_customer_purchase_in_the_last_12_months"]
    total_qty = qty1 * 23 + qty2 * 8 + (qty3 * 23 * 0.8)
populateContainerQuantity(total_qty)