import GS_SerC_Turbo_IO_Calc, GS_SerC_Refresh_Container

def changeCellEvent(Product, IO_Family_Type, IO_Type, changedColumn, newValue, module, colMapping):
    parts_dict = dict()
    if IO_Family_Type == 'Turbomachinery':
        if newValue >= 0:
            if module == '49227':
                ioTypes = ['Number of Servo Position Modules (0-480)', 'Number of Speed Protection Modules (0-480)']
                if IO_Type in ioTypes:
                    GS_SerC_Turbo_IO_Calc.calcIOModule49227(Product, IO_Type, changedColumn, newValue)
                    parts_dict = GS_SerC_Turbo_IO_Calc.getParts49227(Product, {})
            elif module == '49225':
                ioTypes = ['Series-C: DI (32) 24 VDC with Open Wire Detect (0-5000)', 'Series-C: DI (32) 24VDC SOE (0-5000)']
                ioTypes.extend(['Series-C: GI/IS DI (32) 24VDC Solid State (0-5000)', 'Series-C: GI/IS DI (32) 24 VDC Relay (0-5000)'])
                ioTypes.extend(['Series-C: GI/IS DI (32) 24 VDC Relay LFD (0-5000)', 'Series-C: GI/IS DI (32) 24VDC Relay with Expansion Board (0-5000)'])
                ioTypes.extend(['Series-C: GI/IS DI (32) 24VDC SOE Solid State (0-5000)', 'Series-C: GI/IS DI (32) 24 VDC SOE Relay (0-5000)'])
                ioTypes.extend(['Series-C: GI/IS DI (32) 24 VDC SOE Relay LFD (0-5000)', 'Series-C: GI/IS DI (32) 24VDC SOE Relay with Expansion Board (0-5000)'])
                if IO_Type in ioTypes:
                    GS_SerC_Turbo_IO_Calc.calcIOModule49225(Product, IO_Type, changedColumn, newValue)
                    parts_dict = GS_SerC_Turbo_IO_Calc.getParts49225(Product, {})
            elif module == '49229':
                ioTypes = ['Series-C: HLAI (16) with HART with differential inputs (0-5000)','Series-C: HLAI (16) without HART with differential inputs (0-5000)']
                ioTypes.extend(['Series-C: GI/IS HLAI (16) HART (0-5000)', 'Series-C: GI/IS HLAI (16) HART Single Channel Isolator (0-5000)'])
                ioTypes.extend(['Series-C: GI/IS HLAI (16) HART Dual Channel Isolator (0-5000)', 'Series-C: GI/IS HLAI (16) HART Temperature Isolator (0-5000)'])
                ioTypes.extend(['Series-C: GI/IS HLAI (16) (0-5000)', 'Series-C: GI/IS HLAI (16) Single Channel Isolator (0-5000)'])
                ioTypes.extend(['Series-C: GI/IS HLAI (16) Dual Channel Isolator (0-5000)', 'Series-C: GI/IS HLAI (16) Temperature Isolator (0-5000)'])
                if IO_Type in ioTypes:
                    GS_SerC_Turbo_IO_Calc.calcIOModule49229(Product, IO_Type, changedColumn, newValue)
                    parts_dict = GS_SerC_Turbo_IO_Calc.getParts49229(Product, {})
                    #As parameter of the user story (CXCPQ-49230) depends on CXCPQ-49229 calculation
                    parts_dict = GS_SerC_Turbo_IO_Calc.getParts49230(Product, parts_dict)
            elif module == '49231':
                ioTypes = ['Series-C: LLAI (1) Mux RTD (0-5000)', 'Series-C: LLAI (1) Mux TC (0-5000)', 'Series-C: LLAI (1) Mux TC Remote CJR (0-5000)']
                if IO_Type in ioTypes:
                    GS_SerC_Turbo_IO_Calc.calcIOModule49231(Product, IO_Type, changedColumn, newValue)
                    parts_dict = GS_SerC_Turbo_IO_Calc.getParts49231(Product, {})
                    #As parameter of the userstory CXCPQ-49232 depends on CXCPQ-49231
                    parts_dict = GS_SerC_Turbo_IO_Calc.getParts49232(Product, parts_dict)
            elif module == '49228':
                ioTypes = ['Series-C: UIO (32) Analog Input (HLAI Adapt) (0-5000)', 'Series-C: UIO (32) Analog Input (LLAI Adapt) (0-5000)']
                ioTypes.extend(['Series-C: UIO (32) Analog Output (0-5000)', 'Series-C: UIO (32) Digital Input (0-5000)', 'Series-C: UIO (32) Digital Output (0-5000)'])
                if IO_Type in ioTypes:
                    GS_SerC_Turbo_IO_Calc.calcIOModule49228(Product, IO_Type, changedColumn, newValue)
                    parts_dict = GS_SerC_Turbo_IO_Calc.getParts49228(Product, {})
            elif module == '50461':
                ioTypes = ['Series-C: DI (32) 110 VAC (0-5000)', 'Series-C: DI (32) 110 VAC PROX (0-5000)', 'Series-C: DI (32) 220 VAC (0-5000)']
                if IO_Type in ioTypes:
                    GS_SerC_Turbo_IO_Calc.calcIOModule50461(Product, IO_Type, changedColumn, newValue)
                    parts_dict = GS_SerC_Turbo_IO_Calc.getParts50461(Product, {})
            elif module == '49233':
                ioTypes = ['Series-C: AO (16) HART (0-5000)', 'Series-C: GI/IS AO (16) HART (0-5000)', 'Series-C: GI/IS AO (16) HART Single Channel Isolator (0-5000)', 'Series-C: GI/IS AO (16) HART Dual Channel Isolator (0-5000)']
                if IO_Type in ioTypes:
                    GS_SerC_Turbo_IO_Calc.calcIOModule49233(Product, IO_Type, changedColumn, newValue)
                    parts_dict = GS_SerC_Turbo_IO_Calc.getParts49233(Product, {})
            elif module == '50463':
                ioTypes = ['Series-C: DO (32) 24VDC Bus External Power Supply (0-5000)', 'Series-C: DO (32) 24VDC Bus Internal Power Supply (0-5000)', 'Series-C: DO (32) 24VDC Relay Bus above 30V (0-5000)', 'Series-C: DO (32) 24VDC Relay Bus up to 30V (0-5000)', 'Series-C: GI/IS DO (32) 24 VDC Bus with Expansion Board (0-5000)']
                if IO_Type in ioTypes:
                    GS_SerC_Turbo_IO_Calc.calcIOModule50463(Product, IO_Type, changedColumn, newValue)
                    parts_dict = GS_SerC_Turbo_IO_Calc.getParts50463(Product, {})
        else:
            GS_SerC_Turbo_IO_Calc.setIOCount(Product, 'SerC_IO_Params', {colMapping[changedColumn]:0})
        if Product.Name == "Series-C Control Group":
            GS_SerC_Turbo_IO_Calc.setIOCount(Product, 'Series_C_CG_Part_Summary', parts_dict)
            GS_SerC_Refresh_Container.refreshContainer(Product)
            Product.GetContainerByName('Series_C_CG_Part_Summary_Cont').Calculate()
        elif Product.Name == "Series-C Remote Group":
            GS_SerC_Turbo_IO_Calc.setIOCount(Product, 'Series_C_RG_Part_Summary', parts_dict)
            GS_SerC_Refresh_Container.refreshContainer(Product)
            Product.GetContainerByName('Series_C_RG_Part_Summary_Cont').Calculate()