# Iran Cofee Shops

## Ideas
- Mahdi suggested → Table for lat, lang Extract From Google
- Plot on map

```sql
CREATE TABLE cafe_locataion(
  cafe_id INT UNSIGNED,
  lat FLOAT,
  lang FLOAT,
  FOREIGN KEY (cafe_id) REFERENCES cafe(cafe_id)
)
```
