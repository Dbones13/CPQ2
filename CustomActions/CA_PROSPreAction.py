pros_execution = Quote.GetCustomField("PROSActionField").Content
if pros_execution =='no':
    Quote.GetCustomField("PROSActionField").Content = 'yes'