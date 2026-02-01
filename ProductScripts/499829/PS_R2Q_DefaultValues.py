isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
if isR2Qquote:
    Product.Attr("Trace_Software_Architecture_drawing_update").SelectDisplayValue('No')
    Product.Attr("Trace_Software_Is_this_a_customized_installation").SelectDisplayValue('No')
    Product.Attr('Trace_Software_Business_Level_Access').SelectDisplayValue('Yes')
    Product.Attr('Trace_Software_Number_of_Concurrent_Users').SelectDisplayValue('Up to 5 users')
    transpose_container = Product.GetContainerByName('Trace_Software_License_Configuration_transpose')
    for row in transpose_container.Rows:
        row.Product.Attr('Trace_Software_Number_of_Concurrent_Users').SelectValue('Up to 5 users')
        row['Trace_Software_Number_of_Concurrent_Users'] = 'Up to 5 users'
        row['Trace_Software_Years_of_Support'] = '1'