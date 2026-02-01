#Sets product container as complete/Incomple based on valid simple/fme parts populated in respective containers
Product.Attributes.GetByName('HPS_Incomplete_Flag').AssignValue('1')
Product.Attr('HPS_Product_Message').AssignValue("Incomplete Configuration")

Hps_Cont = Product.GetContainerByName('HPS_Valid_Parts')
Valid_Cont = Product.GetContainerByName('HPS_PU_Valid_Parts')
if Valid_Cont.Rows.Count > 0  or Hps_Cont.Rows.Count > 0:
    Product.Attributes.GetByName('HPS_Incomplete_Flag').AssignValue('')
    Product.Attr('HPS_Product_Message').AssignValue('')