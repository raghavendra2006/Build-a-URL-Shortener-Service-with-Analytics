# URL Shortener Service with Analytics

A robust, RESTful microservice built with **Python (FastAPI)** and **SQLAlchemy**. This service efficiently converts long URLs into short, manageable aliases, handles HTTP redirects, and provides real-time click analytics.

## 🚀 Features

* **URL Shortening:** Generates unique, 6-8 character alphanumeric short codes.
* **Analytics Tracking:** Records click counts, timestamps, and user-agent data for every visit.
* **High Performance:** Uses HTTP 302 redirects for accurate tracking without caching issues.
* **Data Integrity:** Built on a relational database (SQLite) to ensure reliable data storage.
* **Auto-Documentation:** Interactive API documentation via Swagger UI.

---

## 🛠️ Tech Stack

* **Language:** Python 3.8+
* **Framework:** FastAPI
* **Server:** Uvicorn
* **Database:** SQLite (via SQLAlchemy ORM)
* **Version Control:** Git & GitHub

---

## ⚙️ Setup & Installation

Follow these steps to run the service locally.

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/url-shortener-service.git](https://github.com/YOUR_USERNAME/url-shortener-service.git)
cd url-shortener-service


2. Create a Virtual EnvironmentIt is recommended to use a virtual environment to manage dependencies.Windows:Bashpython -m venv venv
venv\Scripts\activate
Mac/Linux:Bashpython3 -m venv venv
source venv/bin/activate
3. Install DependenciesBashpip install -r requirements.txt
4. Run the ServerStart the application using Uvicorn:Bashuvicorn main:app --reload
The server will start at: http://127.0.0.1:8000📖 API Documentation1. Shorten a URLAccepts a long URL and returns a unique short code.Endpoint: POST /api/shortenContent-Type: application/jsonRequest Body:JSON{
  "original_url": "[https://www.google.com/search?q=fastapi](https://www.google.com/search?q=fastapi)"
}
Response (201 Created):JSON{
  "original_url": "[https://www.google.com/search?q=fastapi](https://www.google.com/search?q=fastapi)",
  "short_code": "2Bi"
}
cURL Example:Bashcurl -X POST "[http://127.0.0.1:8000/api/shorten](http://127.0.0.1:8000/api/shorten)" \
     -H "Content-Type: application/json" \
     -d '{"original_url": "[https://www.github.com](https://www.github.com)"}'
2. Redirect to Original URLAccessing the short code redirects the user to the original destination.Endpoint: GET /{short_code}Response: HTTP 302 Found (Redirects to original URL)Example:Open http://127.0.0.1:8000/2Bi in your browser.3. Get AnalyticsRetrieves usage statistics for a specific short code.Endpoint: GET /api/stats/{short_code}Response (200 OK):JSON{
  "original_url": "[https://www.google.com/search?q=fastapi](https://www.google.com/search?q=fastapi)",
  "short_code": "2Bi",
  "total_clicks": 12
}
cURL Example:Bashcurl "[http://127.0.0.1:8000/api/stats/2Bi](http://127.0.0.1:8000/api/stats/2Bi)"
🧠 Algorithmic StrategyShort Code Generation (Base62)Instead of using hashing (which causes collisions), this service uses a Base62 Encoding strategy tied to the database's primary key.Auto-Increment ID: When a URL is saved, the database assigns it a unique integer ID (e.g., 10001, 10002).Base62 Conversion: We convert this base-10 integer into a base-62 string using the characters 0-9, a-z, A-Z.Example: ID 10000 $\rightarrow$ 2Bi.Offset: An initial offset (e.g., 10000) is added to the ID to ensure short codes are at least 3 characters long and don't appear predictable (like a, b, c).Collision HandlingStrategy: Mathematical Guarantee.Because the short code is derived directly from the database's Primary Key (which is guaranteed to be unique by the database engine), collisions are mathematically impossible. This eliminates the need for complex "check-if-exists" loops, resulting in faster write speeds (O(1) time complexity).🧪 TestingInteractive Documentation (Swagger UI)FastAPI provides an automatic, interactive dashboard to test all endpoints.Run the server.Visit http://127.0.0.1:8000/docs.OpenAPI Specification (Postman/Insomnia)To easily import this project into Postman or Insomnia:Navigate to http://127.0.0.1:8000/openapi.json.Save the content as openapi.json.Import this file into your API client tool.(Note: This openapi.json file is also included in the repository for convenience).