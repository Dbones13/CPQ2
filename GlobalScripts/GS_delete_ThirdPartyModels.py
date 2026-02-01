models = Product.GetContainerByName('HWOS_Model Scope_3party')
m=[]
for i in models.Rows:
    if i.IsSelected :
        m.append(i.RowIndex)
m.reverse()
for i in m:
    models.DeleteRow(i)
    models.Calculate()
if Product.Name == 'Third Party':
    ent = Product.GetContainerByName('HWOS_Entitlement')
    entsInModels = []
    for i in models.Rows:
        entsInModels.append(i['Entitlement'])
    entsToDelete = []
    for i in ent.Rows:
        if i['Entitlement'] in entsInModels:
            pass
        else:
            entsToDelete.append(i.RowIndex)
    entsToDelete.reverse()
    for i in entsToDelete:
        ent.DeleteRow(i)
        ent.Calculate()
if Product.Name == "Training":
    models = Product.GetContainerByName('HWOS_Model Scope_3party_Training')
    m=[]
    for i in models.Rows:
        if i.IsSelected :
            m.append(i.RowIndex)
    m.reverse()
    for i in m:
        models.DeleteRow(i)
        models.Calculate()