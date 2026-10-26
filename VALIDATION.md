# Assignment validation

Verified locally on 26 October 2026 using Docker Desktop with Linux containers.

- Docker image built successfully from the repository Dockerfile.
- All 9 Django tests passed inside the image.
- Django system check reported no issues.
- Migration consistency check reported no changes detected.
- Home, student entry, course entry, and student report pages returned HTTP 200.
- A real HTTP workflow with CSRF protection created a synthetic student and two courses, and the report returned the expected weighted grade of 85.
- The container passed its health check.
- After `docker compose down` followed by `docker compose up -d`, the same student and grade report were still present in the named volume.

The demo records use ID 123 and the name Demo Student. They live only in the local Docker volume and are not baked into the image or source repository.

Prebuilt Linux amd64 image config ID:

```text
sha256:2deff1c160be498703cbbef7ccf7f363e15d25fb8cd66519aae33335f2f0d96e
```

The archive checksum is supplied separately in `SHA256SUMS.txt` alongside the image download.
