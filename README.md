![Python](https://img.shields.io/badge/python-3.13-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-orange.svg)
![SQLModel](https://img.shields.io/badge/SQLModel-latest-orange.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Hackaton Backend for Frontend
## Installation and Setup of your environment

To run the API, follow these steps to set up your environment:

1. Clone the repository:
    ```bash
    git clone https://github.com/TimWalles/ht_backend_for_frontend.git
    ```

2. Navigate to the project directory:
    ```bash
    cd ht_backend_for_frontend
    ```

3. Create a virtual environment (optional but recommended):
    ```bash
    python3 -m venv env
    ```

4. Activate the virtual environment:
    - For Windows:
      ```bash
      .\env\Scripts\activate
      ```
    - For macOS and Linux:
      ```bash
      source env/bin/activate
      ```

5. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

6. Set up your MySQL database:
    - Create a new MySQL database for users and data.
    - Copy the `.env-dist` file and rename it to `.env`
    - Update the `.env` file with your database credentials:
      ```env
      DATABASE_DOMAIN="your_database_domain"
      DATABASE_USER="your_database_user"
      DATABASE_PASSWORD="your_database_password"
      USERS_DATABASE_NAME="your_users_database_name"
      DATA_DATABASE_NAME="your_data_database_name"
      SECRET_KEY="your_secret_key"
      ALGORITHM="HS256"
      ACCESS_TOKEN_EXPIRE_MINUTES=30
      ```
7. Generate a secret key:
    - You can generate a secret key using the following terminal command:
      ```bash
      openssl rand -hex 32
      ```
    - Copy the generated key and update the `SECRET_KEY` in your `.env` file.

## Commitment
The Data processing pipeline and LabelChecker program are available free of charge and compatible with all major operating systems. All data processing occurs locally, ensuring that there is no transfer of ownership of the complete dataset or any of its components from the user.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.