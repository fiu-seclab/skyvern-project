import csv
import sys
import time

import requests


def run_workflow_test(num_trials, user_prompt):
    """
    Runs the specified number of workflow tests and saves results to CSV.

    Args:
        num_trials (int): How many times to run the test
        user_prompt (str): Prompt to be used for the workflow
    """

    base_url = "http://localhost:8000"
    api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjQ4OTg3MDQ1MjQsInN1YiI6Im9fNDIxMTcwMTgwOTY2Njg3ODk2In0.8oTdic4oatPcnKq6u5AsW4D-OzZCG4eC-Dt1iqu3aN4"

    headers = {"x-api-key": api_key, "Content-Type": "application/json"}

    # Headers for CSV file
    csv_data = []
    csv_headers = ["Trial", "Status", "Action Count", "Score", "URL"]

    for trial in range(1, num_trials + 1):
        print(f"Starting trial {trial}/{num_trials}...")

        try:
            # 1. Workflow start request
            payload = {
                "user_prompt": user_prompt,
                "webhook_callback_url": None,
                "proxy_location": "RESIDENTIAL",
                "browser_session_id": None,
                "totp_identifier": "",
                "publish_workflow": False,
                "max_screenshot_scrolls": None,
                "extracted_information_schema": None,
                "extra_http_headers": None,
            }

            start_response = requests.post(
                f"{base_url}/api/v2/tasks", headers=headers, json=payload
            )
            start_response.raise_for_status()
            start_data = start_response.json()

            # Get required parameters
            workflow_permanent_id = start_data["workflow_permanent_id"]
            workflow_run_id = start_data["workflow_run_id"]

            print(
                f"Workflow started - ID: {workflow_permanent_id}, Run ID: {workflow_run_id}"
            )

            # 2. Track workflow status
            status_url = f"{base_url}/api/v1/workflows/{workflow_permanent_id}/runs/{workflow_run_id}"

            while True:
                status_response = requests.get(status_url, headers=headers)
                status_response.raise_for_status()
                status_data = status_response.json()

                current_status = status_data.get("status", "unknown")
                print(f"Trial {trial} - Status: {current_status}")

                if current_status not in ["running", "queued"]:
                    break

                time.sleep(5)  # Wait 5 seconds

            # 3. Get action count by fetching workflow definition
            workflow_def_url = f"{base_url}/api/v1/workflows/{workflow_permanent_id}"
            workflow_def_response = requests.get(workflow_def_url, headers=headers)
            workflow_def_response.raise_for_status()
            workflow_def_data = workflow_def_response.json()

            action_count = 0
            if (
                "workflow_definition" in workflow_def_data
                and "blocks" in workflow_def_data["workflow_definition"]
            ):
                action_count = len(workflow_def_data["workflow_definition"]["blocks"])

            # 4. Collect result data
            score = None
            url = None

            if "task_v2" in status_data and "output" in status_data["task_v2"]:
                output = status_data["task_v2"]["output"]
                score = output.get("score")
                url = output.get("url")

            # Add CSV data
            csv_row = [
                f"Trial_{trial}",
                current_status,
                action_count,
                score if score is not None else "",
                url if url is not None else "",
            ]
            csv_data.append(csv_row)

            print(f"Trial {trial} completed - Status: {current_status}, Score: {score}")

        except Exception as e:
            print(f"Trial {trial} error: {str(e)}")
            csv_row = [f"Trial_{trial}", "error", "", "", ""]
            csv_data.append(csv_row)

    # 5. Save to CSV file
    csv_filename = f"workflow_results_{num_trials}_trials.csv"
    with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_headers)
        writer.writerows(csv_data)

    print(f"\nResults saved to {csv_filename}.")
    return csv_filename


def main():
    """Main function - processes command line arguments"""

    # Default user prompt
    default_prompt = """Open google.com"""

    # Command line argument check
    if len(sys.argv) < 2:
        print("Usage: python script.py <number_of_trials> [user_prompt]")
        print("Example: python script.py 5")
        print("Example: python script.py 10 'Custom prompt text'")
        return

    try:
        num_trials = int(sys.argv[1])
        if num_trials <= 0:
            print("Number of trials must be a positive number.")
            return
    except ValueError:
        print("Invalid number of trials. Please enter a number.")
        return

    # Get user prompt (if provided)
    user_prompt = sys.argv[2] if len(sys.argv) > 2 else default_prompt

    print(f"Starting {num_trials} trials...")
    print(f"User prompt: {user_prompt[:100]}...")

    # Run tests
    result_file = run_workflow_test(num_trials, user_prompt)
    print(f"All tests completed. Results: {result_file}")


if __name__ == "__main__":
    main()
