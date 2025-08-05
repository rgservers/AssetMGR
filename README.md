# AssetMGR
AssetMGR by RG Servers


To use AssetMGR, there are 2 ways

1. By using docker compose


```
version: '3.8'

services:
  app:
    image: rgservers/assetmgr:latest
    container_name: AssetMGR-app
    ports:
      - "9020:9020"
    depends_on:
      - mongo
    restart: unless-stopped

  mongo:
    image: mongo:6.0
    container_name: AssetMGR-DB
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db
    restart: unless-stopped
  setup:
    image: rgservers/assetmgr-setup:latest
    container_name: assetmgr-setup
    ports:
      - "9030:9030"
    depends_on:
      - mongo
    restart: unless-stopped
volumes:
  mongo-data:
```

This will create 3 docker containers. 
 - On port 9030, you will be able to create your first ever user. Make sure to delete setup segment from the compose file after that to prevent unauthorized access.
 - On port 9020, the main AssetMGR application will start. This will requier you to login
 - final container will be AssetMGR-DB, this runs mongodb which is the backend of the system

