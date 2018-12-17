# Log Analytics of News Website

import psycopg2
import bleach


DBNAME = "news"


# What are the most popular three articles of all time? Which articles
# have been accessed the most? Present this information as a sorted list
# with the most popular article at the top."""
def get_most_popular_articles():

    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    sql = '''
        SELECT
          substring(path, 10, length(path)) article,
          COUNT(1) view_cnt
        FROM log
        WHERE path != '/'
        GROUP BY
          article
        ORDER BY view_cnt DESC
        LIMIT 3
      ;
    '''
    c.execute(sql)
    data = c.fetchall()
    db.close()

    print("1. What are the most popular three articles of all time?")
    for article, view_cnt in data:
        print "\"{}\" - {:,.0f}".format(article, view_cnt)

"""Who are the most popular article authors of all time? That is, 
when you sum up all of the articles each author has written, 
which authors get the most page views? Present this as a sorted 
list with the most popular author at the top."""
def get_most_popular_authors():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    sql = '''
        SELECT 
	  	    authors.name author,
		    COUNT(1) view_cnt
		FROM log 
			LEFT JOIN articles art ON art.slug = substring(path, 10, length(log.path))
			LEFT JOIN authors ON authors.id = art.author
		GROUP BY 
			authors.name
		ORDER BY view_cnt DESC
		LIMIT 5
		;
    '''
    c.execute(sql)
    data = c.fetchall()
    db.close()

    print("2. Who are the most popular article authors of all time?")
    for author, view_cnt in data:    
		print "\"{}\" - {:,.0f}".format(author, view_cnt)

def get_days_with_more_than_one_percent_errors():
  """Who are the most popular article authors of all time? That is, when you 
  sum up all of the articles each author has written, which authors get the most
   page views? Present this as a sorted list with the most popular author at the top."""
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  sql = '''
	SELECT
		DATE(log.time) AS date_day,
		SUM(CASE WHEN log.status <> '200 OK' THEN 1 ELSE 0 END) error_cnt,
		COUNT(1) view_cnt,
		SUM(CASE WHEN log.status <> '200 OK' THEN 1 ELSE 0 END)*100::decimal/COUNT(1) as per_error
	FROM log 
		LEFT JOIN articles ON articles.slug = substring(path, 10, length(log.path))
		LEFT JOIN authors ON authors.id = articles.author
	WHERE path != '/'
	GROUP BY 
		DATE(log.time)
	HAVING SUM(CASE WHEN log.status <> '200 OK' THEN 1 ELSE 0 END)*100::decimal/COUNT(1) >= 1
	ORDER BY view_cnt DESC
	;
  '''
  c.execute(sql)
  data = c.fetchall()
  db.close()

  print("3. On which days did more than 1% of requests lead to errors?")
  for date_day, error_cnt, view_cnt, per_error in data:
    print "{} - {:.2f}% errors".format(date_day.strftime("%B %d, %Y"), per_error)


if __name__ == '__main__':
  get_most_popular_articles()
  get_most_popular_authors()
  get_days_with_more_than_one_percent_errors()

