from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    Dimension,
    Metric,
    MetricType,
    RunRealtimeReportRequest,
)

from actions.tabulated import tabular_output


class GoogleAnalyticsRealTimeReport:
    def __init__(self, credentials):
        self.credentials = credentials

    def run_realtime_report(
            self,
            property_id,
            metrics,
            dimensions
            ):
        """Runs a realtime report on a Google Analytics 4 property."""
        client = BetaAnalyticsDataClient(credentials=self.credentials)

        request = RunRealtimeReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name=dimension) for dimension in dimensions],
            metrics=[Metric(name=metric) for metric in metrics],
        )
        response = client.run_realtime_report(request)
        table_str = tabular_output(response)

        # Build the result string
        metricstype = [MetricType(metricHeader.type_).name for metricHeader in response.metric_headers]
        result = [
            f"Google Analytics RealTime Report for Property {property_id}",
            f"Period: Real time information",
            f"Metrics: {', '.join(metrics)}",
            f"Metrics types: {','.join(metricstype)}"
        ]

        if dimensions:
            result.append(f"Dimensions: {', '.join(dimensions)}")

        result.append("")
        result.append(table_str)

        # Return formatted response
        return "\n".join(result)
