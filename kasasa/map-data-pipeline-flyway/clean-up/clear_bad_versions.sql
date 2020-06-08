SET @last_good_version = 36;
select
  concat('delete from ',table_schema,'.', table_name, ' where installed_rank > ',@last_good_version, ';')
  from information_schema.tables
  where table_name = 'schema_version';
