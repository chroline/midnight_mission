# Midnight Mission data dashboard
## Getting Started

### Step 1: Install Python
First, ensure that Python is installed on your system. You can download Python from the [official Python website](https://www.python.org/downloads/). The `venv` module is included by default from Python 3.3 onwards.

### Step 2: Create a Virtual Environment
Open a terminal (or command prompt on Windows) and navigate to your project directory. Then, run the following command to create a virtual environment:

```bash
python3 -m venv .venv
```

This command creates a directory called `.venv` in your project folder, where all the virtual environment files will be stored. You can name the directory anything you like; `.venv` is just a common convention.

### Step 3: Activate the Virtual Environment
Activating the virtual environment will configure your shell to use the Python and pip executables from the virtual environment rather than the global Python installation. The activation command depends on your operating system:

- **On Windows:**
  ```bash
  .venv\Scripts\activate
  ```

- **On macOS and Linux:**
  ```bash
  source .venv/bin/activate
  ```

Once activated, your command prompt will usually change to indicate that the virtual environment is active. For example, you might see something like `(.venv)` prepended to your prompt.

### Step 4: Install Dependencies
You can install the appropriate dependencies by running:

```bash
pip install -r requirements.txt
```

### Step 5: Run streamlit
To launch the Streamlit application, run:

```bash
streamlit run Home.py
```