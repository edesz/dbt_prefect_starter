WITH small_subset AS (
    SELECT *
    FROM read_csv_auto(
        'https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/6126cc9a-3c15-4cf8-baa5-c8a17d3ecae2/resource/23a0c882-26b0-428e-a6b7-3a3a259c796b/download/Parking%20Occupancy.csv'
    )
    LIMIT 7
)
SELECT *
FROM small_subset
