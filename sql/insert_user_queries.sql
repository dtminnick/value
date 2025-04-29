INSERT INTO user_query (query_title, query_type, query_description, query_purpose, query_string)
VALUES
	('Event Row Number Assignments by Event Date',
     'OLAP Window Function',
     'Assigns a row number for each event per initiative ordered by date.',
     'Helps track the sequence of key events in initiatives.',
     'SELECT 
		CONCAT(i.initiative_title, ": ", e.event_title) AS event,
		e.event_date,
		ROW_NUMBER() OVER (PARTITION BY e.initiative_id
						   ORDER BY e.event_date ASC) AS event_number
	  FROM
		event e
	  JOIN
		initiative i ON e.initiative_id = i.initiative_id;');
        
SELECT * FROM user_query;