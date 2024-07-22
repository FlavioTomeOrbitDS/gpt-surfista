# Use a base image com Python
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port that Streamlit uses
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "app.py"]
