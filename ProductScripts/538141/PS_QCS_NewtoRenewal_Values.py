if Product.Name != "Service Contract Products":
    if Product.Attr('SC_Product_Type').GetValue() == "Renewal":
        Exchange_Rate = float(Quote.GetCustomField('SC_CF_PRVYR_EXCH_RATE').Content) if Quote.GetCustomField('SC_CF_PRVYR_EXCH_RATE').Content else 1
        Subscription_Tier= Product.Attr('SC_QCS_Subscription Tier').GetValue()
        Product.Attr('SC_QCS_Subscription_Tier_PY').AssignValue(str(Subscription_Tier))
        Number_of_Machines= Product.Attr('SC_QCS_Number of Machines').GetValue()
        Number_of_Machines_Support_Centre= Product.Attr('SC_QCS_No_Of_Machines').GetValue()
        ComparisonSummary = Product.GetContainerByName("ComparisonSummary")
        Hidden_QCS_One_Time_Price= float(Product.Attr('Hidden_QCS_One_Time_Price').GetValue()) * Exchange_Rate
        Product.Attr('UI_QCS_One_Time_Price').AssignValue(str(Hidden_QCS_One_Time_Price)) if Hidden_QCS_One_Time_Price != "" else "0"
        if ComparisonSummary.Rows.Count:
            for row in ComparisonSummary.Rows:
                if row['Service_Product'] == "QCS 4.0":
                    Product.Attr('SC_QCS_Number of Machines_Py').AssignValue(str(Number_of_Machines))
                elif row['Service_Product'] == "QCS Support Center":
                    Product.Attr('SC_QCS_No_Of_Machines_Py').AssignValue(str(Number_of_Machines_Support_Centre))
                else:
                    Product.Attr('SC_QCS_Number of Machines_Py').AssignValue(str(0))
                    Product.Attr('SC_QCS_No_Of_Machines_Py').AssignValue(str(0))

        Additional_Cont = Product.GetContainerByName("SC_QCS_Pricing_Details_Cont_Additional")
        if Additional_Cont.Rows.Count:
            for row in Additional_Cont.Rows:
                row['PY_ListPrice'] = str(float(row['CY_ListPrice']) * Exchange_Rate) if row['CY_ListPrice'] else '0'
                row.Calculate()
                row['CY_ListPrice'] = '0'
                row.Calculate()
            Additional_Cont.Calculate()
    Product.Attr('SC_Renewal_check').AssignValue('1')
