cont = Product.GetContainerByName('Number_SM_Remote_Groups_Cont')
if cont.Rows.Count > 0:
    row = cont.Rows[0]
    col = row.GetColumnByName('Number_SM_Remote_Groups')
    col.HeaderLabel = TagParserProduct.ParseString('Number of Remote Groups for <*VALUE(SM_CG_Name)*> (0-15)')