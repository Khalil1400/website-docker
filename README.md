# WebSite

A Django app for managing students, courses, and grade reports.

## Run with Docker

Start Docker Desktop, then run:

```sh
git clone https://github.com/Khalil1400/website-docker.git
cd website-docker
docker compose up --build -d
```

Open **http://localhost:8001/**.

On Windows, you can also double-click `START-WEBSITE.cmd` after downloading the project.

## Stop and start again

```sh
docker compose stop
docker compose start
```

Your records are saved between runs. On Windows, `STOP-WEBSITE.cmd` stops the app.

## Use the ready-made image

Download `website-assignment.tar.gz` from [Releases](https://github.com/Khalil1400/website-docker/releases/latest), then run:

```sh
docker load -i website-assignment.tar.gz
docker run -d --name website -p 127.0.0.1:8001:8000 -v website-data:/app/data website-assignment:latest
```

Use either Docker Compose or the ready-made image so only one copy uses port 8001. The image is for Linux Intel/AMD computers running Docker.
