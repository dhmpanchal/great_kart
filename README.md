# This is Ecommerce Project in django

## setup project

1. clone repository

    ```
    git clone https://github.com/dhmpanchal/great_kart.git
    ```
2. make virtual envirement

    ```
    python -m venv venv
    ```

3. install requirements.

    ```
    pip install -r requirements.txt
    ```

3. add .env file.

    ```
    SECRET_KEY=<SECRET_KEY>
    DEBUG=<DEBUG>
    EMAIL_BACKEND=<EMAIL_BACKEND>
    EMAIL_USE_TLS=<EMAIL_USE_TLS>
    EMAIL_HOST=<EMAIL_HOST>
    EMAIL_PORT=<EMAIL_PORT>
    EMAIL_HOST_USER=<EMAIL_HOST_USER>
    EMAIL_HOST_PASSWORD=<EMAIL_HOST_PASSWORD>
    DEFAULT_FROM_EMAIL=<DEFAULT_FROM_EMAIL>
    DB_NAME=<DB_NAME>
    DB_USER=<DB_USER>
    DB_PASSWORD=<DB_PASSWORD>
    DB_PORT=<DB_PORT>
    DB_HOST_NAME=<DB_HOST_NAME>
    ```
4. Run project

    ```
    python manage.py runserver
    ```