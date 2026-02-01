subLOB = Quote.GetCustomField("Sub-LOB").Content
proposalTemplate = Quote.GetCustomField("Proposal Template Type").Content
attValues1 = Quote.GetCustomField("Proposal Template Type").AttributeValues
attValues2 = Quote.GetCustomField("PMC BOM").AttributeValues

if subLOB == '':
    Quote.GetCustomField("Proposal Template Type").Visible = False
else:
    Quote.GetCustomField("Proposal Template Type").Visible = True

def hideShowOptions(attValues,dropdownList):
    for value in attValues:
        if value.DisplayValue in dropdownList:
            value.Allowed = True
        else:
            value.Allowed = False

if subLOB == "PMC Terminal Automation":
    hideShowOptions(attValues1,['Terminal Automation Standard Form','Terminal Automation SVP Standard Form'])

if subLOB == "PMC Field Products":
    hideShowOptions(attValues1,['FP Standard Form','FP Long Form', 'FP Worksheet'])

if proposalTemplate == "FP Long Form":
    for value in attValues2:
        if value.DisplayValue == 'BOM No Price':
            value.Allowed = True
        else:
            value.Allowed = False
else:
    for value in attValues2:
        value.Allowed = True

if subLOB == "PMC Gas Products":
    hideShowOptions(attValues1,['Gas Standard Form English','Gas Standard Form German','MIQ Template','PMC Productized Skid Template'])
    hideShowOptions(attValues2,['BOM Sell Price'])

if subLOB == "PMC Marine Products":
	hideShowOptions(attValues1,['PMC Marine Gauging product Form','PMC Marine Gauging Spares Form'])