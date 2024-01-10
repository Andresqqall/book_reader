# Book Reader

Welcome to Book Reader

## Quick Start

To run the Book Reader application, use the following Docker Compose command:

bash: docker-compose up --build

# API Documentation

Explore and interact with the Book Reader API using Swagger. The API documentation is available at:

http://localhost:8000/swagger/

# Email Configuration

Book Reader utilizes email functionality for notifications and user communication.
To configure the email settings, follow these steps:

1. Open the .env file in your project's root directory. If it doesn't exist, create one.

2. Add the following lines to the .env file:
  EMAIL_HOST=your_email_host
  EMAIL_PORT=your_email_port
  EMAIL_USE_TLS=your_email_use_tls
  EMAIL_HOST_USER=your_email_host_user
  EMAIL_HOST_PASSWORD=your_email_host_password
