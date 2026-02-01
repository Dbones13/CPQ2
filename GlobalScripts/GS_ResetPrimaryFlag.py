if Quote.OrderStatus.Name == "Preparing":
    Quote.GetCustomField('IsPrimary').Content = ''
    Quote.Save(False)