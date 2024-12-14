import requests
import os
import os.path

def send_request(url, form_data, headers=None):
    """
    Sends an HTTP POST request with credentials and form-encoded data, using a root CA certificate.

    Parameters:
        url (str): The target URL.
        form_data (dict): A dictionary representing the form data.
        headers (dict, optional): A dictionary of HTTP headers to include in the request.

    Returns:
        Response: The response object from the server.
    """
    # Retrieve credentials from environment variables
    username = os.getenv("API_USERNAME")
    password = os.getenv("API_PASSWORD")

    if not username or not password:
        raise ValueError("Missing credentials. Please set API_USERNAME and API_PASSWORD as environment variables.")

    # Set up basic authentication
    auth = (username, password)

    # Use default headers if none are provided
    if headers is None:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

    # Path to the root CA certificate
    root_ca_path = "path/to/rootCA.pem"

    # Validate the root CA certificate path
    if not os.path.isfile(root_ca_path):
        raise FileNotFoundError(f"The root CA certificate file was not found at: {root_ca_path}")

    try:
        # Send the POST request
        response = requests.post(url, auth=auth, data=form_data, headers=headers, verify=root_ca_path)
        
        # Check if the request was successful
        if response.status_code == 200:
            print("Request successful.")
        elif response.status_code == 400:
            print("Bad Request: Check the sent data.")
        elif response.status_code == 401:
            print("Unauthorized: Check your credentials.")
        elif response.status_code == 403:
            print("Forbidden: You do not have access.")
        elif response.status_code == 404:
            print("Not Found: The requested resource could not be found.")
        elif response.status_code >= 500:
            print("Server Error: Try again later.")
        else:
            print(f"Unexpected Status Code: {response.status_code}")
        
        response.raise_for_status()
        
        return response
    except requests.exceptions.RequestException as e:
        # Log the error details to a log file
        with open("error.log", "a") as log_file:
            log_file.write(f"An error occurred: {e}\n")
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    target_url = "https://example.com/api/login"
    form_data = {
        'action': 'login',
        'email': 'user@example.com'
    }

    custom_headers = {
        'Content-Type': 'application/json',
        'X-Custom-Header': 'CustomValue'
    }

    response = send_request(target_url, form_data, headers=custom_headers)

    if response:
        print("Response Status Code:", response.status_code)
        print("Response Body:", response.text)

