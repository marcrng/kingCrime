# Create new schema to hold KC crime data
create schema kc_crime;

show tables;

select *
from records_kcso;

select *
from lex;

# Delete null rows
select *
from lex
where Class is null
  and `Incident #` is null
  and Crime is null
  and `Date/Time` is null
  and `Location Name` is null
  and Address is null
  and Accuracy is null
  and Agency is null;

delete
from lex
where class is null
  and `Incident #` is null
  and Crime is null
  and `Date/Time` is null
  and `Location Name` is null
  and Address is null
  and Accuracy is null
  and Agency is null;

# Delete all 'No results found.' rows
select *
from lex
where Class = 'No results found.'
  and `Incident #` = 'No results found.'
  and Crime = 'No results found.'
  and `Date/Time` = 'No results found.'
  and `Location Name` = 'No results found.'
  and Address = 'No results found.'
  and Accuracy = 'No results found.'
  and Agency = 'No results found.';

delete
from lex
where Class = 'No results found.'
  and `Incident #` = 'No results found.'
  and Crime = 'No results found.'
  and `Date/Time` = 'No results found.'
  and `Location Name` = 'No results found.'
  and Address = 'No results found.'
  and Accuracy = 'No results found.'
  and Agency = 'No results found.';

## Correct column datatypes

# Test str_to_date reformatting from 12hr to datetime format
select STR_TO_DATE(`Date/Time`, '%m/%d/%Y %h:%i %p'), `Date/Time`
from lex;

select STR_TO_DATE(incident_datetime, '%Y-%m-%dT%H:%i:%S.%f'), incident_datetime
from records_kcso;

select STR_TO_DATE(created_at, '%Y-%m-%dT%H:%i:%S.%f'), created_at
from records_kcso;

select STR_TO_DATE(updated_at, '%Y-%m-%dT%H:%i:%S.%f'), updated_at
from records_kcso;

select offense_start_datetime,
       STR_TO_DATE(offense_start_datetime, '%Y-%m-%dT%H:%i:%S.%f'),
       report_datetime,
       STR_TO_DATE(report_datetime, '%Y-%m-%dT%H:%i:%S.%f'),
       offense_end_datetime,
       STR_TO_DATE(offense_end_datetime, '%Y-%m-%dT%H:%i:%S.%f')
from seattle_cases;

# Change datetime formatting for all rows
update lex
set `Date/Time` = STR_TO_DATE(`Date/Time`, '%m/%d/%Y %h:%i %p');

update records_kcso
set incident_datetime = STR_TO_DATE(incident_datetime, '%Y-%m-%dT%H:%i:%S.%f');

update records_kcso
set created_at = STR_TO_DATE(created_at, '%Y-%m-%dT%H:%i:%S.%f');

update records_kcso
set updated_at = STR_TO_DATE(updated_at, '%Y-%m-%dT%H:%i:%S.%f');

update seattle_cases
set offense_start_datetime = STR_TO_DATE(offense_start_datetime, '%Y-%m-%dT%H:%i:%S.%f');

update seattle_cases
set report_datetime = STR_TO_DATE(report_datetime, '%Y-%m-%dT%H:%i:%S.%f');

update seattle_cases
set offense_end_datetime = STR_TO_DATE(offense_end_datetime, '%Y-%m-%dT%H:%i:%S.%f');

# Change Date/Time to datetime datatype
alter table lex
    modify `Date/Time` datetime;

alter table records_kcso
    modify incident_datetime datetime;

alter table records_kcso
    modify created_at datetime;

alter table records_kcso
    modify updated_at datetime;

alter table seattle_cases
    modify offense_start_datetime datetime;

alter table seattle_cases
    modify report_datetime datetime;

alter table seattle_cases
    modify offense_end_datetime datetime;

## Delete duplicates

# Check for duplicates
select `Incident #`, count(`Incident #`)
from lex
group by `Incident #`
order by count(`Incident #`) desc;

select case_number, count(case_number)
from records_kcso
group by case_number
order by count(case_number) desc;

# Delete duplicates
# --Tried to create a unique id column, then delete duplicate rows except for the first, but
#       this took too long with this large of a database
create table tlex as # Duplicate table for testing
select distinct Class,
                `Incident #`,
                Crime,
                `Date/Time`,
                `Location Name`,
                Address,
                Accuracy,
                Agency
from lex;

# Dropping original table and renaming table without duplicates
drop table lex;

rename table tlex to fw;
