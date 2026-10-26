# Validation

Verified locally on 26 October 2026 using Docker Desktop with Linux containers.

- Docker image built successfully from the repository Dockerfile.
- All 9 Django tests passed inside the image.
- Django system check reported no issues.
- Migration consistency check reported no changes detected.
- Home, student entry, course entry, and student report pages returned HTTP 200.
- A real HTTP workflow with CSRF protection created a synthetic student and two courses, and the report returned the expected weighted grade of 85.
- The container passed its health check.
- After `docker compose down` followed by `docker compose up -d`, the same student and grade report were still present in the named volume.
- Cloned this repository from GitHub, built a fresh image from that clone, started it, and verified all four app pages returned HTTP 200.
- Downloaded the published prebuilt image archive back from GitHub Releases, verified its SHA-256 checksum, loaded and ran it, and verified all four app pages returned HTTP 200.

The demo records use ID 123 and the name Demo Student. They live only in the local Docker volume and are not baked into the image or source repository.

Prebuilt Linux amd64 local image ID:

```text
sha256:9ce5ff94f51441e88de38ed1e6a22e7e3f3ad865a30a51d1044fa071f2ca747c
```

The archive checksum is supplied separately in `SHA256SUMS.txt` alongside the image download.

