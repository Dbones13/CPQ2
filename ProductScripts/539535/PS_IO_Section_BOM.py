def setAtvQty(Product,AttrName,sv,qty):
    pvs=Product.Attr(AttrName).Values
    for av in pvs:
        if av.Display == sv:
            av.IsSelected=False
            av.Quantity = 0
            if qty > 0:
                av.IsSelected=True
                av.Quantity=qty
                Trace.Write('Selected ' + sv + ' in attribute ' + AttrName + ' at Qty ' + str(qty))
                break
IO_Section_container =  Product.GetContainerByName('PlantCruise_IO_Section_of_PlantCruise_Group')
for row in IO_Section_container.Rows:
    if row["IO_Section"] == "Analog Inputs, Redundant, HART (16pt)":
        ai_r_h = float(row["Modules_Configured"])
    if row["IO_Section"] == "Analog Inputs, Non-Redundant, HART (16pt)":
        ai_nr_h = float(row["Modules_Configured"])
    if row["IO_Section"] == "Analog Inputs, Redundant, Non-HART (16pt)":
        ai_r_nh = float(row["Modules_Configured"])
    if row["IO_Section"] == "Analog Inputs, Non-Redundant, Non-HART (16pt)":
        ai_nr_nh = float(row["Modules_Configured"])
    if row["IO_Section"] == "Differential AI, Redundant, HART (16pt)":
        da_r_h = float(row["Modules_Configured"])
    if row["IO_Section"] == "Differential AI, Non-Redundant, HART (16pt)":
        da_nr_h = float(row["Modules_Configured"])
    if row["IO_Section"] == "TC/RTD IOM (16pt)":
        t_r_i = float(row["Modules_Configured"])
    if row["IO_Section"] == "Analog Output, Redundant, HART (16pt)":
        ao_r_h = float(row["Modules_Configured"])
    if row["IO_Section"] == "Analog Output, Non-Redundant, HART (16pt)":
        ao_nr_h = float(row["Modules_Configured"])
    if row["IO_Section"] == "Analog Output, Redundant, Non-HART (16pt)":
        ao_r_nh = float(row["Modules_Configured"])
    if row["IO_Section"] == "Analog Output, Non-Redundant, Non-HART (16pt)":
        ao_nr_nh = float(row["Modules_Configured"])
    if row["IO_Section"] == "DI 24VDC Redundant (32pt)":
        di_24_r = float(row["Modules_Configured"])
    if row["IO_Section"] == "DI 24VDC Non-Redundant (32pt)":
        di_24_nr = float(row["Modules_Configured"])
    if row["IO_Section"] == "DI SOE 24 VDC Redundant (32pt)":
        ds_24_r = float(row["Modules_Configured"])
    if row["IO_Section"] == "DI SOE 24 VDC Non-Redundant (32pt)":
        ds_24_nr = float(row["Modules_Configured"])
    if row["IO_Section"] == "DO 24VDC Redundant (32pt)":
        do_24_r = float(row["Modules_Configured"])
    if row["IO_Section"] == "DO 24VDC Non-Redundant (32pt)":
        do_24_nr = float(row["Modules_Configured"])
    if row["IO_Section"] == "Local Relay Board Sink ":
        l_r_b_s = float(row["Modules_Configured"])
    if row["IO_Section"] == "DO Relay Board Source (32pt)":
        do_r_b_s = float(row["Modules_Configured"])
    if row["IO_Section"] == "Pulse Accumulation Module Redundant":
        p_a_m_r = float(row["Modules_Configured"])
    if row["IO_Section"] == "Pulse Accumulation Module Non-Redundant":
        p_a_m_nr = float(row["Modules_Configured"])
    if row["IO_Section"] == "LLMux TC FTA (16pt) PWA":
        l_t_f = float(row["Modules_Configured"])
    if row["IO_Section"] == "LLMux RTD FTA (16pt)":
        l_r_f = float(row["Modules_Configured"])


setAtvQty(Product,"PlantCruise_Part_Summary","8C-TAIDA1",da_nr_h)
setAtvQty(Product,"PlantCruise_Part_Summary","8C-TAIXA1",ai_nr_h + ai_nr_nh)
setAtvQty(Product,"PlantCruise_Part_Summary","8C-TAOXA1",ao_nr_h + ao_nr_nh)
setAtvQty(Product,"PlantCruise_Part_Summary","8C-TAIDB1",da_r_h)
setAtvQty(Product,"PlantCruise_Part_Summary","8C-TAIXB1",ai_r_h + ai_r_nh)
setAtvQty(Product,"PlantCruise_Part_Summary","8C-TAOXB1",ao_r_h + ao_r_nh)
setAtvQty(Product,"PlantCruise_Part_Summary","8C-PAINA1",2*ai_r_nh + ai_nr_nh)
setAtvQty(Product,"PlantCruise_Part_Summary","8C-PAIHA1",2*ai_r_h + ai_nr_h)
setAtvQty(Product,"PlantCruise_Part_Summary","8C-PAIH54",2*da_r_h + da_nr_h)
setAtvQty(Product,"PlantCruise_Part_Summary","8C-PDODA1",2*do_24_r + do_24_nr)
setAtvQty(Product,"PlantCruise_Part_Summary","8C-SDOX01",l_r_b_s + do_r_b_s)
setAtvQty(Product,"PlantCruise_Part_Summary","8C-TDODB1",do_24_r)
setAtvQty(Product,"PlantCruise_Part_Summary","8C-TDODA1",do_24_nr)
setAtvQty(Product,"PlantCruise_Part_Summary","8C-PDISA1",2* ds_24_r + ds_24_nr)
setAtvQty(Product,"PlantCruise_Part_Summary","8C-PDIPA1",2* p_a_m_r + p_a_m_nr)
setAtvQty(Product,"PlantCruise_Part_Summary","8C-PDILA1",2* di_24_r + di_24_nr)
setAtvQty(Product,"PlantCruise_Part_Summary","8C-TDILB1",di_24_r + ds_24_r + 2* p_a_m_r)
setAtvQty(Product,"PlantCruise_Part_Summary","8C-TDILA1",di_24_nr + ds_24_nr + p_a_m_nr)
setAtvQty(Product,"PlantCruise_Part_Summary","8C-PAONA1",2*ao_r_nh + ao_nr_nh)
setAtvQty(Product,"PlantCruise_Part_Summary","8C-PAOHA1",2*ao_r_h + ao_nr_h)
setAtvQty(Product,"PlantCruise_Part_Summary","8C-TAIMA1",t_r_i)
setAtvQty(Product,"PlantCruise_Part_Summary","8C-PAIMA1",t_r_i)
setAtvQty(Product,"PlantCruise_Part_Summary","MC-TAMT04",l_t_f)
setAtvQty(Product,"PlantCruise_Part_Summary","MC-TAMR04",l_r_f)
Product.ApplyRules()