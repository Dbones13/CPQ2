Product.Attributes.GetByName('Incomplete_Flag').AssignValue('1')
Product.Attr('Product_Message').AssignValue("Incomplete Configuration")

Fme_Cont = Product.GetContainerByName('FME_Valid_Parts')
# for row in Fme_Cont.Rows:
#     if row["Message"] == '<label style="color:green">Valid</label>':
#         Product.Attributes.GetByName('Incomplete_Flag').AssignValue('')
#         Product.Attr('Product_Message').AssignValue('')
#         break
Valid_Cont = Product.GetContainerByName('PU_Valid_Parts')
if Valid_Cont.Rows.Count > 0  or Fme_Cont.Rows.Count > 0:
    Product.Attributes.GetByName('Incomplete_Flag').AssignValue('')
    Product.Attr('Product_Message').AssignValue('')