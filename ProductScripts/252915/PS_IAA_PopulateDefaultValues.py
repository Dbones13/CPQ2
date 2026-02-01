productList = Product.Attr("MSID_Selected_Products").GetValue().split('<br>')
if "Integrated Automation Assessment (IAA)" in productList:
    from GS_Integrated_Automation_Assessment_Util import IAA
    pricing_list = ["Integrated Automation Assessment / SPB"]
    product = IAA(Product)
    if Product.GetContainerByName("IAA Pricing").Rows.Count == 0:
    	product.PopulateIAAPricingContainerRows(pricing_list)
    if Product.GetContainerByName("IAA Inputs_Cont_2").Rows.Count == 0 or Product.GetContainerByName("IAA Inputs_Cont").Rows.Count == 0:
    	product.PopulateAssessmentRows()