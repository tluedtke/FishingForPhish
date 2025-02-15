# Temporary file I used to initialize the dataset; could easily be adapted to reinitialize the dataset if needed
# For example if you want to add a new column of data or such
import os
from cs50 import SQL
import sys
from datetime import datetime

# Example usage: python databaseUpdate.py errors.txt combinedDataset.arff URLs.txt
# CREATE TABLE tempresults (id INTEGER PRIMARY KEY, classification TEXT, time INT, externalURL FLOAT, redirectURL FLOAT, hostnameMismatch BINARY, numDash INT, numEmail INT, numDots INT, FCTH18 FLOAT, FCTH24 FLOAT, FCTH25 FLOAT, FCTH42 FLOAT, FCTH43 FLOAT, 'Spatial Pyramid of Local Binary Patterns0' FLOAT, 'Spatial Pyramid of Local Binary Patterns1' FLOAT, 'Spatial Pyramid of Local Binary Patterns34' FLOAT, 'Spatial Pyramid of Local Binary Patterns36' FLOAT, 'Spatial Pyramid of Local Binary Patterns37' FLOAT, 'MPEG-7 Edge Histogram17' FLOAT, 'MPEG-7 Edge Histogram20' FLOAT, 'MPEG-7 Edge Histogram37' FLOAT, 'MPEG-7 Edge Histogram39' FLOAT, 'MPEG-7 Edge Histogram42' FLOAT, 'MPEG-7 Color Layout1' FLOAT, 'MPEG-7 Color Layout3' FLOAT, 'MPEG-7 Color Layout4' FLOAT, 'MPEG-7 Color Layout5' FLOAT, 'MPEG-7 Color Layout8' FLOAT);
### Terry ### I'm a fan of command line parsing libraries, they make documentation of the command line easier, create variables for the arguments and options, and
### Terry ### set defaults. I currently use click https://click.palletsprojects.com/en/8.0.x/
if len(sys.argv) != 4:
    print("Usage: python databaseUpdate.py relativePath:ErrorsFile relativePath:combinedDataset.arff relativePath:URLSuccesses")


# NOTE: This file assumes that combinedDatabuild.py has been run, and thus you have 3 files: 
# errors.txt (if there are errors), urls.txt (successes), and combinedDataset.arff
db = SQL("sqlite:///results.db")

# ID = db.execute("SELECT id FROM screenshots ORDER BY id DESC")
### Terry ### What are these magic numbers?
dataInitial = 33
dataSplit = 229
# urlSplit = 15
# errorSplit = 14

### Terry ### Note comment above about command line parsing. By parsing the command line into variables in one place, you don't have to edit other code if you 
### Terry ### change the command line (e.g. insert another argument, add a option) 
### Terry ###
### Terry ### Also a fan of "literate programming" where code is written to be read. Longer variable names that explain what they are versus single character 
### Terry ### variables (unless they're an obvious counter, but then we don't use numerical loops in Python much since it has powerful for statements)
### Terry ###
### Terry ### Doesn't look like you use the open files after calling readlines() on each. Better to keep with sections as short as possible.
### Terry ### with (open ...
### Terry ###    varible = readlines()
### Terry ### with (open ...

with open(sys.argv[3], "r") as r:
    with open(sys.argv[1], "r") as e:
        with open(sys.argv[2], "r") as f:
            instances = f.readlines()
            urls = r.readlines()
            errors = e.readlines()
            i = 0 ### Terry ### What is variable i ?
                  ### Terry ### After reading code below, it looks like errors from previous runs are reloaded
                  ### Terry ### Using index i, assumes that the URL list and the error list are in the same order (e.g. sorted on URL).
                  ### Terry ### Rather than assume that, you could load erros first, creating a dictionary (or set) of the errored URLs
                  ### Terry ### Then load up the URLs, checking the error dictionary as you go.
            for url in urls:
                url = url.replace('\n', '')
                errorURL, code = errors[i].split("  ")
                errorURL = errorURL.replace("\n", "")
                # https:///addons.mozilla.org/en-US/firefox/               
                print(errorURL) ### Terry ### Check out https://docs.python.org/3/howto/logging.html#logging-basic-tutorial
                if url == errorURL:
                    i += 1   
                    continue
                db.execute("INSERT INTO screenshots (url) VALUES (?)", url) ### Terry ### Using parameterized queries, that's good.
            for error in errors:
                url, code = error.split("  ") ### Terry ### Do you need to strip "\n" like you did above?
                print(url)
                # My initial split into connectionErrors versus other errors; outdated, might be changed in the future
                # As there are likely to be other errors as well, this was just for initialization
                if code != "HTML error" or code != "404":
                    db.execute("INSERT INTO errors (url, error) VALUES (?, ?)", url, code)
                else:
                    db.execute("INSERT INTO connectionErrors (userInput, error) VALUES (?, ?)", url, code)
            ### Terry ### Generally avoid indexed for loops in Python. May loop on an array slice?
            ### Terry ### for line in (instances[dataInitial, (len(instances) - dataSplit)])
            ### Terry ###     ..... = line.split(",")
            for i in range(dataInitial, len(instances) - dataSplit):
                filename, externalURL, redirectURL, hostnameMismatch, numDash, numEmail, numDots, FCTH18, FCTH24, FCTH25, FCTH42, FCTH43, Pyramid0, Pyramid1, Pyramid34, Pyramid36, Pyramid37, Edge17, Edge20, Edge37, Edge39, Edge42, Color1, Color3, Color4, Color5, Color8, classification = instances[i].split(",")
                ### Terry ### If you want a particular string format, can you use strftime() instead of parsing the string? 
                ### Terry ### Note, assuming a particular string format, if you don't explicitly specify it (e.g. str(now)) is brittle
                ### Terry ### time = datetime.now().strftime("%H:%M:%S")
                ### Terry ### https://www.w3schools.com/python/gloss_python_date_format_codes.asp
                time = str(datetime.now())
                time = time[11:19]
                hour = int(time[:2])
                meridian = time[8:]
                # Special-case '12AM' -> 0, '12PM' -> 12 (not 24)
                if (hour == 12):
                    hour = 0
                if (meridian == 'PM'):
                    hour += 12
                time = "%02d" % hour + time[2:8]
                db.execute("INSERT INTO results (classification, time, externalURL, redirectURL, hostnameMismatch, numDash, numEmail, numDots, numLinks, urlLength FCTH18, FCTH24, FCTH25, FCTH42, FCTH43, 'Spatial Pyramid of Local Binary Patterns0', 'Spatial Pyramid of Local Binary Patterns1', 'Spatial Pyramid of Local Binary Patterns34', 'Spatial Pyramid of Local Binary Patterns36', 'Spatial Pyramid of Local Binary Patterns37', 'MPEG-7 Edge Histogram17', 'MPEG-7 Edge Histogram20', 'MPEG-7 Edge Histogram37', 'MPEG-7 Edge Histogram39', 'MPEG-7 Edge Histogram42', 'MPEG-7 Color Layout1', 'MPEG-7 Color Layout3', 'MPEG-7 Color Layout4', 'MPEG-7 Color Layout5', 'MPEG-7 Color Layout8') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                classification, time, externalURL, redirectURL, hostnameMismatch, numDash, numEmail, numDots, "?", "?", FCTH18, FCTH24, FCTH25, FCTH42, FCTH43, Pyramid0, Pyramid1, Pyramid34, Pyramid36, Pyramid37, Edge17, Edge20, Edge37, Edge39, Edge42, Color1, Color3, Color4, Color5, Color8)
