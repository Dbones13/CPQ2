import re
IsR2QparentRG = Product.Attr('IsR2QparentRG').GetValue()
if IsR2QparentRG:
    r2q=dict()
    if Quote.GetCustomField("IsR2QRequest").Content=='Yes':
        res=SqlHelper.GetList("SELECT Attributes FROM R2Q_CONFIGURATION_MASTER_TABLE WHERE ATTRIBUTES NOT LIKE 'Header_%' AND ATTRIBUTES<>'' AND Sub_Module='"+ Product.Name +"'")
        for key in res:
            r2q[key.Attributes]=1
        for item in Product.Attributes.GetEnumerator():
            if r2q.get(item.Name) != 1 and not re.match(r'^Header.',str(item.Name)):
                Trace.Write(item.Name)
                Product.Attributes.GetByName(item.Name).Allowed=False