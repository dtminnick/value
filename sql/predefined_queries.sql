/*

Name:		predefined_queries.sql

Description:	This script contains all predefined queries for the Value Measurement Database Application.
                
Contents:	1. Detecting Anomalous Metric Spikes (Z-Score Calculation)
		2. Identifying â€œFastest Growingâ€ Metrics Over a Rolling Period
		3. Rank Metrics by Consistency (Lowest Variation)
		4. Rank Metrics by Volatility (Highest Variability)
		5. Event Row Number Assignments by Event Date
		6. First and Last Recorded Value for Each Metric
		7. Rank Metrics by Most Frequently Tracked
		8. Identify Top 3 Events That Impact the Most Metrics
		9. Metric with the Most Plan Associations
		10. Identify Metrics with Longest Periods of Inactivity
		11. Rolling 90-day Average for Each Metric
		12. Assign Plan Groups to Quartiles
		13. Cumulative Distribution of Metric Values
		14. Percent Change Over Rolling 4-Week Window
		15. Running Total of Metrics Per Initiative
		16. Rollup of Events by Initiative
		17. Aggregating Plan Metrics by Cube
		18. Average Metric Value Per Initiative
		19. Combined Event and Plan Count Per Initiative Using Union
		20. Common Initiatives with Events and Plans Using Intersect
		21. Initiatives with Events but No Plans Using EXCEPT
		22. Filter Events for Specific Initiatives Using IN
		23. Filter Events for Initiatives Not in a Specified Set Using NOT IN
		24. Filter Events Where Actual Value Exceeds All Values from a Subquery Using ALL
		25. Filter Events Where Actual Value Exceeds Any Value from a Subquery Using ANY
		26. Filter Events Where Actual Value Exceeds Some Value from a Subquery Using SOME
		
Modifications:	2025-05-01 - Final updates for submission.

*/

/*

Detecting Anomalous Metric Spikes (Z-Score Calculation)

Calculates Z-score for each metric value; identifies outliers where the Z-score exceeds 2.	

Identifies and rank outliers based on how many standard deviation they are away from the mean.

*/

WITH MetricStats AS (
    SELECT 
        m.metric_name,
        gmv.metric_date,
        gmv.actual_value,
        AVG(gmv.actual_value) OVER (PARTITION BY m.metric_name) AS mean_value,
        STDDEV_SAMP(gmv.actual_value) OVER (PARTITION BY m.metric_id) AS std_dev
    FROM 
        metric m
    JOIN 
        global_metric_value gmv ON m.metric_id = gmv.metric_id
)
SELECT 
    metric_name,
    metric_date,
    actual_value,
    (actual_value - mean_value) / NULLIF(std_dev, 0) AS z_score
FROM 
    MetricStats
WHERE 
    ABS((actual_value - mean_value) / NULLIF(std_dev, 0)) > 2
ORDER BY 
    ABS((actual_value - mean_value) / NULLIF(std_dev, 0)) DESC;

/*

Identifying Fastest Growing Metrics Over a Rolling Period	

Calculates growth rate of a metricâ€™s value over last 5 periods; 
ranks the metrics based on their growth rate.	

Compares metrics by rate of change.

*/

WITH RankedMetrics AS (
    SELECT 
        m.metric_name,
        gmv.metric_date,
        gmv.actual_value,
        FIRST_VALUE(gmv.actual_value) OVER (
            PARTITION BY m.metric_name 
            ORDER BY gmv.metric_date ASC 
            ROWS BETWEEN 5 PRECEDING AND CURRENT ROW
        ) AS old_value,
        LAST_VALUE(gmv.actual_value) OVER (
            PARTITION BY m.metric_name 
            ORDER BY gmv.metric_date ASC 
            ROWS BETWEEN 5 PRECEDING AND CURRENT ROW
        ) AS recent_value
    FROM 
        metric m
    JOIN 
        global_metric_value gmv ON m.metric_id = gmv.metric_id
)

SELECT 
    metric_name,
    metric_date,
    old_value,
    recent_value,
    ((recent_value - old_value) / NULLIF(old_value, 0)) * 100 AS growth_rate,
    RANK() OVER (ORDER BY ((recent_value - old_value) / NULLIF(old_value, 0)) DESC) AS growth_rank
FROM 
    RankedMetrics
WHERE 
    old_value IS NOT NULL AND recent_value IS NOT NULL
ORDER BY 
    growth_rank;

/*

Rank Metrics by Consistency (Lowest Variation)	

Identifies metrics with the most stable trends as measured by standard deviation.	

Indicates reliability of given metrics in assessing performance

*/

SELECT 
  m.metric_name, 
  ROUND(STDDEV(gmv.actual_value), 2) AS metric_stddev, 
  RANK() OVER (ORDER BY STDDEV(gmv.actual_value) ASC) AS consistency_rank 
FROM 
  metric m
JOIN 
  global_metric_value gmv ON m.metric_id = gmv.metric_id
GROUP BY 
  m.metric_id;

/*

Rank Metrics by Volatility (Highest Variability)	

Identified the most volatile metrics by ranking them from highest to lowest standard deviation.	

Metrics with greater fluctuation receive higher ranks.

*/

SELECT 
  m.metric_name,
  ROUND(STDDEV(gmv.actual_value), 2) AS metric_stddev,
  RANK() OVER (ORDER BY STDDEV(gmv.actual_value) DESC) AS volatility_rank
FROM 
  metric m
JOIN 
  global_metric_value gmv ON m.metric_id = gmv.metric_id
GROUP BY 
  m.metric_id;

/*

Event Row Number Assignments by Event Date	

Assigns a row number for each event per initiative ordered by date.	

Helps track the sequence of key events in initiatives.

*/

SELECT 
  CONCAT(i.initiative_title, ': ', e.event_title) AS event
  e.event_date
  ROW_NUMBER() OVER (PARTITION BY e.initiative_id ORDER BY e.event_date ASC) AS event_number
FROM
  event e
JOIN
  initiative i ON e.initiative_id = i.initiative_id;

/*

First and Last Recorded Value for Each Metric	

Retrieves the first and latest values for each metric based on metric dates.	

Tracks the overall growth or decline of a metric by comparing its first recorded value to its most recent value.

*/

WITH first_last_values AS (
 SELECT
 gmv.metric_id,
 m.metric_name,
 FIRST_VALUE(gmv.actual_value) OVER (PARTITION BY gmv.metric_id
 ORDER BY gmv.metric_date) AS f_value,
 LAST_VALUE(gmv.actual_value) OVER (
 PARTITION BY gmv.metric_id
 ORDER BY gmv.metric_date
 ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
 ) AS l_value,
 ROW_NUMBER() OVER (PARTITION BY gmv.metric_id
 ORDER BY gmv.metric_date) AS row_num
 FROM
 global_metric_value gmv
 JOIN
 metric m ON m.metric_id = gmv.metric_id
)
SELECT
 metric_name,
 f_value,
 l_value
FROM
 first_last_values
WHERE
 row_num = 1;

/*

Rank Metrics by Most Frequently Tracked	

This query determines which metrics are most actively measured	

Compares metrics by frequency of measurement.

*/

SELECT
 m.metric_id,
 m.metric_name,
 COUNT(gmv.metric_date) AS tracking_frequency,
 RANK() OVER (ORDER BY COUNT(gmv.metric_date) DESC) AS tracking_rank,
 DENSE_RANK() OVER (ORDER BY COUNT(gmv.metric_date) DESC) AS dense_tracking_rank
FROM
 metric m
JOIN
 global_metric_value gmv ON m.metric_id = gmv.metric_id
GROUP BY
 m.metric_id;

/*

Identify Top 3 Events That Impact the Most Metrics	

Ranks events based on number of impacted plans; assigns a relative ranking between 0 and 1.	

Assesses events in terms of percent of plans impacted.

*/

SELECT
 e.event_title,
 COUNT(ep.plan_id) AS impacted_plans,
 PERCENT_RANK() OVER (ORDER BY COUNT(ep.plan_id) DESC) AS event_percent_rank
FROM
 event_plan ep
JOIN
 event e ON ep.event_id = e.event_id
GROUP BY
 ep.event_id
LIMIT 3;

/*

Metric with the Most Plan Associations	

Shows which metrics are tied to the most strategic plans.	

Assesses impact in terms of volume of plans.

*/

SELECT
 pmv.metric_id,
 m.metric_name,
 COUNT(pmv.plan_id) AS plan_count,
 RANK() OVER (ORDER BY COUNT(pmv.plan_id) DESC) AS plan_rank
FROM
 plan_metric_value pmv
JOIN
 metric m ON pmv.metric_id = m.metric_id
GROUP BY
 pmv.metric_id;

/*

Identify Metrics with Longest Periods of Inactivity
	
Identifies metrics with large gaps in reporting.
	
Identifies metrics with large gaps in reporting.

*/

WITH Gaps AS (
 SELECT
 m.metric_id,
 m.metric_name,
 gmv.metric_date,
 LAG(gmv.metric_date) OVER (PARTITION BY m.metric_id
 ORDER BY gmv.metric_date) AS prev_date
 FROM
 metric m
 JOIN
 global_metric_value gmv ON m.metric_id = gmv.metric_id
)
SELECT
 metric_name,
 MAX(DATEDIFF(metric_date, prev_date)) AS max_inactive_days
FROM
 Gaps
GROUP BY
 metric_id
ORDER BY
 max_inactive_days DESC;

/*

Rolling 90-day Average for Each Metric	

Calculates a 90-day rolling average for each metric's actual value over time, helping to smooth
out fluctuations and observe trends	

This query calculates a 90-day rolling average for each metric's actual value over time, helping to smooth
out fluctuations and observe trends

*/

SELECT
  m.metric_id,
  m.metric_name,
  gmv.metric_date,
  ROUND(
    AVG(gmv.actual_value) OVER (
      PARTITION BY m.metric_id 
      ORDER BY gmv.metric_date
      ROWS BETWEEN 89 PRECEDING AND CURRENT ROW
    ),
    2
  ) AS rolling_90_day_avg
FROM
  metric m
JOIN
  global_metric_value gmv ON m.metric_id = gmv.metric_id;

/*

Assign Plan Groups to Quartiles	

This query uses NTILE to assign quartiles to metric values within 
each plan.	

Ranks them into four equal groups based on their actual values.

*/

SELECT 
    pmv.plan_id,
    m.metric_name,
    pmv.actual_value,
    NTILE(4) OVER (PARTITION BY pmv.plan_id, m.metric_name
                   ORDER BY pmv.actual_value DESC) AS quartile
FROM 
    plan_metric_value pmv
JOIN 
    metric m ON pmv.metric_id = m.metric_id;

/*

Cumulative Distribution of Metric Values	

This query calculates the cumulative distribution of metric values within each plan.	

This query calculates the cumulative distribution of metric values within each plan.

*/

SELECT 
    pmv.plan_id,
    m.metric_name,
    pmv.actual_value,
    CUME_DIST() OVER (PARTITION BY pmv.plan_id 
                      ORDER BY pmv.actual_value DESC) AS cumulative_distribution
FROM 
    plan_metric_value pmv
JOIN 
    metric m ON pmv.metric_id = m.metric_id;

/*

Percent Change Over Rolling 4-Week Window	

Calculates percentage change in metric values compared to their values four weeks prior for each metric.	

Analyzes metric trends over time. Identifies growth, decline, or stability in metric values.

*/

WITH RankedValues AS (
    SELECT 
        m.metric_id,
        gmv.metric_date,
        gmv.actual_value,
        LAG(gmv.actual_value, 4) OVER (PARTITION BY m.metric_id ORDER BY gmv.metric_date) AS previous_4_weeks
    FROM metric m
    JOIN global_metric_value gmv ON m.metric_id = gmv.metric_id
)
SELECT 
    metric_id,
    metric_date,
    actual_value,
    previous_4_weeks,
    CASE 
        WHEN previous_4_weeks IS NOT NULL AND previous_4_weeks != 0 
        THEN (actual_value - previous_4_weeks) / previous_4_weeks * 100
        ELSE NULL 
    END AS percent_change
FROM RankedValues;

/*

Running Total of Metrics Per Initiative	

Calculates a running total of metric values for a specific initiative over time	

Tracks cumulative performance  of metrics under an initiative. Monitors trend progression over time.

*/

SELECT 
    i.initiative_title,
    m.metric_name,
    gmv.metric_date,
    SUM(gmv.actual_value) OVER (PARTITION BY i.initiative_title 
                                ORDER BY gmv.metric_date) AS running_total
FROM 
    metric m
JOIN 
    global_metric_value gmv ON m.metric_id = gmv.metric_id
JOIN
    initiative i ON i.initiative_id = m.initiative_id
WHERE 
    m.initiative_id IN (1, 2)
ORDER BY 
    m.initiative_id,
    m.metric_id,
    gmv.metric_date;

/*

Rollup of Events by Initiative	

Counts total number of events associated with each initiative; includes totals using the ROLLUP feature.	

Counts total number of events associated with each initiative and includes totals using the ROLLUP feature.

*/

SELECT 
    i.initiative_title,
    COUNT(e.event_id) AS total_events
FROM 
    event e
JOIN 
    initiative i ON i.initiative_id = e.initiative_id
GROUP BY ROLLUP (i.initiative_title);

/*

Aggregating Plan Metrics by Cube	

Calculates average metric value for each combination of plan and initiative; to generates total rows.	

Provides insights into total metric values at multiple levels.

*/

SELECT 
    pmv.plan_id,
    i.initiative_title,
    AVG(pmv.actual_value) AS avg_metric_value
FROM 
    plan_metric_value pmv
JOIN 
    metric m ON pmv.metric_id = m.metric_id
JOIN 
  initiative i ON m.initiative_id = i.initiative_id
GROUP BY i.initiative_title, pmv.plan_id WITH ROLLUP;

/*

Average Metric Value Per Initiative	

Calculates average metric value for each initiative; uses subquery to aggregate metric values for each initiative.	

Provides per-initiative metric summary, calculating the average value of metrics associated with each initiative.

*/

SELECT 
    i.initiative_title,
    (SELECT AVG(pmv.actual_value)
     FROM plan_metric_value pmv
     JOIN metric m ON pmv.metric_id = m.metric_id
     WHERE m.initiative_id = i.initiative_id) AS avg_metric_value
FROM 
    initiative i;

/*

Combined Event and Plan Count Per Initiative Using Union	

Combines counts of events and plans for each initiative (event and plan) using union.	

Summarizes total number of events and plans for each initiative.

*/

SELECT 
    initiative_title, 
    COUNT(event_id) AS event_count
FROM 
    event e
JOIN 
    initiative i ON i.initiative_id = e.initiative_id
GROUP BY 
    initiative_title;

/*

Common Initiatives with Events and Plans Using Intersect	

Finds initiative titles common between the event and plan tables.	

The purpose of this query is to identify initiatives that have both events and plans associated with them.

*/

SELECT 
    initiative_title
FROM 
    event e
JOIN 
    initiative i ON i.initiative_id = e.initiative_id

INTERSECT

SELECT 
    initiative_title
FROM 
    plan p
JOIN 
	event_plan ep ON p.plan_id = ep.plan_id
JOIN
	event e ON e.event_id = ep.event_id
JOIN
    initiative i ON i.initiative_id = e.initiative_id;

/*

Initiatives with Events but No Plans Using EXCEPT	

Returns initiative titles that are present in the event table but not in the plan table.	

Identifies initiatives that have events associated with them but do not have any corresponding plans.

*/

SELECT 
    initiative_title
FROM 
    event
JOIN 
    initiative ON initiative.initiative_id = event.initiative_id

EXCEPT

SELECT 
    initiative_title
FROM 
    plan p
JOIN 
	event_plan ep ON p.plan_id = ep.plan_id
JOIN
	event e ON e.event_id = ep.event_id
JOIN
    initiative i ON i.initiative_id = e.initiative_id;

/*

Filter Events for Specific Initiatives Using IN	

This query retrieves the initiative_title and event_date for events associated with initiatives whose 
initiative_id is in a specified set of values (1, 2, or 3). 
The IN operator is used to check for membership in this set.	

The purpose of this query is to filter and display events that belong to specific 
initiatives, identified by a set of initiative_id values.

*/

SELECT 
    initiative_title,
    event_date
FROM 
    event
JOIN 
    initiative ON initiative.initiative_id = event.initiative_id
WHERE 
    initiative.initiative_id IN (1, 2, 3);

/*

Filter Events for Initiatives Not in a Specified Set Using NOT IN	

This query retrieves the initiative_title and event_date for events 
associated with initiatives whose initiative_id is not in the specified 
set of values (1, 2, or 3). The NOT IN operator is used to exclude initiatives 
with these initiative_id values.	

The purpose of this query is to filter and display events that belong to 
initiatives whose initiative_id does not match the specified values.

*/

SELECT 
    initiative_title,
    event_date
FROM 
    event
JOIN 
    initiative ON initiative.initiative_id = event.initiative_id
WHERE 
    initiative.initiative_id NOT IN (1, 2, 3);

/*

Filter Events Where Actual Value Exceeds All Values from a Subquery Using ALL	

This query retrieves the initiative_title, event_date, and actual_value for 
events where the actual_value is greater than all the actual_value values 
associated with metric_id = 2 in the global_metric_value table. The ALL operator 
is used to compare the actual_value of the event against all values returned by a subquery	

The purpose of this query is to identify events where the actual_value is 
greater than all values associated with a particular metric (metric_id = 2).

*/

SELECT 
    i.initiative_title,
    m.metric_name,
    gmv.actual_value
FROM 
    global_metric_value gmv
JOIN
	metric m ON gmv.metric_id = m.metric_id
JOIN
    initiative i ON i.initiative_id = m.initiative_id
WHERE 
    gmv.actual_value > ALL (SELECT actual_value FROM global_metric_value WHERE metric_id = 2);

/*

Filter Events Where Actual Value Exceeds Any Value from a Subquery Using ANY	

This query retrieves the initiative_title, event_date, and actual_value 
for events where the actual_value is greater than at least one of the 
actual_value values associated with metric_id = 2 in the global_metric_value table.	

The purpose of this query is to identify events where the actual_value 
exceeds at least one value in the set of values related to a specific metric (metric_id = 2)

*/

SELECT 
    i.initiative_title,
    m.metric_name,
    gmv.actual_value
FROM 
    global_metric_value gmv
JOIN
	metric m ON gmv.metric_id = m.metric_id
JOIN
    initiative i ON i.initiative_id = m.initiative_id
WHERE 
    gmv.actual_value > ANY (SELECT actual_value FROM global_metric_value WHERE metric_id = 1);

/*

Filter Events Where Actual Value Exceeds Some Value from a Subquery Using SOME	

This query retrieves the initiative_title, event_date, and actual_value for 
events where the actual_value is greater than at least one value from the set 
of actual_value values associated with metric_id = 2 in the global_metric_value table.	

The purpose of this query is to identify events where the actual_value surpasses 
any one value from a subset of values corresponding to a specific metric (metric_id = 2).

*/

SELECT 
    i.initiative_title,
    m.metric_name,
    gmv.actual_value
FROM 
    global_metric_value gmv
JOIN
  metric m ON gmv.metric_id = m.metric_id
JOIN
   initiative i ON i.initiative_id = m.initiative_id
WHERE 
   gmv.actual_value > SOME (SELECT actual_value FROM global_metric_value WHERE metric_id = 1);








