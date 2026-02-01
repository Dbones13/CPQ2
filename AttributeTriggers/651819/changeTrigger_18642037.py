container = Product.Attr('ES_Count').GetValue()
value = Product.GetContainerByName('ES_Group').Rows.Count

if container <= '1' and not ('1' <= value <= '1'):
    Product.Attr('ExceededLimit').AssignValue('')