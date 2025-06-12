# Python image
FROM python:3.11-slim

# Directory where streamlit_app.py(in my case) is (/fronted -> Dockerfile, /fronted -> streamlit_app.py)
WORKDIR /app

# install dependancies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
 && rm -rf /var/lib/apt/lists/*

 # install pips
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy whole directory
COPY . .


# exposes port 8080, default for cloud deployment, locally at port 8051
EXPOSE 8080

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8080", "--server.address=0.0.0.0"]

