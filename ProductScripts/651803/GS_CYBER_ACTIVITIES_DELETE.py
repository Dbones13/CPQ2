activity_container = Product.GetContainerByName('Activities')
deletelist = []
for row in activity_container.Rows:
    if row['Hours'] in ['0','','0.0']:
        deletelist.append(row.RowIndex)
if len(deletelist) > 0:
    deletelist = deletelist[::-1]
    for rowIndex in deletelist:
        activity_container.DeleteRow(rowIndex)

if Product.PartNumber == 'ASSESSMENT':
    attr_list = ['Remote Instrumentation Enclosures (RIE)','DCS or FTE Communities','Control Rooms','Switches and Routers','Controllers and PLCs',"PC's and Servers",'Firewalls (redundant pair)']
    add_val = 0
    for attr in attr_list:
        val= Product.Attr(attr).GetValue()
        add_val += int(val) if val !='' else 0
    if add_val == 0:
        deletelist = [row.RowIndex for row in activity_container.Rows]
        if len(deletelist) > 0:
            for row_index in sorted(deletelist, reverse=True):
                activity_container.DeleteRow(row_index)
            Product.DisallowAttr('Activities')