

# Apache Iceberg Walkthrough on AWS

## Project Overview
This repository documents my hands-on experience implementing an Apache Iceberg data lake using AWS services, exploring key features and capabilities of Iceberg table format.

## Key Learning Outcomes

### 1. Infrastructure Setup
- AWS S3 Bucket for data storage
- AWS Glue Database
- Configured Athena as a query interface
- Set up necessary IAM permissions

### 2. Iceberg Metadata Insights

#### Metadata Structure
- Discovered Iceberg's metadata folder in S3
- Explored snapshot files
- Understood metadata tracking mechanism

```
s3://bucket-name/table-path/
├── metadata/
│   ├── snap-{uuid}.avro     # Snapshot metadata
│   ├── v{version}.metadata.json  # Table metadata
│   └── .previous.metadata.json  # Historical metadata
```

### 3. Table Creation and Management

#### Iceberg Table Creation
```sql
CREATE TABLE demo_iceberg_table (
    id INT,
    name STRING,
    email STRING,
    created_at TIMESTAMP
)
USING iceberg
PARTITIONED BY (created_at)
LOCATION 's3://my-bucket/iceberg-tables/demo';
```

### 4. Data Manipulation Techniques

#### Bulk Data Ingestion
```python
import pandas as pd
import awswrangler as wr

# Read CSV file
df = pd.read_csv('data.csv')

# Insert into temporary table
wr.athena.to_dataframe(
    sql="INSERT INTO temp_table SELECT * FROM pandas_dataframe",
    database='my_database'
)
```

#### Update Operations
```sql
-- Update specific rows
UPDATE demo_iceberg_table
SET email = 'new_email@example.com'
WHERE id = 123;
```

#### Delete Operations
```sql
-- Delete specific rows
DELETE FROM demo_iceberg_table
WHERE created_at < DATE '2023-01-01';
```

### 5. Time Travel Capabilities

#### Query Historical Data
```sql
-- View data as it was at a specific timestamp
SELECT * FROM demo_iceberg_table
TIMESTAMP AS OF '2023-06-14 12:00:00';

-- View data at a specific snapshot
SELECT * FROM demo_iceberg_table
VERSION AS OF 123456;
```

### 6. Performance Optimization

#### Partition Strategies
- Implemented time-based partitioning
- Improved query performance
- Reduced data scanning costs

### 7. Key Observations

#### Metadata Tracking
- Each operation creates a new snapshot
- Minimal overhead in metadata management
- Efficient tracking of table changes

### 8. Tools and Libraries Used
- AWS Glue
- Amazon Athena
- Pandas
- AWS Wrangler
- Apache Spark (optional)

## Challenges Encountered
- Initial IAM permission setup
- Understanding Iceberg metadata structure
- Configuring correct S3 permissions

## Learnings
- Immutable table format benefits
- Efficient metadata management
- Time travel and version control
- Simplified data lake operations

## Recommended Next Steps
- Implement CDC (Change Data Capture)
- Explore advanced partitioning
- Integrate with streaming sources

## References
- [Apache Iceberg Documentation](https://iceberg.apache.org/)
- [AWS Glue Catalog](https://docs.aws.amazon.com/glue/latest/dg/populate-data-catalog.html)

## License
MIT License
```

### Recommendations for Improvement
1. Add actual screenshots of your implementation
2. Include specific code snippets from your walkthrough
3. Highlight personal insights and challenges

### Potential Enhancements
- Add architecture diagram
- Include performance metrics
- Discuss specific use cases

Would you like me to modify or elaborate on any section of the README?



