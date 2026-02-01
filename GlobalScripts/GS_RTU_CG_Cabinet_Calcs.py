import System.Decimal as d

def calc_cabinet_rtu_system(attrs, parts_dict, io, dio):
    total_ios = 0
    if attrs.controller_redundancy == 'Non Redundant':
        total_ios = str(int(io)-1)
    else:
        total_ios = str(io)
    cabinet_count = 0
    if attrs.cabinet_mounting == 'Yes':
        if attrs.cabinet_type == 'One':
            #CXCPQ-25628
            spare_spc_io = (float(float(io) + float(dio)) * float(attrs.cab_spare_space_per))/100
            tio_model_cab = float(io) + float(dio) + float(spare_spc_io)
            #CXCPQ-25630
            if attrs.integrated_marshalling_cab == 'No':
                cabinet_count = d.Ceiling(float(tio_model_cab) / 15)
            elif attrs.integrated_marshalling_cab == 'Yes':
                cabinet_count = d.Ceiling(float(tio_model_cab) / 8)
        
            # CXCPQ-25632
            if cabinet_count > 0:
                Trace.Write('cabinet_count : ' + str(cabinet_count))
                parts_dict["51196958-400"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'PALLET, RITTAL, 1-BAY'}
                parts_dict["CF-MSD000"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'Ship Crate-IMH-RD-NPK-48x48x52'}
                parts_dict["51198959-200"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'NAMEPLATE, RITTAL'}
                parts_dict["51121311-200"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'KIT, SERIES C STD SGL CABINET HARDWARE'}
                parts_dict["CC-CBDS01"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'CAB ASSY, BASIC SGL ACCESS SERIES-C'}
                parts_dict["MU-C8SSS1"] = {'Quantity' : int(2 * cabinet_count), 'Description': 'SIDE PANEL, SINGLE-ACCESS TS8 CABINET'}
                
                #CXCPQ-25631
                if attrs.ce_proj_site_volt == '120V':
                    parts_dict["51199947-175"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'Fan Assembly Kit,115VAC,EC,CC'}
                elif attrs.ce_proj_site_volt == '240V':
                    parts_dict["51199947-275"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'Fan Assembly Kit,230VAC,EC,CC'}
                # CXCPQ-29570
                if attrs.cabinet_Power_Entry == 'None':
                    parts_dict["51306305-300"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'STD AC TERMINAL ASSY 3-INPUT'}
                elif attrs.cabinet_Power_Entry == 'DoublePole':
                    parts_dict["51403902-100"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'Breaker Box Assembly'}
                # CXCPQ-25624
                if attrs.cabinet_Door_Keylock == "Standard":
                    parts_dict["51197165-100"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'KEYLOCK, INSERT TS8 CAB'}
                elif attrs.cabinet_Door_Keylock == "Pushbutton":
                    parts_dict["51197165-200"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'KEYLOCK, PUSH BUTTON TS8 CAB'}
                #CXCPQ-29568
                if attrs.cabinet_access == 'Single Access':
                    parts_dict["51197150-500"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'INSTRUCTIONS, R-HINGE SINGLE DOOR'}
                    parts_dict["MU-C8DRS1"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'DOOR FULL-SIZE HPM RITTAL TS8 CABINET'}
                elif attrs.cabinet_access == 'Dual Access':
                    parts_dict["MU-C8DRD1"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'TS8 CABINET DOUBLE DOOR W/FILTER/GASKET'}
                # CXCPQ-29569
                if attrs.cabinet_Base_Size == '100mm':
                    parts_dict["MU-C8SBA1"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'BASE/PLINTH,4PIN,SINGLE-ACCESS'}
                    #Below part number is commented as per the business team request
                    #parts_dict["CF-SP0000"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'Ship Crate-PMCab-RD-NPK-39x38x92'}
                elif attrs.cabinet_Base_Size == '200mm':
                    parts_dict["MU-C8SBA2"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'BASE/PLINTH,8IN,SINGLE-ACCESS TS8 CABI'}
                    #Below part number is commented as per the business team request
                    #parts_dict["CF-SP0001"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'Ship Crate-PMCab-RD-NPK-39x38x100'}
                # CXCPQ-25625
                if attrs.Cabinet_Thermostat == 'Yes':
                    parts_dict["MU-C8TRM1"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'THERMOSTAT, TS8 RITTAL CABINET'}
                    
                # CXCPQ-25626
                if attrs.cabinet_light == "Yes":
                    parts_dict["MU-CULF01"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'CABINET LIGHT OPTION'}
                # CXCPQ-25621
                if attrs.pwr_sply_type == 'Redundant':
                    if attrs.pwr_sply_model == 'Meanwell':
                        parts_dict["CU-PWMR20"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'Redundant 20A Power supply-meanwell'}
                    elif attrs.pwr_sply_model == 'PhoenixContact':
                        parts_dict["CU-PWPR20"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'Redundant 20A Power supply-Phoenix contact'}
                elif attrs.pwr_sply_type == 'NonRedundant':
                    if attrs.pwr_sply_model == 'Meanwell':
                        parts_dict["CU-PWMN20"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'Non Redundant 20A Power supply-meanwell'}
                    elif attrs.pwr_sply_model == 'PhoenixContact':
                        parts_dict["CU-PWPN20"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'Non Redundant 20A Power supply-Phoenix contact'}
                #Trace.Write('Parts at one : ' + str(parts_dict))
            '''else:
                #Trace.Write('cabinet_count : ' + str(cabinet_count))
                #CXCPQ-25631
                if attrs.ce_proj_site_volt == '120V':
                    parts_dict["51199947-175"] = {'Quantity' : 1, 'Description': 'Fan Assembly Kit,115VAC,EC,CC'}
                elif attrs.ce_proj_site_volt == '240V':
                    parts_dict["51199947-275"] = {'Quantity' : 1, 'Description': 'Fan Assembly Kit,230VAC,EC,CC'}
                # CXCPQ-29570
                if attrs.cabinet_Power_Entry == 'None':
                    parts_dict["51306305-300"] = {'Quantity' : 1, 'Description': 'STD AC TERMINAL ASSY 3-INPUT'}
                elif attrs.cabinet_Power_Entry == 'DoublePole':
                    parts_dict["51403902-100"] = {'Quantity' : 1, 'Description': 'Breaker Box Assembly'}
                # CXCPQ-25624
                if attrs.cabinet_Door_Keylock == "Standard":
                    parts_dict["51197165-100"] = {'Quantity' : 1, 'Description': 'KEYLOCK, INSERT TS8 CAB'}
                elif attrs.cabinet_Door_Keylock == "Pushbutton":
                    parts_dict["51197165-200"] = {'Quantity' : 1, 'Description': 'KEYLOCK, PUSH BUTTON TS8 CAB'}
                #CXCPQ-29568
                if attrs.cabinet_Door_Type == 'Standard':
                    parts_dict["51197150-500"] = {'Quantity' : 1, 'Description': 'INSTRUCTIONS, R-HINGE SINGLE DOOR'}
                    parts_dict["MU-C8DRS1"] = {'Quantity' : 1, 'Description': 'DOOR FULL-SIZE HPM RITTAL TS8 CABINET'}
                elif attrs.cabinet_Door_Type == 'Double':
                    parts_dict["MU-C8DRD1"] = {'Quantity' : 1, 'Description': 'TS8 CABINET DOUBLE DOOR W/FILTER/GASKET'}
                # CXCPQ-29569
                if attrs.cabinet_Base_Size == '100mm':
                    parts_dict["MU-C8SBA1"] = {'Quantity' : 1, 'Description': 'BASE/PLINTH,4PIN,SINGLE-ACCESS'}
                    #Below part number is commented as per the business team request
                    #parts_dict["CF-SP0000"] = {'Quantity' : 1, 'Description': 'Ship Crate-PMCab-RD-NPK-39x38x92'}
                elif attrs.cabinet_Base_Size == '200mm':
                    parts_dict["MU-C8SBA2"] = {'Quantity' : 1, 'Description': 'BASE/PLINTH,8IN,SINGLE-ACCESS TS8 CABI'}
                    #Below part number is commented as per the business team request
                    #parts_dict["CF-SP0001"] = {'Quantity' : 1, 'Description': 'Ship Crate-PMCab-RD-NPK-39x38x100'}
                # CXCPQ-25625
                if attrs.Cabinet_Thermostat == 'Yes':
                    parts_dict["MU-C8TRM1"] = {'Quantity' : '1', 'Description': 'THERMOSTAT, TS8 RITTAL CABINET'}
        
                # CXCPQ-25626
                if attrs.cabinet_light == "Yes":
                    parts_dict["MU-CULF01"] = {'Quantity' : 1, 'Description': 'CABINET LIGHT OPTION'}
                # CXCPQ-25621
                if attrs.pwr_sply_type == 'Redundant':
                    if attrs.pwr_sply_model == 'Meanwell':
                        parts_dict["CU-PWMR20"] = {'Quantity' : 1, 'Description': 'Redundant 20A Power supply-meanwell'}
                    elif attrs.pwr_sply_model == 'PhoenixContact':
                        parts_dict["CU-PWPR20"] = {'Quantity' : 1, 'Description': 'Redundant 20A Power supply-Phoenix contact'}
                elif attrs.pwr_sply_type == 'NonRedundant':
                    if attrs.pwr_sply_model == 'Meanwell':
                        parts_dict["CU-PWMN20"] = {'Quantity' : 1, 'Description': 'Non Redundant 20A Power supply-meanwell'}
                    elif attrs.pwr_sply_model == 'PhoenixContact':
                        parts_dict["CU-PWPN20"] = {'Quantity' : 1, 'Description': 'Non Redundant 20A Power supply-Phoenix contact'}'''
        
        elif attrs.cabinet_type == 'Dual':
                    
            #CXCPQ-29565
            spare_spc_ned = (float(float(io) + float(dio)) * float(attrs.cab_spare_space_per))/100
            tio_model_cab = float(io) + float(dio) + float(spare_spc_ned)
            #CXCPQ-25623
            if attrs.integrated_marshalling_cab == 'No':
                cabinet_count = d.Ceiling(float(tio_model_cab) / 30)
            elif attrs.integrated_marshalling_cab == 'Yes':
                cabinet_count = d.Ceiling(float(tio_model_cab) / 15)
            # CXCPQ-29567
            if cabinet_count > 0:
                Trace.Write('cabinet_count > 0 and dual : ' + str(cabinet_count))
                parts_dict["51196958-400"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'PALLET, RITTAL, 1-BAY'}
                parts_dict["CF-MSD000"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'Ship Crate-IMH-RD-NPK-48x48x52'}
                parts_dict["51198959-200"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'NAMEPLATE, RITTAL'}
                parts_dict["51121311-100"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'SERIES C DUAL CAB INTERNAL KIT'}
                parts_dict["CC-CBDD01"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'CAB ASSY, BASIC DUAL ACCESS SERIES-C'}
                parts_dict["MU-C8DSS1"] = {'Quantity' : int(2 * cabinet_count), 'Description': 'RITTAL TS8 DUAL ACCESS CABINET SIDESKIN'}
                
                #CXCPQ-29566
                if attrs.ce_proj_site_volt == '120V':
                    if attrs.integrated_marshalling_cab == 'No':
                        if float(io)>15:
                            qty=2
                            parts_dict["51199947-175"] = {'Quantity' : int(qty * cabinet_count), 'Description': 'Fan Assembly Kit,115VAC,EC,CC'}
                        else:
                            qty=1
                            parts_dict["51199947-175"] = {'Quantity' : int(qty * cabinet_count), 'Description': 'Fan Assembly Kit,115VAC,EC,CC'}
                    elif attrs.integrated_marshalling_cab == 'Yes':
                        qty=2
                        parts_dict["51199947-175"] = {'Quantity' : int(qty * cabinet_count), 'Description': 'Fan Assembly Kit,115VAC,EC,CC'}
                elif attrs.ce_proj_site_volt == '240V':
                    if attrs.integrated_marshalling_cab == 'No':
                        if float(io)>15:
                            qty=2
                            parts_dict["51199947-275"] = {'Quantity' : int(qty * cabinet_count), 'Description': 'Fan Assembly Kit,230VAC,EC,CC'}
                        else:
                            qty=1
                            parts_dict["51199947-275"] = {'Quantity' : int(qty * cabinet_count), 'Description': 'Fan Assembly Kit,230VAC,EC,CC'}
                    elif attrs.integrated_marshalling_cab == 'Yes':
                        qty=2
                        parts_dict["51199947-275"] = {'Quantity' : int(qty * cabinet_count), 'Description': 'Fan Assembly Kit,230VAC,EC,CC'}
                        
                #CXCPQ-25615
                if attrs.cabinet_access == 'Single Access':
                    parts_dict["51197150-100"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'INSTRUCTIONS, R-HINGE FRONT AND REAR'}
                    parts_dict["MU-C8DRS1"] = {'Quantity' : int(2 * cabinet_count), 'Description': 'DOOR FULL-SIZE HPM RITTAL TS8 CABINET'}
                elif attrs.cabinet_access == 'Dual Access':
                    parts_dict["MU-C8DRD1"] = {'Quantity' : int(2 * cabinet_count), 'Description': 'TS8 CABINET DOUBLE DOOR W/FILTER/GASKET'}
                #CXCPQ-25616
                if attrs.cabinet_Base_Size == '100mm':
                    parts_dict["MU-C8DBA1"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'DUAL BASE, TS8 RITTAL CABINET, 100MM'}
                    #Below part number is commented as per the business team request
                    #parts_dict["CF-SP0000"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'Ship Crate-PMCab-RD-NPK-39x38x92'}
                elif attrs.cabinet_Base_Size == '200mm':
                    parts_dict["MU-C8DBA2"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'DUAL BASE, TS8 RITTAL CABINET, 200MM'}
                    #Below part number is commented as per the business team request
                    #parts_dict["CF-SP0001"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'Ship Crate-PMCab-RD-NPK-39x38x100'}
                #CXCPQ-25617
                if attrs.cabinet_Door_Keylock == 'Standard':
                    parts_dict["51197165-100"] = {'Quantity' : int(2 * cabinet_count), 'Description': 'KEYLOCK, INSERT TS8 CAB'}
                elif attrs.cabinet_Door_Keylock == 'Pushbutton':
                    parts_dict["51197165-200"] = {'Quantity' : int(2 * cabinet_count), 'Description': 'KEYLOCK, PUSH BUTTON TS8 CAB'}
                #CXCPQ-25618
                if attrs.cabinet_Power_Entry == 'None':
                    parts_dict["51306305-300"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'STD AC TERMINAL ASSY 3-INPUT'}
                elif attrs.cabinet_Power_Entry == 'DoublePole':
                    parts_dict["51403902-100"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'Breaker Box Assembly'}
                #CXCPQ-25620
                if attrs.cabinet_light == "Yes":
                    parts_dict["MU-CULF01"] = {'Quantity' : int(2 * cabinet_count), 'Description': 'CABINET LIGHT OPTION'}
                #CXCPQ-25627
                if attrs.pwr_sply_type == 'Redundant':
                    if attrs.pwr_sply_model == 'Meanwell':
                        parts_dict["CU-PWMR20"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'Redundant 20A Power supply-meanwell'}
                    elif attrs.pwr_sply_model == 'PhoenixContact':
                        parts_dict["CU-PWPR20"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'Redundant 20A Power supply-Phoenix contact'}
                elif attrs.pwr_sply_type == 'NonRedundant':
                    if attrs.pwr_sply_model == 'Meanwell':
                        parts_dict["CU-PWMN20"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'Non Redundant 20A Power supply-meanwell'}
                    elif attrs.pwr_sply_model == 'PhoenixContact':
                        parts_dict["CU-PWPN20"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'Non Redundant 20A Power supply-Phoenix contact'}
                # CXCPQ-25619
                if attrs.Cabinet_Thermostat == 'Yes':
                    if attrs.integrated_marshalling_cab == 'No':
                        if int(total_ios) > 15:
                            parts_dict["MU-C8TRM1"] = {'Quantity' : int(2 * cabinet_count), 'Description': 'THERMOSTAT, TS8 RITTAL CABINET'}
                        else:
                            parts_dict["MU-C8TRM1"] = {'Quantity' : int(1 * cabinet_count), 'Description': 'THERMOSTAT, TS8 RITTAL CABINET'}
                    elif attrs.integrated_marshalling_cab == 'Yes':
                            parts_dict["MU-C8TRM1"] = {'Quantity' : int(2 * cabinet_count), 'Description': 'THERMOSTAT, TS8 RITTAL CABINET'}
                #Trace.Write('Parts : ' + str(parts_dict))
            '''else:
                #Trace.Write('cabinet_count : ' + str(cabinet_count))
            
                #CXCPQ-29566
                if attrs.ce_proj_site_volt == '120V':
                    if attrs.integrated_marshalling_cab == 'No':
                        if float(io)>15:
                            qty=2
                            parts_dict["51199947-175"] = {'Quantity' : int(qty), 'Description': 'Fan Assembly Kit,115VAC,EC,CC'}
                        else:
                            qty=1
                            parts_dict["51199947-175"] = {'Quantity' : int(qty), 'Description': 'Fan Assembly Kit,115VAC,EC,CC'}
                    elif attrs.integrated_marshalling_cab == 'Yes':
                        qty=2
                        parts_dict["51199947-175"] = {'Quantity' : int(qty), 'Description': 'Fan Assembly Kit,115VAC,EC,CC'}
                elif attrs.ce_proj_site_volt == '240V':
                    if attrs.integrated_marshalling_cab == 'No':
                        if float(io)>15:
                            qty=2
                            parts_dict["51199947-275"] = {'Quantity' : int(qty), 'Description': 'Fan Assembly Kit,230VAC,EC,CC'}
                        else:
                            qty=1
                            parts_dict["51199947-275"] = {'Quantity' : int(qty), 'Description': 'Fan Assembly Kit,230VAC,EC,CC'}
                    elif attrs.integrated_marshalling_cab == 'Yes':
                        qty=2
                        parts_dict["51199947-275"] = {'Quantity' : int(qty), 'Description': 'Fan Assembly Kit,230VAC,EC,CC'}
                        
                #CXCPQ-25615
                if attrs.cabinet_Door_Type == 'Standard':
                    parts_dict["51197150-100"] = {'Quantity' : 1, 'Description': 'INSTRUCTIONS, R-HINGE FRONT AND REAR'}
                    parts_dict["MU-C8DRS1"] = {'Quantity' : 2, 'Description': 'DOOR FULL-SIZE HPM RITTAL TS8 CABINET'}
                elif attrs.cabinet_Door_Type == 'Double':
                    parts_dict["MU-C8DRD1"] = {'Quantity' : 2, 'Description': 'TS8 CABINET DOUBLE DOOR W/FILTER/GASKET'}
                #CXCPQ-25616
                if attrs.cabinet_Base_Size == '100mm':
                    parts_dict["MU-C8DBA1"] = {'Quantity' : 1, 'Description': 'DUAL BASE, TS8 RITTAL CABINET, 100MM'}
                    #Below part number is commented as per the business team request
                    #parts_dict["CF-SP0000"] = {'Quantity' : 1, 'Description': 'Ship Crate-PMCab-RD-NPK-39x38x92'}
                elif attrs.cabinet_Base_Size == '200mm':
                    parts_dict["MU-C8DBA2"] = {'Quantity' : 1, 'Description': 'DUAL BASE, TS8 RITTAL CABINET, 200MM'}
                    #Below part number is commented as per the business team request
                    #parts_dict["CF-SP0001"] = {'Quantity' : 1, 'Description': 'Ship Crate-PMCab-RD-NPK-39x38x100'}
                #CXCPQ-25617
                if attrs.cabinet_Door_Keylock == 'Standard':
                    parts_dict["51197165-100"] = {'Quantity' : 2, 'Description': 'KEYLOCK, INSERT TS8 CAB'}
                elif attrs.cabinet_Door_Keylock == 'Pushbutton':
                    parts_dict["51197165-200"] = {'Quantity' : 2, 'Description': 'KEYLOCK, PUSH BUTTON TS8 CAB'}
                #CXCPQ-25618
                if attrs.cabinet_Power_Entry == 'None':
                    parts_dict["51306305-300"] = {'Quantity' : 1, 'Description': 'STD AC TERMINAL ASSY 3-INPUT'}
                elif attrs.cabinet_Power_Entry == 'DoublePole':
                    parts_dict["51403902-100"] = {'Quantity' : 1, 'Description': 'Breaker Box Assembly'}
                #CXCPQ-25620
                if attrs.cabinet_light == "Yes":
                    parts_dict["MU-CULF01"] = {'Quantity' : 2, 'Description': 'CABINET LIGHT OPTION'}
                #CXCPQ-25627
                if attrs.pwr_sply_type == 'Redundant':
                    if attrs.pwr_sply_model == 'Meanwell':
                        parts_dict["CU-PWMR20"] = {'Quantity' : 1, 'Description': 'Redundant 20A Power supply-meanwell'}
                    elif attrs.pwr_sply_model == 'PhoenixContact':
                        parts_dict["CU-PWPR20"] = {'Quantity' : 1, 'Description': 'Redundant 20A Power supply-Phoenix contact'}
                elif attrs.pwr_sply_type == 'NonRedundant':
                    if attrs.pwr_sply_model == 'Meanwell':
                        parts_dict["CU-PWMN20"] = {'Quantity' : 1, 'Description': 'Non Redundant 20A Power supply-meanwell'}
                    elif attrs.pwr_sply_model == 'PhoenixContact':
                        parts_dict["CU-PWPN20"] = {'Quantity' : 1, 'Description': 'Non Redundant 20A Power supply-Phoenix contact'}
                # CXCPQ-25619
                if attrs.Cabinet_Thermostat == 'Yes':
                    if attrs.integrated_marshalling_cab == 'No':
                        if int(total_ios) > 15:
                            parts_dict["MU-C8TRM1"] = {'Quantity' : 2, 'Description': 'THERMOSTAT, TS8 RITTAL CABINET'}
                        else:
                            parts_dict["MU-C8TRM1"] = {'Quantity' : 1, 'Description': 'THERMOSTAT, TS8 RITTAL CABINET'}
                    elif attrs.integrated_marshalling_cab == 'Yes':
                            parts_dict["MU-C8TRM1"] = {'Quantity' : 2, 'Description': 'THERMOSTAT, TS8 RITTAL CABINET'}'''
    return parts_dict