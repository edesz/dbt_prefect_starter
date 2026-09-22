WITH source AS (
    SELECT *
    FROM {{ source('tor_open_data_parking_lot_usage', 'parking_lot_occupancies') }}
),
renamed AS (
    SELECT
        _id AS row_id,
        Year AS year,
        Quarter AS quarter,
        "Car Park Number" AS car_park_number,
        "Car Park Location" AS car_park_location,
        "Total Available Spaces" AS total_available_spaces,
        CAST(
            REPLACE("Average Daily Peak Occupancy %", '%', '') AS INTEGER
        ) AS avg_daily_peak_occupancy
    FROM source
)
SELECT *
FROM renamed
