Flask_Template


Configuration Notes


    a) Go to the config file and insert in the link to the fresh database via AWS
    b) Run the app once to set up the initial database
    c) stop the app
    d) Run the migrations for the first time
            d1) flask db init
            d2) flask db migrate
            d3) flask db upgrade



.config file -> currently setup, gets the information for the postgresql db

flask_monitoringdashboard.db -> is created by the flask monitoring dashboard extension

/dashboard -> this is for flask monitoring dashboard of the API endpoints, how often they are being hit

/migrations folder --> this is created when run the flask db init //
            this should be done:
                    1) CD into folder
                    2) flask db init
                    3) flask db migrate
                    4) flask db upgrade

            > each time the database models change repeat the migrate and upgrade commands.