/*

Name:			create_value_database.sql

Description:	This script creates the value database as well as indexes,
				triggers, stored procedures, functions and views.
                
Contents:		Comments with numbers provide quick search; each number corresponds to a labeled
                section below.

				Section 1. Includes CREATE TABLE and CREATE INDEX statements for each
						   table in the database.
			    
                Section 2. Includes triggers.
                
                Section 3. Includes functions.
                
                Section 4. Includes stored procedures.

				Section 5. Includes temporary tables.
                
                Section 6. Includes views.
				
Modifications:	2025-03-08 - Added and tested CREATE TABLE queries.
				2025-03-09 - Added indexes, triggers, functions, stored procedures, temporary tables, 
		                     and views.
			    2025-04-02 - Added user_query table to Section 1 to store details of pre-defined and 
                             custom user queries.
			    2025-04-05 - Added tooltip table to Section 1 to store tooltips for GUI application.
                2025-04-17 - Added form_configuration table for UI form generation.
                2025-04-21 - Added collection_frequency table.

*/

/*

Section 1 - Create tables and indexes.

*/

CREATE TABLE initiative (
    initiative_id INT AUTO_INCREMENT PRIMARY KEY,
    initiative_title VARCHAR(100) NOT NULL,
    initiative_description TEXT NOT NULL,
    initiative_owner VARCHAR(50) NOT NULL,
    start_date DATE,
    end_date DATE
);

CREATE TABLE event (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    event_title VARCHAR(100) NOT NULL,
    event_description TEXT NOT NULL,
    event_date DATE NOT NULL,
    activation_id INT
);

CREATE INDEX idx_event_date ON event(event_date);

CREATE TABLE collection_frequency (
	collection_id INT AUTO_INCREMENT PRIMARY KEY,
    collection_type VARCHAR(30) NOT NULL
);

INSERT INTO collection_frequency (collection_type)
	VALUES
		("Weekly"),
        ("Monthly");

CREATE TABLE initiative_event (
    initiative_id INT,
    event_id INT,
    impact_summary TEXT,
    PRIMARY KEY (initiative_id, event_id),
    FOREIGN KEY (initiative_id) REFERENCES initiative(initiative_id),
    FOREIGN KEY (event_id) REFERENCES event(event_id)
);

CREATE TABLE plan (
    plan_id INT PRIMARY KEY,
    plan_name VARCHAR(255) NOT NULL
);

CREATE TABLE event_plan (
    event_id INT,
    plan_id INT,
    PRIMARY KEY (event_id, plan_id),
    FOREIGN KEY (event_id) REFERENCES event(event_id),
    FOREIGN KEY (plan_id) REFERENCES plan(plan_id)
);

CREATE TABLE metric (
    metric_id INT AUTO_INCREMENT PRIMARY KEY,
    initiative_id INT,
    metric_name VARCHAR(100) NOT NULL,
    metric_definition TEXT NOT NULL,
    is_plan_level BOOLEAN,
    collection_frequency ENUM('Weekly', 'Monthly') NOT NULL,
    FOREIGN KEY (initiative_id) REFERENCES initiative(initiative_id)
);

CREATE INDEX idx_initiative_id ON metric(initiative_id);

CREATE INDEX idx_is_plan_level ON metric(is_plan_level);

CREATE INDEX idx_collection_frequency ON metric(collection_frequency);

CREATE TABLE global_metric_value (
    global_value_id INT AUTO_INCREMENT PRIMARY KEY,
    metric_id INT,
    metric_date DATE NOT NULL,
    actual_value DECIMAL(10,2) NOT NULL,
    week_start DATE GENERATED ALWAYS AS (DATE_SUB(metric_date, INTERVAL WEEKDAY(metric_date) DAY)) STORED,
    month_start DATE GENERATED ALWAYS AS (DATE_FORMAT(metric_date, '%Y-%m-01')) STORED,
    FOREIGN KEY (metric_id) REFERENCES metric(metric_id)
);

CREATE INDEX idx_metric_id ON global_metric_value(metric_id);

CREATE INDEX idx_week_start ON global_metric_value(week_start);

CREATE INDEX idx_month_start ON global_metric_value(month_start);

CREATE TABLE plan_metric_value (
    plan_value_id INT AUTO_INCREMENT PRIMARY KEY,
    metric_id INT,
    plan_id INT,
    metric_date DATE NOT NULL,
    actual_value DECIMAL(10,2) NOT NULL,
    week_start DATE GENERATED ALWAYS AS (DATE_SUB(metric_date, INTERVAL WEEKDAY(metric_date) DAY)) STORED,
    month_start DATE GENERATED ALWAYS AS (DATE_FORMAT(metric_date, '%Y-%m-01')) STORED,
    FOREIGN KEY (metric_id) REFERENCES metric(metric_id),
    FOREIGN KEY (plan_id) REFERENCES plan(plan_id)
);

CREATE INDEX idx_metric_id ON plan_metric_value(metric_id);

CREATE INDEX idx_plan_id ON plan_metric_value(plan_id);

CREATE INDEX idx_week_start ON plan_metric_value(week_start);

CREATE INDEX idx_month_start ON plan_metric_value(month_start);

CREATE TABLE user_query (
	query_id INT AUTO_INCREMENT PRIMARY KEY,
	query_title VARCHAR(100) NOT NULL,
    query_description TEXT NOT NULL,
    query_purpose TEXT NOT NULL,
    query_string TEXT NOT NULL,
	set_operation BOOLEAN DEFAULT 0,
    set_membership BOOLEAN DEFAULT 0,
    set_comparison BOOLEAN DEFAULT 0,
    subquery BOOLEAN DEFAULT 0,
    cte BOOLEAN DEFAULT 0,
    aggregate_function BOOLEAN DEFAULT 0,
    window_function BOOLEAN DEFAULT 0,
    olap BOOLEAN DEFAULT 0
);

CREATE TABLE tooltip (
	widget_id VARCHAR(200) PRIMARY KEY,
    tooltip_text TEXT NOT NULL
);

CREATE TABLE form_config (
	id INT AUTO_INCREMENT PRIMARY KEY,
    form_name VARCHAR(100),
    frame_name VARCHAR(50),
    command_name VARCHAR(50),
    field_name VARCHAR(100),
    widget_text VARCHAR(100),
    widget_type VARCHAR(50),
    required BOOLEAN,
    lookup_table VARCHAR(100),
    lookup_id_col VARCHAR(100),
    lookup_display_col VARCHAR(100),
    row_pos INT,
    col_pos INT,
    field_order INT,
    source_table VARCHAR(50),
    joins VARCHAR(200),
	tab_order INT,
	tab_display_name VARCHAR(50),
    treeview_columns TEXT
);

/*

Section 2 - Create triggers to ensure global_metric_value and plan_metric_value
            tables store zero or positive values in the actual_value attribute.

*/

DELIMITER //
CREATE TRIGGER validate_global_metric_value
	BEFORE INSERT ON global_metric_value
	FOR EACH ROW
	BEGIN
	  IF NEW.actual_value < 0 THEN
		SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Metric values cannot be negative.';
	  END IF;
	END;
DELIMITER ;
    
DELIMITER //
CREATE TRIGGER validate_plan_metric_value
	BEFORE INSERT ON plan_metric_value
	FOR EACH ROW
	BEGIN
	  IF NEW.actual_value < 0 THEN
		SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Metric values cannot be negative.';
	  END IF;
	END;
DELIMITER ;

/*

Section 3 - Create functions.

*/

-- Use end_date attribute to return initiative time remaining to planned completion.

DELIMITER //
	CREATE FUNCTION time_remaining(initiativeID INT) RETURNS INT
	DETERMINISTIC
	BEGIN
	  DECLARE days_left INT;
	  SELECT DATEDIFF(end_date, CURDATE()) INTO days_left
	  FROM initiative WHERE initiative_id = initiativeID;
	  RETURN IFNULL(days_left, 0);
	END;
DELIMITER ;

-- Use metric_id attribute to get the most recent global metric value.

DELIMITER //
	CREATE FUNCTION latest_glocal_metric_value(metricID INT) RETURNS DECIMAL(10,2)
	DETERMINISTIC
	BEGIN
	  DECLARE latest_value DECIMAL(10,2);
	  SELECT actual_value INTO latest_value
	  FROM global_metric_value
	  WHERE metric_id = metricID
	  ORDER BY metric_date DESC
	  LIMIT 1;
	  RETURN latest_value;
	END;
DELIMITER ;

-- Use metric_id attribute to get the most recent plan metric value.

DELIMITER //
	CREATE FUNCTION latest_plan_metric_value(metricID INT) RETURNS DECIMAL(10,2)
	DETERMINISTIC
	BEGIN
	  DECLARE latest_value DECIMAL(10,2);
	  SELECT actual_value INTO latest_value
	  FROM plan_metric_value
	  WHERE metric_id = metricID
	  ORDER BY metric_date DESC
	  LIMIT 1;
	  RETURN latest_value;
	END;
DELIMITER ;

/*

Section 4 - Create stored procedures

*/

-- Retrieve global metrics for a given initiative.

DELIMITER //
	CREATE PROCEDURE get_global_initiative_metrics(IN initiativeID INT)
	BEGIN
	  SELECT m.metric_name, g.metric_date, g.actual_value
	  FROM metric m
	  JOIN global_metric_value g ON m.metric_id = g.metric_id
	  WHERE m.initiative_id = initiativeID;
	END;
DELIMITER ;

-- Retrieve plan metrics for a given initiative.

DELIMITER //
	CREATE PROCEDURE get_plan_initiative_metrics(IN initiativeID INT)
	BEGIN
	  SELECT m.metric_name, g.metric_date, g.actual_value
	  FROM metric m
	  JOIN plan_metric_value g ON m.metric_id = g.metric_id
	  WHERE m.initiative_id = initiativeID;
	END;
DELIMITER ;

-- Insert a new event and link it to an initiative.

DELIMITER //
	CREATE PROCEDURE add_event(IN e_title VARCHAR(255), IN e_desc TEXT, IN e_date DATE, IN initiativeID INT)
	BEGIN
	  DECLARE new_event_id INT;
	  INSERT INTO event (event_title, event_description, event_date) VALUES (e_title, e_desc, e_date);
	  SET new_event_id = LAST_INSERT_ID();
	  INSERT INTO initiative_event (initiative_id, event_id) VALUES (initiativeID, new_event_id);
	END;
DELIMITER ;

/*

Section 5 - Create temporary tables

*/

-- Create temporary table to store monthly average metrics

CREATE TEMPORARY TABLE temp_avg_metrics (
    metric_id INT,
    metric_name VARCHAR(255),
    month_year DATE,
    avg_value DECIMAL(10,2)
);

INSERT INTO temp_avg_metrics
SELECT m.metric_id, m.metric_name, DATE_FORMAT(g.metric_date, '%Y-%m-01') AS month_year, 
       AVG(g.actual_value) AS avg_value
FROM metric m
JOIN global_metric_value g ON m.metric_id = g.metric_id
GROUP BY m.metric_id, month_year;

SELECT * FROM temp_avg_metrics;

/*

Section 6 - Create views

*/

-- Active initiatives view.

CREATE VIEW active_initiatives AS
	SELECT initiative_id, initiative_title, start_date, end_date
	FROM initiative
	WHERE end_date IS NULL OR end_date > CURDATE();

-- Global metric performance summary view.

CREATE VIEW metric_summary AS
	SELECT m.metric_id, m.metric_name, g.metric_date, g.actual_value
	FROM metric m
	JOIN global_metric_value g ON m.metric_id = g.metric_id;
    
-- Plan metric performance summary view.

CREATE VIEW metric_summary AS
	SELECT m.metric_id, m.metric_name, g.metric_date, g.actual_value
	FROM metric m
	JOIN plan_metric_value g ON m.metric_id = g.metric_id;

-- Plan-based metric performance view.alter

CREATE VIEW plan_metric_summary AS
	SELECT p.plan_name, pm.metric_id, pm.metric_date, pm.actual_value
	FROM plan p
	JOIN plan_metric_value pm ON p.plan_id = pm.plan_id;