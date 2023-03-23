# NBA_pipeline01

![nba_project_pic](https://user-images.githubusercontent.com/105791967/219845142-339ded9c-fd49-4cfe-a0e9-7247c0d00499.jpg)

This project scraped data from https://www.basketball-reference.com stored in database and ELT to do transformation in Databricks save it as a delta table to make some prediction.

## Step to run this project
1. run 	`code`docker-compose -f db.yml to first build Postgres database
2. run 	`code`docker-compose up -d
