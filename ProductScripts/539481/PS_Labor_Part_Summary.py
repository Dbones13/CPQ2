from PMC_MIQ_Update_System_Labor_Cost_Price import updateLaborCostPrice
if Quote:
    contList = ['MIQ Engineering Labor Container', 'MIQ Additional Custom Deliverables']
    partList = ["SVC-NT-EIT-E-FD-NC"]
    updateLaborCostPrice(Product, Quote, TagParserQuote, contList, True, partList, Session)

Product.Attr('PERF_ExecuteScripts').AssignValue('')