# a utlity function to convert tables to str
import pandas as pd


def tabular_output(response) -> str:
    """

    Args:
        response (google analytics data): _description_

    Returns:
        str: returns a string formatted table
    """

    # Create headers for the DataFrame
    dimension_headers = [header.name for header in response.dimension_headers]
    metric_headers = [header.name for header in response.metric_headers]
    headers = dimension_headers + metric_headers

    # Create rows for the DataFrame
    rows = []
    for row in response.rows:
        # Gather dimension values
        dimension_values = [dimension_value.value for dimension_value in row.dimension_values]

        # Gather metric values
        metric_values = [metric_value.value for metric_value in row.metric_values]

        # Combine dimension and metric values into a single row
        rows.append(dimension_values + metric_values)

    # Create a DataFrame
    df = pd.DataFrame(rows, columns=headers)

    # Format the DataFrame as a string table
    table_str = df.to_string(index=False)

    return table_str
