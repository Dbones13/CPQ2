from Update_System_Labor_Cost_Price import updateLaborCostPrice

def get_ges_location_code(ges_location):
    ges_mapping = {
        'GES India': 'IN',
        'GES China': 'CN',
        'GES Romania': 'RO',
        'GES Uzbekistan': 'UZ',
        'GES Egypt': 'EG',
        'None': 'None'
    }
    return ges_mapping.get(ges_location, 'None')

# Get the GES location value and map it to its corresponding code
ges_location = Product.Attr("MSE GES Location").GetValue()
ges_location_vc = get_ges_location_code(ges_location)

# Fetch the container for labor price cost
labor_price_cost_container = Product.GetContainerByName('Labor_PriceCost_Cont')

if Quote:
    containers_list = ['MSE_Engineering_Labor_Container', 'MSE_Additional_Labor_Container']
    fo_eng_columns = {
        'MSE_Engineering_Labor_Container': 'MSE_FO_ENG',
        'MSE_Additional_Labor_Container': 'MSE_Addi_Labor_FO_Eng'
    }

    updateLaborCostPrice(
        Product,
        Quote,
        TagParserQuote,
        containers_list,
        fo_eng_columns,
        ges_location_vc,
        True
    )
