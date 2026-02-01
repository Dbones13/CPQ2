import GS_R2Q_Configuration_Data as ConfigHTMLData
import re
non_cpq_label =['Operator Training','Small Volume Prover','Skid and Instruments',"Industrial Security (Access Control)","Tank Gauging Engineering","Fire Detection & Alarm Engineering","Digital Video Manager"]
TASProduct={"Industrial Security (Access Control)":"Personnel Access Control",
               "Tank Gauging Engineering":"Tank Gauging",
               "Fire Detection & Alarm Engineering":"Fire Alarm Panel",
               "Digital Video Manager":"CCTV System",
            "Operator Training":"Operator Training",
            "Small Volume Prover":"Small Volume Prover",
            "Skid and Instruments":"Skid and Instruments"
}
def get_last_child_product(key):
    if ".Child_Products." in key:
        parts = key.split(".Child_Products.")
        last_part = parts[-1]
        child_product = last_part.split(".")[0]
        child_product = child_product.split("[")[0]
        return child_product
    return ""
def flatten_dict(nested_dict, parent_key='', separator='.'):
    items = {}
    if isinstance(nested_dict, dict):
        for key, value in nested_dict.items():
            new_key = "{}{}{}".format(parent_key, separator, key) if parent_key else key
            if isinstance(value, dict):
                items.update(flatten_dict(value, new_key, separator=separator))
            elif isinstance(value, list):
                for old_key, item in enumerate(value):
                    if isinstance(item, dict):
                        items.update(flatten_dict(item, "{}[{}]".format(new_key, old_key), separator=separator))
                    else:
                        items["{}[{}]".format(new_key, old_key)] = item
            else:
                items[new_key] = value
    else:
        items[parent_key] = nested_dict
    return items
def container_functions():
    for item in Quote.MainItems:
        if item.ProductName == "New / Expansion Project":
            newProd = item.Edit()
            ScriptExecutor.Execute('GS_DEF_CA_DICT')
    dict1 = eval(Quote.GetGlobal('r2qcompare'))
    dict2 = eval(Quote.GetGlobal('normalcompare'))
    dict3 = eval(Quote.GetGlobal('r2qcompare_label'))
    flat1 = flatten_dict(dict1)
    flat2 = flatten_dict(dict2)
    flat3 = flatten_dict(dict3)
    SelectCategory=Quote.GetCustomField("R2Q_Category_PRJT").Content 
    excluded_substrings = {"product_name", "Header_", "Parent_Product", "QuoteNumber", "R2QRequest","message_","Part_Summary"}
    all_keys = sorted([ key for key in flat1.keys() if not any(excluded in key for excluded in excluded_substrings) ])
    all_keys_label = sorted([ key for key in flat3.keys() if not any(excluded in key for excluded in excluded_substrings) ])
    html = """
    <table class='fiori3-table fiori3-products-list-table table table-hover' id='r2Q_compatability_table'>
        <thead>
        <tr>
            <th style="Width:80%" class='d-none'>Parent Product</th>
            <th style="Width:100%" >Product Name</th>
            <th style="Width:100%" >Attribute Name</th>
            <th style="Width:100%" >Attribute Label</th>
            <th style="Width:100%" >R2Q Attribute Value</th>
            <th style="Width:100%" >CPQ Attribute Value</th>
        </tr>
        </thead>
        <tbody>
    """
    html += """    <tbody>
"""

    # Add two default rows at the beginning
    html += "      <tr>
"
    html += "        <td class='d-none'>New / Expansion Project</td>
"
    html += "        <td>New / Expansion Project</td>
"
    html += "        <td>R2Q Select Category</td>
"
    html += "        <td>Select Category</td>
"
    html += "        <td>{}</td>
".format(SelectCategory)
    html += "        <td>{}</td>
".format(SelectCategory)
    html += "      </tr>
"

    html += "      <tr>
"
    html += "        <td class='d-none'>New / Expansion Project</td>
"
    html += "        <td>New / Expansion Project</td>
"
    html += "        <td>MIB Configuration Required?</td>
"
    html += "        <td>MIB Configuration Required?</td>
"
    html += "        <td>No</td>
"
    html += "        <td>No</td>
"
    html += "      </tr>
"

    keylog=1
    empty_values = [None, "",'None',0,'0','none','']
    exception_keys = [
        'C300_RG_UPC_Cab_Count',
        'C300_RG_UPC_Universal_IO_Count',
        'PUIO_Count',
        'PDIO_Count'
    ]
    for key, key1 in zip(all_keys, all_keys_label):
        value1 = flat1.get(key, None)
        value2 = flat2.get(key, None)
        value3 = flat3.get(key1, None)
        keypr=get_last_child_product(key)
        #if  keypr not in TASProduct and keypr not in non_cpq_label:
        if SelectCategory=='ICS System':
            key_name = key.split('.')[-1]
        else:
            key_name = key
        if (key.split('.')[-1])=='Experion Enterprise Group Name' and keylog==1:
            value3='Experion Enterprise Group Name'
            key_name ='Experion Enterprise Group Name'
            keylog=2
        if value3 in [None, ""] or (value3=='Percentage Spare Space in Marshalling Cabinet (0-100%)' and value1!=value2):
            continue
        if value1 in empty_values and key_name not in exception_keys:
            continue
        if str(value3) == "IO Type" and value1 not in empty_values and value2 in empty_values:
            continue
        if re.search(r'<a\b[^>]*>', value1):
            value1=re.sub(r'<a[^>]*>.*?</a>', '', value1)
            value2=re.sub(r'<a[^>]*>.*?</a>', '',  value2 )
        if ((key.split('.')[-1]).strip())=='of FDM System groups':
            key_name='No. of FDM System groups'
        key_parts = key.split('.')
        parent_product = key_parts[0] if len(key_parts) > 0 else ""
        last_child_product = get_last_child_product(key)
        last_child_product = last_child_product if last_child_product !='' else parent_product
        row_color = "" if (value1 == value2 or last_child_product in non_cpq_label) else ' style="background-color: #ffcccc;"'
        last_child_product = last_child_product if last_child_product not in non_cpq_label else TASProduct[last_child_product]
        html += "      <tr{}>
".format(row_color)
        html += "        <td class='d-none'>{}</td>
".format(parent_product)
        html += "        <td>{}</td>
".format(last_child_product)
        html += "        <td>{}</td>
".format(key_name)
        html += "        <td>{}</td>
".format(value3 if value3 is not None else '')
        html += "        <td>{}</td>
".format(value1 if value1 is not None else '')
        html += "        <td>{}</td>
".format(value2 if value2 is not None else '')
        html += "      </tr>
"
    html += """    </tbody>
    </table>"""
    return html
ApiResponse = ApiResponseFactory.JsonResponse(container_functions() if next((True for item in Quote.Items if item.PartNumber == "PRJT R2Q"), False) else ConfigHTMLData.getHTMLDataTable(Quote))