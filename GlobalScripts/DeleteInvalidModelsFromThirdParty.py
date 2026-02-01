if Product.Name == "Training":
    tainingCont = Product.GetContainerByName('HWOS_Invalid_Model Scope_3party_Training')
    m=[]
    for i in tainingCont.Rows:
        if i.IsSelected :
            m.append(i.RowIndex)
    m.reverse()
    for i in m:
        tainingCont.DeleteRow(i)
        tainingCont.Calculate()
else:
    models = Product.GetContainerByName('HWOS_Invalid_Model Scope_3party')
    m=[]
    for i in models.Rows:
        if i.IsSelected :
            m.append(i.RowIndex)
    m.reverse()
    for i in m:
        models.DeleteRow(i)
        models.Calculate()