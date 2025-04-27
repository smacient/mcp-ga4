from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    OrderBy,
    RunReportRequest,
)

from actions.tabulated import tabular_output


class GoogleAnalyticsReportWithOrdering:
    def __init__(self, credentials):
        self.credentials = credentials

    def run_report_with_ordering(
            self,
            property_id,
            metrics,
            dimensions,
            start_date,
            end_date,
            orderby,
            ):
        """Runs a report of active users grouped by three dimensions, ordered by
            the total revenue in descending order.
            ARG:
                property_id: A valid property_id
                metrics: a list of metrics or metric
                start_date: start_date of report in the format 'YYYY-MM-DD' or today, or yesterday, or 'NdaysAgo' e.g "7daysAgo",
                end_date: end date of report
                Orderby: specify the metrics to orderby

        """
        client = BetaAnalyticsDataClient(credentials=self.credentials)

        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name=dimension) for dimension in dimensions],
            metrics=[
                Metric(name=metric) for metric in metrics
            ],
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            order_bys=[
                OrderBy(metric=OrderBy.MetricOrderBy(metric_name=orderby), desc=True)
            ],
        )

        response = client.run_report(request)
        table_str = tabular_output(response)

        # Build the result string
        result = [
            f"Google Analytics Report for Property {property_id}",
            f"Period: {start_date} to {end_date}",
            f"Metrics: {', '.join(metrics)}",
        ]

        if dimensions:
            result.append(f"Dimensions: {', '.join(dimensions)}")

        result.append("")
        result.append(table_str)

        # Return formatted response
        return "\n".join(result)
