if Product.GetContainerByName('CE_General_Inputs_Cont') is not None:
    if Product.GetContainerByName('CE_General_Inputs_Cont').Rows.Count > 0:
        msid = Product.GetContainerByName('CE_General_Inputs_Cont').Rows[0].GetColumnByName('CE_System_Asset').Value
        Trace.Write("MSID: {0}".format(msid))
        Quote.GetCustomField('DCS_MSID').Content = msid