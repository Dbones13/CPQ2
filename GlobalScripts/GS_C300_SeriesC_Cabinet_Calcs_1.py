import GS_Get_Set_AtvQty
import System.Decimal as D
import GS_C300_MCAR_calcs
import GS_C300_SeriesC_cabinet_bays_Cal
#47585,35490
def C300_calcs_part2(Product):
    A,B,C,D,E,F=GS_C300_SeriesC_cabinet_bays_Cal.cab_bays(Product)
    CADS11,part600,part400,part500,CBDS01,CASS12,part200,CASS11,part300,part100,CBDD01,CADS12,X,Y,Z,K,L,C1,C2,C3,C4,C8SS01=GS_C300_MCAR_calcs.cab_c(Product) #CXCPQ-116603
    QTY_F=QTY_G1=QTY_G2=QTY_G3=0
    QTY_H1=QTY_H2=QTY_H3=QTY_H4=QTY_H5=QTY_H6=QTY_H7=QTY_H8=0
    if Product.Name=="Series-C Control Group":
        io_family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        mounting_sol=Product.Attr('SerC_CG_IO_Mounting_Solution').GetValue()
        mounting_panel=Product.Attr('SerC_CG_Mounting_Panel_Type').GetValue()
        Cabinet_access=Product.Attr('SerC_CG_Cabinet_Access').GetValue()
        Cabinet_type=Product.Attr('SerC_CG_Cabinet_Type_03').GetValue()
        Power_entry_default=Product.Attr('SerC_CG_Power_Entry_Default').GetValue()
        Terminal_side=Product.Attr('SerC_CG_Terminal_Block_Mounting_Side').GetValue()
        Cabinet_Hinge_Type=Product.Attr('SerC_CG_Cabinet_Hinge_Type').GetValue()
        Cabinet_Door_Default=Product.Attr('SerC_CG_Cabinet_Doors_Default').GetValue()
        
        #35490,CXCPQ-82918
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Dual Access' and (Cabinet_type=='Normal Cabinet' or Cabinet_type=='Generic Cabinet'):
            if Cabinet_Door_Default == 'Reverse Front':
                QTY_G1 = (CBDD01+part100+part200+CADS12)*1
            if Cabinet_Door_Default=='Reverse Rear':
                QTY_G2= (CBDD01+part100+part200+CADS12)*1
            if Cabinet_Door_Default=='Reverse Front & Rear':
                QTY_G3= (CBDD01+part100+part200+CADS12)*1
        #47585
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Dual Access' and (Cabinet_type=='Normal Cabinet' or Cabinet_type== 'Alternate Cabinet'):
            QTY_F=(2*(B+D+E+F))
        #35486
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Single Access' and Cabinet_type=='Normal Cabinet':
            if Cabinet_Door_Default=='Standard' or Cabinet_Door_Default == 'Reverse Front' or Cabinet_Door_Default=='Reverse Rear' or Cabinet_Door_Default=='Reverse Front & Rear':
                QTY_H1=(CBDS01+part300)*1
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Single Access' and Cabinet_type=='Normal Cabinet':
            if Cabinet_Door_Default=='Double':
                QTY_H2=(CBDS01+part300)*1
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Dual Access' and Cabinet_type=='Normal Cabinet':
            if Cabinet_Door_Default=='Standard' or Cabinet_Door_Default == 'Reverse Front' or Cabinet_Door_Default=='Reverse Rear' or Cabinet_Door_Default=='Reverse Front & Rear':
                QTY_H3=(CBDD01+part100+part200)*2
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Dual Access' and Cabinet_type=='Normal Cabinet':
            if Cabinet_Door_Default=='Double':
                QTY_H4=(CBDD01+part100+part200)*2
        # CXCPQ-82272
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Single Access' and Cabinet_type=='Generic Cabinet':
            if Cabinet_Door_Default=='Standard' or Cabinet_Door_Default == 'Reverse Front' or Cabinet_Door_Default=='Reverse Rear' or Cabinet_Door_Default=='Reverse Front & Rear':
                QTY_H5=(CASS12)*1
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Single Access' and Cabinet_type=='Generic Cabinet':
            if Cabinet_Door_Default=='Double':
                QTY_H6=(CASS12)*1
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Dual Access' and Cabinet_type=='Generic Cabinet':
            if Cabinet_Door_Default=='Standard' or Cabinet_Door_Default == 'Reverse Front' or Cabinet_Door_Default=='Reverse Rear' or Cabinet_Door_Default=='Reverse Front & Rear':
                QTY_H7=(CADS12)*2
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Dual Access' and Cabinet_type=='Generic Cabinet':
            if Cabinet_Door_Default=='Double':
                QTY_H8=(CADS12)*2
    elif Product.Name=="Series-C Remote Group":
        io_family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        mounting_sol=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
        mounting_panel=Product.Attr('Ser_C_RG_Mounting_Panel_Type').GetValue()
        Cabinet_access=Product.Attr('SerC_RG_Cabinet_Access').GetValue()
        Cabinet_type=Product.Attr('SerC_RG_Cabinet_Type').GetValue()
        Power_entry_default=Product.Attr('SerC_RG_Power_Entry_Default').GetValue()
        Terminal_side=Product.Attr('SerC_RG_TerminalBlockMounting_Side_For_MountingPnl').GetValue()
        Cabinet_Hinge_Type=Product.Attr('SerC_RG_Cabinet_Hinge_Type_Default').GetValue()
        Cabinet_Door_Default=Product.Attr('SerC_RG_Cabinet_Doors_Default').GetValue()
        
        #34590,CXCPQ-82918
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Dual Access' and (Cabinet_type=='Normal Cabinet' or Cabinet_type=='Generic Cabinet'):
            if Cabinet_Door_Default == 'Reverse Front':
                QTY_G1 = (CBDD01+part100+part200+CADS12)*1
            if Cabinet_Door_Default=='Reverse Rear':
                QTY_G2= (CBDD01+part100+part200+CADS12)*1
            if Cabinet_Door_Default=='Reverse Front & Rear':
                QTY_G3= (CBDD01+part100+part200+CADS12)*1
        #47585
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Dual Access' and (Cabinet_type=='Normal Cabinet' or Cabinet_type== 'Alternate Cabinet'):
            QTY_F=(2*(B+D+E+F))
        #35486
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Single Access' and Cabinet_type=='Normal Cabinet':
            if Cabinet_Door_Default=='Standard' or Cabinet_Door_Default == 'Reverse Front' or Cabinet_Door_Default=='Reverse Rear' or Cabinet_Door_Default=='Reverse Front & Rear':
                QTY_H1=(CBDS01+part300)*1
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Single Access' and Cabinet_type=='Normal Cabinet':
            if Cabinet_Door_Default=='Double':
                QTY_H2=(CBDS01+part300)*1
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Dual Access' and Cabinet_type=='Normal Cabinet':
            if Cabinet_Door_Default=='Standard' or Cabinet_Door_Default == 'Reverse Front' or Cabinet_Door_Default=='Reverse Rear' or Cabinet_Door_Default=='Reverse Front & Rear':
                QTY_H3=(CBDD01+part100+part200)*2
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Dual Access' and Cabinet_type=='Normal Cabinet':
            if Cabinet_Door_Default=='Double':
                QTY_H4=(CBDD01+part100+part200)*2
        # CXCPQ-82272
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Single Access' and Cabinet_type=='Generic Cabinet':
            if Cabinet_Door_Default=='Standard' or Cabinet_Door_Default == 'Reverse Front' or Cabinet_Door_Default=='Reverse Rear' or Cabinet_Door_Default=='Reverse Front & Rear':
                QTY_H5=(CASS12)*1
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Single Access' and Cabinet_type=='Generic Cabinet':
            if Cabinet_Door_Default=='Double':
                QTY_H6=(CASS12)*1
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Dual Access' and Cabinet_type=='Generic Cabinet':
            if Cabinet_Door_Default=='Standard' or Cabinet_Door_Default == 'Reverse Front' or Cabinet_Door_Default=='Reverse Rear' or Cabinet_Door_Default=='Reverse Front & Rear':
                QTY_H7=(CADS12)*2
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Dual Access' and Cabinet_type=='Generic Cabinet':
            if Cabinet_Door_Default=='Double':
                QTY_H8=(CADS12)*2
        
    return QTY_F,QTY_G1,QTY_G2,QTY_G3,QTY_H1,QTY_H2,QTY_H3,QTY_H4,QTY_H5,QTY_H6,QTY_H7,QTY_H8
#47519
def C300_calcs_part3(Product):
    CADS11,part600,part400,part500,CBDS01,CASS12,part200,CASS11,part300,part100,CBDD01,CADS12,X,Y,Z,K,L,C1,C2,C3,C4,C8SS01=GS_C300_MCAR_calcs.cab_c(Product) #CXCPQ-116603
    QTY_I=QTY_I1=QTY_I2=0
    #A,B,C,D,E,F=GS_C300_SeriesC_cabinet_bays_Cal.cab_bays(Product)
    A=B=C=F=D=E=0
    CADS= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','CADS'))
    if Product.Name=="Series-C Control Group":
        io_family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        mounting_sol=Product.Attr('SerC_CG_IO_Mounting_Solution').GetValue()
        mounting_panel=Product.Attr('SerC_CG_Mounting_Panel_Type').GetValue()
        Cabinet_access=Product.Attr('SerC_CG_Cabinet_Access').GetValue()
        Cabinet_type=Product.Attr('SerC_CG_Cabinet_Type_03').GetValue()
        Power_entry_default=Product.Attr('SerC_CG_Power_Entry_Default').GetValue()
        Integrated_marshalling=Product.Attr('SerC_CG_Integrated_Marshalling_Cabinet').GetValue()
        #47519
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Dual Access' and Cabinet_type== 'Alternate Cabinet' and Integrated_marshalling=='No':
            A=CADS
            if True:
                B=int(A/4)
                C=A%4
                if C==1:
                    F=1
                if C==0:
                    B=B
                if C==2:
                    D=1
                if C==3:
                    E=1
            QTY_I=B
            QTY_I1=E
            QTY_I2=D
    elif Product.Name=="Series-C Remote Group":
        io_family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        mounting_sol=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
        mounting_panel=Product.Attr('Ser_C_RG_Mounting_Panel_Type').GetValue()
        Cabinet_access=Product.Attr('SerC_RG_Cabinet_Access').GetValue()
        Cabinet_type=Product.Attr('SerC_RG_Cabinet_Type').GetValue()
        Power_entry_default=Product.Attr('SerC_RG_Power_Entry_Default').GetValue()
        Integrated_marshalling=Product.Attr('SerC_RG_Integrated_Marshalling_Cabinet').GetValue()
        #47519
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Dual Access' and Cabinet_type== 'Alternate Cabinet' and Integrated_marshalling == 'No':
            A=CADS
            if True:
                B=int(A/4)
                C=A%4
                if C==1:
                    F=1
                if C==0:
                    B=B
                if C==2:
                    D=1
                if C==3:
                    E=1
            QTY_I=B
            QTY_I1=E
            QTY_I2=D
    return QTY_I,QTY_I1,QTY_I2
#CXCPQ-34702
def C300_calcs_part4(Product):
    CADS11,part600,part400,part500,CBDS01,CASS12,part200,CASS11,part300,part100,CBDD01,CADS12,X,Y,Z,K,L,C1,C2,C3,C4,C8SS01=GS_C300_MCAR_calcs.cab_c(Product) #CXCPQ-116603
    QTY1=QTY2=0
    CADS= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','CADS'))
    CASS= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','CASS'))
    if Product.Name=="Series-C Control Group":
        io_family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        mounting_sol=Product.Attr('SerC_CG_IO_Mounting_Solution').GetValue()
        mounting_panel=Product.Attr('SerC_CG_Mounting_Panel_Type').GetValue()
        Cabinet_access=Product.Attr('SerC_CG_Cabinet_Access').GetValue()
        Cabinet_type=Product.Attr('SerC_CG_Cabinet_Type_03').GetValue()
        Cabinet_thermostat=Product.Attr('SerC_CG_Cabinet_Thermostat_Default').GetValue()
        
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Single Access' and Cabinet_type in ['Normal Cabinet','Alternate Cabinet', 'Generic Cabinet'] and Cabinet_thermostat=='Yes':
            QTY1=((CBDS01 or C8SS01)+CASS+part300+part600+CASS12)*1
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Dual Access' and Cabinet_type in ['Normal Cabinet','Alternate Cabinet', 'Generic Cabinet'] and Cabinet_thermostat=='Yes':
            CBDD01 = int(GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','CC-C8DS01')) if CBDD01 == 0 else CBDD01
            QTY2=(CBDD01+part100+part200+CADS+part400+part500+CADS12)*2
            
    elif Product.Name=="Series-C Remote Group":
        io_family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        mounting_sol=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
        mounting_panel=Product.Attr('Ser_C_RG_Mounting_Panel_Type').GetValue()
        Cabinet_access=Product.Attr('SerC_RG_Cabinet_Access').GetValue()
        Cabinet_type=Product.Attr('SerC_RG_Cabinet_Type').GetValue()
        Power_entry_default=Product.Attr('SerC_RG_Power_Entry_Default').GetValue()
        Cabinet_thermostat=Product.Attr('SerC_RG_Cabinet_Thermostat_Default').GetValue()
        
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Single Access' and Cabinet_type in ['Normal Cabinet','Alternate Cabinet', 'Generic Cabinet'] and Cabinet_thermostat=='Yes':
            QTY1=(CBDS01+CASS+part300+part600+CASS12)*1
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Dual Access' and Cabinet_type in ['Normal Cabinet','Alternate Cabinet', 'Generic Cabinet'] and Cabinet_thermostat=='Yes':
            QTY2=(CBDD01+part100+part200+CADS+part400+part500+CADS12)*2
    return QTY1,QTY2

#CXCPQ-34703
def C300_calcs_part5(Product):
    CADS11,part600,part400,part500,CBDS01,CASS12,part200,CASS11,part300,part100,CBDD01,CADS12,X,Y,Z,K,L,C1,C2,C3,C4,C8SS01=GS_C300_MCAR_calcs.cab_c(Product) #CXCPQ-116603
    qty1=qty2=0
    if Product.Name=="Series-C Control Group":
        io_family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        mounting_sol=Product.Attr('SerC_CG_IO_Mounting_Solution').GetValue()
        mounting_panel=Product.Attr('SerC_CG_Mounting_Panel_Type').GetValue()
        Cabinet_access=Product.Attr('SerC_CG_Cabinet_Access').GetValue()
        Cabinet_type=Product.Attr('SerC_CG_Cabinet_Type_03').GetValue()
        Cabinet_thermostat=Product.Attr('SerC_CG_Cabinet_Thermostat_Default').GetValue()
        Cabinet_Door_Default=Product.Attr('SerC_CG_Cabinet_Doors_Default').GetValue()
        #CXCPQ-82655
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Single Access' and (Cabinet_type=='Normal Cabinet' or Cabinet_type=='Generic Cabinet'):
            if Cabinet_Door_Default=='Standard' or Cabinet_Door_Default=='Reverse Rear' or Cabinet_Door_Default=='Reverse Front & Rear':
                qty1=(CBDS01+part300+CASS12)*1
            if Cabinet_Door_Default == 'Reverse Front':
                qty2=(CBDS01+part300+CASS12)*1
        else:
            qty1=0
            qty2=0    
    elif Product.Name=="Series-C Remote Group":
        io_family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        mounting_sol=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
        mounting_panel=Product.Attr('Ser_C_RG_Mounting_Panel_Type').GetValue()
        Cabinet_access=Product.Attr('SerC_RG_Cabinet_Access').GetValue()
        Cabinet_type=Product.Attr('SerC_RG_Cabinet_Type').GetValue()
        Power_entry_default=Product.Attr('SerC_RG_Power_Entry_Default').GetValue()
        Cabinet_thermostat=Product.Attr('SerC_RG_Cabinet_Thermostat_Default').GetValue()
        Cabinet_Door_Default=Product.Attr('SerC_RG_Cabinet_Doors_Default').GetValue()
        #CXCPQ-82655
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Single Access' and (Cabinet_type=='Normal Cabinet' or Cabinet_type=='Generic Cabinet'):
            if Cabinet_Door_Default=='Standard' or Cabinet_Door_Default=='Reverse Rear' or Cabinet_Door_Default=='Reverse Front & Rear':
                qty1=(CBDS01+part300+CASS12)*1
            if Cabinet_Door_Default == 'Reverse Front':
                qty2=(CBDS01+part300+CASS12)*1
        else:
            qty1=0
            qty2=0
    return qty1,qty2
#CXCPQ-34708
def C300_calcs_part6(Product,Quote):
    CADS11,part600,part400,part500,CBDS01,CASS12,part200,CASS11,part300,part100,CBDD01,CADS12,X,Y,Z,K,L,C1,C2,C3,C4,C8SS01=GS_C300_MCAR_calcs.cab_c(Product) #CXCPQ-116603
    qty1=qty2=qty3=qty4=qty5=qty6=qty7=qty8=qty9=qty10=qty11=qty12=qty13=0
    CADS= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','CADS'))
    CASS= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','CASS'))
    if Product.Name=="Series-C Control Group":
        io_family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        if Quote.GetCustomField('R2QFlag').Content == "Yes":
            Product.Attr('CE_Site_Voltage').AssignValue('120V')
            Product.Attr('SerC_CG_Cabinet_Type_03').SelectDisplayValue('Normal Cabinet')
        mounting_sol=Product.Attr('SerC_CG_IO_Mounting_Solution').GetValue()
        mounting_panel=Product.Attr('SerC_CG_Mounting_Panel_Type').GetValue()
        Cabinet_access=Product.Attr('SerC_CG_Cabinet_Access').GetValue()
        Cabinet_type=Product.Attr('SerC_CG_Cabinet_Type_03').GetValue()
        Cabinet_thermostat=Product.Attr('SerC_CG_Cabinet_Thermostat_Default').GetValue()
        Cabinet_Door_Default=Product.Attr('SerC_CG_Cabinet_Doors_Default').GetValue()
        Fan_option=Product.Attr('SerC_CG_Fan_Option').GetValue()
        Site_voltage=Product.Attr('CE_Site_Voltage').GetValue()
        CBDS01 = C8SS01 if CBDS01 == 0 else CBDS01
        CBDD01 = int(GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','CC-C8DS01')) if CBDD01 == 0 else CBDD01
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Single Access' and (Cabinet_type=='Normal Cabinet' or Cabinet_type== 'Alternate Cabinet' or Cabinet_type=='Generic Cabinet'):
            if Fan_option=='TopCoverPlate':
                qty1=(CBDS01+part300+CASS+part600+CASS12)*1
            else:
                Trace.Write("test")
                if Fan_option=='Assembly - Universal Fan' or Fan_option=='24V Assembly':
                    qty1=(CBDS01+CASS12)*1
            if Fan_option=='Assembly' and Site_voltage=='120V':
                qty3=(CBDS01+part300+CASS+part600+CASS12)*1
            if Fan_option=='Assembly' and Site_voltage=='240V':
                qty4=(CBDS01+part300+CASS+part600+CASS12)*1
            if Fan_option=='Assembly - Universal Fan':
                qty5=(CBDS01+part300+CASS+part600+CASS12)*1
            if Fan_option=='Grille':
                qty6=(CBDS01+part300+CASS+part600+CASS12)*1
            if Fan_option=='24V Assembly':
                qty7=(CBDS01+part300+CASS+part600+CASS12)*1
        elif io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Dual Access' and (Cabinet_type=='Normal Cabinet' or Cabinet_type== 'Alternate Cabinet' or Cabinet_type=='Generic Cabinet'):
            if Fan_option=='TopCoverPlate':
                qty8=(CBDD01+part100+part200+CADS+part400+part500+CADS12)*2
            if Fan_option=='Assembly' and Site_voltage=='120V':
                qty9=(CBDD01+part100+part200+CADS+part400+part500+CADS12)*2
            if Fan_option=='Assembly' and Site_voltage=='240V':
                qty10=(CBDD01+part100+part200+CADS+part400+part500+CADS12)*2
            if Fan_option=='Assembly - Universal Fan':
                qty11=(CBDD01+part100+part200+CADS+part400+part500+CADS12)*2
            if Fan_option=='Grille':
                qty12=(CBDD01+part100+part200+CADS+part400+part500+CADS12)*2
            if Fan_option=='24V Assembly':
                qty13=(CBDD01+part100+part200+CADS+part400+part500+CADS12)*1
        else:
            qty1=0
            qty3=0
            qty4=0
            qty5=0
            qty6=0
            qty7=0
            qty8=0
            qty9=0
            qty10=0
            qty11=0
            qty12=0
            qty13=0
    elif Product.Name=="Series-C Remote Group":
        io_family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        if Quote.GetCustomField('R2QFlag').Content == "Yes":
            Product.Attr('CE_Site_Voltage').AssignValue('120V')
            Product.Attr('SerC_RG_Cabinet_Type').SelectDisplayValue('Normal Cabinet')
        mounting_sol=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
        mounting_panel=Product.Attr('Ser_C_RG_Mounting_Panel_Type').GetValue()
        Cabinet_access=Product.Attr('SerC_RG_Cabinet_Access').GetValue()
        Cabinet_type=Product.Attr('SerC_RG_Cabinet_Type').GetValue()
        Power_entry_default=Product.Attr('SerC_RG_Power_Entry_Default').GetValue()
        Cabinet_thermostat=Product.Attr('SerC_RG_Cabinet_Thermostat_Default').GetValue()
        Cabinet_Door_Default=Product.Attr('SerC_RG_Cabinet_Doors_Default').GetValue()
        Fan_option=Product.Attr('SerC_RG_Fan_Option').GetValue()
        Site_voltage=Product.Attr('CE_Site_Voltage').GetValue()
        if io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Single Access' and (Cabinet_type=='Normal Cabinet' or Cabinet_type== 'Alternate Cabinet' or Cabinet_type=='Generic Cabinet'):
            if Fan_option=='TopCoverPlate':
                qty1=(CBDS01+part300+CASS+part600+CASS12)*1
            else:
                if Fan_option=='Assembly - Universal Fan' or Fan_option=='24V Assembly':
                    Trace.Write("test")
                    qty1=(CBDS01+CASS12)*1
            if Fan_option=='Assembly' and Site_voltage=='120V':
                qty3=(CBDS01+part300+CASS+part600+CASS12)*1
            if Fan_option=='Assembly' and Site_voltage=='240V':
                qty4=(CBDS01+part300+CASS+part600+CASS12)*1
            if Fan_option=='Assembly - Universal Fan':
                qty5=(CBDS01+part300+CASS+part600+CASS12)*1
            if Fan_option=='Grille':
                qty6=(CBDS01+part300+CASS+part600+CASS12)*1
            if Fan_option=='24V Assembly':
                qty7=(CBDS01+part300+CASS+part600+CASS12)*1
        elif io_family=='Series C' and mounting_sol=='Cabinet' and Cabinet_access=='Dual Access' and (Cabinet_type=='Normal Cabinet' or Cabinet_type== 'Alternate Cabinet' or Cabinet_type=='Generic Cabinet'):
            if Fan_option=='TopCoverPlate':
                qty8=(CBDD01+part100+part200+CADS+part400+part500+CADS12)*2
            if Fan_option=='Assembly' and Site_voltage=='120V':
                qty9=(CBDD01+part100+part200+CADS+part400+part500+CADS12)*2
            if Fan_option=='Assembly' and Site_voltage=='240V':
                qty10=(CBDD01+part100+part200+CADS+part400+part500+CADS12)*2
            if Fan_option=='Assembly - Universal Fan':
                qty11=(CBDD01+part100+part200+CADS+part400+part500+CADS12)*2
            if Fan_option=='Grille':
                qty12=(CBDD01+part100+part200+CADS+part400+part500+CADS12)*2
            if Fan_option=='24V Assembly':
                qty13=(CBDD01+part100+part200+CADS+part400+part500+CADS12)*1
        else:
            qty1=0
            qty3=0
            qty4=0
            qty5=0
            qty6=0
            qty7=0
            qty8=0
            qty9=0
            qty10=0
            qty11=0
            qty12=0
            qty13=0
    return qty1,qty3,qty4,qty5,qty6,qty7,qty8,qty9,qty10,qty11,qty12,qty13
#Temp=C300_calcs_part3(Product)
#Trace.Write(Temp)