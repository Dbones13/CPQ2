SC_Number_of_Concurrent_Users = Product.Attr('SC_Number_of_Concurrent_Users').GetValue()

if SC_Number_of_Concurrent_Users == "Up to 5 users":
    Product.Attr('SC_Standard_User_CALs').AssignValue('5')

elif SC_Number_of_Concurrent_Users == "6 to 10 user":
    Product.Attr('SC_Standard_User_CALs').AssignValue('10')

elif SC_Number_of_Concurrent_Users == "11 to 15 user":
    Product.Attr('SC_Standard_User_CALs').AssignValue('15')

elif SC_Number_of_Concurrent_Users == "More than 15 user":
    Product.Attr('SC_Standard_User_CALs').AssignValue('16')
Product.Attr('SC_Product_Status').AssignValue("0")