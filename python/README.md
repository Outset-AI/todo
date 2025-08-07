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


- Switch to an ORM, sqlalcehmy. Also handles migrations 
- Add a helper script to create a new db instance instead of in get_db
- split routes into seperate functions per request method
- Use pydantic for post params. Will allow for better data validation and serializeation
- Add a file for the db models
- Add a file for all the db operations
- Add a file for the pydantic models
- created_at should be an int not a string date
- instead of returning a dict, can probably return a serialized version of the added sqlalchemy model
- get function is wrapping dict around the row object, sqlalchemy fixes this, consider having a pydantic model for the return object
- get endpoint should take in limit/offset params for large batches. Instead of returning a list, return a dict with the list as a value as well as stats such as current limit and offset or maybe a pointer for next
- Don't want to bubble up db errors to the frontend, might reveal information. Wrap all the calls the the new db fn file with try/except blocks with more human readable but generic error messages
-Add an index to created_at because we're sorting on it
-Completed should be renamed status or something so it can be a enum. Define an enum class in the pydantic file with current values
-Instead of deleting entries, maybe just use a deleted enum value and filter those out in the get
- Patch and Delete endpoints should be merged into a single status update endpoint
- Either use openapi or write an api spec to share with FE/Design
- Write unit tests!1!!!!!!!