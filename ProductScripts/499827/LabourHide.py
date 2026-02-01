system = Product.GetContainerByName('CE_SystemGroup_Cont')
count = 0
for i in system.Rows:
    if i['Scope'] == 'HWSWLABOR':
        Trace.Write("true")
        count += 1
if count > 0:
    #Product.AllowAttr('Labor_Details_New/Expansion_Cont')
    TagParserProduct.ParseString('<*CTX( Container(Labor_Details_New/Expansion_Cont).Column(Site_Survey_Required).SetPermission(Editable) )*>,<*CTX( Container(Labor_Details_New/Expansion_Cont).Column(Labor_Unreleased_Product).SetPermission(Editable) )*>,<*CTX( Container(Labor_Details_New/Expansion_Cont).Column(Labor_Loop_Drawings).SetPermission(Editable) )*>,<*CTX( Container(Labor_Details_New/Expansion_Cont).Column(Labor_Marshalling_Database).SetPermission(Editable) )*>,<*CTX( Container(Labor_Details_New/Expansion_Cont).Column(Labor_Percentage_FAT).SetPermission(Editable) )*>,<*CTX( Container(Labor_Details_New/Expansion_Cont).Column(Labor_Site_Activities).SetPermission(Editable) )*>,<*CTX( Container(Labor_Details_New/Expansion_Cont).Column(Labor_Operation_Manual_Scope).SetPermission(Editable) )*>,<*CTX( Container(Labor_Details_New/Expansion_Cont).Column(Labor_Custom_Scope).SetPermission(Editable) )*>')
else:
    #Product.DisallowAttr('Labor_Details_New/Expansion_Cont')
    TagParserProduct.ParseString('<*CTX( Container(Labor_Details_New/Expansion_Cont).Column(Site_Survey_Required).SetPermission(Hidden) )*>,<*CTX( Container(Labor_Details_New/Expansion_Cont).Column(Labor_Unreleased_Product).SetPermission(Hidden) )*>,<*CTX( Container(Labor_Details_New/Expansion_Cont).Column(Labor_Loop_Drawings).SetPermission(Hidden) )*>,<*CTX( Container(Labor_Details_New/Expansion_Cont).Column(Labor_Marshalling_Database).SetPermission(Hidden) )*>,<*CTX( Container(Labor_Details_New/Expansion_Cont).Column(Labor_Percentage_FAT).SetPermission(Hidden) )*>,<*CTX( Container(Labor_Details_New/Expansion_Cont).Column(Labor_Site_Activities).SetPermission(Hidden) )*>,<*CTX( Container(Labor_Details_New/Expansion_Cont).Column(Labor_Operation_Manual_Scope).SetPermission(Hidden) )*>,<*CTX( Container(Labor_Details_New/Expansion_Cont).Column(Labor_Custom_Scope).SetPermission(Hidden) )*>')
    Trace.Write("false")