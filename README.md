# WebSite Docker Assignment 5

CSC263 Software Engineering — Haigazian University

This repository packages the supplied WebSite student/course application as a Docker image. It supports adding and deleting students and courses and viewing a student's weighted grade report.

## Build and run from GitHub

Install Docker Desktop (Linux containers) and Git, then open a terminal:

```sh
git clone https://github.com/Khalil1400/website-docker-assignment.git
cd website-docker-assignment
docker compose up --build -d
```

Open **http://localhost:8001/**. No Python installation is required on your computer. The host uses port 8001 so the earlier tutorial can use port 8000 separately.

The Dockerfile uses Python 3.11 slim, installs pinned dependencies from the included wheels, copies the app, and runs as an unprivileged user. Startup applies database migrations automatically and starts Django on container port 8000. The health check verifies the home page. The dependency wheels avoid package downloads during the build; the Python base image may need to download on a new machine.

## Demonstrate the app

1. Open Docker Desktop → Images and show `website-assignment:latest`.
2. Open Containers and show the Compose `website` service running and healthy.
3. Visit the home page, then Add / Delete Students. Add ID `123`, name `Demo Student`, GPA `0`.
4. Add course `101`, semester `Fall`, credits `3`, grade `90` for that student.
5. Add course `102`, semester `Fall`, credits `1`, grade `70` for the same student.
6. Open Report Student and enter `123`. The weighted grade is `(90*3 + 70*1)/4 = 85`.
7. Stop and restart the service; the same records remain in the named Docker volume.

The supplied model stores GPA as an integer. This packaging preserves that model and its original minimal interface. The submission fixes course GPA updates, validation of positive credits, and missing-student reports so these flows can be demonstrated reliably.

## Stop and resume

```sh
docker compose stop
docker compose start
```

To remove the container while keeping saved records:

```sh
docker compose down
```

Run `docker compose up -d` to recreate it with the saved database. Avoid `down --volumes` if you want to retain records. After stopping, you may quit Docker Desktop to conserve power. Start Docker Desktop before resuming.

## Run the prebuilt image from GitHub Releases

Download `website-assignment.tar.gz` and `SHA256SUMS.txt` from this repository's **Releases** page. Verify the archive checksum, then:

```sh
docker load -i website-assignment.tar.gz
docker run -d --name website-from-github -p 127.0.0.1:8001:8000 -v website-github-data:/app/data website-assignment:latest
```

Open http://localhost:8001/. Stop another copy using port 8001 before this command. The prebuilt archive targets Linux x86-64 (typical Intel/AMD Windows PCs). Other architectures can build the source instead.

## Verification

```sh
docker compose run --rm --entrypoint python website manage.py test --verbosity 2
docker compose run --rm --entrypoint python website manage.py check
docker compose run --rm --entrypoint python website manage.py makemigrations --check --dry-run
```

The tests cover the student/course/report workflow, weighted GPA, invalid credits, unknown students, deletion/cascade behavior, and CSRF protection. The local SQLite database and accounts from the original working folder are excluded. A fresh run starts with an empty database.

This is a local coursework demonstration using Django's development server and DEBUG mode. It binds to localhost; public production hosting would require a separate deployment configuration. No Docker Hub sign-in is required.
