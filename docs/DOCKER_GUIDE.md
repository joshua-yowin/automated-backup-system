# Docker Guide

This guide provides instructions for building, running, and managing the Automated Backup System using Docker.

## 1. Build Docker Image

To build the Docker image for the backup system, navigate to the root of your project and run the following command:

```bash
docker build -t backup-system:dev -f docker/Dockerfile .
```

-   `-t backup-system:dev`: Tags the image with the name `backup-system` and version `dev`.
-   `-f docker/Dockerfile`: Specifies the Dockerfile to use, located in the `docker/` directory.
-   `.`: Indicates that the build context is the current directory (the project root).

## 2. Run Locally (Single Container)

You can run the backup system in a single Docker container for local testing. This command mounts the `data/` and `backups/` directories from your host machine into the container, allowing data persistence and access to sample data.

```bash
docker run -it --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/backups:/app/backups \
  backup-system:dev
```

-   `-it`: Runs the container in interactive mode with a pseudo-TTY.
-   `--rm`: Automatically removes the container when it exits.
-   `-v $(pwd)/data:/app/data`: Mounts the host's `data` directory to `/app/data` in the container.
-   `-v $(pwd)/backups:/app/backups`: Mounts the host's `backups` directory to `/app/backups` in the container.
-   `backup-system:dev`: The name and tag of the Docker image to run.

## 3. Test Backup Inside Container

To test the backup functionality within a running container, you need to get the container ID and then execute the backup script inside it:

1.  **Get Container ID:** First, find the ID of your running `backup-system:dev` container:

    ```bash
docker ps
    ```

    Look for the container running the `backup-system:dev` image.

2.  **Execute Backup Script:** Replace `<container-id>` with the actual ID of your container:

    ```bash
docker exec -it <container-id> python3 app/backup.py
    ```

    This will run the `backup.py` script, creating a backup within the container's mounted `backups` directory.

## 4. Verify Backup Files

After running the backup, you can verify that the backup files were created on your host machine in the `backups/` directory:

```bash
ls -lh backups/
```

## 5. Docker Compose for Complete Stack

For a more comprehensive local testing environment, use `docker-compose` to orchestrate multiple services (backup service, scheduler, web dashboard, Jenkins, Prometheus).

To start the entire stack:

```bash
docker-compose up -d
```

-   `-d`: Runs the containers in detached mode (in the background).

## 6. Verify All Services

Check the status of all services defined in your `docker-compose.yml`:

```bash
docker-compose ps
```

This command will list all running containers managed by `docker-compose` and their status.

## 7. Test Backup Service (Docker Compose)

Execute the backup script within the `backup-service` container managed by Docker Compose:

```bash
docker-compose exec backup-service python3 app/backup.py
```

## 8. View Scheduler Logs

Monitor the automated backup scheduler's logs:

```bash
docker-compose logs -f backup-scheduler
```

This will show real-time logs from the `backup-scheduler` service, indicating when backups are being triggered.

## 9. Access Web Dashboard

If your `web-dashboard` service is running and exposing port 5000, you can access its health endpoint:

```bash
curl http://localhost:5000/health
```

## 10. Scale Backup Services

Demonstrate scaling of your backup services using Docker Compose:

```bash
docker-compose up --scale backup-service=3 -d
```

This command will scale the `backup-service` to run 3 instances in parallel.

```