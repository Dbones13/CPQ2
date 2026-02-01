###############################################################################################
# Class CL_PriceBookMapping:
#       Class to store Price Book Mappings
###############################################################################################
class CL_PriceBookMapping():
    # Mapping variable holders
    priceBookMapping = list()

    # Integration Mapping Section
    # mapping = dict()
    # mapping["CPQ_MARKET_ID"] = 1  # USA in $
    # mapping["SF_PRICEBOOK_ID"] = "01s8d000005VljzAAC"  # USA in $
    # priceBookMapping.append(mapping)

    # Salesforce Standard Price Book Id (Mandatory)
    STANDARD_PRICE_BOOK_ID = "01s1a0000009KkvAAE"
    # Salesforce Service Contract Price Book Id (Mandatory)
    SERVICE_PRICE_BOOK_ID = "01s1P000002JsTJQA0"