-- This script creates an Iceberg table in Athena, inserts data, performs updates, deletes, and queries.
CREATE TABLE fruits (
    id bigint,
    fruit string,
    berry boolean,
    update_timestamp timestamp
)
    PARTITIONED BY (berry)
LOCATION 's3://kestra-iceberg-demo/fruits/' -- adjust to your S3 bucket name
TBLPROPERTIES ('table_type'='ICEBERG');


-- Create a raw data table for upsert operations
INSERT INTO fruits (id, fruit, berry) 
    VALUES (1,'Apple', false), 
           (2, 'Banana', false), 
           (3, 'Orange', false), 
           (4, 'Blueberry', true), 
           (5, 'Raspberry', true), 
           (6, 'Pear', false);
           
-- Insert more data into the fruits table          
           INSERT INTO fruits (id, fruit, berry) 
    VALUES (7,'Mango', false), 
           (8, 'Strawberry', true), 
           (9, 'Kiwi', false), 
           (10, 'Cranberry', true);
           


-- Query the fruits table
select * from fruits order by berry;


-- Update and delete operations
UPDATE fruits 
SET fruit = 'Bilberry' 
WHERE fruit = 'Blueberry';

DELETE FROM fruits 
WHERE fruit = 'Banana';

SELECT * 
FROM fruits 
ORDER BY berry;

-- Query the history of the table
SELECT * 
FROM "fruits$history";

-- Query the current snapshot of the table
SELECT snapshot_id, summary 
FROM "fruits$snapshots";

-- Query the current version of the table
SELECT * 
FROM fruits 
FOR VERSION AS OF 4111858955684891680;

-- Query the table as of a specific timestamp
SELECT * 
FROM fruits 
FOR TIMESTAMP AS OF (current_timestamp - interval '50' minute) 
WHERE berry = true;

-- Create a raw data table for upsert operations
SELECT * 
FROM raw_fruits;

---- upsert
-- Create a raw data table for upsert operations
MERGE INTO fruits f USING raw_fruits r
    ON f.fruit = r.fruit
    WHEN MATCHED
        THEN UPDATE
            SET id = r.id, berry = r.berry, update_timestamp = current_timestamp
    WHEN NOT MATCHED
        THEN INSERT (id, fruit, berry, update_timestamp)
              VALUES(r.id, r.fruit, r.berry, current_timestamp);
              
-- Query the updated fruits table              
SELECT * 
FROM fruits 
WHERE fruit LIKE 'B%';

-- Query the files associated with the fruits table
SELECT * 
FROM "fruits$files";

--  Query the record count and file path of the fruits table
SELECT record_count, file_path 
FROM "fruits$files";

-- Optimize the table to compact small files into larger ones
OPTIMIZE fruits REWRITE DATA USING BIN_PACK;

-- Vacuum the table to remove obsolete files
VACUUM fruits;