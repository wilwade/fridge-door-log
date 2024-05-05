# Log Freezer Door Opens

Simple Python script to log freezer door opening and closing via gehomesdk.

## Quick Start

1. Init the Python Env
    ```sh
    python -m venv env
    ```
2. Trigger the Env
    ```sh
    source ./env/bin/activate
    ```
3. Install Dependencies
    ```sh
    pip install -r requirements.txt
    ```
4. Create Credentials File
    ```sh
    cp credentials.py.template credentials.py
    ```
5. Update `credentials.py` with correct values

## Helpful Notes

- `pip freeze > requirements.txt` when updating deps
