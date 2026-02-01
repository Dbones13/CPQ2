if Quote.GetCustomField("R2QFlag").Content == "Yes":

    # Keep transport parsing as-is
    truck = Product.ParseString('<* IsSelected(Terminal_Mode_of_Transport.Truck loading/unloading) *>')
    rail = Product.ParseString('<* IsSelected(Terminal_Mode_of_Transport.Rail Wagon loading/unloading) *>')
    pipe = Product.ParseString('<* IsSelected(Terminal_Mode_of_Transport.Pipeline loading/unloading) *>')
    marine = Product.ParseString('<* IsSelected(Terminal_Mode_of_Transport.Marine loading/unloading) *>')

    # Helpers
    if Product.Attr('Terminal_value_set').GetValue() == '':
        def set_attr(attr_name, value):
            Product.Attr(attr_name).AssignValue(value)
            Product.Attr(attr_name).SelectDisplayValue(value)

        # Attributes needing both AssignValue and SelectDisplayValue
        attrs_with_display = {
            "Terminal_Experion_Server_(ESV)_Type": "Desk",
            "Terminal_Experion_Server_Hardware": "DELL T550 STD TPM",
            "Terminal_Additional_Hard_Drive": "No",
            "Terminal_Additional_Memory": "None",
            "Terminal_Optional_DVD": "No",
            "Terminal_Display_Required": "27 Inch",
            "Terminal_Trackball": "No",
            "Terminal_Cabinet_Mounting_Type": "None",
            "Terminal_TM_System_Complexity": "Moderate",
            "Terminal_Feature_Type": "New Features (upto 5)"
        }

        for attr, val in attrs_with_display.items():
            set_attr(attr, val)

        # Attributes needing only AssignValue
        attrs_assign_only = {
            "Terminal_Number_of_Days_per_Design_Review": "3",
            "Terminal_Number_of_Reviews": "2",
            "Terminal_Number_of_Days_for_TM_FAT": "5",
            "Terminal_Number_of_Engineer_for_FAT": "1",
            "Terminal_Number_of_Days_for_TM_SAT": "0",
            "Terminal_Number_of_Engineer_for_SAT": "0",
            "Terminal_No_of_Reports_with_Simple_Changes": "5",
            "Terminal_No_of_Reports_with_Complex_Changes": "3",
            "Terminal_Number_of_New_Simple_Reports": "2",
            "Terminal_Number_of_New_Moderate_Reports": "3",
            "Terminal_Number_of_New_Complex_Reports": "2",
            "Terminal_Number_of_Simple_Screens_for_new_UI": "5",
            "Terminal_Number_of_Moderate_Screens_for_new_UI": "3",
            "Terminal_Number_of_Complex_Screens_for_new_UI": "2"
        }

        for attr, val in attrs_assign_only.items():
            Product.Attr(attr).AssignValue(val)
        Product.Attr('Terminal_value_set').AssignValue('True')

    # Apply transport mode logic
    def apply_modes(row):
        if truck == "1":
            row.GetColumnByName('Truck Road').ReferencingAttribute.SelectValue("Y")
        if rail == "1":
            row.GetColumnByName('Rail Wagon').ReferencingAttribute.SelectValue("Y")
        if marine == "1":
            row.GetColumnByName('Marine').ReferencingAttribute.SelectValue("Y")
        if pipe == "1":
            row.GetColumnByName('Pipeline').ReferencingAttribute.SelectValue("Y")

    # Workflow container
    weighbridge = Product.Attr('Terminal_Weighbridge_Interface_required?').GetValue()
    workflow_container = Product.GetContainerByName('Terminal_Workflow_Scope')
    allowlist = {"Loading/Dispatch", "Unloading/Receipt"}
    weighbridge_list = {"Weigh Bridge (IN)", "Weigh Bridge (OUT)", "PC DET"}

    for row in workflow_container.Rows:
        row.GetColumnByName('Complexity').SetAttributeValue("Moderate")
        if row["Element"] in allowlist:
            apply_modes(row)
        elif row["Element"] in weighbridge_list:
            if weighbridge == "Yes":
                row.GetColumnByName('Truck Road').ReferencingAttribute.SelectValue("Y")
            else:
                row.GetColumnByName('Truck Road').ReferencingAttribute.SelectValue("N")
        elif row["Element"] != "Mercury Terminal":
            row.GetColumnByName('Truck Road').ReferencingAttribute.SelectValue("Y")

    workflow_container.Calculate()

    # Device scope container
    device_container = Product.GetContainerByName('Terminal_Devices_Scope')
    std_devices = {
        "BCU (Accuload)", "TopTech Multiload II", "Smith’s Accuload III Net",
        "DanLoad8000", "Virtual Preset", "Access Control (SIGNO 40)",
        "Access Control (Nedap RFID)", "Mercury Terminal"
    }
    new_driver_devices = {
        "BCU (1010 CB)", "BCU (1010 CJ)", "Smith’s Accuload IV", "PC DET", "Experion Panel PC"
    }

    for row in device_container.Rows:
        element = row["Element"]
        if element == "BCU (MSC-L)":
            row.GetColumnByName('Type').SetAttributeValue("Standard")
            row.GetColumnByName('Complexity').SetAttributeValue("Moderate")
            apply_modes(row)
        elif element in std_devices:
            row.GetColumnByName('Type').SetAttributeValue("Standard")
        elif element in new_driver_devices:
            row.GetColumnByName('Type').SetAttributeValue("New Driver")

    # SAP/ERP container
    sap_container = Product.GetContainerByName('Terminal_SAP_ERP_BSI_Interface_Scope')
    for row in sap_container.Rows:
        if row["Element"] == "Business System Interface":
            row.GetColumnByName('Type').SetAttributeValue("Standard")
            row.GetColumnByName('Complexity').SetAttributeValue("Moderate")
            apply_modes(row)