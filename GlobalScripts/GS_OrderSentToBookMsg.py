OrderId = Quote.GetCustomField("CF_SalesOrderId").Content if Quote.GetCustomField("CF_Manual_Booking").Content == 'True' else Quote.OrderId
if OrderId == '' and Quote.OrderStatus.Name == "Pending Order Confirmation":
    if not Quote.Messages.Contains(Translation.Get('message.orderSentToBooked')):
        Quote.Messages.Add(Translation.Get('message.orderSentToBooked'))
if Quote.GetCustomField('OrderProcessingIssue').Content != '' and Quote.OrderStatus.Name == "Accepted by Customer":
    if not Quote.Messages.Contains(Translation.Get('message.OrderProcessing.issue')):
        Quote.Messages.Add(Translation.Get('message.OrderProcessing.issue'))
if OrderId != '' and Quote.OrderStatus.Name == "Booked":
    if not Quote.Messages.Contains(Translation.Get('message.orderBooked').format(OrderId)):
        Quote.Messages.Add(Translation.Get('message.orderBooked').format(OrderId))