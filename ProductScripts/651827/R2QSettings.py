if Quote.GetCustomField('R2QFlag').Content != 'Yes':
    Quote.GetCustomField('IsR2QRequest').Content = Quote.GetCustomField('R2QFlag').Content
    Product.DisallowAttr('Sell Price Strategy')
    Product.DisallowAttr('AR_HCI_Proposal Language')
Quote.GetCustomField('R2Q_PRJT_Execution_Year').Content = Product.Attr('Project_Execution_Year').GetValue()
Product.Attr("Order_Status").AssignValue(str(Quote.OrderStatus.Name))
Product.Attr("R2QRequest").AssignValue("")
if Quote.GetCustomField('IsR2QRequest').Content == 'Yes':
	Product.Attr("R2QRequest").AssignValue("Yes")
	Product.Attr('R2Q_EGAP_Approval').AssignValue(str(Quote.GetCustomField('R2Q_Save').Content))
	Log.Info('Quote.CompositeNumber HCI--'+str(Quote.CompositeNumber))
	Product.Attr("R2Q_QuoteNumber").AssignValue(str(Quote.CompositeNumber))