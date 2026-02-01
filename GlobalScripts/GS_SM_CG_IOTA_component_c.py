def getFloat(var):
    if var:
        return float(var)
    return 0
def get_comp_c(Product):
    if Product.Name == "SM Control Group":
        power_supply = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName("Power_Supply").DisplayValue
                #DI
        uio_di_sil2 = getFloat(Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[1].GetColumnByName("Red (IS)").Value)
        uio_di_sil2_nr = getFloat(Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[1].GetColumnByName("Non Red (IS)").Value)

        uio_di_sil3 = getFloat(Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[2].GetColumnByName("Red (IS)").Value)
        uio_di_sil3_nr = getFloat(Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[2].GetColumnByName("Non Red (IS)").Value)

                # AI
        uio_ai_pf = getFloat(Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[1].GetColumnByName("Red (IS)").Value)
        uio_ai_pf_nr = getFloat(Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[1].GetColumnByName("Non Red (IS)").Value)
                # AO
        uio_ao_pf = getFloat(Product.GetContainerByName('SM_IO_Count_Analog_Output_Cont').Rows[0].GetColumnByName("Red (IS)").Value)
        uio_ao_pf_nr = getFloat(Product.GetContainerByName('SM_IO_Count_Analog_Output_Cont').Rows[0].GetColumnByName("Non Red (IS)").Value)
        
                # DO
        uio_do_sil3 = getFloat(Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[1].GetColumnByName("Red (IS)").Value)
        uio_do_sil3_nr = getFloat(Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[1].GetColumnByName("Non Red (IS)").Value)
        

        sil2_di = sil3_di = typePf_ai = typePf_ao = sil3_do = 0
        component_C = 0
        if power_supply == "Redundant":
                # DI
            sil2_di = (int(uio_di_sil2) * 7.0) + 600.0
            sil3_di = (int(uio_di_sil3) * 7.0) + 600.0
                    # AI
            typePf_ai = (int(uio_ai_pf) * 25.0) + 600.0
                    # AO
            typePf_ao = (int(uio_ao_pf) * 25.0) + 600.0
                    # DO
            sil3_do = (int(uio_do_sil3) * 70.0) + 600.0
        

        elif power_supply == "Non Redundant":
                # DI
            sil2_di = (int(uio_di_sil2_nr) * 7.0) + 300.0
            sil3_di = (int(uio_di_sil3_nr) * 7.0) + 300.0
                    # AI
            typePf_ai = (int(uio_ai_pf_nr) * 25.0) + 300.0
                    # AO
            typePf_ao = (int(uio_ao_pf_nr) * 25.0) + 300.0
                    # DO
            sil3_do = (int(uio_do_sil3_nr) * 70.0) + 300.0
        component_C = sil2_di+sil3_di+typePf_ai+typePf_ao+sil3_do
        return component_C
        Trace.Write(component_C)

    elif Product.Name == "SM Remote Group":
        power_supply = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName("Power_Supply").DisplayValue

        uio_di_sil2 = getFloat(Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[1].GetColumnByName("Red_IS").Value)
        uio_di_sil2_nr = getFloat(Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[1].GetColumnByName("Non_Red_IS").Value)

        uio_di_sil3 = getFloat(Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[2].GetColumnByName("Red_IS").Value)
        uio_di_sil3_nr = getFloat(Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[2].GetColumnByName("Non_Red_IS").Value)

                # AI
        uio_ai_pf = getFloat(Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[1].GetColumnByName("Red_IS").Value)
        uio_ai_pf_nr = getFloat(Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[1].GetColumnByName("Non_Red_IS").Value)
                # AO
        uio_ao_pf = getFloat(Product.GetContainerByName('SM_RG_IO_Count_Analog_Output_Cont').Rows[1].GetColumnByName("Red_IS").Value)
        uio_ao_pf_nr = getFloat(Product.GetContainerByName('SM_RG_IO_Count_Analog_Output_Cont').Rows[1].GetColumnByName("Non_Red_IS").Value)
                # DO
        uio_do_sil3 = getFloat(Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[1].GetColumnByName("Red_IS").Value)
        uio_do_sil3_nr = getFloat(Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[1].GetColumnByName("Non_Red_IS").Value)

        sil2_di = sil3_di = typePf_ai = typePf_ao = sil3_do = 0
        component_C = 0
        if power_supply == "Redundant":
                    # DI
            sil2_di = (int(uio_di_sil2) * 7.0) + 600.0
            sil3_di = (int(uio_di_sil3) * 7.0) + 600.0
                    # AI
            typePf_ai = (int(uio_ai_pf) * 25.0) + 600.0
                    # AO
            typePf_ao = (int(uio_ao_pf) * 25.0) + 600.0
                    # DO
            sil3_do = (int(uio_do_sil3) * 70.0) + 600.0
            

        elif power_supply == "Non Redundant":
                    # DI
            sil2_di = (int(uio_di_sil2_nr) * 7.0) + 300.0
            sil3_di = (int(uio_di_sil3_nr) * 7.0) + 300.0
                    # AI
            typePf_ai = (int(uio_ai_pf_nr) * 25.0) + 300.0
                    # AO
            typePf_ao = (int(uio_ao_pf_nr) * 25.0) + 300.0
                    # DO
            sil3_do = (int(uio_do_sil3_nr) * 70.0) + 300.0
        component_C = sil2_di+sil3_di+typePf_ai+typePf_ao+sil3_do
        return component_C
Trace.Write(get_comp_c(Product))