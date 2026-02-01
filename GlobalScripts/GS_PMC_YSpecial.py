# ========================================================================================================
#   Component: GS_PMC_YSpecial
#   Copyright: Honeywell Inc
#   Purpose: - This script is used to fetch YSpecial information on cart page.
# ========================================================================================================
import re
def YSpecial_Set(y_quote,y_desc,y_adder,y_total,y_list,y_cost):
    Trace.Write(str(y_quote)+"--GS_PMC_YSpecial--set-->"+str(y_adder))
    ace_quote = re.sub(r'[^a-zA-Z0-9\s]', '', y_quote)
    ace_desc = re.sub(r'[^a-zA-Z0-9\s]', '', y_desc)
    Product.SetGlobal('y_quote',ace_quote)
    Product.SetGlobal('y_desc',ace_desc)
    Product.SetGlobal('y_list',y_list)
    Product.SetGlobal('y_cost',y_cost)
    if y_adder:
        Product.SetGlobal('y_adder', 'Adder')
    elif y_total:
        Product.SetGlobal('y_adder', 'Total LP')
    return Quote.GetGlobal('y_quote'),Quote.GetGlobal('y_desc'),Quote.GetGlobal('y_list'),Quote.GetGlobal('y_cost'),Quote.GetGlobal('y_adder')

def YSpecial_Get():
    curr_item = TagParserProduct.ParseString('<*CTX( Quote.CurrentItem.CartItemGuid )*>')
    Trace.Write(str()+"--GS_PMC_YSpecial--get-->"+str(curr_item))
    for item in Quote.Items:
		if item.PartNumber==Product.PartNumber and item.QuoteItemGuid==curr_item and item.MrcListPrice:
			#Trace.Write(str(item.QuoteItemGuid)+"--->"+str(dir(item)))
			return item['QI_Ace_Quote_Number'].Value,item['QI_Ace_Description'].Value,item['QI_Adder_LP'].Value,item.MrcListPrice,item.MrcCost
    return ''
def YSpecial_Type():
	query = "select PartNumber,family_code from PMC_GASETO_YSPEC_MARINE_PRODUCTS where PartNumber = '{}'".format(Product.PartNumber)
	result = SqlHelper.GetFirst(query)
	if result is not None:
		result = SqlHelper.GetFirst(query)
		#Trace.Write("---->"+str(result.family_code))
        return result.family_code
	return ''

if Param.y_special=='set':
    ApiResponse = ApiResponseFactory.JsonResponse(YSpecial_Set(Param.y_quote,Param.y_desc,Param.y_adder,Param.y_total,Param.y_list,Param.y_cost))
elif Param.y_special=='get':
    ApiResponse = ApiResponseFactory.JsonResponse(YSpecial_Get())
elif Param.y_special=='type':
    ApiResponse = ApiResponseFactory.JsonResponse(YSpecial_Type())
