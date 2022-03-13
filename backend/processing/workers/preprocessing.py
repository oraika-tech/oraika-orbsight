# Input workflow id
# Get state data
State (last record processed),
# Fetch records from DB based on workflow
# Extract, Emojis, URL, Currency, Hashtags
# Clean text (remove hashtags, url, replace emojis with text, remove unwanted space etc)
# Detect language if non-english then translate to english
# Call Analyzer API
# Store data back to DB
# Update state data


# Fetch data from (Twitter, Apps) -> Raw Data / SQS

# SQS (Text, Ids) -> Find categories -> Preprocess and Process -> Processed data db
