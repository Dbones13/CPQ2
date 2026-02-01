attrlist = ["Header_15_close","Header_15_open","SerC_RG_Enhanced_Function_IO_Cont","SerC_RG_Enhanced_Function_IO_Cont2","Header_21_close","Header_21_open","C300_RG_Universal_IO_cont_1","C300_RG_Universal_IO_cont_2"]
ioFamilyType = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
if ioFamilyType in ("Series C","Turbomachinery"):
    for attr in attrlist:
        Product.AllowAttr(attr)
else:
    for attr in attrlist:
        Product.DisallowAttr(attr)