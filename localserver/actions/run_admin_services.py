from google.analytics.admin import AnalyticsAdminServiceClient
from google.analytics.admin_v1alpha.types import ListPropertiesRequest

from logfolder.logger import setup_logging, logger
from exception.exception import CustomException
import sys


class GoogleAnalyticsAdminServices:
    def __init__(self, credentials):
        self.credentials = credentials

    def list_accounts(self, transport: str = None):
        """
        Lists the available Google Analytics accounts.

        Args:
            transport(str): The transport to use. For example, "grpc"
                or "rest". If set to None, a transport is chosen automatically.
        """

        # Using a default constructor instructs the client to use the credentials
        # specified in GOOGLE_APPLICATION_CREDENTIALS environment variable.
        client = AnalyticsAdminServiceClient(
            credentials=self.credentials,
            transport=transport
            )

        results = client.list_accounts()

        # Displays the configuration information for all Google Analytics accounts
        # available to the authenticated user.
        feedback = []
        print("Result:")
        for account_ in results:
            feedback.append(account_)
        return feedback

    def list_properties(self, account_id: str, transport: str = None):
        """
        Lists Google Analytics 4 properties under the specified parent account
        that are available to the current user, Including deleted properties

        Args:
            account_id(str): The Google Analytics account ID.
            transport(str): The transport to use. For example, "grpc"
                or "rest". If set to None, a transport is chosen automatically.
        """
        client = AnalyticsAdminServiceClient(
            credentials=self.credentials,
            transport=transport
            )
        results = client.list_properties(
            ListPropertiesRequest(
                filter=f"parent:accounts/{account_id}",
                show_deleted=True
                )
        )

        feedback = []

        print("Result:")
        for property_ in results:
            feedback.append(property_)
        return feedback
