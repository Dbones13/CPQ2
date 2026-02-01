system = Product.GetContainerByName('CE_SystemGroup_Cont')
#system.GetColumnByName('Selection').DisplayValue
count=count1= 0
for i in system.Rows:
    #if i.IsSelected and i['Scope'] == 'HWSWLABOR' and TagParserProduct.ParseString('[LIKE](<*VALUE(CE_Selected_Products)*>,Experion Enterprise System)')=='1':
    if i['Scope'] == 'HWSWLABOR' and i['Selected_Products']:#TagParserProduct.ParseString('[LIKE](<*CTX( Container(CE_SystemGroup_Cont).SelectedRowsColumn(Selected_Products).Separator() )*>,Experion Enterprise System)')=='1':
        ab=i['Selected_Products']
        Trace.Write(ab)
        ab=ab.split("<br>")
        Trace.Write(str(ab))
        for j in ab:
            Trace.Write(j)
            if j=="Experion Enterprise System":
                Trace.Write('true')
                Trace.Write((i['Scope']))
                count += 1
                Trace.Write(count)
if (count > 0):
    Product.AllowAttr('Labor_details_newexapnsion_cont2')
    Trace.Write("True")
else:
    Product.DisallowAttr('Labor_details_newexapnsion_cont2')
    Trace.Write("False")