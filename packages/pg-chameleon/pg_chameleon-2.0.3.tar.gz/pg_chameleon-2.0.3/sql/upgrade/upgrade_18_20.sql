ALTER SCHEMA sch_chameleon RENAME TO sch_chameleon_old;
 --create schema
SELECT 
	i_id_source,t_source,''::jsonb as t_dest_schema
FROM 
	sch_chameleon_old.t_sources;


SELECT 
	* 
FROM 
	sch_chameleon.t_sources;