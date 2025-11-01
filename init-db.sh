#!/bin/bash
sleep 30

# Create the database if it doesn't exist
/opt/mssql-tools18/bin/sqlcmd -S sqlserver -U sa -P "Pass1234" -C -Q "IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'synonymdb') CREATE DATABASE synonymdb;" -b

# Create table and insert test data if it doesn't exist
/opt/mssql-tools18/bin/sqlcmd -S sqlserver -U sa -P "Pass1234" -C -d synonymdb -Q "
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
    ('small', 'tiny, little, minute, petite, compact'),
    ('smart', 'intelligent, clever, bright, brilliant, wise'),
    ('strong', 'powerful, robust, sturdy, mighty, tough'),
    ('weak', 'feeble, frail, fragile, delicate, powerless'),
    ('beautiful', 'pretty, attractive, gorgeous, lovely, stunning'),
    ('ugly', 'unattractive, hideous, unsightly, grotesque, plain'),
    ('brave', 'courageous, fearless, bold, valiant, heroic'),
    ('scared', 'afraid, frightened, terrified, anxious, alarmed'),
    ('angry', 'mad, furious, irate, enraged, livid'),
    ('calm', 'peaceful, tranquil, serene, relaxed, composed'),
    ('hot', 'warm, heated, burning, scorching, blazing'),
    ('cold', 'chilly, freezing, icy, frigid, cool'),
    ('new', 'fresh, recent, modern, novel, current'),
    ('old', 'ancient, aged, antique, elderly, worn'),
    ('easy', 'simple, effortless, straightforward, uncomplicated, basic'),
    ('difficult', 'hard, challenging, tough, demanding, complex');
END
" -b
