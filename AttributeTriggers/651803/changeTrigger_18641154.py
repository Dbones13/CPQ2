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

value = process_input(Product.Attr('Number of Windows Assets').GetValue())
Product.Attr('Number of Windows Assets').AssignValue(str(value))