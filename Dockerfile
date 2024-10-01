# to clean the docker stuff in linux use : docker system prune -a -f
# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory to /app
WORKDIR /app

# Copy the entire app into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && \
    echo "Starting up project" && \
    pip install -e .

# Expose the port the app runs on
EXPOSE 8080

#Startup the python server
ENTRYPOINT ["uvicorn", "src.DeliveryServer.server.server:app", "--host", "0.0.0.0", "--port", "8080"]
