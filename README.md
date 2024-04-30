## Run

docker-compose up -d --build

docker ps
docker exec -it <container_id_or_name> bash
docker-compose up tests

docker-compose down
docker-compose down -v  # This removes the containers along with their volumes
docker-compose up -d    # This recreates the containers and volumes, and starts them


docker-compose logs -f



## Bugs in the assignment

* `assignment.md` states "Once you have managed to create the tables, you can find a dump in the data folder to populate it." However, there was no code snippet to do so. Hence I defined SQL scripts to create the tables and dump the values.

* organisation_id 50 not defined:
  ```
  psql:docker-entrypoint-initdb.d/dump_scripts/bikes.sql:1395: ERROR:  insert or update on table "bikes" violates foreign key constraint "bikes_organisation_id_fkey"
  DETAIL:  Key (organisation_id)=(50) is not present in table "organisations".
  ```

## Test

Approach 1: Running Tests in the Server Container
Pros:

Simplicity: This approach leverages the existing Dockerfile, which simplifies setup. You only need to add testing dependencies and can run tests within the same container as your main application.
Consistency: Running tests in the same container ensures the environment for testing and deployment is identical, minimizing configuration discrepancies.
Efficient for Development: For quick iterations and local development, having tests run directly in the server container can streamline workflows.
Cons:

Startup Time: Running tests directly in the container might extend startup time for the main service if the tests run during the startup phase.
Environment Coupling: Combining testing and deployment environments tightly can lead to inflexibility. Any changes to the container for deployment or testing might necessitate adjustments to both.
Approach 2: Using a Separate Testing Container
Pros:

Separation of Concerns: This approach clearly separates the deployment and testing workflows, making it easier to manage and update them independently.
CI/CD Integration: A separate testing container can be more seamlessly integrated into CI/CD pipelines, allowing automated tests to run as part of the build and deployment process.
Scalability: This structure makes it easier to extend your testing suite with additional tests or environments without affecting the main deployment setup.
Cons:

Setup Complexity: This approach may require more initial setup and configuration, including creating a separate service in your docker-compose.yml and managing network access between services.
Test Environment Setup: Ensuring that the testing container has the necessary configurations and dependencies can add complexity, especially for mocking or managing database connections.