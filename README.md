# Summarize App

## Project Overview
Summarize App is a versatile application designed to help users efficiently process and summarize information across multiple platforms.

## Project Structure
- `backend/`: Django-based backend server
- `mobile/`: Mobile application component
- `requirements.txt`: Project dependencies

## Technologies Used
- Backend: Django (5.1.4)
- Mobile: Flet (0.25.1)
- Authentication: Django AllAuth
- AI Integration: OpenAI API
- Language: Python

## Prerequisites
- Python 3.8+
- pip
- Virtual Environment (recommended)

## Setup and Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/summerize-app.git
cd summerize-app
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Backend Setup
```bash
cd backend
python manage.py migrate
python manage.py runserver
```

### 5. Mobile App Setup
```bash
cd ../mobile
# Follow specific mobile app setup instructions
```

## Features
- Cross-platform summarization
- AI-powered text processing
- User authentication
- Mobile and web interfaces

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
Distributed under the MIT License. See `LICENSE` for more information.

