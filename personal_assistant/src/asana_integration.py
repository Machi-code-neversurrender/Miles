import asana
import logging

class AsanaIntegration:
    def __init__(self):
        # Pass the access token as a string
        self.client = asana.Client.access_token('2/1203963127593922/1209079337408326:d93bdf5bd31a37f50e67c694aa956465')
        self.logger = logging.getLogger(__name__)

    def fetch_tasks(self, project_id):
        """
        Fetch tasks from Asana.
        """
        if not project_id:
            self.logger.warning("No project ID provided for fetching tasks.")
            return []

        try:
            tasks = self.client.tasks.find_by_project(project_id)
            return tasks
        except Exception as e:
            self.logger.error(f"Error fetching tasks from Asana: {e}")
            return []