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
