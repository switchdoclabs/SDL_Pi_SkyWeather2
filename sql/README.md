# Database upgrade scripts

- uses [flyway](https://flywaydb.org/documentation/usage/commandline/") to manage db versioning
    - assumes you installed it and is on the path
- use flyway.sh to run migrations
    - currently assumes localhost
    - use migrate as the argument
    - DO NOT USE clean if you don't want to loose all your data
- use local docker container for testing

# existing users
- seed database with patch.sql script to add version information