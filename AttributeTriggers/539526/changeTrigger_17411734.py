Soft_rel = Product.Attr('PLC_Software_Release').GetValue()
if Soft_rel == 'R172':
    r_uio_cont = Product.GetContainerByName('PLC_RG_UIO_Cont').Rows[1]
    r_uio_cont.GetColumnByName('PLC_AI_HART_Points').Value = '0'
    r_uio_cont.GetColumnByName('PLC_AO_HART_100_250').Value = '0'
    r_uio_cont.GetColumnByName('PLC_AO_HART_250_499').Value = '0'
    r_uio_cont.GetColumnByName('PLC_AO_HART_500').Value = '0'