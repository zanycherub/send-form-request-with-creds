 Sends an HTTP POST request with credentials and form-encoded data, using a root CA certificate.

    Parameters:
        url (str): The target URL.
        form_data (dict): A dictionary representing the form data.
        headers (dict, optional): A dictionary of HTTP headers to include in the request.

    Returns:
        Response: The response object from the server.
