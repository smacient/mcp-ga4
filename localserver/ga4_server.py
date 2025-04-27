from typing import Any

# import httpx
# import mcp
from mcp.server.fastmcp import FastMCP

# Proceed with importing your module
from actions.run_report import GoogleAnalyticsReport
from actions.run_admin_services import GoogleAnalyticsAdminServices
from actions.run_realtime_report import GoogleAnalyticsRealTimeReport
from actions.run_comparative_report import GoogleAnalyticsComparativeReport
from actions.run_report_with_ordering import GoogleAnalyticsReportWithOrdering

# initialize authentication
from google.oauth2 import service_account
credentials = service_account.Credentials.from_service_account_file(
    "C:\\Users\\anibr\\Downloads\\credentials.json"
)

# Initialize FastMCP server
mcp = FastMCP(
    name="google analytics 4",
    host="127.0.0.1",
    port=5000,
    timeout=30
    )


# property_id = "256742771"
# account_id = "140900748"

@mcp.tool()
def get_report(
    property_id: str,
    dimensions: list,
    metrics: list,
    start_date: str,
    end_date: str,
) -> str:
    """Returns a customized report of your Google Analytics event data.
    Args:
        property: A Google Analytics GA4 property identifier(e.g., "123456789")
        metrics: Metrics attributes for your data.
                 Examples: "screenPageViews", "sessions", "conversions"
        dimensions: Optional dimension attributes. 
                 Examples: "date", "city", "browser"
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    Returns:
        returns a string formatted table of requested metrics and dimension
    """
    report = GoogleAnalyticsReport(credentials)
    return report.run_report(
        property_id,
        dimensions,
        metrics,
        start_date,
        end_date
        )

@mcp.tool()
def get_realtime_report(
    property_id: str,
    metrics: list,
    dimensions: list = None
) -> str:
    """Returns real-time data from Google Analytics 4.   
    Args:
        property: A Google Analytics GA4 property identifier (e.g., "123456789")
        metrics: Metrics attributes for real-time data. Examples: "activeUsers", "screenPageViews"
        dimensions: Optional dimension attributes. Examples: "city", "browser"
    """
    real_time_report = GoogleAnalyticsRealTimeReport(credentials)
    return real_time_report.run_realtime_report(property_id, metrics, dimensions)

@mcp.tool()
def compare_period_metrics(
    property_id: str,
    period_1_start_date: str,
    period_1_end_date: str,
    period_2_start_date: str,
    period_2_end_date: str,
    metrics: list,
    dimensions: list = [],
) -> str:
    """Compare Google Analytics metrics between two time periods.    
    Args:
        property: A Google Analytics GA4 property identifier (e.g., "123456789")
        metrics: Metrics to compare. Examples: "screenPageViews", "sessions", "conversions"
        current_start_date: Start date for current period in YYYY-MM-DD format
        current_end_date: End date for current period in YYYY-MM-DD format
        previous_start_date: Start date for previous period in YYYY-MM-DD format
        previous_end_date: End date for previous period in YYYY-MM-DD format
        dimensions: Optional dimension attributes. Examples: "date", "city", "browser"
    """
    compare_report = GoogleAnalyticsComparativeReport(credentials)
    return compare_report.run_report_with_named_date_ranges(
        property_id,
        period_1_start_date,
        period_1_end_date,
        period_2_start_date,
        period_2_end_date,
        metrics,
        dimensions,
        )

@mcp.tool()
def get_report_with_order(
        property_id,
        metrics,
        dimensions,
        start_date,
        end_date,
        orderby,
) -> str:
    """Runs a report of active users grouped by three dimensions, ordered by
        the indicated metric in descending order.
        ARG:
            property_id: A valid property_id
            metrics: a list of metrics or metric
            start_date: start_date of report in the format 'YYYY-MM-DD' or today, or yesterday, or 'NdaysAgo' e.g "7daysAgo",
            end_date: end date of report
            Orderby: specify the metrics to orderby

    """
    orderedreport = GoogleAnalyticsReportWithOrdering(credentials)
    return orderedreport.run_report_with_ordering(
        property_id,
        metrics,
        dimensions,
        start_date,
        end_date,
        orderby
        )


@mcp.tool()
def list_all_properties(account_id: str, transport: str) -> list:
    """
        Lists all Google Analytics properties under the specified parent account
        that are available to the current user.
        Provides property_id for other tasks

        Args:
            account_id(str): The Google Analytics account ID.
            transport(str): The transport to use. For example, "grpc"
                or "rest". If set to None, a transport is chosen automatically.
        Returns:
            returns a list of properties associated with this account_id
    """
    admin = GoogleAnalyticsAdminServices(credentials)
    return admin.list_properties(account_id, transport)

@mcp.tool()
def list_all_accounts(self, transport: str = None) -> list:
    """
        Lists the available Google Analytics accounts.

        Args:
            transport(str): The transport to use. For example, "grpc"
            or "rest". If set to None, a transport is chosen automatically.
        Returns:
            returns a list of accounts
    """
    admin = GoogleAnalyticsAdminServices(credentials)
    return admin.list_accounts(transport)


if __name__ == "__main__":
    ga4_server()
    # admin = GoogleAnalyticsAdminServices()
    # admin.list_properties(account_id)
    # admin.list_accounts()
    # reportga = GoogleAnalyticsGA4Report(property_id)
    # reportga.run_report(start_date="2020-03-31", end_date="today", metrics="activeUsers")
    # reportga.run_report("2020-03-31", "today", metrics="activeUsers")
    # report = GoogleAnalyticsReport()
    # report.run_report(property_id)
    # realtimerequest = GoogleAnalyticsRealTimeReport()
    # realtimerequest.run_realtime_report(property_id)
    # orderedreport = GoogleAnalyticsReportWithOrdering()
    # orderedreport.run_report_with_ordering(property_id)
    # comparereport = GoogleAnalyticsComparativeReport()
    # comparereport.run_report_with_named_date_ranges(property_id)
