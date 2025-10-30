#!/bin/bash
sleep 30

# Create the database if it doesn't exist
/opt/mssql-tools18/bin/sqlcmd -S sqlserver -U sa -P "Pass@1234" -C -Q "IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'synonymdb') CREATE DATABASE synonymdb;" -b

# Create table and insert test data if it doesnt' exist
/opt/mssql-tools18/bin/sqlcmd -S sqlserver -U sa -P "Pass@1234" -C -d synonymdb -Q "
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'synonyms')
BEGIN
    CREATE TABLE synonyms (
        word_id INT PRIMARY KEY IDENTITY(1,1),
        word NVARCHAR(255) NOT NULL,
        synonyms NVARCHAR(MAX) NOT NULL
    );
    
    INSERT INTO synonyms (word, synonyms) VALUES
    ('happy', 'joyful, cheerful, content, pleased, delighted'),
    ('sad', 'unhappy, sorrowful, dejected, melancholy, gloomy'),
    ('fast', 'quick, rapid, swift, speedy, hasty'),
    ('big', 'large, huge, enormous, massive, gigantic'),
    ('small', 'tiny, little, minute, petite, compact');
END
" -b


