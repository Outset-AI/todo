# Clojure To-Do Web Application

1. **Run the application:**
   Start the web server with:
   ```
   lein run
   ```

2. **Access the application:**
   Open your web browser and navigate to `http://localhost:3000` to access the to-do list application.

3. **Roadmap**
- Add full error handling for unexpected exceptions
- Add parse helper based on incoming spec map, coercion helper fns
- Finish refactoring keyword usage, error handling helpers
- Improve cache middleware applicability
- Break out SQL handling fns into separate ns
- Break out routing sub-sections into other nses as needed
- Minor code style changes
   * Rewrapping lines and SQL formatting
   * Reducing :handler redundancy
