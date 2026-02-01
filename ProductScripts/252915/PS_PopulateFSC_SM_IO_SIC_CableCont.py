msid_cont = Product.GetContainerByName('MSID_Product_Container')

for row in msid_cont.Rows:
    if row['Product Name'] == 'FSC to SM IO Migration':
        sic_cont = Product.GetContainerByName('FSC_SM_IO_SIC_Cable')
        if sic_cont.Rows.Count == 0:
            values=['3 mts','5 mts','6 mts','8 mts','10 mts','15 mts','20 mts','25 mts','30 mts']
            for value in values:
                new_row = sic_cont.AddNewRow()
                new_row.GetColumnByName('Length').SetAttributeValue(value)
        break