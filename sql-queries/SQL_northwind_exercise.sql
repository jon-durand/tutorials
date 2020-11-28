-- Q1. Write a query to get Product name and quantity/unit.
select productname, quantityperunit
from products
;

-- Q2. Write a query to get most expense and least expensive Product list (name and unit price)
select productname, unitprice
from products
where unitprice in ( (select min(unitprice) from products),(select max(unitprice) from products) )
;

-- Q3. Write a query to count current and discontinued products.
select count(productname)
from products
group by discontinued

-- Q4. Select all product names and their category names (77 rows)
select productname, categoryname
from products
join categories
on products.categoryid = categories.categoryid
;


-- Q5. Select all product names, unit price and the supplier region that don't have suppliers from USA region. (26 rows)
select productname, unitprice, region
from products
join suppliers
on products.supplierid = suppliers.supplierid
where region not like 'USA'
;

-- Q6. Get the total quantity of orders sold.( 51317)


-- Q7. Get the total quantity of orders sold for each order.(830 rows)


-- Q8. Get the number of employees who have been working more than 5 year in the company. (9 rows)

