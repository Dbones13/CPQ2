container = Product.Attr('Number of Experion Enterprise Groups').GetValue()
value = Product.GetContainerByName('Experion_Enterprise_Cont').Rows.Count

if container <= '1' and not ('1' <= value <= '1'):
    Product.Attr('ExceededLimit').AssignValue('')