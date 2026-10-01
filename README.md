# ❤️ HelpReach — Donation & NGO Platform

HelpReach is a full-stack web application designed to connect donors with non-governmental organizations (NGOs). The platform aims to make it easier to discover donation opportunities, coordinate support, and connect people who want to help with organizations working to address community needs.

## ✨ Features

- 🤝 Donor and NGO connection
- 👤 User authentication and account management
- 🏢 NGO-oriented platform workflow
- 🎁 Donation coordination interface
- 🗄️ MySQL database integration
- ⚙️ Flask backend and application logic
- 🎨 User-friendly web interface
- 📱 Responsive website design

## 🛠️ Technologies Used

- **Python** — Backend programming
- **Flask** — Web application framework
- **MySQL** — Database management
- **HTML5** — Website structure
- **CSS3** — Styling and responsive layouts
- **JavaScript** — Frontend interactions

## 🏗️ Application Architecture

The application follows a frontend-backend-database architecture.

```text
        User Interface
              |
              v
       Flask Backend
              |
              v
        MySQL Database
```

The frontend provides the user interface, Flask handles application logic and requests, and MySQL stores application data.

## 🚀 Getting Started

### Prerequisites

- Python installed
- MySQL Server installed and running
- pip package manager

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/helpreach.git
   ```

2. Navigate to the project directory:

   ```bash
   cd helpreach
   ```

3. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

4. Activate the environment on Windows PowerShell:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

5. Install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

6. Configure the MySQL database and the required environment variables.

7. Run the Flask application using its configured entry-point file:

   ```bash
   python app.py
   ```

8. Open the local URL displayed in the terminal.

## 🔐 Environment Configuration

Configure your database connection and application secrets through environment variables.

Never commit database passwords, secret keys, or private credentials to the repository.

## 🔮 Future Enhancements

- Online payment gateway integration
- Donation tracking and status updates
- NGO verification
- Donation history and reports
- Campaign creation and management
- Email notifications
- Impact reports and transparency dashboards
- Advanced search and filtering
- Administrative dashboard

## 🎯 Project Objective

To create a digital platform that connects people willing to contribute with NGOs seeking support, helping improve donation coordination and community participation.

## 🌍 Social Impact

HelpReach explores how technology can support charitable initiatives by improving the connection between donors and organizations and making donation opportunities easier to discover.

## 👩‍💻 Developer

**Sakhi Prasad Tapre**

Computer Engineering Student | Aspiring Software Developer

## 📄 License

Add an appropriate license if you intend to distribute this project publicly.
