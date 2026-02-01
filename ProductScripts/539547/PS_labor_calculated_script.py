from GS_scada_labor_calculation import scadalabor
def getContainer(Product,Name):
    return Product.GetContainerByName(Name)
scada_laborCon = getContainer(Product,"SCADA_Engineering_Labor_Container")
Tempused = Product.Attr('Scada_Are_Equipment_Templates_Used').GetValue()
def calculate_hr_based_temp_used(Deliverable):
    import math
    scada_points = float(Product.Attr('Number_of_SCADA_points').GetValue())
    scada_tags = math.ceil(scada_points * 3.6 / 6.2)

    if Deliverable == 'SCADA Design Specification':
        if 0 < scada_tags <= 2000:
            return 80
        elif 2000 < scada_tags <= 5000:
            return 160
        elif scada_tags > 5000:
            return 320
        else:
			return 0
    if Deliverable == 'SCADA Site Survey Report':
        if 0 < scada_tags <= 2000:
            return 40
        elif 2000 < scada_tags <= 5000:
            return 60
        elif scada_tags > 5000:
            return 80
        else:
			return 0
    elif Deliverable == 'SCADA QDB Development':
        if scada_tags <= 2000:
            factor = 5
        elif 2000 < scada_tags <= 5000:
            factor = 4
        elif scada_tags > 5000:
            factor = 3
        return float(scada_tags * factor / 60)
if scada_laborCon.Rows.Count > 0:
    scada_sat, scada_site_survey_report, scada_ds, scada_special, scada_order, scada_app_build, scada_test = scadalabor(Product)
    for row in scada_laborCon.Rows:
        oldCalHrs = row["Calculated Hrs"]
        if row["Deliverable"] == "SCADA Site Survey Report":
            if Tempused !='Yes':
                hrs=calculate_hr_based_temp_used('SCADA Site Survey Report')
                row["Calculated Hrs"] = str(hrs)
            else:
                row["Calculated Hrs"] = str(scada_site_survey_report)

        elif row["Deliverable"] == "SCADA Design Specification":
            if Tempused !='Yes':
                Log.Info("777")
                hrs=calculate_hr_based_temp_used('SCADA Design Specification')
                Log.Info("hrs+++++ "+str(hrs))
                row["Calculated Hrs"] = str(hrs)
            else:
                row["Calculated Hrs"] = str(scada_ds)

        elif row["Deliverable"] == "SCADA Specials or Equipment Templates":
            row["Calculated Hrs"] = str(scada_special)

        elif row["Deliverable"] == "SCADA Order":
            row["Calculated Hrs"] = str(scada_order)

        elif row["Deliverable"] == "SCADA Application Build":
            row["Calculated Hrs"] = str(scada_app_build)

        elif row["Deliverable"] == "SCADA Test Procedure and Testing":
            row["Calculated Hrs"] = str(scada_test)

        elif row["Deliverable"] == "SCADA Site Acceptance Test":
            row["Calculated Hrs"] = str(scada_sat)

        elif row["Deliverable"] == "SCADA Commissioning and Start Up Activities":
            row["Calculated Hrs"] = "0"
        elif row["Deliverable"] == "SCADA QDB Development":
            hrs=calculate_hr_based_temp_used('SCADA QDB Development')
            Log.Info("SCADA QDB Developmenthrs+++++ "+str(hrs))
            row["Calculated Hrs"] = str(hrs)
    #ScriptExecutor.Execute('final_hr')
    #ScriptExecutor.Execute('PS_Populate_Prices')