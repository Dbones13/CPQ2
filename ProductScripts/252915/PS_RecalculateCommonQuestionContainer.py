con = Product.GetContainerByName('MSID_CommonQuestions')
row = con.AddNewRow()
con.DeleteRow(row.RowIndex)
con.Calculate()