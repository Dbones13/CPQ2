def deleteRows(table , ids):
    for id in ids:
        table.DeleteRow(id)

def populateQuoteTableRow(table , dataDict , row = None):
    if not row:
        row = table.AddNewRow()
    for key , value in dataDict.items():
        row[key] = value

def fn_get_yspec_info(yqt,yso,yspectable):
    remain_data = SqlHelper.GetList("SELECT DISTINCT Yspecial_Quote,Sub_Option,LP_Part,Sample_Model,Comments,Y_Description FROM {} WHERE Yspecial_Quote = '{}' AND Sub_Option = '{}'".format(yspectable,yqt,yso))
    Trace.Write("SELECT DISTINCT Yspecial_Quote,Sub_Option,LP_Part FROM {} WHERE Yspecial_Quote = '{}' AND Sub_Option = '{}'".format(yspectable,yqt,yso))
    final_list = []
    for rw in remain_data:
        final_list.append([rw.Yspecial_Quote,rw.Y_Description,rw.Comments,rw.LP_Part,rw.Sub_Option,rw.Sample_Model])
    return final_list

def fet_Qtrows():
    try:
        Yspec_data_Lookedup=Quote.GetGlobal('Yspec_data_Lookedup')
        final_list = []
        if Yspec_data_Lookedup != 'Yes':
            remain_data = SqlHelper.GetList("SELECT * FROM QT__Yspecial_Selection WHERE cartid = '{}' AND CartItemGUID = '{}' AND MainPart = '{}'".format(str(Quote.QuoteId),TagParserProduct.ParseString("<*CTX( Quote.CurrentItem.CartItemGuid )*>"),Product.PartNumber))
            Trace.Write('Row cnt:'+str(remain_data.Count))
            Trace.Write('QuoteId:'+str(Quote.QuoteId))
            Trace.Write('CartItemGuid:'+str(TagParserProduct.ParseString("<*CTX( Quote.CurrentItem.CartItemGuid )*>")))
            Trace.Write('PartNumber:'+str(Product.PartNumber))
            for rw in remain_data:
                Trace.Write('In Loop:'+ str(rw.Yspecial_Quote) + ':' +str(rw.CartItemGUID))
                final_list.append([rw.Yspecial_Quote,rw.Y_Description,rw.Comments,rw.LP_Part,rw.Sub_Option,rw.Sample_Model])
            Quote.SetGlobal('Yspec_data_Lookedup', 'Yes')
        return final_list
    except:
    	Trace.Write('in excep')



action = Param.action
yqt = Param.yqt
yso = Param.yso
if Quote.GetCustomField('Sales Area').Content == "1109":
    yspectable = "YSpecial_US"
else:
    yspectable = "YSpecial"
if action == "get_yspec_info":
    ApiResponse = ApiResponseFactory.JsonResponse(fn_get_yspec_info(yqt,yso,yspectable))
if action == "view":
    ApiResponse = ApiResponseFactory.JsonResponse(fet_Qtrows())
if action == "add":
	yspec_json_data=str(Param.yspec_json_data)
	yspec_row_cnt=str(Param.yspec_row_cnt)
	Quote.SetGlobal('G_yspec_json_data', yspec_json_data)
	Quote.SetGlobal('G_yspec_row_cnt', yspec_row_cnt)