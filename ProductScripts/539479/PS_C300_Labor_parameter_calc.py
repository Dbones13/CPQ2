ffb = 0
iof = 0
ffs = 0
family_type_set = set()
uni_mar_cab = set()
rows = Product.GetContainerByName('Series_C_Control_Groups_Cont').Rows
for row in rows:
    product = row.Product
    total_sumof_ff_io_ai = product.Attr('Sum_FFIO_AI').GetValue()
    total_sumof_ff_io_ao = product.Attr('Sum_FFIO_AO').GetValue()
    total_numof_ff_seg = product.Attr('Total_Numof_FF_Segments').GetValue()
    ffb += int(total_sumof_ff_io_ai) if total_sumof_ff_io_ai.isdigit() else 0
    ffb += int(total_sumof_ff_io_ao) if total_sumof_ff_io_ao.isdigit() else 0
    family_type_set.add(product.Attr('SerC_CG_IO_Family_Type').GetValue())
    ffs += int(total_numof_ff_seg) if total_numof_ff_seg.isdigit() else 0
    uni_mar_cab.add(product.Attr('SerC_CG_Universal_Marshalling_Cabinet').GetValue())
Product.Attr('C300_Labor_parameter_ffb').AssignValue(str(ffb))
Product.Attr('C300_Labor_parameter_iof').AssignValue(str(len(family_type_set)))
Product.Attr('C300_Labor_parameter_ffs').AssignValue(str(ffs))
cab_val = '0.9' if 'Yes' in uni_mar_cab else '1'
Product.Attr('C300_Labor_parameter_ms').AssignValue(cab_val)