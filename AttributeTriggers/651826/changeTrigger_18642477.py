container = Product.Attr('Number_of_Series_C_Control_Groups').GetValue()
value = Product.GetContainerByName('Series_C_Control_Groups_Cont').Rows.Count

if container <= '10' and not ('1' <= value <= '10'):
    Product.Attr('ExceededLimit').AssignValue('')