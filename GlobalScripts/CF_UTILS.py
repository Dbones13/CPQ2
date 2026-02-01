"""Module that contains utility functions and constants for CPQ Custom Fields"""

# Constants for Custom Fields
CF_CONSTANTS = {
    "SALES_ORG": "Sales ORG",
    # "DIST_CHANNEL": "Distribution Channel",
    # "SOLD_TO": "Sold To Party",
    # "SHIP_TO": "Ship To Party",
    "QUOTE_LEVEL_PLANT_FIELD": "CF_Plant",
}


"""Section for re-usable functions for Custom Fields"""

def get_custom_field_value(quote, custom_field_name):
    # type: (Quote, str) -> str
    """Fetches the value of a custom field from the quote."""
    custom_field = quote.GetCustomField(custom_field_name)
    if custom_field:
        return custom_field.Content
    else:
        Log.Info("Custom field '{custom_field_name}' not found in quote.")
        return ""


def split_after_comma(custom_field_value):
	# type: (str) -> (str, str)
    """Splits the custom field value into two parts after the first comma."""
    x, y = custom_field_value.split(",",1)
    return x.strip(), y.strip()