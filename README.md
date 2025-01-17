# Dockerized MAGE Data Pipelines

## How to Deploy

To run the container, clone the repository by executing the following command:

```bash
git clone https://github.com/impoflow/mage
```

Once the repository is cloned, navigate into the directory:

```bash
cd mage
```

Build the Docker image using the following command:

```bash
docker build -t mage-pipeline .
```

After the image is built, you can run the container with:
a
```bash
docker run -p 6789:6789 mage-pipeline
```

This will start the container and expose the API on port `6789`.

## How to Use

### Pre-requisite: AWS S3 Bucket

This pipeline requires an AWS S3 bucket where you upload a zip file. This zip file is critical for triggering the pipeline.

### Accessing the API

The Mage Trigger API is exposed at:

```
http://localhost:6789/api/pipeline_schedules/1/pipeline_runs/s3PutTrigger
```

This API is a RESTful endpoint that supports `POST` requests to trigger the data pipeline.

### JSON Payload Strucutre

Here’s an example payload for running the pipeline:

```json
{
  "pipeline_run": {
    "variables": {
      "user": "josejuan",
      "bucket_name": "TSCD",
      "project_name": "feeder",
      "collaborators": ["ricardocardn", "oscarrico"]
    }
  }
}
```

#### Explanation of the Fields:

- `user`: The owner of the project (e.g., `josejuan`).
- `bucket_name`: The AWS S3 bucket where the zip file is stored (e.g., `TSCD`).
- `project_name`: The name of the project being added (e.g., `feeder`). _# Note: the project_name must mach with the zip filename._
- `collaborators`: A list of collaborators for the project.

When this payload is sent, the system uses the provided details to create a project in the Neo4j database.

## Example Request with cURL

To post the example project using `curl`, run the following command:

```bash
curl -X POST \
  http://localhost:6789/api/pipeline_schedules/1/pipeline_runs/998deabc21aa46d6af8c06c51dd0a0cb \
  -H "Content-Type: application/json" \
  -d '{
    "pipeline_run": {
      "variables": {
        "user": "josejuan",
        "bucket_name": "TSCD",
        "project_name": "feeder",
        "collaborators": ["ricardocardn", "oscarrico"]
      }
    }
  }'
```
