if Product.Name == "Labor Deliverables":
    HW_ListPrice = float(Product.Attr('SC_Labor_Honeywell_List_Price').GetValue()) if Product.Attr('SC_Labor_Honeywell_List_Price').GetValue() else 0
    customer_ListPrice = float(Product.Attr('SC_Labor_Customer_List_Price').GetValue()) if Product.Attr('SC_Labor_Customer_List_Price').GetValue() else 0
    SC_Labor_PY_CustomerLP = float(Product.Attr('SC_Labor_PY_CustomerLP').GetValue()) if Product.Attr('SC_Labor_PY_CustomerLP').GetValue() else 0
    SC_Labor_PY_ResourceType = Product.Attr('SC_Labor_PY_ResourceType').GetValue().split(',')[0] if Product.Attr('SC_Labor_PY_ResourceType').GetValue() else 0
    deliv_hrs = float(Product.Attr('SC_Labor_Deliverable_Hours').GetValue()) if Product.Attr('SC_Labor_Deliverable_Hours').GetValue() else 0
    PY_deliv_hrs = float(Product.Attr('SC_Labor_PY_Deliverables_Hours').GetValue()) if Product.Attr('SC_Labor_PY_Deliverables_Hours').GetValue() else 0
    RT = Product.Attr('SC_Labor_Resource_Type').Values
    Country = Quote.GetCustomField('Opportunity Tab Booking Country').Content
    part = Product.Attr('SC_Labor_Resource_Type').GetValue().split(',')[0]

    table = SqlHelper.GetFirst("SELECT Work_Hour FROM CT_SC_Labor_ResourceType WHERE  PartNumber = '{}'and Country = '{}'".format(part,Country))
    workhrs_query = SqlHelper.GetFirst("select Work_Hour from CT_SC_LABOR_RESOURCETYPE where Country = '{0}' and (PartNumber = '{1}' or Type = '{1}')".format(Country,SC_Labor_PY_ResourceType))
    if table is not None:
        SC_Labor_total_HW_LP = ((HW_ListPrice) / float(table.Work_Hour) ) * (deliv_hrs)
        if Product.Attr('SC_Labor_Pricing_Escalation_Based').GetValue() != 'Yes':
            Product.Attr('SC_Labor_Customer_List_Price').AssignValue(str(round(HW_ListPrice,2)))
            customer_ListPrice = float(Product.Attr('SC_Labor_Customer_List_Price').GetValue()) if Product.Attr('SC_Labor_Customer_List_Price').GetValue() else 0
            SC_Labor_total_Customer_LP = ((customer_ListPrice) / float(table.Work_Hour) ) * (deliv_hrs)
        else:
            if Product.Attr('SC_Labor_Product_Type').GetValue() != '1':
                Product.Attr('SC_Labor_Customer_List_Price').AssignValue(str(round(SC_Labor_PY_CustomerLP,2)))
                SC_Labor_total_Customer_LP = 0
                if workhrs_query is not None:
                    if deliv_hrs > PY_deliv_hrs:
                        SC_Labor_total_Customer_LP = str((PY_deliv_hrs * float((SC_Labor_PY_CustomerLP) / float(workhrs_query.Work_Hour))) + ((deliv_hrs - PY_deliv_hrs)*float((customer_ListPrice) / float(table.Work_Hour))))
                    else:
                        SC_Labor_total_Customer_LP = ((SC_Labor_PY_CustomerLP) / float(workhrs_query.Work_Hour) ) * (deliv_hrs)
            else:
                Product.Attr('SC_Labor_Customer_List_Price').AssignValue(str(round(HW_ListPrice,2)))
                customer_ListPrice = float(Product.Attr('SC_Labor_Customer_List_Price').GetValue()) if Product.Attr('SC_Labor_Customer_List_Price').GetValue() else 0
                SC_Labor_total_Customer_LP = ((customer_ListPrice) / float(table.Work_Hour) ) * (deliv_hrs)

        Product.Attr('SC_Labor_total_HW_LP').AssignValue(str(SC_Labor_total_HW_LP))
        Product.Attr('SC_Labor_total_Customer_LP').AssignValue(str(SC_Labor_total_Customer_LP))

    RT1 = Product.Attr('SC_Labor_Resource_Type').SelectedValue.ValueCode if Product.Attr('SC_Labor_Resource_Type').SelectedValue != None else ''
    if RT1 == "":
        Product.Attr('SC_Labor_Honeywell_List_Price').AssignValue('')
        Product.Attr('SC_Labor_Burden_for_Hr_Day').AssignValue('')
        Product.Attr('SC_Labor_Hrs_per_Full_Day').AssignValue('')
        if Product.Attr('SC_Labor_Pricing_Escalation_Based').GetValue() != 'Yes':
            Product.Attr('SC_Labor_Customer_List_Price').AssignValue('')