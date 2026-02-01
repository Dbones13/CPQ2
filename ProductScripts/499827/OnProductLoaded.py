import GS_CE_Utils

def getContainer(Name):
    return Product.GetContainerByName(Name)
attrs = ["CE_Project_Questions_Cont","Labor_Details_New/Expansion_Cont","Number_System_Groups", "Labor_details_newexapnsion_cont2","ExpProject_Que_Right","New_exp_common_prj_input","New_exp_common_prj_input1","PM_Additional_Custom_Deliverables_Labor_Container"]
for attr in attrs:
    container = getContainer(attr)
    if container.Rows.Count == 0:
        container.AddNewRow(False)
isR2Qquote = Quote.GetCustomField("R2QFlag").Content
attrs = ["ExpProject_Que_Right","CE_Project_Questions_Cont"]
for attr in attrs:
    container = getContainer(attr)
    if container.Rows.Count != 0:
        for row in container.Rows:
            if attr == 'ExpProject_Que_Right':
                row.SetColumnValue('NonStandard TC_Used', '0')
                row.GetColumnByName('NonStandard TC_Used').SetAttributeValue('No')
                row.SetColumnValue('Estimated_Project_Value_Cost', '2')
                row.GetColumnByName('Estimated_Project_Value_Cost').SetAttributeValue('$250K - $1M')
                if isR2Qquote:
                    row.SetColumnValue('Estimated_Project_Value_Cost', '3')
                    row.GetColumnByName('Estimated_Project_Value_Cost').SetAttributeValue('$1M - $5M')
                row.SetColumnValue('Liquidated Damages Included', '0')
                row.GetColumnByName('Liquidated Damages Included').SetAttributeValue('No')
                for col_name in ['Number of Subcontracts', 'Number of Extra Progress Reports or Meetings', 'Project Duration in weeks', 'FAT Duration in weeks', 'SAT Duration in weeks']:
                    row.SetColumnValue(col_name, '0')
            if attr=="CE_Project_Questions_Cont":
                if isR2Qquote:
                    row.SetColumnValue('Estimated_Project_Value_Cost', '3')
                    row.GetColumnByName('Estimated_Project_Value_Cost').SetAttributeValue('$1M - $5M')
                row.SetColumnValue('Project Category', '3')
                row.GetColumnByName('Project Category').SetAttributeValue('B')
                row.SetColumnValue('Project Type', 'Fixed Price')
                row.GetColumnByName('Project Type').SetAttributeValue('Fixed Price')
                row.SetColumnValue('Contracting Parties', '2')
                row.GetColumnByName('Contracting Parties').SetAttributeValue('Customer + EPC or Consultant')
                if not isR2Qquote:
                    row.SetColumnValue('Internal Parties', '1')
                    row.GetColumnByName('Internal Parties').SetAttributeValue('HPS')
                row.SetColumnValue('Internal Parties', 'HPS')
                row.GetColumnByName('Internal Parties').SetAttributeValue('HPS')
                row.SetColumnValue('Project Exeuction Locations', '2')
                row.GetColumnByName('Project Exeuction Locations').SetAttributeValue('Home +1')
                row.SetColumnValue('Project Team Size', '2')
                row.GetColumnByName('Project Team Size').SetAttributeValue('3 - 5  Members')
                #row.GetColumnByName('Cabinet').SetAttributeValue('Dual Access')
            row.Calculate()

            

GS_CE_Utils.setContainerDefaults(Product)

ce_proj_cont = Product.GetContainerByName('CE_Project_Questions_Cont')
if ce_proj_cont.Rows.Count == 1:
    ce_proj_site_volt = ce_proj_cont.Rows[0].GetColumnByName('CE_Site_Voltage').Value
    Product.Attr('CE_Site_Voltage').AssignValue(ce_proj_site_volt)
    ce_proj_site_frequency = ce_proj_cont.Rows[0].GetColumnByName('CE_Site_Frequency').Value
    Product.Attr('CE_Site_Frequency').SelectValue(ce_proj_site_frequency)
else:
    Product.Attr('CE_Site_Voltage').AssignValue("120V")
common_prj_cont = Product.GetContainerByName('New_exp_common_prj_input1')
if common_prj_cont.Rows.Count == 1:
    Crate_type = common_prj_cont.Rows[0].GetColumnByName('Crate Type').Value
    Product.Attr('Crate Type').SelectValue(Crate_type)
    Crate_design = common_prj_cont.Rows[0].GetColumnByName('Crate Design').Value
    Product.Attr('Crate Design').SelectValue(Crate_design)


Labor_Details_Cont = Product.GetContainerByName('Labor_Details_New/Expansion_Cont')
if Labor_Details_Cont.Rows.Count == 1:
    Labor_Details_Row0=Labor_Details_Cont.Rows[0]
    Labor_Loop_Drawings = Labor_Details_Row0.GetColumnByName('Labor_Loop_Drawings').Value
    Labor_Unreleased_Product = Labor_Details_Row0.GetColumnByName('Labor_Unreleased_Product').Value
    Labor_Marshalling_Database = Labor_Details_Row0.GetColumnByName('Labor_Marshalling_Database').Value
    Labor_Percentage_FAT = Labor_Details_Row0.GetColumnByName('Labor_Percentage_FAT').Value
    Labor_Site_Activities = Labor_Details_Row0.GetColumnByName('Labor_Site_Activities').Value
    Labor_Operation_Manual_Scope = Labor_Details_Row0.GetColumnByName('Labor_Operation_Manual_Scope').Value
    Labor_Custom_Scope = Labor_Details_Row0.GetColumnByName('Labor_Custom_Scope').Value
    Product.Attr('Labor_Loop_Drawings').AssignValue(Labor_Loop_Drawings)
    Product.Attr('Labor_Unreleased_Product').AssignValue(Labor_Unreleased_Product)
    Product.Attr('Labor_Marshalling_Database').AssignValue(Labor_Marshalling_Database)
    Product.Attr('Labor_Percentage_FAT').AssignValue(Labor_Percentage_FAT)
    Product.Attr('Labor_Site_Activities').AssignValue(Labor_Site_Activities)
    Product.Attr('Labor_Operation_Manual_Scope').AssignValue(Labor_Operation_Manual_Scope)
    Product.Attr('Labor_Custom_Scope').AssignValue(Labor_Custom_Scope)
Product.SetGlobal('OnProductLoad', 'No')
Product.ParseString('<*CTX( Container(CE_Project_Questions_Cont).Row(1).Column(Internal Parties).Set(1) )*>')