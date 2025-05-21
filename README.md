# Cafe & Wifi ☕📶

A responsive web application that helps users discover and manage cafes with essential amenities like WiFi, power sockets, restrooms, and more.

## Features

- 🔍 **Search Cafes**: Filter cafes by location.
- 🎲 **Random Cafe**: Get a featured cafe suggestion.
- ➕ **Add New Cafe**: Submit cafe details with amenities.
- ✏️ **Update Price**: Modify the coffee price for any cafe.
- 🗑️ **Delete Cafe**: Securely remove a cafe with API key protection.
- 💬 **Chatbot Assistant**: Ask questions about cafes, amenities, and features.

## Tech Stack

- **Frontend**: HTML, CSS (Bootstrap 5), JavaScript
- **UI Framework**: Bootstrap 5 + Bootstrap Icons
- **Interactive Features**: Modals, cards, form validation, dynamic DOM updates
- **Backend (assumed)**: RESTful API endpoints (e.g., `/all`, `/add`, `/random`, `/search`, `/update-price`, `/report-closed`)

## How It Works

- **Dynamic Loading**: On page load, cafes are fetched from `/all` and displayed.
- **Random Selection**: A random cafe is retrieved from `/random`.
- **Add Cafe**: The "Add New Cafe" modal allows users to enter data and submit it via `POST` to `/add`.
- **Update/Delete**: Actions like updating price or deleting a cafe use modals and API calls to backend endpoints.

## File Structure
````
Cafe-Wifi/
│
├── main.py # Flask application
├── requirements.txt # Dependencies
├── README.md # Project documentation
│
├── instance/
│ └── cafes.db # SQLite database
│
└── templates/
└── index.html # Main frontend template
````
## 🔧 Setup Instructions

1. **Clone the Repository**

```bash
git clone https://github.com/your-username/cafe-wifi.git
cd cafe-wifi
```

2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

3. Install Dependencies
```bash
pip install -r requirements.txt
```

4. Run the App
```bash
python main.py
```

## 🗄️Backend API Endpoints

| Method | Endpoint              | Description                      |
| ------ | --------------------- | -------------------------------- |
| GET    | `/all`                | Get all cafes                    |
| GET    | `/random`             | Get a random cafe                |
| GET    | `/search?loc=...`     | Search cafes by location         |
| POST   | `/add`                | Add a new cafe                   |
| PATCH  | `/update-price/<id>`  | Update coffee price              |
| DELETE | `/report-closed/<id>` | Delete a cafe (requires API key) |
