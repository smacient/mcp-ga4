from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    MetricType,
    RunReportRequest,
)

from actions.tabulated import tabular_output


class GoogleAnalyticsReport:
    def __init__(self, credentials):
        self.credentials = credentials

    def run_report(
        self,
        property_id: str,
        dimensions: list,
        metrics: list,
        start_date: str,
        end_date: str,
    ) -> str:
        """Runs a report of active users grouped by country."""
        client = BetaAnalyticsDataClient(credentials=self.credentials)

        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name=dimension) for dimension in dimensions],
            metrics=[Metric(name=metric) for metric in metrics],
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        )
        response = client.run_report(request)

        table_str = tabular_output(response)

        # Build the result string
        metricstype = [MetricType(metricHeader.type_).name for metricHeader in response.metric_headers]
        result = [
            f"Google Analytics Report for Property {property_id}",
            f"Period: {start_date} to {end_date}",
            f"Metrics: {', '.join(metrics)}",
            f"Metrics types: {','.join(metricstype)}"
        ]

        if dimensions:
            result.append(f"Dimensions: {', '.join(dimensions)}")

        result.append("")
        result.append(table_str)

        # Return formatted response
        return "\n".join(result)
