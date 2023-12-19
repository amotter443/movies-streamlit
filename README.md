# movies-streamlit
>Creating a Streamlit single-paged app version of my Letterboxd personal data analysis project

In 2021 I set out on a project to leverage my movie data on Letterboxd to perform analytics and gather insights. Each year since I have slightly modified or expanded on the code base, and 2023 was no exception. If you're interested in more information about the initial project and its methodology, please check out my [LinkedIn article](https://www.linkedin.com/pulse/how-i-used-machine-learning-quantify-my-movie-obsession-alex-motter) and its [follow-up](https://www.linkedin.com/pulse/using-personal-analytics-determine-my-most-watched-actors-alex-motter/) expanding the credits on the film.

The first iteration of the project displayed the final result of the scripts in a PowerBI dashboard. With Streamlit's acquisition by Snowflake and its overall ease of web deployment, I built this repo in order to enable a Streamlit version of the results page


Project Execution Steps
------------------------
- Complete all the required steps/code execution in [previous movie repo](https://github.com/amotter443/movies)
- Register for a free MongoDB Atlas account
- Create a MongoDB cluster and a 'letterboxd' database
- In the Network Access section of MongoDB, allow 0.0.0 for credential-based web access
- Execute the `mongodb_create.py` to write user data to MongoDB via PyMongo
- Modify and configure `web_movie_viz.py` (Change the title to your name, add in any date modifications based on when you joined Letterboxd, etc.)
- Embed username, pwd, and cluster name to secrets.toml file in Streamlit
- Deploy Streamlit page to prod


Helpful Resources
--------
- [Setting up a MongoDB Cluster/Database](https://www.mongodb.com/basics/create-database)
- [PyMongo Starter Guide](https://www.w3schools.com/python/python_mongodb_getstarted.asp) 
- [Streamlit MongoDB Integration ](https://docs.streamlit.io/knowledge-base/tutorials/databases/mongodb)
