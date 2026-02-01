import math as m

def getContainer(Product,Name):
    return Product.GetContainerByName(Name)

def getRowData(Product,container,column):
    Container = getContainer(Product,container)
    for row in Container.Rows:
        return row[column]

def getRowDataIndex(Product,container,column,index):
    Container = getContainer(Product,container)
    for row in Container.Rows:
        if row.RowIndex == index:
            return row[column]

def getFloat(Var):
    if Var:
        return float(Var)
    return 0

def getgraphicsMigrationUI(Product):
    parameters ={"Graphics_Migration_Migration_Scenario":{"var_26":"Graphics_Migration_Type_of_Existing_Displays","var_21":"Graphics_Migration_Is_the_system_connected_to_Hiway_Gateway_Controllers?","var_16":"Graphics_Migration_Using_device_control_digital_composite_block_for_all_digital_equipment?","var_17":"Graphics_Migration_Have_multiple_DI_or_DO_parameters_that_must_be_combined_in_one_shape?","var_18":"Graphics_Migration_Require_multi_tag_shapes?","var_19":"Graphics_Migration_Have_process_module_point_AM_custom_Data_points_as_part_of_the_point_config","var_31":"Graphics_Migration_Have_array_point_that_requires_a_HMIWeb_interface?","var_32":"Graphics_Migration_Willing_to_accept_alternative_visualization_solution_for_specific_functions?","var_51":"Graphics_Migration_For_existing_US_GUS_DSP_what_percentage_of_Standard_Builds_will_be_used?","var_34":"Graphics_Migration_Have_specific_native_or_GUS_displays_that_support_a_specific_application?","var_33":"Graphics_Migration_Require_an_HMI_interface_for_AM_or_HPM_CL_applications?"},"Graphics_Migration_Displays_Shapes_Faceplates":{"var_2":"Total_Number_of_Displays","var_35":"Experion_shapes_multiplier"}}
    for key in parameters:
        if key == "Graphics_Migration_Migration_Scenario":
            var_26_check = getRowData(Product,key,parameters[key]["var_26"])
            var_21 = getRowData(Product,key,parameters[key]["var_21"])
            var_16 = getRowData(Product,key,parameters[key]["var_16"])
            var_17 = getRowData(Product,key,parameters[key]["var_17"])
            var_18 = getRowData(Product,key,parameters[key]["var_18"])
            var_19 = getRowData(Product,key,parameters[key]["var_19"])
            var_31 = getRowData(Product,key,parameters[key]["var_31"])
            var_32 = getRowData(Product,key,parameters[key]["var_32"])
            var_33 = getRowData(Product,key,parameters[key]["var_33"])
            var_34 = getRowData(Product,key,parameters[key]["var_34"])
            var_51 = getFloat(getRowData(Product,key,parameters[key]["var_51"]))
        if key == "Graphics_Migration_Displays_Shapes_Faceplates":
            var_2 = getFloat(getRowData(Product,key,parameters[key]["var_2"]))
            var_35_check = getRowData(Product,key,parameters[key]["var_35"])
            if var_35_check:
                var_35 = getFloat(var_35_check)
            else:
                var_35 = 1

    if var_26_check == "Existing US Graphics":
        var_26 = 1
    elif var_26_check == "Existing GUS Graphics":
        var_26 = 2
    elif var_26_check == "Existing Experion .DSP Graphics":
        var_26 = 3
    elif var_26_check == "Existing Experion HMI Web Graphics Release 200-310":
        var_26 = 4
    elif var_26_check == "Existing Experion HMI Web Graphics Release 311-400":
        var_26 = 5
    elif var_26_check == "Existing Experion HMI Web Graphics Release 400-510":
        var_26 = 6
    else:
        var_26 = 0

    L21 = 1 if(var_26<4) else 0
    L22 = 1 if(var_21== "Yes") else 0 
    L24=0
    L24 += 0 if(var_16=="Yes") else 1      
    L24 += 1 if(var_17=="Yes") else 0
    L24 += 0 if(var_18=="No") else 1
    L24 += 1 if(var_19=="Yes") else 0
    L24 += 1 if(var_31=="Yes") else 0
    L24 += 0 if(var_32=="Yes") else 1   
    L24 += 1 if(var_33=="Yes") else 0    
    L24 += 1 if(var_34=="Yes") else 0    
    L25=0
    L25 += 0.8 if(L24==1 or L24==2) else 0
    L25 += 1.4 if(L24==3 or L24==4 or L24==5) else 0
    L25 += 2.8 if(L24==6 or L24==7 or L24==8) else 0
    
    Experion = (var_2 * 0.05 * var_35) if(var_26>3) else 0
    
    TPS_SB = 150 if((m.sqrt(L21+L22)*(L25*m.sqrt(var_2)))>150) else (m.sqrt(L21+L22)*(L25*m.sqrt(var_2)))
    TPS_SB = TPS_SB*var_51/100
    
    TPS_no_SB = 600 if((m.sqrt(L21+L22)*(10*m.sqrt(var_2)))>600) else ((m.sqrt(L21+L22))*(10*m.sqrt(var_2)))
    TPS_no_SB = TPS_no_SB*(100-var_51)/100
    
    
    standard_builds = 0
    x=0
    if var_26 > 3:
        x = var_2* 0.0145
    else:
        x =0.5*m.sqrt(var_2)
    x=m.ceil(x)
    if x > 25:
        standard_builds = 25
    else:
        if var_26>3 :
            standard_builds = var_2*0.0145
        else:
            standard_builds = 0.5*m.sqrt(var_2)
    standard_builds = (m.ceil(standard_builds)* (var_51/100))

    

    Non_standard_builds = 0
    Y=0
    if var_26 > 3:
        Y = var_2* 0.0145
    else:
        Y =1.2*m.sqrt(var_2)
    Y=m.ceil(Y)
    if Y > 50:
         Non_standard_builds = 50
    else:
        if var_26>3 :
            Non_standard_builds = var_2*0.0145
        else:
            Non_standard_builds = 1.2*m.sqrt(var_2)
    Non_standard_builds = (m.ceil((Non_standard_builds) *getFloat(100-var_51)/100.00))
    shape = getFloat(m.ceil(Experion+TPS_SB+TPS_no_SB))
    facePlates = getFloat(standard_builds + Non_standard_builds)

    container_check = Product.GetContainerByName("Graphics_Migration_Migration_Scenario")
    row_check = container_check.Rows[0]
    check = row_check["Graphics_Migration_Select_Vertical_Market_Picklist_with_values"]
    display = getFloat(var_2)
    multipliers = {"Display":{"HPI":{"Ds":"0.1","Dm":"0.7","Dc":"0.2"},"Chemical":{"Ds":"0.3","Dm":"0.3","Dc":"0.4"},"Oil and Gas":{"Ds":"0.15","Dm":"0.6","Dc":"0.25"},"Pharma":{"Ds":"0.1","Dm":"0.2","Dc":"0.7"},"Sheet Manufacturing":{"Ds":"0.25","Dm":"0.4","Dc":"0.35"},"Power Gen":{"Ds":"0.2","Dm":"0.5","Dc":"0.3"},"Other":{"Ds":"0.4","Dm":"0.1","Dc":"0.5"}},"Shapes":{"HPI":{"Ss":"0.2","Sm":"0.7","Sc":"0.1"},"Chemical":{"Ss":"0.4","Sm":"0.4","Sc":"0.2"},"Oil and Gas":{"Ss":"0.25","Sm":"0.65","Sc":"0.1"},"Pharma":{"Ss":"0.1","Sm":"0.7","Sc":"0.2"},"Sheet Manufacturing":{"Ss":"0.25","Sm":"0.4","Sc":"0.35"},"Power Gen":{"Ss":"0.1","Sm":"0.7","Sc":"0.2"},"Other":{"Ss":"0.2","Sm":"0.6","Sc":"0.2"}},"FacePlates":{"Fs":"0.2","Fm":"0.4","Fc":"0.3","Fvc":"0.1"}}
    for key in  multipliers:
        if key == "Display":
            Ds = m.ceil(display * float(multipliers[key][check]["Ds"]))
            Dm = m.ceil(display * float(multipliers[key][check]["Dm"]))
            Dc = m.ceil(display * float(multipliers[key][check]["Dc"]))
        if key == "Shapes":
            Ss = m.ceil(shape * float(multipliers[key][check]["Ss"]))
            Sm = m.ceil(shape * float(multipliers[key][check]["Sm"]))
            Sc = m.ceil(shape * float(multipliers[key][check]["Sc"]))
        if key == "FacePlates":
            Fs = m.ceil(facePlates * float(multipliers[key]["Fs"]))
            Fm = m.ceil(facePlates * float(multipliers[key]["Fm"]))
            Fc = m.ceil(facePlates * float(multipliers[key]["Fc"]))
            Fvc = m.ceil(facePlates * float(multipliers[key]["Fvc"]))
    return Ds,Dm,Dc,Ss,Sm,Sc,Fs,Fm,Fc,Fvc,shape,facePlates