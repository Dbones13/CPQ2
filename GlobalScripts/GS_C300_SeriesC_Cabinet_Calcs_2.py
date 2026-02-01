import System.Decimal as D
import GS_C300_MCAR_calcs
import GS_C300_Series_C_Turbomachinery_cabinet_bays
#51553
def C300_part1(Product):
    CBDS01,CBDD01,RF_4,RR_3,RFR_2,RF_6,RR_5,RFR_5,Std_5,Gray_200,Custom_100,Single_S1,Single_D1,Dual_S1,Dual_D1,Single_130,Single_180,Dual_130,Dual_180,X,Y,Z,L,C1,C2=GS_C300_MCAR_calcs.cab_51436(Product)
    
    Turbo1=Turbo2=Turbo3=Turbo4=MU_CULF01=MU_C8TRM1=Q_51199948100=Turbo5=Turbo6=0
    Turbo7=0
    if Product.Name=="Series-C Control Group":
        io_family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        Cabinet_access=Product.Attr('SerC_CG_Cabinet_Access').GetValue()
        Cabinet_Light_default=Product.Attr('SerC_CG_Cabinet_Light_Default').GetValue()
        Cabinet_Thermostat_Default=Product.Attr('SerC_CG_Cabinet_Thermostat_Default').GetValue()
        Fan_option=Product.Attr('SerC_CG_Fan_Option').GetValue()
        power_entry_default=Product.Attr('SerC_CG_Power_Entry_Default').GetValue()
        
        #51553
        if io_family=='Turbomachinery' and Cabinet_access=='Single Access' and power_entry_default=='Double Pole':
            Turbo1=CBDS01*1
        if io_family=='Turbomachinery' and Cabinet_access=='Dual Access' and power_entry_default=='Double Pole':
            Turbo2=CBDD01*2
        if io_family=='Turbomachinery' and Cabinet_access=='Single Access':
            Turbo3=CBDS01*1
        if io_family=='Turbomachinery' and Cabinet_access=='Dual Access':
            Turbo4=CBDD01*2
        #51554
        if io_family=='Turbomachinery' and Cabinet_access=='Single Access':
            Turbo5=CBDS01*1
        if io_family=='Turbomachinery' and Cabinet_access=='Dual Access':
            Turbo5=CBDD01*1
        if io_family=='Turbomachinery' and Cabinet_access=='Dual Access':
            Turbo6=CBDD01*1
        if io_family=='Turbomachinery' and Cabinet_access=='Single Access':
            Turbo7=CBDS01*1
        #51551
        if io_family=='Turbomachinery' and Cabinet_access=='Single Access' and Cabinet_Light_default=="Yes":
            MU_CULF01=CBDS01*1
        if io_family=='Turbomachinery' and Cabinet_access=='Dual Access' and Cabinet_Light_default=="Yes":
            MU_CULF01=CBDD01*2
        #51552
        if io_family=='Turbomachinery' and Cabinet_access=='Single Access' and Cabinet_Thermostat_Default=="Yes":
            MU_C8TRM1=CBDS01*1
        if io_family=='Turbomachinery' and Cabinet_access=='Dual Access' and Cabinet_Thermostat_Default=="Yes":
            MU_C8TRM1=CBDD01*2
        #51530
        if io_family=='Turbomachinery' and Cabinet_access=='Single Access' and Fan_option=="Assembly - Universal Fan":
            Q_51199948100=CBDS01*1
        if io_family=='Turbomachinery' and Cabinet_access=='Dual Access' and Fan_option=="Assembly - Universal Fan":
            Q_51199948100=CBDD01*2
    elif Product.Name=="Series-C Remote Group":
        io_family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        Cabinet_access=Product.Attr('SerC_RG_Cabinet_Access').GetValue()
        Cabinet_Light_default=Product.Attr('SerC_RG_Cabinet_Light_Default').GetValue()
        Cabinet_Thermostat_Default=Product.Attr('SerC_RG_Cabinet_Thermostat_Default').GetValue()
        Fan_option=Product.Attr('SerC_RG_Fan_Option').GetValue()
        power_entry_default=Product.Attr('SerC_RG_Power_Entry_Default').GetValue()
        
        #51553
        if io_family=='Turbomachinery' and Cabinet_access=='Single Access' and power_entry_default=='Double Pole':
            Turbo1=CBDS01*1
        if io_family=='Turbomachinery' and Cabinet_access=='Dual Access' and power_entry_default=='Double Pole':
            Turbo2=CBDD01*2
        if io_family=='Turbomachinery' and Cabinet_access=='Single Access':
            Turbo3=CBDS01*1
        if io_family=='Turbomachinery' and Cabinet_access=='Dual Access':
            Turbo4=CBDD01*2
        #51554
        if io_family=='Turbomachinery' and Cabinet_access=='Single Access':
            Turbo5=CBDS01*1
        if io_family=='Turbomachinery' and Cabinet_access=='Dual Access':
            Turbo5=CBDD01*1
        if io_family=='Turbomachinery' and Cabinet_access=='Dual Access':
            Turbo6=CBDD01*1
        if io_family=='Turbomachinery' and Cabinet_access=='Single Access':
            Turbo7=CBDS01*1
        #51551
        if io_family=='Turbomachinery' and Cabinet_access=='Single Access' and Cabinet_Light_default=="Yes":
            MU_CULF01=CBDS01*1
        if io_family=='Turbomachinery' and Cabinet_access=='Dual Access' and Cabinet_Light_default=="Yes":
            MU_CULF01=CBDD01*2
        #51552
        if io_family=='Turbomachinery' and Cabinet_access=='Single Access' and Cabinet_Thermostat_Default=="Yes":
            MU_C8TRM1=CBDS01*1
        if io_family=='Turbomachinery' and Cabinet_access=='Dual Access' and Cabinet_Thermostat_Default=="Yes":
            MU_C8TRM1=CBDD01*2
        #51530
        if io_family=='Turbomachinery' and Cabinet_access=='Single Access' and Fan_option=="Assembly - Universal Fan":
           Q_51199948100=CBDS01*1
        if io_family=='Turbomachinery' and Cabinet_access=='Dual Access' and Fan_option=="Assembly - Universal Fan":
            Q_51199948100=CBDD01*2
    return Turbo1,Turbo2,Turbo3,Turbo4,MU_CULF01,MU_C8TRM1,Q_51199948100,Turbo5,Turbo6,Turbo7


#51529
def C300_part3(Product):
    CBDS01,CBDD01,RF_4,RR_3,RFR_2,RF_6,RR_5,RFR_5,Std_5,Gray_200,Custom_100,Single_S1,Single_D1,Dual_S1,Dual_D1,Single_130,Single_180,Dual_130,Dual_180,X,Y,Z,L,C1,C2=GS_C300_MCAR_calcs.cab_51436(Product)
    MU_C8SBA1=MU_C8SBA2=MU_C8DBA1=MU_C8DBA2=0 
    if Product.Name=="Series-C Control Group":
        io_family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        Cabinet_access=Product.Attr('SerC_CG_Cabinet_Access').GetValue()
        Cabinet_base_plinth=Product.Attr('SerC_CG_Cabinet_Base_(Plinth)').GetValue()
        Cabinet_base_size=Product.Attr('SerC_CG_Cabinet_Base_Size').GetValue()
        if io_family=='Turbomachinery' and Cabinet_access=='Single Access' and Cabinet_base_plinth=='Yes':
            if Cabinet_base_size=='100mm':
                MU_C8SBA1=CBDS01*1
            if Cabinet_base_size=='200mm':
                MU_C8SBA2=CBDS01*1
        if io_family=='Turbomachinery' and Cabinet_access=='Dual Access' and Cabinet_base_plinth=='Yes':
            if Cabinet_base_size=='100mm':
                MU_C8DBA1=CBDD01*1
            if Cabinet_base_size=='200mm':
                MU_C8DBA2=CBDD01*1
    elif Product.Name=="Series-C Remote Group":
        io_family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        Cabinet_access=Product.Attr('SerC_RG_Cabinet_Access').GetValue()
        Cabinet_base_plinth=Product.Attr('SerC_RG_Cabinet_Base_(Plinth)').GetValue()
        Cabinet_base_size=Product.Attr('SerC_RG_Cabinet_Base_Size').GetValue()

        if io_family=='Turbomachinery' and Cabinet_access=='Single Access' and Cabinet_base_plinth=='Yes':
            if Cabinet_base_size=='100mm':
                MU_C8SBA1=CBDS01*1
            if Cabinet_base_size=='200mm':
                MU_C8SBA2=CBDS01*1
        if io_family=='Turbomachinery' and Cabinet_access=='Dual Access' and Cabinet_base_plinth=='Yes':
            if Cabinet_base_size=='100mm':
                MU_C8DBA1=CBDD01*1
            if Cabinet_base_size=='200mm':
                MU_C8DBA2=CBDD01*1
    return MU_C8SBA1,MU_C8SBA2,MU_C8DBA1,MU_C8DBA2
#CXCPQ-51526,51550
def C300_part2(Product):
    CBDS01,CBDD01,RF_4,RR_3,RFR_2,RF_6,RR_5,RFR_5,Std_5,Gray_200,Custom_100,Single_S1,Single_D1,Dual_S1,Dual_D1,Single_130,Single_180,Dual_130,Dual_180,X,Y,Z,L,C1,C2=GS_C300_MCAR_calcs.cab_51436(Product)
    Q51197165_100=Q51197165_200=Q51199947_175=Q51199947_275=Q51199947_375=0
    if Product.Name=="Series-C Control Group":
        io_family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        Cabinet_access=Product.Attr('SerC_CG_Cabinet_Access').GetValue()
        Cabinet_door_keylock=Product.Attr('SerC_CG_Cabinet_Door_Keylock _Default').GetValue()
        Fan_option=Product.Attr('SerC_CG_Fan_Option').GetValue()
        site_voltage =Product.Attr('CE_Site_Voltage').GetValue()
        if io_family=='Turbomachinery' and Cabinet_access=='Single Access':
            if Cabinet_door_keylock=='Standard':
                Q51197165_100=CBDS01*1
            if Cabinet_door_keylock=='Pushbutton':
                Q51197165_200=CBDS01*1
        if io_family=='Turbomachinery' and Cabinet_access=='Dual Access':
            if Cabinet_door_keylock=='Standard':
                Q51197165_100=CBDD01*2
            if Cabinet_door_keylock=='Pushbutton':
                Q51197165_200=CBDD01*2
        #51550
        if io_family=='Turbomachinery' and Cabinet_access=='Single Access':
            if Fan_option=='Assembly' and site_voltage=='120V':
                Q51199947_175=CBDS01*1
            if Fan_option=='Assembly'and site_voltage=='240V':
                Q51199947_275=CBDS01*1
            if Fan_option=='Assembly - Universal Fan':
                Q51199947_375=CBDS01*1
        if io_family=='Turbomachinery' and Cabinet_access=='Dual Access':
            if Fan_option=='Assembly' and site_voltage=='120V':
                Q51199947_175=CBDD01*2
            if Fan_option=='Assembly'and site_voltage=='240V':
                Q51199947_275=CBDD01*2
            if Fan_option=='Assembly - Universal Fan':
                Q51199947_375=CBDD01*2
    elif Product.Name=="Series-C Remote Group":
        io_family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        Cabinet_access=Product.Attr('SerC_RG_Cabinet_Access').GetValue()
        Cabinet_door_keylock=Product.Attr('SerC_RG_Cabinet_Door_Keylock_Default').GetValue()
        Fan_option=Product.Attr('SerC_RG_Fan_Option').GetValue()
        site_voltage =Product.Attr('CE_Site_Voltage').GetValue()

        if io_family=='Turbomachinery' and Cabinet_access=='Single Access':
            if Cabinet_door_keylock=='Standard':
                Q51197165_100=CBDS01*1
            if Cabinet_door_keylock=='Pushbutton':
                Q51197165_200=CBDS01*1
        if io_family=='Turbomachinery' and Cabinet_access=='Dual Access':
            if Cabinet_door_keylock=='Standard':
                Q51197165_100=CBDD01*2
            if Cabinet_door_keylock=='Pushbutton':
                Q51197165_200=CBDD01*2
        #51550
        if io_family=='Turbomachinery' and Cabinet_access=='Single Access':
            if Fan_option=='Assembly' and site_voltage=='120V':
                Q51199947_175=CBDS01*1
            if Fan_option=='Assembly'and site_voltage=='240V':
                Q51199947_275=CBDS01*1
            if Fan_option=='Assembly - Universal Fan':
                Q51199947_375=CBDS01*1
        if io_family=='Turbomachinery' and Cabinet_access=='Dual Access':
            if Fan_option=='Assembly' and site_voltage=='120V':
                Q51199947_175=CBDD01*2
            if Fan_option=='Assembly'and site_voltage=='240V':
                Q51199947_275=CBDD01*2
            if Fan_option=='Assembly - Universal Fan':
                Q51199947_375=CBDD01*2
    return Q51197165_100,Q51197165_200,Q51199947_175,Q51199947_275,Q51199947_375
#CXCPQ-51528,51527
def C300_part4(Product):
    A,B,C,D,E,F=GS_C300_Series_C_Turbomachinery_cabinet_bays.Turbo_cab_bays(Product)
    Trace.Write('A'+str(A))
    Trace.Write('B'+str(B))
    Trace.Write('C'+str(C))
    Trace.Write('D'+str(D))
    Trace.Write('E'+str(E))
    Trace.Write('F'+str(F))
    MU_C8DSS1=MU_C8SSS1=0
    if Product.Name=="Series-C Control Group":
        io_family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        Cabinet_access=Product.Attr('SerC_CG_Cabinet_Access').GetValue()
        #51527
        if io_family=='Turbomachinery' and Cabinet_access=='Single Access':
            MU_C8SSS1=(B+D+E+F)*2
        #51528
        if io_family=='Turbomachinery' and Cabinet_access=='Dual Access':
            MU_C8DSS1=(B+D+E+F)*2
    elif Product.Name=="Series-C Remote Group":
        io_family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
        Cabinet_access=Product.Attr('SerC_RG_Cabinet_Access').GetValue()
        #51527
        if io_family=='Turbomachinery' and Cabinet_access=='Single Access':
            MU_C8SSS1=(B+D+E+F)*2
        #51528
        if io_family=='Turbomachinery' and Cabinet_access=='Dual Access':
            MU_C8DSS1=(B+D+E+F)*2
    return MU_C8DSS1,MU_C8SSS1
#Temp=C300_part3(Product)
#Trace.Write(Temp)