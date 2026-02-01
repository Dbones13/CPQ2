Product.Attr("R2QRequest").AssignValue("Yes")
#Trace.Write("QuoteNumber:"+str(Quote.CompositeNumber))
Product.Attr("R2Q_QuoteNumber").AssignValue(str(Quote.CompositeNumber))
#Trace.Write(Product.Attr("R2Q_QuoteNumber").GetValue())
Product.Attr("Order_Status").AssignValue(str(Quote.OrderStatus.Name))
#Product.Attr("R2Q_EGAP_Approval").AssignValue(str(Quote.GetCustomField('EGAP_Highest_Approval_Level_for_the_Quote').Content))
Product.Attr('R2Q_EGAP_Approval').AssignValue(str(Quote.GetCustomField('R2Q_Save').Content))
Product.Attr('Labor_Percentage_FAT').AssignValue('100')