CE_General_Inputs_Cont = Product.GetContainerByName('CE_General_Inputs_Cont')
if CE_General_Inputs_Cont.Rows.Count == 1:
    CE_Cutover = CE_General_Inputs_Cont.Rows[0].GetColumnByName('CE_Cutover').Value
    Product.Attr('CE_Cutover').AssignValue(CE_Cutover)