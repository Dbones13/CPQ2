if Quote.GetCustomField("isR2QRequest").Content != 'Yes':
    sData = SqlHelper.GetFirst("select count(*) Total from MPA_PRICE_PLAN_MAPPING where Honeywell_Ref = '{}' and Price_Plan_Status= 'Active' and Price_Plan_Parts_Discount = 'Y' and Price_Plan_Start_Date < '{}' and Price_Plan_End_Date > '{}' and Honeywell_Ref <>''".format(Quote.GetCustomField('MPA Honeywell Ref').Content, DateTime.Now.ToString('MM/dd/yyyy'), DateTime.Now.ToString('MM/dd/yyyy')))
    if sData.Total > 0:
        Product.Attr('MSID_Active_Service_Contract').SelectValue('Yes')
        Product.Attr('MSID_Active_Service_Contract').Access = AttributeAccess.Hidden