models = Product.GetContainerByName('SC_InvalidModels_HR_RWL')
m=[]
for i in models.Rows:
    if i.IsSelected :
        m.append(i.RowIndex)
m.reverse()
for i in m:
    models.DeleteRow(i)
    models.Calculate()