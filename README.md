# DeliveryService 🚀
<img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI Logo" style="width: 300px; display: block; margin: 0 auto;"/>


Welcome to ****DeliveryService****, a cutting-edge solution designed for the efficient delivery of data generated within your infrastructure! 🌟

# Welcome 
This project is built for the best developers around, crafted by talented individuals who have made history in data science. Join us on this journey to streamline data delivery and revolutionize how we manage information! 💻💡

Key Features 🌟
FastAPI: High-performance web framework for building APIs with Python 3.7+.
Docker: Containerization for easy deployment and scalability.
Database Connectivity: Efficient data handling with robust database integration and SSH-Tunnel option.
DTO Support: Streamlined data transfer between services.
Dependencies 📦

To ensure everything works seamlessly, please make sure you have the following dependencies installed:

## Table of Contents 📚

- [Installation](#installation)
- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Dependencies](#dependencies)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Installation 🔧

Follow these steps to get your **DeliveryService** up and running:

### Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/Leohanhart/DeliveryService.git
cd your project
Create a Virtual Environment
Set up a virtual environment to manage your dependencies:

bash
python -m venv venv
Activate the virtual environment using the command appropriate for your operating system:

On Windows:
venv\Scripts\activate

On macOS/Linux:
source venv/bin/activate

Install the required dependencies and build the working package with the following command:
pip install -e .

Run Your Project
Finally, run the main script to start your project:

python src/DeliveryService/Processes/Main.py

# Dont forget to set the python interpreter to the one in the VENV in you IDE.
Type 'where python' to find your python envoirment.
Type 'pip list' to check if package is installed correctly.

``` 
Project Overview 🌐
DeliveryService is powered by FastAPI, providing a robust server architecture. It utilizes Data Transfer Objects (DTOs) for efficient data handling and communication. With seamless Docker integration, it simplifies deployment and management, making it easy to scale as your needs grow.

The project also includes a comprehensive database connection setup to ensure that your data flows smoothly through the infrastructure, making it a reliable choice for all your data delivery needs! 📦✨


dotenv: For loading environment variables.
FastAPI: For building the API.
SQLAlchemy: For database interaction (if using SQL).
Docker: For containerization.
Configuration ⚙️
To configure your project, you will need to set up the following environment variables in a .env file:

# .env file template
```
# SSH Configuration
SSH_NAME=*******
SSH_HOST=*******
SSH_PORT=*******
SSH_USER=*******
SSH_PASSWORD=*******

# DB
DB_HOST=*******
DB_PORT=*******
DB_USER=*******
DB_PASSWORD=*******
DB_DATABASE=*******

# Private Container Registry
PCR_SERVER=*******
PCR_USER=*******
PCR_PASSWORD=*******
Make sure to replace the ******

with your actual configuration values.
```
Contributing 🤝
We welcome contributions from everyone! If you have suggestions or improvements, please feel free to fork the repository and submit a pull request. Together, let's make DeliveryService even better!

License 📄
This project is licensed under the MIT License. See the LICENSE file for details.



