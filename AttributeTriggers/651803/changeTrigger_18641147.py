def process_input(value):
    if isinstance(value, str):
        if value.isdigit():
            return int(value)

        if value.replace('.', '', 1).isdigit():
            float_value = float(value)
            if float_value >= 0:
                return round(float_value)

    if isinstance(value, int):
        if value >= 0:
            return value

    if isinstance(value, float):
        if value >= 0:
            return round(value)

    return 0

value = process_input(Product.Attr('Number of Tokens Required').GetValue())
Product.Attr('Number of Tokens Required').AssignValue(str(value))

scrTok = Product.Attr('Secure Remote Access Token BOM')
numTok = Product.Attr('Number of Tokens Required').GetValue()
for val in scrTok.SelectedValues:
    val.Quantity = float(numTok)