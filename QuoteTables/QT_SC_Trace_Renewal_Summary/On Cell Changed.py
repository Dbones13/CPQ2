QT = Quote.QuoteTables['QT_SC_Trace_Renewal_Summary']
for qt_row in QT.Rows:
    qt_row['Total_Discount_Price'] = (qt_row['Final_List_Price']/100) * qt_row['Total_Discount']
    qt_row['Previous_Year_Sell_Price'] = qt_row['Previous_Year_List_Price'] - ((qt_row['Previous_Year_List_Price']/100)*qt_row['Last_Year_Discount'])
    qt_row['Final_Sell_Price'] = qt_row['Final_List_Price'] - qt_row['Total_Discount_Price']
    qt_row['Scope_Change'] = (qt_row['Scope_reduction_Price']*(qt_row['Previous_Year_Sell_Price']/qt_row['Previous_Year_List_Price'])) + (qt_row['Scope_Addition_Price']*(qt_row['Final_Sell_Price']/qt_row['Final_List_Price']))
    qt_row['Price_Impact'] = qt_row['Final_Sell_Price'] - (qt_row['Scope_Change'] + qt_row['Previous_Year_Sell_Price'])
    QT.Save()