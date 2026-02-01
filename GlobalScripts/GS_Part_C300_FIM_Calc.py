#CXCPQ-41843, 41327, 44565, 44563
import System.Decimal as D

#41843, 44565
def part_qty_FIM8(Product):
    if Product.Name == "Series-C Control Group":
        if Product.Attributes.GetByName("SerC_CG_IO_Family_Type").GetValue():
            family_type = Product.Attributes.GetByName("SerC_CG_IO_Family_Type").GetValue()
        else:
            family_type = ''
        if family_type != 'Series C' and family_type != 'Series-C Mark II':
            return int(0), int(0)
        if Product.Attributes.GetByName("FIM_Type").GetValue():
            fim_type = Product.Attributes.GetByName("FIM_Type").GetValue()
        else:
            fim_type = ''
        if fim_type != 'FIM8':
            return int(0), int(0)
        ff_tot_seg_cont = Product.GetContainerByName('SerC_CG_FIM_FF_Tot_Seg_transpose')
        i = 10
        for cont_row in ff_tot_seg_cont.Rows:
            if cont_row.GetColumnByName('Final_Tot_Seg').Value:
                globals()['R'+str(i)] = cont_row.GetColumnByName('Final_Tot_Seg').Value
            else:
                globals()['R'+str(i)] = 0
            i = i + 1
        if R10 == 0 and R11 == 0 and R12 == 0 and R13 == 0 and R14 == 0 and R15 == 0:
            return int(0), int(0)
        CC_PFB801 = CC_TFB811 = DC_TFB813 = 0
        CC_PFB801 = (2 * D.Ceiling(float(R10)/float(8))) + D.Ceiling(float(R11)/float(8)) + D.Ceiling(float(R12)/float(8)) + (2 * D.Ceiling(float(R13)/float(8))) + D.Ceiling(float(R14)/float(8)) + D.Ceiling(float(R15)/float(8))
        if family_type == 'Series C':
            CC_TFB811 = D.Ceiling(float(R10)/float(8)) + D.Ceiling(float(R11)/float(8)) + D.Ceiling(float(R12)/float(8)) + D.Ceiling(float(R13)/float(8)) + D.Ceiling(float(R14)/float(8)) + D.Ceiling(float(R15)/float(8))
            return int(CC_PFB801), int(CC_TFB811)
        elif family_type == 'Series-C Mark II':
            DC_TFB813 = D.Ceiling(float(R10)/float(8)) + D.Ceiling(float(R11)/float(8)) + D.Ceiling(float(R12)/float(8)) + D.Ceiling(float(R13)/float(8)) + D.Ceiling(float(R14)/float(8)) + D.Ceiling(float(R15)/float(8))
            return int(CC_PFB801), int(DC_TFB813)

#41327, 44563
def part_qty_FIM4(Product):
    if Product.Name == "Series-C Control Group":
        if Product.Attributes.GetByName("SerC_CG_IO_Family_Type").GetValue():
            family_type = Product.Attributes.GetByName("SerC_CG_IO_Family_Type").GetValue()
        else:
            family_type = ''
        if family_type != 'Series C' and family_type != 'Series-C Mark II':
            return int(0), int(0), int(0)
        if Product.Attributes.GetByName("FIM_Type").GetValue():
            fim_type = Product.Attributes.GetByName("FIM_Type").GetValue()
        else:
            fim_type = ''
        if fim_type != 'FIM4':
            return int(0), int(0), int(0)
        ff_tot_seg_cont = Product.GetContainerByName('SerC_CG_FIM_FF_Tot_Seg_transpose')
        i = 10
        for cont_row in ff_tot_seg_cont.Rows:
            if cont_row.GetColumnByName('Final_Tot_Seg').Value:
                globals()['R'+str(i)] = cont_row.GetColumnByName('Final_Tot_Seg').Value
            else:
                globals()['R'+str(i)] = 0
            i = i + 1
        if R10 == 0 and R11 == 0 and R12 == 0 and R13 == 0 and R14 == 0 and R15 == 0:
            return int(0), int(0), int(0)
        CC_PFB402 = CC_TFB412 = CC_TFB402 = DC_TFB413 = DC_TFB403 = 0
        CC_PFB402 = (2 * D.Ceiling(float(R10)/float(4))) + D.Ceiling(float(R11)/float(4)) + D.Ceiling(float(R12)/float(4)) + (2 * D.Ceiling(float(R13)/float(4))) + D.Ceiling(float(R14)/float(4)) + D.Ceiling(float(R15)/float(4))
        if family_type == 'Series C':
            CC_TFB412 = (2 * D.Ceiling(float(R10)/float(4))) + D.Ceiling(float(R11)/float(4)) + (2 * D.Ceiling(float(R13)/float(4))) + D.Ceiling(float(R14)/float(4))
            CC_TFB402 = D.Ceiling(float(R12)/float(4)) + D.Ceiling(float(R15)/float(4))
            return int(CC_PFB402), int(CC_TFB412), int(CC_TFB402)
        elif family_type == 'Series-C Mark II':
            DC_TFB413 = (2 * D.Ceiling(float(R10)/float(4))) + D.Ceiling(float(R11)/float(4)) + (2 * D.Ceiling(float(R13)/float(4))) + D.Ceiling(float(R14)/float(4))
            DC_TFB403 = D.Ceiling(float(R12)/float(4)) + D.Ceiling(float(R15)/float(4))
            return int(CC_PFB402), int(DC_TFB413), int(DC_TFB403)

#x, y = part_qty_FIM8(Product)
#a, b, c = part_qty_FIM4(Product)