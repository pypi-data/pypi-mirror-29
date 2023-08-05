# python-event-bridge

## for run nats server(ubuntu)
1. Get nats project server
```bash
wget https://github.com/nats-io/gnatsd/releases/download/v0.9.4/gnatsd-v0.9.4-linux-amd64.zip
```
sudo apt-get install -y unzip
unzip -p gnatsd-v0.9.4-linux-amd64.zip gnatsd-v0.9.4-linux-amd64/gnatsd > gnatsd
chmod +x gnatsd
./gnatsd --addr 0.0.0.0 --port 4222
