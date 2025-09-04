# PlayCation 

PlayCation is a Django-based web application that suggests **outdoor activities near a user’s location** and includes **group activities like charades**.  



## 🐳 1. Install Docker

### 🔹 Linux (Ubuntu/Debian)
Run the following commands in your terminal:

```bash
# Update existing packages
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install ca-certificates curl gnupg lsb-release -y

# Add Docker’s official GPG key
sudo mkdir -m 0755 -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo tee /etc/apt/keyrings/docker.asc > /dev/null
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add Docker repo
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine & Compose plugin
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

# Add your user to the docker group (so you don’t need sudo)
sudo usermod -aG docker $USER
newgrp docker


## Verify installation by running the following commands in your terminal

docker --version
docker compose version

### 🔹 Windows
1. Download Docker Desktop : Link -> https://www.docker.com/products/docker-desktop/
2. Install it and restart your machine
3. Open Docker Desktop and ensure it is running.
4. Verify installation in terminal (Powershell or CommandPrompt)
Commands::
docker --version
docker compose version


## 🚀 2. Running the Project with Docker
- Clone the Repository
git clone https://github.com/SusanGicheru07/PlayCation.git
cd PlayCation

- Create .env file and copy the example environment file:
cp .env.example .env

- Build and run containers
docker compose up -d --build

* THEN everytime you want to run the server
docker compose exec web python manage.py runserver

NB: To create a superuser
docker compose exec web python manage.py createsuperuser

To run migrations and migrate
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate



