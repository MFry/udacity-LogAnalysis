
#Software and Data Preperation

##Download the data

Next, [download the data here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). You will need to unzip this file after downloading it. The file inside is called `newsdata.sql`. Put this file into the `vagrant` directory, which is shared with your virtual machine.

To build the reporting tool, you'll need to load the site's data into your local database. Review how to use the psql command in this lesson.

To load the data, use the command psql -d news -f newsdata.sql.
Here's what this command does:

   * `psql` — the PostgreSQL command line program
   * `-d news` — connect to the database named news which has been set up for you
   * `-f newsdata.sql` — run the SQL statements in the file newsdata.sql

Running this command will connect to your installed database server and execute the SQL commands in the downloaded file, creating tables and populating them with data.

###Getting an error?

If this command gives an error message, such as —
`psql: FATAL: database "news" does not exist`
`psql: could not connect to server: Connection refused`
— this means the database server is not running or is not set up correctly. This can happen if you have an older version of the VM configuration from before this project was added. To continue, download the virtual machine configuration into a fresh new directory and start it from there.

##Explore the data

Once you have the data loaded into your database, connect to your database using psql -d news and explore the tables using the `\dt` and `\d` table commands and select statements.

   * `\dt` — display tables — lists the tables that are available in the database.
   * `\d table` — (replace table with the name of a table) — shows the database schema for that particular table.

Get a sense for what sort of information is in each column of these tables.

The database includes three tables:

   * The `authors` table includes information about the authors of articles.
   * The `articles` table includes the articles themselves.
   * The `log` table includes one entry for each time a user has accessed the site.

As you explore the data, you may find it useful to take notes! Don't try to memorize all the columns. Instead, write down a description of the column names and what kind of values are found in those columns.
