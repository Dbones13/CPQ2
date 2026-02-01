if Quote.OrderStatus.Name in ['Submitted to Customer', 'Preparing', 'Accepted by Customer'] :
    today = UserPersonalizationHelper.ToUserFormat(DateTime.Now)
    Quote.GetCustomField('Quote Reprice Date').Content = today