import GS_C300_IO_Calc2
IO_Family_Type = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
parts_dict = dict()
if IO_Family_Type == 'Series-C Mark II':
    parts_dict = GS_C300_IO_Calc2.getParts44489(Product, parts_dict)
if len(parts_dict) > 0:
    GS_C300_IO_Calc2.setIOCount(Product, 'Series_C_RG_Part_Summary', parts_dict)
    ScriptExecutor.Execute('PS_Series_C_RG_Part_Summary_Cont_update_parts')
    Product.GetContainerByName('Series_C_RG_Part_Summary_Cont').Calculate()