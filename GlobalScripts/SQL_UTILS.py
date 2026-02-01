"""
SQL Utility Functions for CPQ
This module contains reusable SQL functions for SAP CPQ implementation.
Uses SqlHelper (Scripting.ISqlHelper) to access custom tables data.
"""


def get_all_records(sql_helper, base_query, page_size=1000):
    # type: (object, str, int) -> list
    """
    This function handles pagination automatically using OFFSET to retrieve all records.

    Args:
        sql_helper: SqlHelper object of type Scripting.ISqlHelper
        base_query: Base SQL query string (e.g., "SELECT * FROM CustomTable WHERE Status = 'Active'")
        page_size: Number of records to fetch per page (default: 1000)
    Returns:
        list: Combined list of all records from all pages
    Note:
        - Base query should include ORDER BY clause for consistent pagination
        - A default/ dummy ORDER BY is added to the query if missing
        - Function automatically appends OFFSET and FETCH NEXT clauses
    """

    all_records = []
    offset = 0
    has_more_records = True

    # Check if query has ORDER BY clause (case-insensitive)
    query_upper = base_query.upper()
    if "ORDER BY" not in query_upper:
        # Add ORDER BY (SELECT NULL) to satisfy OFFSET requirement
        base_query = base_query + " ORDER BY (SELECT NULL)"

    while has_more_records:
        # Build paginated query
        paginated_query = "{0} OFFSET {1} ROWS FETCH NEXT {2} ROWS ONLY".format(
            base_query,
            offset,
            page_size
        )

        # Execute query using SqlHelper
        result = sql_helper.GetList(paginated_query)
        if result and len(result) > 0:
            # Add records from current page to results
            all_records.extend(result)
            # Check if we have all results
            if len(result) < page_size:
                has_more_records = False
            else:
                # Move to next batch
                offset += page_size
        else:
            # No more records found
            has_more_records = False
    return all_records