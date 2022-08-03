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

# Find days with 50 records
alter table lex
    modify `Date/Time` datetime;

select STR_TO_DATE(`Date/Time`, '%m/%d/%Y %h:%i %p')
from lex
