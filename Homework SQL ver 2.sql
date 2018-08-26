Use sakila;

Select first_name, last_name
from actor
print;

-- 1b Show in Table Actor the full name in uppercase in a single column
Alter table actor
add column full_name varchar(50);


Insert into actor (full_name)
values
	(Select concat(first_name, " ", last_name) as full_name 
from actor)
);

SET SESSION sql_mode = '';

SET SQL_SAFE_UPDATES=0;
UPDATE actor SET full_name = CONCAT(first_name, " ", last_name);


-- INSERT INTO actor (full_name) SELECT CONCAT(first_name, " ", last_name) AS full_name FROM actor;

 
Select * from actor
Print;

-- 2a. First Name Joe
select actor_id, first_name, last_name 
from actor 
where first_name="Joe"
;

-- 2b Actors with gen in last name
select first_name, last_name 
from actor
where last_name like "%gen%";

-- 2c last name includes LI
select last_name, first_name
from actor
where last_name like "%li%" 
order by last_name, first_name;

-- 2d 
select country, country_id 
where country =(Afghanistan, Bangladesh, China)
in country

-- 3a  add middle name column between first and last 
alter table actor
add column middle_name varchar (2) after first_name 

-- 3b Change middle name tp typpe blob
alter table actor
where middle_name type=blob; 

middle_name (type)

-- 3c delete middle name column
alter table actor drop middle_name

-- 4a freq of last names
select last_name, count(last_name) from actor
group by last_name


-- 4b freq last name more than twice only
select last_name, count(last_name) from actor
group by last_name 
having count(last_name) >1

-- 4c Groucho to Harpo
select * from actor
where first_name="groucho" and last_name ="williams"


-- 4c swappng out first name
update actor
set first_name="harpo" 
where actor_id=172

-- 4d change harpo back to Groucho and Mucho Groucho 
select * from actor
where last_name ="williams"

-- 5a schema of address table
-- schema of address table
-- select * from address 
-- show tables(address)
desc address


-- 6a display first name, last name and address of each staff memember 
select staff.first_name, staff.last_name, address.address
from staff
left JOIN address ON
staff.address_id=address.address_id;


-- 6b display Total Amt rung up by each staff members in Aug 2009
SELECT SUM(amount) AS 'Total Amt Payments'
FROM payment
GROUP BY staff_id
having payment_date >+5/1/2009 and payment_date<=5/30/2009;
-- last line doesnt work


-- 6c list film, number of actors  for that film 
-- Select title, Count(actor_id) as "Number of Films"
-- from  film
-- inner join film_actor
-- on film.film_id=film_actor.film_id;

Create view subquery1 as
SELECT title, (
    SELECT COUNT(*) FROM film_actor
    WHERE film.film_id = film_actor.film_id) AS 'Number of  Actors'
FROM film;

-- select * from subquery1;

-- select title, actor_id as 'Number of Actors' from film 
-- join (
   -- SELECT film_id, COUNT(film_id) AS NumAct
   -- FROM film_actor
   -- group by film_id 
-- on (film.film_id=film_actor.film_id)

-- 6d How many copies of Hunchback Impossible exists
select film_id, title 
-- where title like "%Hunchback% "
from film;

select count(film_ID)
from inventory
where film_id = 439;


-- 6e total paid by each customer in alphbetically order
select customer.customer_id, customer.first_name, customer.last_name, sum(payment.amount)
from customer
inner join payment
on customer.customer_id=payment.customer_id
group by customer_id
order by customer.last_name;

-- 7a Movies starting with Q and K Subquery titles with lang = english
select title
from film
where language_id="1" and (title="q%" or title="k%");

create view subquery2 as
select language_id="1", (
	select title
	where title="q%" or title="%k")
from film;

-- 7b subquery actors in Alone trip
SELECT actor.actor_id, actor.full_name
FROM actor
WHERE actor_id IN
(
  SELECT actor_id 
  FROM film_actor
  WHERE film_id IN
  (
    SELECT film_id
    FROM film
    WHERE title="Alone Trip"));
    
-- 7c all canadian customers
--  customer.name to customer.address_id to address.address_id to address.city id, city.city id to city.county id to country.country_id to country.country
-- Select  customer.first_name, customer.last_name, customer.email 
-- from customer
-- left join country on 
-- country="Canada" 

SELECT first_name, last_name, email, country
  FROM customer cus
  JOIN address a
  ON (cus.address_id = a.address_id)
  JOIN city cit
  ON (a.city_id = cit.city_id)
  JOIN country ctr
  ON (cit.country_id = ctr.country_id)
  WHERE ctr.country = 'canada';
  
  
-- 7d all family movies 
-- category_id category=family,
-- film_category.category_ID to Film ID
-- then film film_id to film title
-- category is Name under table category

	select title, name 
    from film flm
	join film_category fcat
	on(flm.film_id= fcat.film_id)
	join category cat
	on cat.category_id=fcat.category_id
    where cat.name="Family"
 
 
-- 7e Most rented movies in desc order
-- rental inventory_id  to get frequency of 
-- inventory table to get inventory ID to film ID.  
-- film table filmID to title


select title, count(rental_duration)
from rental r
join inventory inv
on (r.inventory_id=inv.inventory_id)
join film f
on (inv.film_id=f.film_id)
group by title
order by count(rental_duration) desc;

-- 7f Query on  Dollars each store brought in
-- staff table will give store_id and staff_id
-- payment table will give staff_id and amount that was paid 
select store_id, sum(amount)
from staff s
join payment p
on (s.staff_id=p.staff_id)
group by store_id;

-- 7g Display each store id, city and country
-- store table gives store_id and address_id
-- address table gives address_id and city_id
-- city table gives city_id and city (name of) and counry_id
-- country table gives county_id and country (name of)

select store_id, city, country
from store s
join address a
on (s.address_id=a.address_id)
join city c
on (a.city_id=c.city_id)
join country ctry
on (ctry.country_id=c.country_id);

-- 7h list top five genres in gross revenue in descending order
-- category tables category_id and name
--  film_cateogry table category_id and film_id
-- inventory table gives film_id and inventory_id
-- rental table gives staff_id and inventory_id
--  payment table will give staff_id and amount that was paid 

-- KEEPS LOSING CCONNECTION AND QUERY IS INTERRUPTED BEFORE CAN SEE IF WOKS even limited to 10 rows. 

select name, Sum(amount) 
    from category c
	join film_category fcat
	on c.category_id=fcat.category_id
    join inventory i
    on fcat.film_id=i.film_id
    join rental r
    on r.inventory_id=i.inventory_id
    join payment p
    on p.staff_id=r.staff_id
    group by name
    order by Sum(amount)
    limit 5;
    
 -- 8a create a view of top 5 grossing generes
 create view Top_5_Grossing_Generes as
 select name, Sum(amount) 
    from category c
	join film_category fcat
	on c.category_id=fcat.category_id
    join inventory i
    on fcat.film_id=i.film_id
    join rental r
    on r.inventory_id=i.inventory_id
    join payment p
    on p.staff_id=r.staff_id
    group by name
    order by Sum(amount)
    limit 5;
 
 - -8c display the view.  
 -- I would go to the navigator on the left, scroll down to views, select Top_5_Grossing_Generes and click the talble icon 
 
 -- 8c Delete query
 drop view Top_5_Grossing_Generes;
 
--  Turn safe updates on
SET SQL_SAFE_UPDATES = 1;
