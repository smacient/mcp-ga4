from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    MetricType,
    RunReportRequest,
)

from actions.tabulated import tabular_output


class GoogleAnalyticsComparativeReport:
    def __init__(self, credentials):
        self.credentials = credentials

    def run_report_with_named_date_ranges(
              self,
              property_id,
              period_1_start_date,
              period_1_end_date,
              period_2_start_date,
              period_2_end_date,
              metrics,
              dimensions,
              ):
        """Runs a report using named date ranges."""
        client = BetaAnalyticsDataClient(credentials=self.credentials)

        request = RunReportRequest(
            property=f"properties/{property_id}",
            date_ranges=[
                DateRange(
                    start_date=period_1_start_date, end_date=period_1_end_date, name="period 1"
                ),
                DateRange(
                    start_date=period_2_start_date, end_date=period_2_end_date, name="period 2"
                ),
            ],
            dimensions=[Dimension(name=dimension) for dimension in dimensions],
            metrics=[Metric(name=metric) for metric in metrics],
        )
        response = client.run_report(request)
        table_str = tabular_output(response)

        # Build the result string
        metricstype = [MetricType(metricHeader.type_).name for metricHeader in response.metric_headers]
        result = [
            f"Google Analytics comparison Report for Property {property_id}",
            f"Comapared Period: {period_1_start_date} to {period_1_end_date} and {period_2_start_date} to {period_2_end_date}",
            f"Metrics: {', '.join(metrics)}",
            f"Metrics types: {','.join(metricstype)}"
        ]

        if dimensions:
            result.append(f"Dimensions: {', '.join(dimensions)}")

        result.append("")
        result.append(table_str)

        # Return formatted response
        return "\n".join(result)
