Platopt = Product.Attr("Virtualization_Platform_Options").GetValue()
Virhst = Product.Attr("Virtualization_for_Hosts_and_Switches").GetValue()
if Platopt == 'Essentials Platforms-Dell Servers' and Virhst =='Yes':
    Product.AllowAttr('Header_05_open')
    Product.AllowAttr('Header_05_close')
    Product.AllowAttr('Virtualization_Cabinet_Depth_Size')
    Product.AllowAttr('Virtualization_Power_Supply_Voltage')
    Product.AllowAttr('Virtualization_Cabinet_Door_Type')
    Product.AllowAttr('Virtualization_Cabinet_Keylock_Type')
    Product.AllowAttr('Virtualization_Cabinet_Hinge_Type')
    Product.AllowAttr('Virtualization_Cabinet_Thermostat_Required')
    Product.AllowAttr('Virtualization_Cabinet_Base_Required')
    Product.AllowAttr('Virtualization_Cabinet_Color')
else:
    Product.DisallowAttr('Header_05_open')
    Product.DisallowAttr('Header_05_close')
    Product.DisallowAttr('Virtualization_Cabinet_Depth_Size')
    Product.DisallowAttr('Virtualization_Power_Supply_Voltage')
    Product.DisallowAttr('Virtualization_Cabinet_Door_Type')
    Product.DisallowAttr('Virtualization_Cabinet_Keylock_Type')
    Product.DisallowAttr('Virtualization_Cabinet_Hinge_Type')
    Product.DisallowAttr('Virtualization_Cabinet_Thermostat_Required')
    Product.DisallowAttr('Virtualization_Cabinet_Base_Required')
    Product.DisallowAttr('Virtualization_Cabinet_Color')
if Platopt == 'Premium Platforms Gen 3 - Performance A/B':
    Product.AllowAttr('Virtualization_Number_of_Clusters_in_the_network')
    Product.AllowAttr('Virtualization_Enter_the_starting_Cluster_Number')
else:
    Product.DisallowAttr('Virtualization_Number_of_Clusters_in_the_network')
    Product.DisallowAttr('Virtualization_Enter_the_starting_Cluster_Number')
if Platopt in ('Premium Platforms Gen 3 - Performance A/B', 'Premium Platforms Gen 3 - 2 node cluster' ) and Quote.GetCustomField('R2QFlag').Content =='Yes':
    Product.AllowAttr('Virtualization_Warranty_Extension')
else:
    Product.DisallowAttr('Virtualization_Warranty_Extension')
if Quote.GetCustomField('R2QFlag').Content =='Yes':
    Product.AllowAttr('Virtualization_Windows_RDS_CAL')
else:
    Product.DisallowAttr('Virtualization_Windows_RDS_CAL')

# Set attribute value by default if it is empty and required
import GS_DropDown_Implementation
GS_DropDown_Implementation.SetDropDownDefaultvalue(Product)


if Quote.GetCustomField('ISR2QREQUEST').Content == "Yes" and Product.Attr("VS_Platform_Options").GetValue() in ("Number of Performance A Servers (0-9 per cluster)", "Number of Performance B Servers (0-9 per cluster)"):
    if not Product.Attr('VS_Number_of_Clusters_in_the_network').Allowed:
        Product.AllowAttr('VS_Number_of_Clusters_in_the_network')
        Product.Attr("VS_Number_of_Clusters_in_the_network").AssignValue("1")
    else:
        if not Product.Attr("VS_Number_of_Clusters_in_the_network").GetValue():
            Product.Attr("VS_Number_of_Clusters_in_the_network").AssignValue("1")
else:
    Product.DisallowAttr('VS_Number_of_Clusters_in_the_network')