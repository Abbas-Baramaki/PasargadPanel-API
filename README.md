# Pasargad Panel API Client & Scraper 💳🐍

A lightweight and efficient Python client designed to interact with administrative panels (such as Marzban-based or similar management panels). This tool was created to help users seamlessly authenticate, manage subscriptions, and automate panel interactions via direct HTTP requests—ideal for those whose panel providers lack official API support or documentation.

---

## 🚀 Features
* **Authentication Handler:** Easily logs in using admin credentials, manages access tokens, and handles session states.
* **Subscription Management:** Create new user subscriptions with custom data limits, expiration periods, groups, and randomized suffixes.
* **User Lookup:** Search and retrieve detailed subscription and status information for specific users.
* **Custom Exception Handling:** Built-in error management for authentication failures (`401`), duplicate users (`201`), and missing endpoints (`404`).
* **Lightweight:** Built entirely on the standard `requests` library with zero heavy browser-automation overhead.

---

## 📦 Prerequisites
Ensure you have Python 3.x installed. Install the required dependency using pip:

```bash
pip install requests
```
⚙️ Usage Example
Here is how to initialize the configuration, log in, and create or fetch user subscriptions:
```python
from main import Config, AuthenticationError, UserAlreadyExists

# 1. Initialize the panel configuration
panel_client = Config(
    panel="[https://your-panel-domain.com](https://your-panel-domain.com)",
    username="your_admin_username",
    password="your_admin_password"
)

try:
    # 2. Authenticate
    if panel_client.login():
        print("Successfully logged in!")

        # 3. Create a new subscription (Data limit in GB, Expiry in days)
        new_user = panel_client.create_sub(
            data_limit=50.0,
            expire=30,
            name="client_user",
            note="Created via automation script"
        )
        print("User Created:", new_user)

        # 4. Fetch subscription details
        user_info = panel_client.subscription("client_user_randomsuffix")
        print("User Info:", user_info)

except AuthenticationError:
    print("Authentication failed: Check your credentials.")
except UserAlreadyExists:
    print("User already exists in the panel.")
except Exception as e:
    print(f"An error occurred: {e}")
```
⚠️ Disclaimer
This utility is developed for educational purposes and to assist administrators and users in managing and recovering their own data. The author assumes no responsibility for any misuse, policy violations, or damages resulting from the use of this software.

🤝 Contributing
Contributions, issues, and pull requests are welcome! Feel free to open an issue if you encounter bugs or want to suggest improvements.
