FROM python:3.12

# Set the working directory in the container
WORKDIR /app
COPY requirements.txt .
# Install dependencies
RUN pip install -r requirements.txt --index-url https://mirrors.aliyun.com/pypi/simple/
# Copy the rest of the application code to the working directory
COPY . .
# Expose port 5000
EXPOSE 5000
# Start the application
CMD ["python", "dictionary_backend.py"]
