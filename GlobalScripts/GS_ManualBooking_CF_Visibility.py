if User.BelongsToPermissionGroup('GCC place order Group') and Quote.GetCustomField('Quote Type').Content not in ('Contract New','Contract Renewal'):
    Quote.GetCustomField('CF_Manual_Booking').Editable = True
    ManualBook = Quote.GetCustomField('CF_Manual_Booking').Content
    if ManualBook == 'True':
        Quote.GetCustomField('CF_ProjectId').Editable = Quote.GetCustomField('CF_SalesOrderId').Editable = True
    else:
        Quote.GetCustomField('CF_ProjectId').Editable = Quote.GetCustomField('CF_SalesOrderId').Editable = False
else:
    Quote.GetCustomField('CF_Manual_Booking').Editable = False
