# roadmap

## Hyperbee
 - Acquire GOES-16 data using NOAA's API or data feed
 - Process raw or semi-processed data to be suitable for Hyperbee
    - Parse data
    - Clean data
    - Convert data to JSON or other suitable format
 - Stream processed data into Hyperbee
    - Create a write stream in Hyperbee
    - Write processed data into the stream
 - Retrieve data from Hyperbee using its API
    - Get value of a specific key
    - Iterate over keys
    - Perform batch operations
 - Note: specifics may vary depending on GOES-16 data feed details and application specifics
 - Note: likely need server-side language (e.g., Node.js) for data acquisition and writing to Hyperbee
 - Start by exploring GOES-16 data feed specifics
 - Explore Hyperbee's API for potential data storage use cases
 - Explore Hyperbee's API for potential data retrieval use cases
    - Explore Hyperbee's API for potential data processing use cases
    - Explore Hyperbee's API for potential data visualization use cases
