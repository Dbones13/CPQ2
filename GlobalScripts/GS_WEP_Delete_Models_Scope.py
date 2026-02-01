tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
if 'Honeywell Integrated Field App' in tabs:
    hifvalid = Product.GetContainerByName("SC_WEP_Models_Scope_HIF")
    m = []
    for row in hifvalid.Rows:
        if row.IsSelected:
            m.append(row.RowIndex)
    m.reverse()
    for i in m:
        hifvalid.DeleteRow(i)
        hifvalid.Calculate()
    ScriptExecutor.Execute('PS_HIF_Error_Message')
elif 'Immersive Field Simulator' in tabs:
    ifsvalid = Product.GetContainerByName("SC_WEP_Models_Scope_IFS")
    m = []
    for row in ifsvalid.Rows:
        if row.IsSelected:
            m.append(row.RowIndex)
    m.reverse()
    for i in m:
        ifsvalid.DeleteRow(i)
        ifsvalid.Calculate()
    ScriptExecutor.Execute('PS_IFS_Error_Message')
elif 'HALO OA' in tabs:
    halovalid = Product.GetContainerByName("SC_WEP_Models_Scope_Halo")
    m = []
    for row in halovalid.Rows:
        if row.IsSelected:
            m.append(row.RowIndex)
    m.reverse()
    for i in m:
        halovalid.DeleteRow(i)
        halovalid.Calculate()
    ScriptExecutor.Execute('PS_Halo_Error_Message')
elif 'Training' in tabs:
    trainingvalid = Product.GetContainerByName("SC_WEP_Models_Scope_Training")
    m = []
    for row in trainingvalid.Rows:
        if row.IsSelected:
            m.append(row.RowIndex)
    m.reverse()
    for i in m:
        trainingvalid.DeleteRow(i)
        trainingvalid.Calculate()
    ScriptExecutor.Execute('PS_Training_Error_Message')
elif 'Training Needs Assessment' in tabs:
    tnavalid = Product.GetContainerByName("SC_WEP_Models_Scope_TNA")
    m = []
    for row in tnavalid.Rows:
        if row.IsSelected:
            m.append(row.RowIndex)
    m.reverse()
    for i in m:
        tnavalid.DeleteRow(i)
        tnavalid.Calculate()
    ScriptExecutor.Execute('PS_TNA_Error_Message')
if len(m)>0:
    Product.Attr('SC_Product_Status').AssignValue("0")