# Deployment Guide 🚀

This guide covers different deployment options for the Senti-Nalysis Streamlit application.

## Table of Contents
1. [Local Development](#local-development)
2. [Streamlit Community Cloud](#streamlit-community-cloud)
3. [Docker Deployment](#docker-deployment)
4. [Traditional Server Deployment](#traditional-server-deployment)
5. [Cloud Platform Deployment](#cloud-platform-deployment)

---

## Local Development 💻

Perfect for testing and development.

### Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py
```

Access at: `http://localhost:8501`

### Configuration
Edit `.streamlit/config.toml` to customize:
- Theme colors
- Port number
- Server settings

---

## Streamlit Community Cloud ☁️

**Best for**: Free hosting, easy deployment, automatic updates

### Prerequisites
- GitHub account
- GitHub repository with your code
- Streamlit Cloud account (free at streamlit.io/cloud)

### Steps

1. **Prepare Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect your GitHub repository
   - Select branch: `main`
   - Main file path: `streamlit_app.py`
   - Click "Deploy"

3. **Configure Secrets (if needed)**
   - In Streamlit Cloud dashboard, go to your app settings
   - Add secrets in `.streamlit/secrets.toml` format
   - Example:
     ```toml
     [passwords]
     admin = "your_password_here"
     ```

4. **Monitor Deployment**
   - Check build logs
   - Fix any errors
   - App will be live at: `https://your-app-name.streamlit.app`

### Limitations
- Files written to disk may not persist between sessions
- For persistent storage, consider cloud storage (S3, GCS, etc.)
- Resources limited on free tier

### Best Practices
- Use environment variables for sensitive data
- Minimize file system writes
- Use cloud storage for large files
- Monitor usage to stay within limits

---

## Docker Deployment 🐳

**Best for**: Consistent environments, scalability

### Create Dockerfile

Create `Dockerfile` in your project root:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Create docker-compose.yml

```yaml
version: '3.8'

services:
  senti-nalysis:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./documents:/app/documents:ro
      - ./results:/app/results
      - ./images:/app/images:ro
    environment:
      - STREAMLIT_SERVER_PORT=8501
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
    restart: unless-stopped
```

### Build and Run

```bash
# Build the image
docker build -t senti-nalysis .

# Run the container
docker run -p 8501:8501 -v $(pwd)/results:/app/results senti-nalysis

# Or use docker-compose
docker-compose up -d
```

### Access
- Local: `http://localhost:8501`
- Remote: `http://<server-ip>:8501`

---

## Traditional Server Deployment 🖥️

**Best for**: Internal servers, full control

### Prerequisites
- Linux server (Ubuntu 20.04+ recommended)
- Python 3.8+
- Nginx (for reverse proxy)
- Systemd (for service management)

### Setup Steps

1. **Install Python and Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3.10 python3-pip nginx
   ```

2. **Clone Repository**
   ```bash
   cd /opt
   sudo git clone <your-repo-url> senti-nalysis
   cd senti-nalysis
   sudo pip3 install -r requirements.txt
   ```

3. **Create Systemd Service**
   
   Create `/etc/systemd/system/senti-nalysis.service`:
   ```ini
   [Unit]
   Description=Senti-Nalysis Streamlit App
   After=network.target

   [Service]
   Type=simple
   User=www-data
   WorkingDirectory=/opt/senti-nalysis
   ExecStart=/usr/local/bin/streamlit run streamlit_app.py --server.port=8501 --server.address=127.0.0.1
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

4. **Configure Nginx**
   
   Create `/etc/nginx/sites-available/senti-nalysis`:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
           proxy_read_timeout 86400;
       }
   }
   ```

5. **Enable and Start**
   ```bash
   # Enable Nginx site
   sudo ln -s /etc/nginx/sites-available/senti-nalysis /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx

   # Enable and start service
   sudo systemctl enable senti-nalysis
   sudo systemctl start senti-nalysis
   ```

6. **Check Status**
   ```bash
   sudo systemctl status senti-nalysis
   sudo journalctl -u senti-nalysis -f
   ```

### SSL/HTTPS Setup

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal is configured automatically
sudo certbot renew --dry-run
```

---

## Cloud Platform Deployment ☁️

### AWS EC2

1. **Launch EC2 Instance**
   - Choose Ubuntu 20.04 AMI
   - t2.micro for small usage (free tier eligible)
   - Configure security group: Allow HTTP (80), HTTPS (443), SSH (22)

2. **Connect and Setup**
   ```bash
   ssh -i your-key.pem ubuntu@<ec2-ip>
   ```

3. **Follow Traditional Server Deployment steps**

4. **Configure Elastic IP** (optional)
   - Allocate Elastic IP
   - Associate with instance
   - Update DNS records

### Google Cloud Platform (GCP)

1. **Create Compute Engine Instance**
   - Choose Ubuntu 20.04
   - e2-micro for small usage (free tier)
   - Allow HTTP/HTTPS traffic

2. **SSH and Setup**
   ```bash
   gcloud compute ssh your-instance-name
   ```

3. **Follow Traditional Server Deployment steps**

### Microsoft Azure

1. **Create Virtual Machine**
   - Ubuntu 20.04 LTS
   - B1s size for small usage
   - Add inbound port rules: 80, 443

2. **Connect and Setup**
   ```bash
   ssh azureuser@<vm-ip>
   ```

3. **Follow Traditional Server Deployment steps**

### DigitalOcean

1. **Create Droplet**
   - Ubuntu 20.04
   - Basic plan: $6/month
   - Add SSH key

2. **Connect and Setup**
   ```bash
   ssh root@<droplet-ip>
   ```

3. **Follow Traditional Server Deployment steps**

---

## Environment Variables 🔐

For production deployments, use environment variables for sensitive data:

### .env file (local development)
```bash
ADMIN_PASSWORD=your_secure_password
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
```

### Load in streamlit_app.py
```python
import os
from dotenv import load_dotenv

load_dotenv()

admin_password = os.getenv('ADMIN_PASSWORD')
```

### Streamlit Secrets
For Streamlit Cloud, use `.streamlit/secrets.toml`:
```toml
admin_password = "your_secure_password"
database_url = "your_database_url"
```

Access in code:
```python
import streamlit as st

admin_password = st.secrets["admin_password"]
```

---

## Performance Optimization 🚀

### 1. Caching
Use Streamlit's caching for expensive operations:

```python
@st.cache_data
def load_csv_file(filename):
    # Expensive operation
    return pd.read_csv(filename)

@st.cache_resource
def init_database():
    # Resource initialization
    return create_connection()
```

### 2. Lazy Loading
Load data only when needed:

```python
if st.session_state.stage == 'labeling':
    # Only load data for labeling stage
    display_record()
```

### 3. Minimize Reruns
Use callbacks to avoid full reruns:

```python
def on_submit():
    st.session_state.current_index += 1

st.button("Submit", on_click=on_submit)
```

### 4. Resource Management
Clean up resources when done:

```python
# Close file handles
# Clear large data from session state
if 'large_data' in st.session_state:
    del st.session_state.large_data
```

---

## Monitoring & Maintenance 📊

### Logs

**Local:**
```bash
# View app output
streamlit run streamlit_app.py --logger.level=debug
```

**Production:**
```bash
# View systemd logs
sudo journalctl -u senti-nalysis -f

# View Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Health Checks

Add health check endpoint:
```python
# Streamlit automatically provides /_stcore/health
# Check with: curl http://localhost:8501/_stcore/health
```

### Backup

**Automated backup script:**
```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups/senti-nalysis"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup results
tar -czf "$BACKUP_DIR/results_$DATE.tar.gz" /opt/senti-nalysis/results/

# Backup completed files tracking
cp /opt/senti-nalysis/.completed_files.txt "$BACKUP_DIR/completed_$DATE.txt"

# Keep only last 30 days
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +30 -delete
```

Add to crontab:
```bash
# Backup daily at 2 AM
0 2 * * * /opt/senti-nalysis/backup.sh
```

---

## Security Best Practices 🔒

1. **Use HTTPS**: Always use SSL/TLS in production
2. **Authentication**: Add user authentication if needed
3. **Rate Limiting**: Use Nginx to limit requests
4. **Input Validation**: Validate all user inputs
5. **Update Dependencies**: Regularly update packages
6. **Firewall**: Use UFW or cloud firewalls
7. **Backup**: Regular automated backups
8. **Monitoring**: Set up alerts for errors

---

## Troubleshooting Common Issues 🔧

### App crashes on startup
- Check Python version (3.8+)
- Verify all dependencies installed
- Check file permissions
- Review error logs

### Port already in use
```bash
# Find process using port 8501
sudo lsof -i :8501
# Kill process
kill -9 <PID>
```

### Memory issues
- Increase server resources
- Optimize data loading
- Clear session state regularly

### Slow performance
- Enable caching
- Reduce data processing
- Use database for large datasets
- Upgrade server resources

---

## Cost Estimates 💰

| Platform | Monthly Cost | Best For |
|----------|-------------|----------|
| Streamlit Cloud | Free | Testing, small projects |
| DigitalOcean | $6-12 | Small to medium apps |
| AWS EC2 (t2.micro) | $8-10 | AWS ecosystem users |
| GCP (e2-micro) | $7-9 | Google Cloud users |
| Azure (B1s) | $9-11 | Microsoft ecosystem |
| Docker on VPS | $5-20 | Custom setups |

---

## Next Steps ✨

After deployment:
1. Test all functionality
2. Monitor performance
3. Set up backups
4. Configure monitoring/alerts
5. Document your setup
6. Train users
7. Plan for scaling

---

**Happy Deploying! 🎉**

For questions or issues, refer to the main README.md or open an issue on GitHub.

