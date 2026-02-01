import GS_C300_Calc_Module,GS_SerC_parts
def ID_E_Pos(Product):
    Controller_list = ['CN100 CEE','CN100 I/O HIVE - C300 CEE','Control HIVE - Physical','Control HIVE - Virtual']
    Type_of_Controller_Required=Product.Attr('SerC_CG_Type_of_Controller_Required').GetValue()
    Specify_ID = Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
    IO_Mounting_Solution=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
    UPC_Id_Modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
    if IO_Mounting_Solution == "Universal Process Cab - 1.3M" and Specify_ID == "Yes":
        Trace.Write("UPC_Id_Modifier:"+str(UPC_Id_Modifier))
        if Type_of_Controller_Required in Controller_list and UPC_Id_Modifier != '':
            if UPC_Id_Modifier[5] != '0':
                return False
            else:
                return True
Controller_list = ['CN100 CEE','CN100 I/O HIVE - C300 CEE','Control HIVE - Physical','Control HIVE - Virtual']
Type_of_Controller_Required=Product.Attr('SerC_CG_Type_of_Controller_Required').GetValue()
Specify_ID = Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
IO_Mounting_Solution=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
UPC_Id_Modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
msgAttr = Product.Attr('C300_Modifier_ID_Validation_Error_E_Pos')
error_msg  = 'The FOE IO Link is not qualified with CN100. This will be supported in further release.'
msg = ""
E_pos = ID_E_Pos(Product)
if not E_pos and IO_Mounting_Solution == "Universal Process Cab - 1.3M" and Specify_ID == "Yes" and Type_of_Controller_Required in Controller_list and UPC_Id_Modifier != '':
    msgAttr.AssignValue(error_msg)
else:
    msgAttr.AssignValue(msg)
Product.Attr("C300_RG_Total_IO_Load").AssignValue(str(GS_C300_Calc_Module.getTotalLoadIO(Product)))
Product.Attr("C300_RG_Total_IO_Point_Load").AssignValue(str(GS_C300_Calc_Module.getTotalIoPointLoad(Product)))
totalLoadIO = GS_C300_Calc_Module.getTotalLoadIO_PMIO(Product)
Product.Attr("C300_RG_PMIO_Total_IO_Load").AssignValue(str(totalLoadIO))
qty_8939_HN, qty_8937_HN2, qty_A2, qty_A3 = GS_SerC_parts.Get_RG_IOTA(Product)
Product.Attr("RG_HN").AssignValue(str(qty_8939_HN))
Product.Attr("RG_HN2").AssignValue(str(qty_8937_HN2))
qty_SDRX, qty_HPSC, qty_100 = GS_SerC_parts.RG_iota(Product)
Product.Attr("qty_hpsc").AssignValue(str(qty_HPSC))