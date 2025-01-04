# Dockerized MAGE Data Pipelines

### How to deploy
To run the container, you can simply run the `run.sh` script given on this repo. To do so, first clone the repository executing the next command:

```bash
git clone https://github.com/impoflow/mage
```

One should place oneself inside the cloned repository. Done this, we need to add the required permissions to execute the script:

```bash
chmod +x run.sh
```

Now you'll be able to run the script and start the pipelines.

### How to use

You can easily run the data pipeline by using the API already deployed by a MAGE Trigger. This API Restful has the following URL: `http://localhost:6789/api/pipeline_schedules/1/pipeline_runs/998deabc21aa46d6af8c06c51dd0a0cb`. This API offers a POST method to add projects to the Neo4j database. The following chunk shows an example of a project you can post using this method.

```json
{
  "pipeline_run": {
    "variables": {
      "user": "josejuan",
      "project_name": "feeder",
      "collaborators": ["ricardocardn", "oscarrico"]
    }
  }
}
```

This will result in a project owned by user `josejuan`, where users `ricardocardn` and `oscarrico` are collaborators.
