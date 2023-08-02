POSTGRES_DATABASE='demographics'
POSTGRES_HOST='localhost'
POSTGRES_PASSWORD='alpha'
POSTGRES_PORT='5432'
POSTGRES_USERNAME='minion'
export PGPASSWORD="$POSTGRES_PASSWORD"

# NOTE:- Remove headers from the file
file_path="/home/dell/Desktop/dist_work/ADCURATIO_MATCHES_TO_VIZIO_20210429.CSV"
table_name="vizio_temp"

sql="CREATE TABLE $table_name(epsilon_id text,ma_id text);"
psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -d "$POSTGRES_DATABASE" -U "$POSTGRES_USERNAME" -c "$sql"

sql="\copy $table_name(epsilon_id,ma_id) FROM $file_path DELIMITER '|' CSV"
psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -d "$POSTGRES_DATABASE" -U "$POSTGRES_USERNAME" -c "$sql"

echo "DONE!!!!!"