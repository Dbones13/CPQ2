import GS_Exp_ENT_BOM_Calcs
import GS_PS_Exp_Ent_BOM

serever_qnt_T, serever_qntnode_T, station_37200 = GS_Exp_ENT_BOM_Calcs.server_qnt1(Product)

#Product.ExecuteRulesOnce = True

def setAtvQty(AttrName, sv, qty):
    pvs = Product.Attr(AttrName).Values
    for av in pvs:
        if av.Display == sv:
            av.IsSelected = True
            av.Quantity = qty
            Trace.Write('Selected ' + sv + ' in  attribute ' + AttrName + ' at Qty ' + str(qty))
            break

def resetAtvQty(AttrName):
    pvs = Product.Attr(AttrName).Values
    for av in pvs:
        av.IsSelected = False
        av.Quantity = 0
        Trace.Write('Reset ' + str(av.Display) + ' IsSelected=' + str(av.IsSelected) + ' Qty=' + str(av.Quantity))

def get_int(val):
    if val:
        return int(val)
    return 0

# Helper function to add or update part quantity
def add_part(part_no, qty):
    if part_no in parts_to_add_update:
        parts_to_add_update[part_no] = int(parts_to_add_update[part_no]) + int(qty)
    else:
        parts_to_add_update[part_no] = int(qty)
    Trace.Write('Added/Updated part: ' + part_no + ' Qty: ' + str(parts_to_add_update[part_no]))

Trace.Write(Product.Name)
Log.Info('script started 1122e')

# Add all the products from List of Locations/Clusters/ Network Groups product that should be added in Experion Enterprise group
lcp_prod_for_expentgrp = ['51305786-520', '51305786-510', '51305786-502', '51305786-505','51199562-201', '51199562-205', '51199562-207', '51199562-202', '51199562-203', '51199562-201', '51305482-102', '51305482-105', '51305482-110', '51305482-120', '51305482-202', '51305482-205', '51305482-210', '51305482-220', 'SI-9200R4', 'SI-9300R4']

# =============================================================================
# FIX: Define all UI-driven parts that should NOT be read back from container
# These are controlled ONLY by current attribute selections
# =============================================================================
ui_driven_parts = set([
    # Crossover Cables (Backbone + L3)
    '51305786-520', '51305786-510', '51305786-502', '51305786-505',
    # Power Cords - ALL country types (Backbone + L3)
    '51199562-200',  # US
    '51199562-201',  # Europe
    '51199562-202',  # UK
    '51199562-203',  # Japan
    '51199562-205',  # Italy
    '51199562-207',  # Argentina
    # Tree Cables A (Backbone + L3)
    '51305482-102', '51305482-105', '51305482-110', '51305482-120',
    # Tree Cables B (Backbone + L3)
    '51305482-202', '51305482-205', '51305482-210', '51305482-220',
    # Switches
    'SI-9200R4', 'SI-9300R4'
])

# =============================================================================
# IMPORTANT: Reset attribute FIRST before building new data
# =============================================================================
Trace.Write('=== RESETTING ATTRIBUTE BEFORE PROCESSING ===')
resetAtvQty('Exp_Ent_Grp_Part_Summary')

# Start with empty dictionary
parts_to_add_update = {}

loc_groups = Product.GetContainerByName('List of Locations/Clusters/Network Groups').Rows
for lcp in loc_groups:
    loc_clu_prod = lcp.Product
    Trace.Write(loc_clu_prod.Name)
    lcp_part_cont = loc_clu_prod.GetContainerByName('Location_Cluster_Part_Summary_Cont').Rows
    for lcp_parts in lcp_part_cont:
        part_no = lcp_parts.GetColumnByName('PartNumber').Value
        part_qty = lcp_parts.GetColumnByName('Final_Quantity').Value
        Trace.Write("LCP Prod Name = " + str(part_no) + " Qty = " + str(part_qty))
        
        # Only add if in lcp_prod_for_expentgrp AND NOT a UI-driven part
        # This prevents Location/Cluster UI selections from bleeding into Enterprise level
        if part_no in lcp_prod_for_expentgrp and part_no not in ui_driven_parts:
            add_part(part_no, part_qty)

exp_ent_grp_part_cont = Product.GetContainerByName('Exp_Ent_Grp_Part_Summary_Cont')
Trace.Write("Exp Ent Group Parts count = " + str(exp_ent_grp_part_cont.Rows.Count))

backbone_switch = Product.Attributes.GetByName("Backbone Switch Required").GetValue()
Trace.Write("Backbone Switch Required = " + str(backbone_switch))

Default_Switch = Product.Attributes.GetByName("Default Switch").GetValue()
Default_Crossover_Cable = Product.Attributes.GetByName("Default Crossover Cable").GetValue()
Power_Cord_Type = Product.Attributes.GetByName("Power Cord Type").GetValue()

Trace.Write("=== CURRENT UI SELECTIONS ===")
Trace.Write("Default_Switch = " + str(Default_Switch))
Trace.Write("Default_Crossover_Cable = " + str(Default_Crossover_Cable))
Trace.Write("Power_Cord_Type = " + str(Power_Cord_Type))

Tree1 = get_int(Product.Attributes.GetByName("Tree A 2m cable (0-1000)").GetValue())
Tree2 = get_int(Product.Attributes.GetByName("Tree A 5m cable (0-1000)").GetValue())
Tree3 = get_int(Product.Attributes.GetByName("Tree A 10m cable (0-1000)").GetValue())
Tree4 = get_int(Product.Attributes.GetByName("Tree A 20m cable (0-1000)").GetValue())
Tree5 = get_int(Product.Attributes.GetByName("Tree B 2m cable (0-1000)").GetValue())
Tree6 = get_int(Product.Attributes.GetByName("Tree B 5m cable (0-1000)").GetValue())
Tree7 = get_int(Product.Attributes.GetByName("Tree B 10m cable (0-1000)").GetValue())
Tree8 = get_int(Product.Attributes.GetByName("Tree B 20m cable (0-1000)").GetValue())

if backbone_switch == "Yes":
    Trace.Write("=== PROCESSING BACKBONE SWITCH ===")
    
    if Default_Switch == "SW_L3_RT_CISCO_24PT_REDPS":
        add_part("SI-9300R4", 2)
    
    if Default_Switch == "SW_L3_RT_CISCO_24PT":
        add_part("SI-9200R4", 2)

    # Crossover Cables - only ONE should be added based on selection
    if Default_Crossover_Cable == "20M":
        add_part("51305786-520", 1)
    elif Default_Crossover_Cable == "10M":
        add_part("51305786-510", 1)
    elif Default_Crossover_Cable == "2M":
        add_part("51305786-502", 1)
    elif Default_Crossover_Cable == "5M":
        add_part("51305786-505", 1)

    # Power Cords - only ONE should be added based on selection
    if Power_Cord_Type == "US":
        add_part("51199562-200", 1)
    elif Power_Cord_Type == "Europe":
        add_part("51199562-201", 1)
    elif Power_Cord_Type == "UK":
        add_part("51199562-202", 1)
    elif Power_Cord_Type == "Japan":
        add_part("51199562-203", 1)
    elif Power_Cord_Type == "Italy":
        add_part("51199562-205", 1)
    elif Power_Cord_Type == "Argentina":
        add_part("51199562-207", 1)

    # Tree cables
    if Tree1 > 0:
        add_part("51305482-102", Tree1)
    if Tree2 > 0:
        add_part("51305482-105", Tree2)
    if Tree3 > 0:
        add_part("51305482-110", Tree3)
    if Tree4 > 0:
        add_part("51305482-120", Tree4)
    if Tree5 > 0:
        add_part("51305482-202", Tree5)
    if Tree6 > 0:
        add_part("51305482-205", Tree6)
    if Tree7 > 0:
        add_part("51305482-210", Tree7)
    if Tree8 > 0:
        add_part("51305482-220", Tree8)


# =============================================================================
# L3 SWITCH PROCESSING
# =============================================================================
L3_Switch_Required = Product.Attributes.GetByName("L3 Switch Required").GetValue()
Trace.Write("L3 Switch Required = " + str(L3_Switch_Required))

L3_Switch_Default = Product.Attributes.GetByName("Default Switch L3").GetValue()
L3_Crossover_Cable = Product.Attributes.GetByName("Default Crossover Cable L3").GetValue()
L3_Power_Cord_Type = Product.Attributes.GetByName("Power Cord Type L3").GetValue()

Trace.Write("=== L3 UI SELECTIONS ===")
Trace.Write("L3_Switch_Default = " + str(L3_Switch_Default))
Trace.Write("L3_Crossover_Cable = " + str(L3_Crossover_Cable))
Trace.Write("L3_Power_Cord_Type = " + str(L3_Power_Cord_Type))

L3_Tree1 = get_int(Product.Attributes.GetByName("Tree A 2m cable (0-1000) L3").GetValue())
L3_Tree2 = get_int(Product.Attributes.GetByName("Tree A 5m cable (0-1000) L3").GetValue())
L3_Tree3 = get_int(Product.Attributes.GetByName("Tree A 10m cable (0-1000) L3").GetValue())
L3_Tree4 = get_int(Product.Attributes.GetByName("Tree A 20m cable (0-1000) L3").GetValue())
L3_Tree5 = get_int(Product.Attributes.GetByName("Tree B 2m cable (0-1000) L3").GetValue())
L3_Tree6 = get_int(Product.Attributes.GetByName("Tree B 5m cable (0-1000) L3").GetValue())
L3_Tree7 = get_int(Product.Attributes.GetByName("Tree B 10m cable (0-1000) L3").GetValue())
L3_Tree8 = get_int(Product.Attributes.GetByName("Tree B 20m cable (0-1000) L3").GetValue())

if L3_Switch_Required == "Yes":
    Trace.Write("=== PROCESSING L3 SWITCH ===")

    if L3_Switch_Default == "SW_L3_RT_CISCO_24PT_REDPS":
        add_part("SI-9300R4", 2)

    if L3_Switch_Default == "SW_L3_RT_CISCO_24PT":
        add_part("SI-9200R4", 2)

    # L3 Crossover Cables - only ONE based on selection
    if L3_Crossover_Cable == "2m":
        add_part("51305786-502", 1)
    elif L3_Crossover_Cable == "5m":
        add_part("51305786-505", 1)
    elif L3_Crossover_Cable == "10m":
        add_part("51305786-510", 1)
    elif L3_Crossover_Cable == "20m":
        add_part("51305786-520", 1)

    # L3 Power Cords - only ONE based on selection
    if L3_Power_Cord_Type == "US":
        add_part("51199562-200", 1)
    elif L3_Power_Cord_Type == "Europe":
        add_part("51199562-201", 1)
    elif L3_Power_Cord_Type == "UK":
        add_part("51199562-202", 1)
    elif L3_Power_Cord_Type == "Japan":
        add_part("51199562-203", 1)
    elif L3_Power_Cord_Type == "Italy":
        add_part("51199562-205", 1)
    elif L3_Power_Cord_Type == "Argentina":
        add_part("51199562-207", 1)

    # L3 Tree cables
    if L3_Tree1 > 0:
        add_part("51305482-102", L3_Tree1)
    if L3_Tree2 > 0:
        add_part("51305482-105", L3_Tree2)
    if L3_Tree3 > 0:
        add_part("51305482-110", L3_Tree3)
    if L3_Tree4 > 0:
        add_part("51305482-120", L3_Tree4)
    if L3_Tree5 > 0:
        add_part("51305482-202", L3_Tree5)
    if L3_Tree6 > 0:
        add_part("51305482-205", L3_Tree6)
    if L3_Tree7 > 0:
        add_part("51305482-210", L3_Tree7)
    if L3_Tree8 > 0:
        add_part("51305482-220", L3_Tree8)


# =============================================================================
# Read NON-UI-driven parts from container
# =============================================================================
Trace.Write("=== READING NON-UI PARTS FROM CONTAINER ===")
for exp_ent_grp_parts in exp_ent_grp_part_cont.Rows:
    part_no = exp_ent_grp_parts.GetColumnByName('PartNumber').Value
    part_qty = exp_ent_grp_parts.GetColumnByName('Part_Qty').Value
    Trace.Write("Container Part: " + str(part_no) + " Qty: " + str(part_qty) + " UI-Driven: " + str(part_no in ui_driven_parts))
    
    # ONLY add if NOT a UI-driven part
    if part_no not in ui_driven_parts:
        parts_to_add_update[part_no] = int(part_qty)

# =============================================================================
# FINAL: Set attribute values
# =============================================================================
Trace.Write("=== FINAL PARTS TO SET ===")
Trace.Write(str(parts_to_add_update))

# Reset again to be absolutely sure
Trace.Write("=== FINAL RESET ===")
resetAtvQty('Exp_Ent_Grp_Part_Summary')

# Set only the parts we want
Trace.Write("=== SETTING PARTS ===")
for part_no in parts_to_add_update:
    setAtvQty('Exp_Ent_Grp_Part_Summary', part_no, parts_to_add_update[part_no])

Trace.Write("=== SCRIPT COMPLETE ===")