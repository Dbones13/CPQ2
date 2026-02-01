container = Product.Attr('Scada_CCR_Unit_Count').GetValue()
value = Product.GetContainerByName('Scada_CCR_Unit_Cont').Rows.Count

if container <= '10' and not ('1' <= value <= '10'):
    Product.Attr('ExceededLimit').AssignValue('')