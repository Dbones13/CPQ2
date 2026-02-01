selected_prds = Product.Attr('CE_Selected_Products').GetValue()
Trace.Write(str(selected_prds))
prd_list = selected_prds.split('<br>')
Trace.Write(str(prd_list))
sm_products = ['Safety Manager ESD','Safety Manager FGS', 'Safety Manager BMS', 'Safety Manager HIPPS']
#Trace.Write(str(sm_products))
show_base = ''
for i in prd_list:
    if i in sm_products:
        show_base = i
        Product.Attr('SM_Product_Name').AssignValue(i)
        Trace.Write(Product.Attr('SM_Product_Name').GetValue())
        break
#Trace.Write(str(show_base))
CE_QTY=SM_QTY=UIO=qntmarsh=UIO1=SeriesC=MarkC=TurboC=UioCalcs=0
if Product.GetContainerByName("CE_System_Cont").Rows.Count >0:
    for row in Product.GetContainerByName("CE_System_Cont").Rows:
        system_Product = row.Product
        if system_Product.Name in ["ControlEdge UOC System","C300 System"]:
            UioCalcs+=1
        if system_Product.Name in ["ControlEdge PLC System","ControlEdge UOC System","ControlEdge RTU System","C300 System"]:
            CE_QTY+=1
        if str(SM_QTY)=="0" and system_Product.Name in ["Safety Manager ESD","Safety Manager FGS","Safety Manager HIPPS","Safety Manager BMS"]:
            SM_QTY = 1
        if row['C300_Exp_Labor_Uni_qntCG1'] !='':
            UIO1+=int(row['C300_Exp_Labor_Uni_qntCG1'])
        if row['C300_Exp_Labor_Uni_qntCG'] !='':
            UIO+=int(row['C300_Exp_Labor_Uni_qntCG'])
        if row['C300_Exp_Labor_Uni_qntmarsh'] !='':
            qntmarsh+=int(row['C300_Exp_Labor_Uni_qntmarsh'])
if UioCalcs >1:
    UIO= UIO1+UIO if (UIO1 >0 and UIO >0) else 0
else:
    UIO= UIO1+UIO
if Product.Attr('C300_IO_FamilY1_for_proposal').GetValue() !='':
    SeriesC= 1 if int(Product.Attr('C300_IO_FamilY1_for_proposal').GetValue()) >0 else 0
if Product.Attr('C300_IO_FamilY2_for_proposal').GetValue() !='':
    MarkC= 1 if int(Product.Attr('C300_IO_FamilY2_for_proposal').GetValue()) >0 else 0
if Product.Attr('IO_Family_document').GetValue() !='':
    TurboC= 1 if int(Product.Attr('IO_Family_document').GetValue()) >0 else 0
ITQty=(SeriesC+MarkC+TurboC)-1 if int(SeriesC+MarkC+TurboC) >0 else 0
Product.Attr('EX_Labor_CT_Qty').AssignValue(str(CE_QTY+SM_QTY))
Product.Attr('EX_Labor_IT_Qty').AssignValue(str(ITQty+CE_QTY+SM_QTY))
Product.Attr('C300_Exp_Labor_Uni_qntCG').AssignValue(str(UIO))
Product.Attr('C300_Exp_Labor_Uni_qntmarsh').AssignValue(str(qntmarsh))