# Use a lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install the library needed for Modbus
RUN pip install pymodbus==3.1.0

# Copy your script into the container
COPY honeypot_logic.py .

# Expose the Modbus port
EXPOSE 5020

# Run the honeypot
CMD ["python", "honeypot_logic.py"]
