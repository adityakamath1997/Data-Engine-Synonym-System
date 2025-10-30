#!/bin/bash
sleep 30
/opt/mssql-tools18/bin/sqlcmd -S sqlserver -U sa -P "Pass@1234" -C -Q "IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'synonymdb') CREATE DATABASE synonymdb;" -b

