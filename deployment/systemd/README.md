# Systemd Service Files for MediChain AI

This directory contains systemd service files for running MediChain AI agents as system services on Linux (Ubuntu/Debian).

## Service Files

- `medichain-coordinator.service` - Coordinator agent (port 8001)
- `medichain-patient-intake.service` - Patient intake agent (port 8000)
- `medichain-symptom-analysis.service` - Symptom analysis agent (port 8004)
- `medichain-treatment.service` - Treatment recommendation agent (port 8005)

## Installation

### 1. Create User and Directory

```bash
# Create medichain user
sudo useradd -r -s /bin/false medichain

# Create installation directory
sudo mkdir -p /opt/medichain
sudo chown medichain:medichain /opt/medichain
```

### 2. Deploy Application

```bash
# Clone repository
cd /opt/medichain
sudo -u medichain git clone https://github.com/RECTOR-LABS/asi-agents-track.git
cd asi-agents-track

# Setup virtual environment
sudo -u medichain python3 -m venv venv
sudo -u medichain venv/bin/pip install -r requirements.txt

# Configure environment variables
sudo -u medichain cp .env.example .env
sudo -u medichain nano .env  # Edit with actual values
sudo chmod 600 .env  # Secure permissions
```

### 3. Install Service Files

```bash
# Copy service files
sudo cp deployment/systemd/*.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload
```

### 4. Enable and Start Services

```bash
# Enable services to start on boot
sudo systemctl enable medichain-coordinator.service
sudo systemctl enable medichain-patient-intake.service
sudo systemctl enable medichain-symptom-analysis.service
sudo systemctl enable medichain-treatment.service

# Start services
sudo systemctl start medichain-coordinator.service
sudo systemctl start medichain-patient-intake.service
sudo systemctl start medichain-symptom-analysis.service
sudo systemctl start medichain-treatment.service
```

## Service Management

### Check Status

```bash
# Check all services
sudo systemctl status medichain-*.service

# Check specific service
sudo systemctl status medichain-coordinator.service
```

### View Logs

```bash
# Follow logs for all medichain services
sudo journalctl -f -u medichain-*.service

# View logs for specific service
sudo journalctl -u medichain-coordinator.service

# View logs from last hour
sudo journalctl -u medichain-coordinator.service --since "1 hour ago"
```

### Restart Services

```bash
# Restart all services
sudo systemctl restart medichain-*.service

# Restart specific service
sudo systemctl restart medichain-coordinator.service
```

### Stop Services

```bash
# Stop all services
sudo systemctl stop medichain-*.service

# Stop specific service
sudo systemctl stop medichain-coordinator.service
```

### Disable Services

```bash
# Disable from starting on boot
sudo systemctl disable medichain-coordinator.service
```

## Security Hardening

All service files include security hardening options:

- **NoNewPrivileges**: Prevents privilege escalation
- **PrivateTmp**: Isolated /tmp directory
- **ProtectSystem**: Read-only access to /usr, /boot, /efi
- **ProtectHome**: No access to home directories
- **ReadWritePaths**: Only /opt/medichain/asi-agents-track is writable

## Troubleshooting

### Service Won't Start

```bash
# Check service status
sudo systemctl status medichain-coordinator.service

# Check detailed logs
sudo journalctl -xe -u medichain-coordinator.service

# Verify file permissions
ls -la /opt/medichain/asi-agents-track/.env
# Should show: -rw------- 1 medichain medichain

# Test manual start
sudo -u medichain /opt/medichain/asi-agents-track/venv/bin/python src/agents/coordinator.py
```

### Environment Variables Not Loaded

```bash
# Verify .env file exists
ls -la /opt/medichain/asi-agents-track/.env

# Check systemd can read it
sudo systemd-analyze cat-config medichain-coordinator.service | grep EnvironmentFile

# Test environment loading
sudo -u medichain bash -c 'source /opt/medichain/asi-agents-track/.env && env | grep AGENTVERSE'
```

### Port Already in Use

```bash
# Check what's using the port
sudo lsof -i :8001

# If another service is using it, either:
# 1. Stop that service
# 2. Change the port in the agent code
```

### Permission Denied Errors

```bash
# Fix ownership
sudo chown -R medichain:medichain /opt/medichain/asi-agents-track

# Fix .env permissions
sudo chmod 600 /opt/medichain/asi-agents-track/.env
sudo chown medichain:medichain /opt/medichain/asi-agents-track/.env
```

## Updating Application

```bash
# Stop services
sudo systemctl stop medichain-*.service

# Pull latest code
cd /opt/medichain/asi-agents-track
sudo -u medichain git pull

# Update dependencies
sudo -u medichain venv/bin/pip install -r requirements.txt --upgrade

# Reload systemd (if service files changed)
sudo systemctl daemon-reload

# Restart services
sudo systemctl start medichain-*.service
```

## Monitoring

### CPU and Memory Usage

```bash
# Check resource usage
systemctl status medichain-coordinator.service | grep "Memory\|CPU"

# Or use top/htop filtered for Python processes
ps aux | grep "python src/agents"
```

### Log Rotation

Logs are automatically managed by systemd-journald. To configure retention:

```bash
# Edit journald config
sudo nano /etc/systemd/journald.conf

# Set retention (example: 1 week)
SystemMaxUse=1G
MaxRetentionSec=1week

# Restart journald
sudo systemctl restart systemd-journald
```

## Firewall Configuration

```bash
# Allow agent ports (if using ufw)
sudo ufw allow 8000/tcp comment "MediChain Patient Intake"
sudo ufw allow 8001/tcp comment "MediChain Coordinator"
sudo ufw allow 8004/tcp comment "MediChain Symptom Analysis"
sudo ufw allow 8005/tcp comment "MediChain Treatment"

# Or restrict to specific IP (recommended)
sudo ufw allow from YOUR_IP to any port 8000:8005 proto tcp
```

## References

- [systemd Service Documentation](https://www.freedesktop.org/software/systemd/man/systemd.service.html)
- [systemd Security Options](https://www.freedesktop.org/software/systemd/man/systemd.exec.html#Security)
- [journalctl Documentation](https://www.freedesktop.org/software/systemd/man/journalctl.html)
