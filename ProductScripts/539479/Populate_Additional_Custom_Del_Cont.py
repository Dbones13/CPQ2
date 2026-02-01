'''additionalDelData = [
	{
        "Deliverable Name" : "Commissining",
        "Final Hrs" : "16",
        "Standard Deliverable" : "Plant Commissioning, Start-up & Support",
        "GES Eng" : "SYS GES Eng-BO-IN",
        "FO Eng" : "SYS LE1-Lead Eng",
        "Execution Country" : "Australia"
    },
    {
        "Deliverable Name" : "Misc",
        "Final Hrs" : "24",
        "Standard Deliverable" : "Implement Other/Misc",
        "GES Eng" : "SYS GES Eng-BO-IN",
        "FO Eng" : "SYS LE1-Lead Eng",
        "Execution Country" : "Canada"
    }
]
Product.ExecuteRulesOnce = True
laborAddi = Product.GetContainerByName('C300_Additional_Custom_Deliverables_Container')
for data in additionalDelData:
    newRow = laborAddi.AddNewRow(False)
    newRow["Deliverable Name"] = data["Deliverable Name"]
    newRow["Final Hrs"] = data["Final Hrs"]
    newRow.GetColumnByName("Standard Deliverable").SetAttributeValue(data["Standard Deliverable"])
    newRow.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue(data["GES Eng"])
    newRow.GetColumnByName('FO Eng').ReferencingAttribute.SelectDisplayValue(data["FO Eng"])
    newRow["Execution Country"] = data["Execution Country"]
    newRow.ApplyProductChanges()
    newRow.Calculate()
laborAddi.Calculate()
Product.ExecuteRulesOnce = False'''
labor_cont = Product.GetContainerByName('C300_Additional_Custom_Deliverables_Container')
Booking_LOB = TagParserQuote.ParseString('<* QuoteProperty (Booking LOB) *>')
newRow = labor_cont.AddNewRow(False)
newRow.GetColumnByName('Standard Deliverable').SetAttributeValue("PEP-PQP-HSE-Org Chart-Schedule")
newRow['Standard Deliverable'] = "PEP-PQP-HSE-Org Chart-Schedule"
if Booking_LOB != 'LSS':
    '''not_allowed = ['SVC-PMGT-ST','SVC-ECON-ST','SVC-ESSS-ST','SVC-EAPS-ST','SVC-EST1-ST','SVC-PMGT-ST-NC','SVC-ECON-ST-NC','SVC-ESSS-ST-NC','SVC-EAPS-ST-NC','SVC-EST1-ST-NC']
    newRow.Product.DisallowAttrValues('C300_FO_ENG', *not_allowed)'''
    newRow.GetColumnByName('FO Eng').ReferencingAttribute.SelectDisplayValue('SYS LE1-Lead Eng')
    newRow['FO Eng'] = "SYS LE1-Lead Eng"
else:
    newRow.GetColumnByName('FO Eng').ReferencingAttribute.SelectDisplayValue('SVC-ESSS-ST Site Support Spec')
    newRow['FO Eng'] = "SVC-ESSS-ST Site Support Spec"
newRow.ApplyProductChanges()
newRow.Calculate()
labor_cont.Calculate()