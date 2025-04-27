import os
import json
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)

from logfolder.logger import setup_logging, logger
from exception.exception import CustomException
import sys

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'localserver/actions/credentials.json'


class GoogleAnalyticsGA4Report:
    def __init__(self, property_id, analytics_client=None):
        self.property_id = property_id
        self.analytics_client = BetaAnalyticsDataClient()
        setup_logging()

    try:
        logger.info("run_report started")

        def run_report(self, start_date, end_date, metrics, dimensions=None, dimension_filter=None):
            # Prepare the request data
            date_ranges = [DateRange(start_date=start_date, end_date=end_date)]
            metrics = [Metric(name=metric) for metric in metrics]
            dimensions = [Dimension(name=dimension) for dimension in dimensions or []]

            if isinstance(dimension_filter, str):
                dimension_filter = json.loads(dimension_filter)
            """
            request = RunReportRequest(
                property=f"properties/{self.property_id}",
                date_ranges=date_ranges,
                metrics=metrics,
                dimensions=dimensions,
                dimension_filter=dimension_filter,
            )
            """
            request = RunReportRequest(
                property=f"properties/{self.property_id}",
                dimensions=[Dimension(name="city")],
                metrics=[Metric(name="activeUsers")],
                date_ranges=[DateRange(start_date="2025-03-31", end_date="today")],
            )

            if not os.path.exists('localserver/actions/credentials.json'):
                raise FileNotFoundError("The 'credentials.json' file was not found.")

            # Run the report
            try:
                report = self.analytics_client.run_report(request)
                print(report)
                print(f"Successfully retrieved report for the property {self.property_id}")
                # return report
                
                # print("Report result:")
                # for row in report.rows:
                    # print(row.dimension_values[0].value, row.metric_values[0].value)
            except Exception as a:
                logger.critical("An error occured in Google server{e}")
                raise CustomException(a, sys)

    except Exception as e:
        logger.error("run report ended without success")
        raise CustomException(e, sys)
