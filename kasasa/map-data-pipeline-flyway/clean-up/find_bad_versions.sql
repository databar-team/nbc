SET @limit_length = 3;
select
  concat('select installed_rank,version,script from ',table_schema,'.', table_name, ' order by installed_rank desc limit ',@limit_length,' ;')
from information_schema.tables
where table_name = 'schema_version';
