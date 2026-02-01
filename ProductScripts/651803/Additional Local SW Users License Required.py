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

value = process_input(Product.Attr('Additional Local SW Users License Required').GetValue())
Product.Attr('Additional Local SW Users License Required').AssignValue(str(value))

fifteens = value // 15
remainder = value % 15

fives = 0
tens = 0

if 11 <= remainder <= 14:
	fives = 1
	tens = 1
elif 0 < remainder <= 5:
	fives = 1
	tens = 0
elif 6 <= remainder <= 10:
	fives = 0
	tens = 1

if fifteens > 0:
	attr = Product.Attr('Local_SW_Users_License_15')
	attr.SelectValues('CS-MSS-15U-B','CS-MSS-15U-ANL')
	for selected_value in attr.SelectedValues:
		if selected_value.ValueCode == 'CS-MSS-15U-B':
			selected_value.Quantity = fifteens
		if selected_value.ValueCode == 'CS-MSS-15U-ANL':
			selected_value.Quantity = fifteens
else:
	Product.ResetAttr('Local_SW_Users_License_15')

if tens > 0:
	attr = Product.Attr('Local_SW_Users_License_10')
	attr.SelectValues('CS-MSS-10U-B','CS-MSS-10U-ANL')
	for selected_value in attr.SelectedValues:
		if selected_value.ValueCode == 'CS-MSS-10U-B':
			selected_value.Quantity = tens
		if selected_value.ValueCode == 'CS-MSS-10U-ANL':
			selected_value.Quantity = tens

else:
	Product.ResetAttr('Local_SW_Users_License_10')

if fives > 0:
	attr = Product.Attr('Local_SW_Users_License_5')
	attr.SelectValues('CS-MSS-5U-B','CS-MSS-5U-ANL')
	for selected_value in attr.SelectedValues:
		if selected_value.ValueCode == 'CS-MSS-5U-B':
			selected_value.Quantity = fives
		if selected_value.ValueCode == 'CS-MSS-5U-ANL':
			selected_value.Quantity = fives
else:
	Product.ResetAttr('Local_SW_Users_License_5')