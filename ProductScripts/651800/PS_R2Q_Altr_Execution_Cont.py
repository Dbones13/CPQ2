import datetime
if Quote.GetCustomField('IsR2QRequest').Content:
    pole = Quote.GetCustomField('R2Q_Booking_Pole').Content
    if pole == 'APAC':
        allowlist = ['India','None']
    elif pole == 'EMEA':
        allowlist = ['France', 'Finland', 'Italy', 'United Kingdom','None']
    elif pole == 'AMER':
        allowlist = ['United States', 'Canada','None']
    else:
        allowlist = []

    disallowlist = []

    attr_val = Product.Attr("R2Q_Alternate_Execution_Country").Values
    disallowlist = [i.ValueCode for i in attr_val if i.ValueCode not in allowlist]
    Product.DisallowAttrValues("R2Q_Alternate_Execution_Country", *disallowlist)
    alncntry_length = len(allowlist)
    if alncntry_length == 2 and allowlist[1] == 'None':
		Product.Attributes.GetByName('R2Q_Alternate_Execution_Country').SelectDisplayValue(allowlist[0])

    if Product.Attr('Sell Price Strategy').SelectedValue.Display == 'Customer Budget':
        Product.AllowAttr('Customer_Budget_TextField')
        Product.AllowAttr('Customer_Budget_USD')
        Product.Attr('Customer_Budget_USD').Access = AttributeAccess.ReadOnly
        customerBudget = Product.Attr('Customer_Budget_TextField').GetValue()
        Quote_Currency = Quote.GetCustomField("SC_CF_CURRENCY").Content
        if customerBudget and Quote_Currency !='USD':
            from GS_Curr_ExchRate_Mod import fn_get_curr_exchrate
            exchange_rate = fn_get_curr_exchrate(Quote_Currency, "USD")
            cust_bud_usd = round(float(customerBudget)*exchange_rate, 2)
            formatted_value = "{:,.2f}".format(cust_bud_usd)
            Product.Attr('Customer_Budget_USD').AssignValue(str(formatted_value))
        else:
            Product.Attr('Customer_Budget_USD').AssignValue('')
    else:
        Product.DisallowAttr('Customer_Budget_TextField')
        Product.DisallowAttr('Customer_Budget_USD')

    current_year = datetime.datetime.now().year
    #yearlist = [str(current_year+i) for i in range(0,4)]
    yearlist = [str(current_year)]
    a=Product.Attr("Project_Execution_Year").Values
    removelist = [i.ValueCode for i in a if i.ValueCode not in yearlist]
    Product.DisallowAttrValues("Project_Execution_Year",*removelist)