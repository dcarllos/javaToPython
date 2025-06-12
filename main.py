import logging
from dotenv import load_dotenv
import sys
import os
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from dotenv import load_dotenv
from src.az_devops.service.azure_service import AzureDevopsService
import csv


def main():
    """Fetch Azure DevOps repository metrics and export them to a CSV file."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

    load_dotenv()
    service = AzureDevopsService()
    metrics = service.get_all_azure_devops_repositories()

    if metrics:
        output_path = "./azure_legacy-v2.csv"
        try:
            with open(output_path, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
                writer.writerows(metrics)
            logging.info(f"Data successfully saved to: {output_path}")
        except Exception as e:
            logging.error(f"Error while saving CSV: {e}")
    else:
        logging.warning("No data found.")


if __name__ == "__main__":
    main()
