use test
set names utf8;

-- 1. Select all products (all fields)
select * from product;

-- 2. Select the names of all automated warehouses
select * from store;

-- 3. Calculate the total amount in money of all sales
select sum(total) from sale;

-- 4. Get unique store_id of all warehouses from which there was at least one sale
SELECT DISTINCT store_id from sale;

-- 5. Get unique store_id of all warehouses from which there was no sale
select store.store_id from store left join sale on store.store_id = sale.store_id where sale.quantity is NULL;

-- 6. Get for each product the name and average unit cost of the product avg (total / quantity), if the product was not sold, it does not appear in the report.
select name, avg(total/quantity) from product right join sale on product.product_id = sale.product_id group by name order by avg(total/quantity);

-- 7. Get the names of all products that were sold only from a single warehouse
select name from (select name, count(DISTINCT store_id) as F from product inner join sale using(product_id) group by name) as F where F = 1;

-- 8. Get the names of all warehouses from which only one product was sold
select name from (select name, count(DISTINCT product_id) F from sale right join store using (store_id) group by name) F where F = 1;

-- 9. Select all rows (all fields) from sales in which the total amount (total) is maximum (equal to the maximum of all encountered)
select * from sale where total = (select max(total) from sale);

-- 10. Print the date of the highest sales, if there are several such dates, then the earliest of them
select date from (select date, sum(quantity) S from sale group by date) F order by S DESC limit 1;
