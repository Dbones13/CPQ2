from System import DateTime
import math
def calculate_duration(start_date, end_date):
    # Calculate the difference between dates
    date_difference = end_date.Subtract(start_date)

    years = str(int(math.ceil(date_difference.Days // 365.2425)))
    years_r = date_difference.Days % 365.2425
    days_r = int(math.ceil(years_r % 30.436875))
    if days_r <= 15:
        months = str(int(math.ceil(years_r // 30.436875)))
    else:
        months = str(int(math.ceil(years_r // 30.436875)) + 1)
        if int(months) == 12:
        	years = str(int(years)+1)
        	months = str(0)
    #months = (date_difference.Days % 365) // 30
    #days = (date_difference.Days % 365.436875) % 30

    # Convert months and days to a fractional year
    fractional_year = years + "." + months

    return fractional_year
current_start_date = Product.Attr('ContractStartDate_EnabledService').GetValue()
current_end_date = Product.Attr('ContractEndDate_EnabledService').GetValue()
if current_start_date and current_end_date:
	duration = calculate_duration(DateTime.Parse(current_start_date), DateTime.Parse(current_end_date))
	Product.Attr('DurationOfPlan_enabledServices').AssignValue(str(duration))