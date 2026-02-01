network_level_container = Product.GetContainerByName('Network Level Container')
net_Level = Product.Attr('Network Level').GetValue()
network_levels = [x.strip() for x in net_Level.split(',')]
rows_to_delete = []
if len(network_levels) == 0 or network_levels[0] == '':
    network_level_container.Rows.Clear()
else:
    for netwrk_level in network_levels:
        row_exist = False
        Trace.Write('-------netwrk_level-----'+ netwrk_level+'|')
        for row in network_level_container.Rows:
            Trace.Write('-------netwrk_level-----'+ netwrk_level+'|------'+row['Network Level'])
            if row['Network Level'] == netwrk_level:
                Trace.Write("Make row exit True")
                row_exist = True
        if row_exist == False:
            Trace.Write('-----Make row exist False')
            newRow = network_level_container.AddNewRow()
            newRow['Network Level'] = netwrk_level.strip()
        for row in network_level_container.Rows:
            Trace.Write(str(network_levels) + '---'+ row['Network Level']+'|')
            Trace.Write(row['Network Level'] not in network_levels)
            if row['Network Level'] not in network_levels:
                rows_to_delete.append(row.RowIndex)
if len(rows_to_delete) > 0:
    Trace.Write("Rows to be deleted -- "+ str(rows_to_delete))
    ar_to_delete = sorted(rows_to_delete, reverse=True)
    for item_delete in ar_to_delete:
        network_level_container.DeleteRow(item_delete)