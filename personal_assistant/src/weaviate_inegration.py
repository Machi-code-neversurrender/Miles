import weaviate
import logging

class WeaviateIntegration:
    def __init__(self, url):
        self.client = weaviate.Client(url)
        self.logger = logging.getLogger(__name__)

    def store_tasks(self, tasks):
        """
        Store tasks in Weaviate.
        """
        if not tasks:
            self.logger.warning("No tasks provided for storage.")
            return

        for task in tasks:
            try:
                task_data = {
                    "name": str(task.get("name", "")),
                    "description": str(task.get("notes", "")),
                    "due_date": str(task.get("due_on", ""))
                }
                self.client.data_object.create(
                    data_object=task_data,
                    class_name="Task"
                )
            except Exception as e:
                self.logger.error(f"Error storing task in Weaviate: {e}")

    def store_data(self, data, data_type):
        """
        Store data in Weaviate.
        """
        if not data:
            self.logger.warning(f"No data provided for storage in {data_type}.")
            return

        for item in data:
            try:
                item_data = {
                    "content": str(item),
                    "source": "web"
                }
                self.client.data_object.create(
                    data_object=item_data,
                    class_name=data_type
                )
            except Exception as e:
                self.logger.error(f"Error storing data in Weaviate: {e}")