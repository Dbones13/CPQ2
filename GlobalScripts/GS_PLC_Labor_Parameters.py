class AttrStorage:
    def __init__(self, Product):

        self.project_type = Product.Attr('New_Expansion').GetValue()
        self.loop_drawings = Product.Attr('Labor_Loop_Drawings').GetValue()
        self.unreleased_product = Product.Attr('Labor_Unreleased_Product').GetValue()
        self.marshalling_db = Product.Attr('Labor_Marshalling_Database').GetValue()
        self.perc_fat = Product.Attr('Labor_Percentage_FAT').GetValue()
        self.site_activities = Product.Attr('Labor_Site_Activities').GetValue()
        self.operation_manual = Product.Attr('Labor_Operation_Manual_Scope').GetValue()
        self.custom_scope = Product.Attr('Labor_Custom_Scope').GetValue()
        self.iot = Product.Attr('Number of Total IO Types').GetValue()
        self.sys = 0
        
        #PLC System level Parameters
        self.process_type = Product.GetContainerByName('PLC_Labour_Details').Rows[0].GetColumnByName("PLC_Process_Type").Value
        self.marshalling_cabinets = Product.GetContainerByName('PLC_Labour_Details').Rows[0].GetColumnByName("PLC_Marshalling_Cabinet_Cont").Value
        self.total_count_Typicals_Prototypes = Product.GetContainerByName('PLC_Labour_Details').Rows[0].GetColumnByName("PLC_Enter_Total_Cont").Value
        self.loop_count = Product.GetContainerByName('PLC_Labour_Details').Rows[0].GetColumnByName("PLC_Enter_Total_Cont").Value
        self.seq = Product.GetContainerByName('PLC_Labour_Details').Rows[0].GetColumnByName("PLC_Number_of_Sequences").Value
        self.engineering_stations = Product.GetContainerByName('CE_PLC_System_Hardware').Rows[0].GetColumnByName("PLC_Engineering_Station_Qty").Value
        self.TPY= Product.GetContainerByName('PLC_Labour_Details').Rows[0].GetColumnByName("PLC_3rd_Party_Communication_Signals").Value
        self.hrd_design= Product.GetContainerByName('PLC_Labour_Details').Rows[0].GetColumnByName("PLC_Hardware_Design_Drawing_Complexity").DisplayValue


        #Section to read from Control and Remote Groups
        AI = AO = DI = DO = MODBUS = self.num_switches = self.num_cim = self.num_cpm = self.num_cabinet = self.num_rg = 0.0
        cg_labor_data = SqlHelper.GetList("Select * from Labor_Parameters where Product = 'PLC Control Group' ")
        rg_labor_data = SqlHelper.GetList("Select * from Labor_Parameters where Product = 'PLC Remote Group' ")
        control_groups = Product.GetContainerByName('PLC_ControlGroup_Cont').Rows
        for control_group in control_groups:
            control = control_group.Product
            #This is to read UI inputs
            for record in cg_labor_data: 
                locals()[record.Parameter] += int(control.GetContainerByName(record.Container).Rows[int(record.Row)].GetColumnByName(record.Column).Value)

            #This is to read from Part Summary table
            parts = control.GetContainerByName('PLC_CG_PartSummary_Cont').Rows
            cpu_type = control.GetContainerByName('PLC_CG_Controller_Rack_Cont').Rows[0].GetColumnByName('PLC_Controller_Type').Value
            for part in parts:
                name = part.GetColumnByName('CE_Part_Number').Value
                if name in ['50008930-001', '50008930-002', '50008930-004', '50008930-003', '50135395-001', '50135395-002', '50135395-003', '50008930-008']:
                    self.num_switches += int(part.GetColumnByName('CE_Part_Qty').Value)
                elif name == '900ES1-0100':
                    self.num_cim += 4 * int(part.GetColumnByName('CE_Part_Qty').Value)
                elif name == "CC-CBDS01" or name == "CC-CBDD01":
                    Trace.Write("here cab")
                    self.sys+=int(part.GetColumnByName('CE_Part_Qty').Value)
                elif name == '900CP2-0100' or name == '900CP1-0200':  #Replaced part number 900CP1-0200 by 900CP2-0100 on account of requirement CCEECOMMBR-5445
                    if cpu_type == 'NonRedundant':
                        self.num_cpm += int(part.GetColumnByName('CE_Part_Qty').Value)
                    elif cpu_type == 'Redundant':
                        qty = float(part.GetColumnByName('CE_Part_Qty').Value)
                        if qty % 2 == 0: #This is used just so we don't have to import any modules here. It is really just dividing by 2 and rounding to ceiling.
                            self.num_cpm += int(qty / 2)
                        else:
                            self.num_cpm += int(qty / 2 + 1)
                elif name == '51196958-400': #This is technically just the part number for pallets, but, there is always 1 pallet per cabinet.
                    if control.GetContainerByName('PLC_CG_Cabinet_Cont').Rows[0].GetColumnByName('PLC_Cabinet_Type').Value == 'Dual':
                        self.num_cabinet += int(part.GetColumnByName('CE_Part_Qty').Value)
                    else:
                        qty = float(part.GetColumnByName('CE_Part_Qty').Value)
                        if qty % 2 == 0: #This is used just so we don't have to import any modules here. It is really just dividing by 2 and rounding to ceiling.
                            self.num_cabinet += int(qty / 2)
                        else:
                            self.num_cabinet += int(qty / 2 + 1)
                elif name == "MU-C8SS01" or name == "MU-C8DS01":
                     self.sys+=int(part.GetColumnByName('CE_Part_Qty').Value)

            remote_groups = control.GetContainerByName('PLC_RemoteGroup_Cont').Rows
            if remote_groups.Count != 0:
                #This is to read UI inputs
                for remote_group in remote_groups:
                    self.num_rg += 1
                    remote = remote_group.Product
                    for record in rg_labor_data:
                         if remote.GetContainerByName(record.Container).Rows[int(record.Row)].GetColumnByName(record.Column).Value != '':
							locals()[record.Parameter] += int(remote.GetContainerByName(record.Container).Rows[int(record.Row)].GetColumnByName(record.Column).Value)

                    #This is to read from Part Summary table
                    parts = remote.GetContainerByName('PLC_RG_PartSummary_Cont').Rows
                    for part in parts:
                        name = part.GetColumnByName('CE_Part_Number').Value
                        if name == '900ES1-0100':
                            self.num_cim += 4 * int(part.GetColumnByName('CE_Part_Qty').Value)
                        elif name == "CC-CBDS01" or name == "CC-CBDD01":
                            Trace.Write("here cab")
                            self.sys+=int(part.GetColumnByName('CE_Part_Qty').Value)
                        elif name == '51196958-400': #This is technically just the part number for pallets, but, there is always 1 pallet per cabinet.
                            if remote.GetContainerByName('PLC_RG_Cabinet_Cont').Rows[0].GetColumnByName('PLC_Cabinet_Type').Value == 'Dual':
                                self.num_cabinet += int(part.GetColumnByName('CE_Part_Qty').Value)
                            else:
                                qty = float(part.GetColumnByName('CE_Part_Qty').Value)
                                if qty % 2 == 0: #This is used just so we don't have to import any modules here. It is really just dividing by 2 and rounding to ceiling.
                                    self.num_cabinet += int(qty / 2)
                                else:
                                    self.num_cabinet += int(qty / 2 + 1)
        self.AI = int(AI)
        self.AO = int(AO)
        self.DI = int(DI)
        self.DO = int(DO)
        self.MODBUS = MODBUS
        self.PIDLoops=self.AI
        self.AIIndicator=self.AI-self.AO
        self.Digital1Loop=self.DO/2
        self.Digital2Loop=self.DO/4
        self.DIIndicator=self.DI-(self.Digital1Loop+self.Digital2Loop*2)
        Product.Attr('PLC_PID_Loops').AssignValue(str(self.PIDLoops))
        Product.Attr('PLC_1_IO_Digital_Loop').AssignValue(str(self.Digital1Loop))
        Product.Attr('PLC_2_IO_Digital_Loop').AssignValue(str(self.Digital2Loop))
        Product.Attr('PLC_DI_Indicator').AssignValue(str(self.DIIndicator))
        Product.Attr('PLC_AI_Indicator').AssignValue(str(self.AIIndicator))
        Trace.Write("from attrStorage AI: {0}, AO: {1}, DI: {2}, DO: {3}, MODBUS: {4}".format(AI, AO, DI, DO, MODBUS))
        Trace.Write("num_switches: {0}, num_cim: {1}, num_cpm: {2}, num_cabinet: {3}, num_rg: {4}".format(self.num_switches, self.num_cim, self.num_cpm, self.num_cabinet, self.num_rg))