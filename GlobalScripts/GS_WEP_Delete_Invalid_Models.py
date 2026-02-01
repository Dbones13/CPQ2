tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
if 'Honeywell Integrated Field App' in tabs:
    hifInvalid = Product.GetContainerByName("SC_WEP_Invalid_Models_HIF")
    m = []
    for row in hifInvalid.Rows:
        if row.IsSelected:
            m.append(row.RowIndex)
    m.reverse()
    for i in m:
        hifInvalid.DeleteRow(i)
        hifInvalid.Calculate()
elif 'Immersive Field Simulator' in tabs:
    ifsInvalid = Product.GetContainerByName("SC_WEP_Invalid_Models_IFS")
    m = []
    for row in ifsInvalid.Rows:
        if row.IsSelected:
            m.append(row.RowIndex)
    m.reverse()
    for i in m:
        ifsInvalid.DeleteRow(i)
        ifsInvalid.Calculate()
elif 'HALO OA' in tabs:
    haloInvalid = Product.GetContainerByName("SC_WEP_Invalid_Models_Halo")
    m = []
    for row in haloInvalid.Rows:
        if row.IsSelected:
            m.append(row.RowIndex)
    m.reverse()
    for i in m:
        haloInvalid.DeleteRow(i)
        haloInvalid.Calculate()
elif 'Training' in tabs:
    trainingInvalid = Product.GetContainerByName("SC_WEP_Invalid_Models_Training")
    m = []
    for row in trainingInvalid.Rows:
        if row.IsSelected:
            m.append(row.RowIndex)
    m.reverse()
    for i in m:
        trainingInvalid.DeleteRow(i)
        trainingInvalid.Calculate()
elif 'Training Needs Assessment' in tabs:
    tnaInvalid = Product.GetContainerByName("SC_WEP_Invalid_Models_TNA")
    m = []
    for row in tnaInvalid.Rows:
        if row.IsSelected:
            m.append(row.RowIndex)
    m.reverse()
    for i in m:
        tnaInvalid.DeleteRow(i)
        tnaInvalid.Calculate()