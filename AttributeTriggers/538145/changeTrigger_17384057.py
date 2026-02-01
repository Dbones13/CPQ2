SC_Number_of_Concurrent_Users_PY = Product.Attr('SC_Number_of_Concurrent_Users_PY').GetValue()

if SC_Number_of_Concurrent_Users_PY == "Up to 5 users":
    Product.Attr('SC_Standard_User_CALs_PY').AssignValue('5')

elif SC_Number_of_Concurrent_Users_PY == "6 to 10 user":
    Product.Attr('SC_Standard_User_CALs_PY').AssignValue('10')

elif SC_Number_of_Concurrent_Users_PY == "11 to 15 user":
    Product.Attr('SC_Standard_User_CALs_PY').AssignValue('15')

elif SC_Number_of_Concurrent_Users_PY == "More than 15 user":
    Product.Attr('SC_Standard_User_CALs_PY').AssignValue('16')