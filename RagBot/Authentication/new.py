import bcrypt
import yaml

# Define usernames and their corresponding plain-text passwords
users = {
    'Rachit': 'password123',
    'Shivang': 'admin123',
    'Test': 'test123',
    'Test2': 'test1234'
}

# Function to hash passwords
def hash_password(plain_password):
    return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()

# Prepare the credentials dictionary
credentials = {
    'credentials': {
        'usernames': {}
    }
}

# Hash the passwords and add to the dictionary
for username, password in users.items():
    hashed_password = hash_password(password)
    credentials['credentials']['usernames'][username] = {
        'name': username.capitalize(),  # You can change this to actual names if needed
        'password': hashed_password
    }

# Write the credentials dictionary to the YAML file
with open("credentials.yaml", "w") as file:
    yaml.dump(credentials, file, default_flow_style=False)

print("credentials.yaml file has been updated with hashed passwords!")
