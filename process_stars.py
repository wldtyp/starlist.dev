import json
import sqlite3
from pathlib import Path
from contextlib import contextmanager

@contextmanager
def database():
    con = sqlite3.connect('stars.db')
    cur = con.cursor()
    try:
        yield cur
    finally:
        con.commit()
        con.close()


with database() as db:
    db.execute("CREATE TABLE IF NOT EXISTS repositories (id integer primary key, full_name text, description text, language text)")
    db.execute("CREATE TABLE IF NOT EXISTS stats (day date, repository_id integer, stars integer, forks integer, PRIMARY KEY ( day, repository_id))")


with database() as db:
    pathlist = Path('./').glob('*.json')
    for path in pathlist:
        with open(path) as f:
            search_results = json.load(f)
            for result in search_results['items']:
                insert_query = "insert or replace into repositories (id, full_name, description, language) values (?,?,?,?)"
                db.execute(insert_query, (result['id'], result['full_name'], result['description'], result['language']))
            
            for result in search_results['items']:
                db.execute("insert or replace into stats values (DATE('now'),?,?,?)", (result['id'], result['stargazers_count'], result['forks']))


with database() as db:
    with open('table.md', 'w') as f:
        result = db.execute("Select stars, forks, language, full_name, description from stats join repositories on stats.repository_id = repositories.id where stats.day = DATE('now') order by stats.stars desc")
        c = 1
        f.write('''
| Number | Stars | Forks | Language| Name  | Description |
| :---   | :---: | :---: | :---    | :---  | :---        |
''')
        for row in result:
            stars, forks, language, full_name, description = (map(str,row))
            description = description.replace('|','')[:500]
            line = f"| {c} | {stars} | {forks} | {language} | {full_name} | {description} | \n" 
            f.write(line)
            c += 1

