# Iran Cofee Shops

## Ideas
- Mahdi suggested → Table for lat, lang Extract From Google
- Plot on map

```sql
CREATE TABLE cafe_location(
    cafe_id INT UNSIGNED,
    latitude DECIMAL(20, 16),
    longitude DECIMAL(20, 16),
    FOREIGN KEY (cafe_id) REFERENCES cafe(cafe_id)
);

INSERT INTO
    cafe_location (cafe_id, latitude, longitude)
VALUES
(1, 54.7110300331244, 51.40699736773968);

SELECT
    *
FROM
    cafe_location;
```
