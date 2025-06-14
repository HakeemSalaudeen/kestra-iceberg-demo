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
CREATE TABLE fruits (
    id bigint,
    fruit string,
    berry boolean,
    update_timestamp timestamp
)
    PARTITIONED BY (berry)
LOCATION 's3://kestra-iceberg-demo/fruits/' 
TBLPROPERTIES ('table_type'='ICEBERG');
```

### 4. Data Manipulation Techniques

#### Bulk Data Ingestion
- [Bulk Data Ingestion](https://github.com/HakeemSalaudeen/kestra-iceberg-demo/blob/d63fd042d4a7784e0e67346fae69975df3de4d9a/kestra-iceberg-demo.py)


#### Update Operations
```sql
-- Update specific rows
UPDATE fruits 
SET fruit = 'Bilberry' 
WHERE fruit = 'Blueberry';
```

#### Delete Operations
```sql
-- Delete specific rows
DELETE FROM fruits 
WHERE fruit = 'Banana';
```

### 5. Time Travel Capabilities

#### Query Historical Data
```sql
-- View data as it was at a specific timestamp
SELECT * 
FROM fruits 
FOR TIMESTAMP AS OF (current_timestamp - interval '50' minute) 
WHERE berry = true;

-- View data at a specific snapshot
SELECT * 
FROM fruits 
FOR VERSION AS OF 4111858955684891680;
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

## Learnings
- Immutable table format benefits
- Efficient metadata management
- Time travel and version control
- Simplified data lake operations

## References
- [Kestra Iceberg Guide](https://kestra.io/blogs/2023-08-05-iceberg-for-aws-users)
- [Apache Iceberg Documentation](https://iceberg.apache.org/)
- [AWS Glue Catalog](https://docs.aws.amazon.com/glue/latest/dg/populate-data-catalog.html)




