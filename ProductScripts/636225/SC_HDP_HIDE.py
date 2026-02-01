Cont= Product.GetContainerByName('SC_SESP_MultiSites')
MSID=Product.GetContainerByName('SC_MSID_Container')

for rows in Cont.Rows:
    Trace.Write(rows.IsSelected)
    if rows.IsSelected== False:
        MSID.Rows.Clear()