# Honeypot Flask Application

This is a simple Flask-based honeypot application designed to log unauthorized access attempts to your web server. It captures the incoming requests' IP address, HTTP method, path, user agent, and geographical information (such as country and ISP) for each request made to any endpoint. It then sends these details to a Discord channel via a webhook and saves them in a JSON log file.

## Features

- Logs unauthorized access attempts to any endpoint of the Flask application.
- Retrieves geographical information about the IP address of the requester.
- Sends a notification to a Discord webhook when an unauthorized access attempt is made.
- Saves access attempt logs in a JSON file.

## Requirements

- Python 3.x
- Flask
- Requests library

You can install the required Python libraries using pip:

```bash
pip install flask requests
