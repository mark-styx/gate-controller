# 3-0

## To do

- [ ] 1. Create a robust logging system that stores to an exernal database
- [ ] 2. Create an application to view events and history
- [x] 3. Wrap the processes in a cleanup mode that other processes can react deal with gracefully
- [x] 4. Add event source to event object


### Logger

#### Requirements

- External Database
    - Define Schema
    - Expose to the network
    - Maintenance for large record counts (optional, probably not necessary anytime soon)
- Log Decorator Function
    - Able to wrap all other functions throughout the application
    - Flag to print to stdout or not
    - Accepts generic event information used to triage

### App History (TBD)
- Off the shelf Bokeh/Grafana maybe?
- Could just do a custom integration using a flask api
- pbi or tableau or something similar
- in the short term, a script that calls the db and returns a dataframe is probably good enough for now to see the event logs.


### Cleanup

#### Requirements

- Wrapping the main loops should be simple to implement
- Gracefully dealing with other objects
    - Within the try->except->finally should handle the exception of GPIO being undeclared.
    - Technically, the object isn't shared across the services; Only the definition is. This means that the running services shouldn't be affected directly.
        - Based on this assumption, implementing the finally statement should be sufficient.
        - A cleanup function needs to be implemented in the Mock GPIO object for testing.
        