import System.Decimal as D
import GS_Get_Set_AtvQty
import GS_C300_MCAR_calcs

#Qty_R01=GS_Get_Set_AtvQty.getAtvQty(Product,"Series_C_CG_Part_Summary","CC-MCAR01")
#Qty_N01=GS_Get_Set_AtvQty.getAtvQty(Product,"Series_C_CG_Part_Summary","MU-TMCN01")

def C300_calcs_part(Product,Qty_R01,Qty_N01):
    #SUM_HI,SUM_LO,SUM_HI1,SUM_LO1,SUM_HI11,SUM_LO11,SUM_D,HI,LO,LL=GS_C300_MCAR_calcs.mcar_cals(Product)
    CADS11,part600,part400,part500,CBDS01,CASS12,part200,CASS11,part300,part100,CBDD01,CADS12,X,Y,Z,K,L,C1,C2,C3,C4,C8SS01=GS_C300_MCAR_calcs.cab_c(Product) #CXCPQ-116603
    CADS= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','CADS'))
    CASS= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','CASS'))
    QTY_A=QTY_B=QTY_C=QTY_D=QTY_E1=QTY_E2=QTY_E3=QTY_E4=Val_A=Val_B=Val_C=0
    XXYY = Qty_R01
    SUM_D = Qty_N01
    if Product.Name=="Series-C Control Group":
        Trace.Write("XXYY"+str(XXYY))
        #Trace.Write("Y"+str(YY))
        io_family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        mounting_sol=Product.Attr('SerC_CG_IO_Mounting_Solution').GetValue()
        mounting_panel=Product.Attr('SerC_CG_Mounting_Panel_Type').GetValue()
        Cabinet_access=Product.Attr('SerC_CG_Cabinet_Access').GetValue()
        Cabinet_type=Product.Attr('SerC_CG_Cabinet_Type_03').GetValue()
        Power_entry_default=Product.Attr('SerC_CG_Power_Entry_Default').GetValue()
        Terminal_side=Product.Attr('SerC_CG_Terminal_Block_Mounting_Side').GetValue()
        Cabinet_Hinge_Type=Product.Attr('SerC_CG_Cabinet_Hinge_Type').GetValue()

        #CXCPQ-45701
        if io_family=='Series C' and mounting_sol=='Mounting Panel' and mounting_panel=='2 Column Wide Full Size':
            QTY_A= D.Ceiling((XXYY+SUM_D)/4.0)
        #CXCPQ-45698
        if io_family=='Series C' and mounting_sol=='Mounting Panel' and mounting_panel=='3 Column Wide Full Size':
            Val_A= D.Ceiling((XXYY+SUM_D)/6.0)
            Trace.Write('Val_A :'+str(Val_A))
        #CXCPQ-45699
        if io_family=='Series C' and mounting_sol=='Mounting Panel' and mounting_panel=='3 Column Wide Half Size':
            QTY_B= D.Ceiling((XXYY+SUM_D)/3.0)
            Trace.Write('QTY_B :'+str(QTY_B))
        #CXCPQ-45706
        if io_family=='Series C' and mounting_sol=='Mounting Panel' and Terminal_side=='Right' and mounting_panel=='3 Column Wide Full Size':
            Val_B= int(Val_A)*1
        if io_family=='Series C' and mounting_sol=='Mounting Panel' and Terminal_side=='Left' and mounting_panel=='3 Column Wide Full Size':
            Val_C= int(Val_A)*1
        if io_family=='Series C' and mounting_sol=='Mounting Panel' and Terminal_side=='Right' and mounting_panel=='3 Column Wide Half Size':
            Val_B= int(QTY_B)*1
        if io_family=='Series C' and mounting_sol=='Mounting Panel' and Terminal_side=='Left' and mounting_panel=='3 Column Wide Half Size':
            Val_C= int(QTY_B)*1
            
        #CXCPQ-45702
        if io_family=='Series C' and mounting_sol=='Mounting Panel' and mounting_panel=='2 Column Wide Half Size':
            QTY_D= D.Ceiling((XXYY+SUM_D)/2.0)
        #CXCPQ-47614
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Single Access' and (Cabinet_type=='Normal Cabinet' or Cabinet_type== 'Alternate Cabinet' or Cabinet_type=='Generic Cabinet') and Power_entry_default=='Double Pole':
            QTY_C= (CBDS01+part300+part600+CASS+CASS12)*1
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Dual Access' and (Cabinet_type=='Normal Cabinet' or Cabinet_type== 'Alternate Cabinet' or Cabinet_type=='Generic Cabinet') and Power_entry_default=='Double Pole':
            QTY_C=(CBDD01+part100+part200+CADS+part400+part500+CADS12)*2
        #CXCPQ-34707
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Single Access' and Cabinet_type=='Normal Cabinet':
            if Cabinet_Hinge_Type=='130 Degree':
                QTY_E1=(CBDS01+part300)*1
            if Cabinet_Hinge_Type=='180 Degree':
                QTY_E2=(CBDS01+part300)*1
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Dual Access' and Cabinet_type=='Normal Cabinet':
            if Cabinet_Hinge_Type=='130 Degree':
                QTY_E1=(CBDD01+part100+part200)*2
            if Cabinet_Hinge_Type=='180 Degree':
                QTY_E2=(CBDD01+part100+part200)*2
        #CXCPQ-82919
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Single Access' and (Cabinet_type=='Normal Cabinet' or Cabinet_type=='Generic Cabinet'):
            if Cabinet_Hinge_Type=='130 Degree':
                QTY_E3=(CASS12)*1
            if Cabinet_Hinge_Type=='180 Degree':
                QTY_E4=(CASS12)*1
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Dual Access' and (Cabinet_type=='Normal Cabinet' or Cabinet_type=='Generic Cabinet'):
            if Cabinet_Hinge_Type=='130 Degree':
                QTY_E3=(CADS12)*2
            if Cabinet_Hinge_Type=='180 Degree':
                QTY_E4=(CADS12)*2
    elif Product.Name=="Series-C Remote Group":
        Trace.Write("XXYY"+str(XXYY))
        io_family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        mounting_sol=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
        mounting_panel=Product.Attr('Ser_C_RG_Mounting_Panel_Type').GetValue()
        Cabinet_access=Product.Attr('SerC_RG_Cabinet_Access').GetValue()
        Cabinet_type=Product.Attr('SerC_RG_Cabinet_Type').GetValue()
        Power_entry_default=Product.Attr('SerC_RG_Power_Entry_Default').GetValue()
        Terminal_side=Product.Attr('SerC_RG_TerminalBlockMounting_Side_For_MountingPnl').GetValue()
        Cabinet_Hinge_Type=Product.Attr('SerC_RG_Cabinet_Hinge_Type_Default').GetValue()
        
        #CXCPQ-45701
        if io_family=='Series C' and mounting_sol=='Mounting Panel' and mounting_panel=='2 Column Wide Full Size':
            QTY_A= D.Ceiling((XXYY+SUM_D)/4.0)
        #CXCPQ-45698
        if io_family=='Series C' and mounting_sol=='Mounting Panel' and mounting_panel=='3 Column Wide Full Size':
            Val_A= D.Ceiling((XXYY+SUM_D)/6.0)
            Trace.Write('Val_A :'+str(Val_A))
        #CXCPQ-45699
        if io_family=='Series C' and mounting_sol=='Mounting Panel' and mounting_panel=='3 Column Wide Half Size':
            QTY_B= D.Ceiling((XXYY+SUM_D)/3.0)
        #CXCPQ-45706
        if io_family=='Series C' and mounting_sol=='Mounting Panel' and Terminal_side=='Right' and mounting_panel=='3 Column Wide Full Size':
            Val_B= int(Val_A)*1
        if io_family=='Series C' and mounting_sol=='Mounting Panel' and Terminal_side=='Left' and mounting_panel=='3 Column Wide Full Size':
            Val_C= int(Val_A)*1
        if io_family=='Series C' and mounting_sol=='Mounting Panel' and Terminal_side=='Right' and mounting_panel=='3 Column Wide Half Size':
            Val_B= int(QTY_B)*1
        if io_family=='Series C' and mounting_sol=='Mounting Panel' and Terminal_side=='Left' and mounting_panel=='3 Column Wide Half Size':
            Val_C= int(QTY_B)*1
        #CXCPQ-45702
        if io_family=='Series C' and mounting_sol=='Mounting Panel' and mounting_panel=='2 Column Wide Half Size':
            QTY_D= D.Ceiling((XXYY+SUM_D)/2.0)
        #CXCPQ-47614
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Single Access' and (Cabinet_type=='Normal Cabinet' or Cabinet_type== 'Alternate Cabinet' or Cabinet_type=='Generic Cabinet') and Power_entry_default=='Double Pole':
            QTY_C= (CBDS01+part300+part600+CASS+CASS12)*1
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Dual Access' and (Cabinet_type=='Normal Cabinet' or Cabinet_type== 'Alternate Cabinet' or Cabinet_type=='Generic Cabinet') and Power_entry_default=='Double Pole':
            QTY_C=(CBDD01+part100+part200+CADS+part400+part500+CADS12)*2
        #CXCPQ-34707
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Single Access' and Cabinet_type=='Normal Cabinet':
            if Cabinet_Hinge_Type=='130 Degree':
                QTY_E1=(CBDS01+part300)*1
            if Cabinet_Hinge_Type=='180 Degree':
                QTY_E2=(CBDS01+part300)*1
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Dual Access' and Cabinet_type=='Normal Cabinet':
            if Cabinet_Hinge_Type=='130 Degree':
                QTY_E1=(CBDD01+part100+part200)*2
            if Cabinet_Hinge_Type=='180 Degree':
                QTY_E2=(CBDD01+part100+part200)*2
        #CXCPQ-82919
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Single Access' and (Cabinet_type=='Normal Cabinet' or Cabinet_type=='Generic Cabinet'):
            if Cabinet_Hinge_Type=='130 Degree':
                QTY_E3=(CASS12)*1
            if Cabinet_Hinge_Type=='180 Degree':
                QTY_E4=(CASS12)*1
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Dual Access' and (Cabinet_type=='Normal Cabinet' or Cabinet_type=='Generic Cabinet'):
            if Cabinet_Hinge_Type=='130 Degree':
                QTY_E3=(CADS12)*2
            if Cabinet_Hinge_Type=='180 Degree':
                QTY_E4=(CADS12)*2
    return QTY_A,QTY_B,QTY_C,QTY_D,QTY_E1,QTY_E2,QTY_E3,QTY_E4,Val_A,Val_B,Val_C
#Temp=C300_calcs_part(Product,Qty_R01,Qty_N01)
#Trace.Write(Temp)