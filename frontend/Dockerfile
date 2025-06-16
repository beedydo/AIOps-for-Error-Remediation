# Use a standard Red Hat Universal Base Image with Python 3.11
FROM registry.redhat.io/ubi9/python-311

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY app.py .

# Expose the port Streamlit runs on by default
EXPOSE 8501

# Command to run the Streamlit application
# The server address 0.0.0.0 is crucial for it to be accessible inside the cluster
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
