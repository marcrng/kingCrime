use kc_crime;

select * from kc_crime.records_kcso;

select * from kc_crime.seattle_cases;

select * from fw;

select *
from records_kcso kc
join seattle_cases sc on kc.incident_datetime = sc.offense_start_datetime;

select `Incident #`, count(`Incident #`)
from tlex
group by `Incident #`
order by count(`Incident #`) desc;

select distinct `Incident #`, Crime, `Date/Time`, count(`Incident #`)
from lex
group by `Incident #`, Crime, `Date/Time`
order by count(`Incident #`) desc;
