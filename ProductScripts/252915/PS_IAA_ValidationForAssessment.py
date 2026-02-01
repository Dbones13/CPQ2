productList = Product.Attr("MSID_Selected_Products").GetValue().split('<br>')
if "Integrated Automation Assessment (IAA)" in productList:
    from GS_Integrated_Automation_Assessment_Util import IAA
    product = IAA(Product)
    product.ValidationForAssessment()