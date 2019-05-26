# Given linkedin user data. We need to parse their profiles.

## Data Description:
- ein: ein code of organization where that user worked/works
- city: city where that company is/were located
- state: USA state code for that location
- organization: name of that organization
- business_name: business name of that organization (these two names mostly are the same. Search for DBA, AKA for more information)
- person_name: full name of the person
- title: job title of the person

## Parsing Recommendations:
- we need to search LinkedIn profiles if it exist for that users.
- using ask.com website for searching is recommended (google is detecting the scrapers better)
- LinkedIn parsing isn't easy. If you crete usual fake profile and start parsing of 100s of data you will be 
immediately blocked. Usually it blocks after parsing 20-30 records.

## What to parse:
- user name: full name of user
- experience: working experience (Where he/she worked)
- position: current position or job title (CTO, CEO, Senior Engineer, etc)
- companies: list of companies where he/she worked at

## Functionality:
- it should support multiple LinkedIn connections and parsing in parallel. You will create several fake users and use their credentials to log in, then parse records in parallel. It will make it possible to overcome daily parsing limit.
- it should take that file as an input, user credentials list from json file as an configuration, initialise parsers and parse data.
- it should store results in MongoDB indexed with LinkedinUrls.