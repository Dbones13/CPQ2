lob = Quote.GetCustomField('Booking Lob').Content
vc = Quote.QuoteTables["VCModelConfiguration"]
#Trace.Write(lob)
if lob == 'PMC' and vc.Rows.Count > 0:
    delAttrs = list()
    attrs = SqlHelper.GetList("select Attribute_Name from VC_ToBeDeleted")
    setPointAttrs = SqlHelper.GetList("select Attr_Name from VC_SetPointAttrs")
    SP_Attrs = list()
    for atr in setPointAttrs:
        try:
            SP_Attrs.append(str(unicode(atr.Attr_Name)))
        except Exception as e:
            Trace.Write("error at 12 " + str(e))

    for atr in attrs:
        try:
            delAttrs.append(str(atr.Attribute_Name))
        except Exception as e:
            Trace.Write("error at 18 " + str(e))

    for row in vc.Rows:
        if row['AttributeName'] in delAttrs:
            vc.DeleteRow(row.Id)

    for row in vc.Rows:
        if row['AttributeValueSystemId'] == '' and row['AttributeName'] in SP_Attrs:
            vc.DeleteRow(row.Id)
    vc.Save()
