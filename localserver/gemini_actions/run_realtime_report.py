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

        return client.run_realtime_report(request)
