# spending-app

## .env File

The `.env` file is used to store environment variables that are essential for the application to run securely and configure certain settings.

### Creating and Configuring the `.env` File

1. **Create a `.env` file** in the root directory of the project.

2. Add the following variables to the `.env` file:

    ```env
    SECRET_KEY=your_secret_key_here
    ```

   - `SECRET_KEY`: This key is used for cryptographic operations, such as password hashing and generating tokens. It must be kept secret. You can generate a secure random string for it using various tools or libraries.

### How to Set Up `SECRET_KEY`

To create a strong `SECRET_KEY`, you can use Python's built-in libraries. Here is an example of how to generate a secure key:

```python
import secrets
print(secrets.token_hex(32))
```

## Managing the Spending App Backend with Docker Scripts

This guide explains how to use the provided Bash scripts to manage the Spending App Backend using Docker.

### Prerequisites
1. Ensure you have **Docker** installed and running on your machine.
2. Clone the Spending App Backend repository or place the Dockerfile and scripts in the appropriate directory.

---

### **Start the Backend**

This script builds the Docker image, creates a database file (`test.db`), and runs the container.

#### **Usage**
Run the script using the command:
```bash
./start-backend.sh
```

#### **What It Does**
1. Builds the Docker image and tags it as `spending-app-backend`.
2. Creates a SQLite database file `test.db` in the current directory.
3. Runs a Docker container named `spending-app-backend-container` in detached mode:
   - Maps the local file `test.db` to `/app/test.db` inside the container.
   - Exposes the backend on port **8000**.

#### **Accessing the Backend**
Once the container is running, the backend is accessible at:
```
http://localhost:8000
```

You can access the API documentation at:
```
http://localhost:8000/docs
```

---

### **Stop the Backend**

This script stops and removes the running container and cleans up the database file.

#### **Usage**
Run the script using the command:
```bash
./stop-backend.sh
```

#### **What It Does**
1. Stops the running Docker container (`spending-app-backend-container`).
2. Deletes the `test.db` file from the current directory.
3. Removes the container from Docker.

---

### Notes
- Ensure these scripts have executable permissions before running. Use the following command to make them executable:
  ```bash
  chmod +x start-backend.sh stop-backend.sh
  ```
- If you need to persist the database between runs, avoid deleting `test.db` in the `stop-backend.sh` script.
- Modify the scripts to change ports or file paths as needed for your environment.
