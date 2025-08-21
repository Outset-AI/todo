# Python To-Do Web Application

1. **Run the application:**
   Start the web server with:
   ```
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   python app.py
   ```

2. **Access the application:**
   Open your web browser and navigate to `http://localhost:3000` to access the to-do list application.


# comments

1. create separate config file for environment, to store constants, config.py or a yaml file

2. set up app factory pattern

3. db should a separte module, out of app.py

4. support db migration/ update, cli tool 

5. use boolean for completed instead of integer 

6. using production grade db, like Postgres, 

7. for sharding, shard on user_id for fast read, further (add ":01"). sharding on id itself, will require gathing on read

8. conn be managed by "with", context mamanger (implement db module)

9. create validation classes for the request and content of the body

10. should be reading the newly written record, instead of creating the response; read the last row, build a response 

11. pagination, limit in get all

12. add openAPI spec for the endpoints, good reason to rewrite using FastAPI to get the endpoint spec for free

13. seperation handling logic of differnt http methods 

14. add proper index based on accessing pattern 

15. if QPS is too high for the db, option1, shard the db option2 batching the db writes, to avoid losses, delivery batch write into message queue; for read use cache, key value redis, lru 

16. add more tests

17.  validation on title size, the content check

18. framework on front end tests

19. add logging, exception tracking, type hinting 