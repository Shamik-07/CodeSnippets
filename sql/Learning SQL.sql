-- inline calculations
-- multiplying two columns on the fly to create a separate column
select market_date, customer_id, vendor_id, quantity, cost_to_customer_per_qty,
round(quantity * cost_to_customer_per_qty, 2) as price from farmers_market.customer_purchases;

-- concatenating the first name with the last name of the customer
select customer_id,
upper(concat(customer_last_name, ', ', customer_first_name)) as customer_name 
from farmers_market.customer
order by customer_last_name, customer_first_name;

-- selecting with a specific condition for a single column
SELECT product_id, product_name FROM farmers_market.product WHERE
product_id = 10 OR (product_id > 3 AND product_id < 8);

-- selecting with a specific condition for multiple columns
SELECT market_date, customer_id, vendor_id, quantity * cost_to_customer_per_qty AS price
FROM farmers_market.customer_purchases
WHERE customer_id = 4 AND vendor_id = 7;

-- selecting all customer first name which match any of these below
SELECT customer_id, customer_first_name, customer_last_name
FROM farmers_market.customer
WHERE customer_first_name IN ('Renee', 'Rene', 'Renée', 'René', 'Renne');

-- selecting a column where a field is blank
SELECT * FROM farmers_market.product
WHERE product_size IS NULL;

-- selecting a column with a blank or whitespace field
SELECT * FROM farmers_market.product
WHERE product_size IS NULL OR TRIM(product_size) = '';
select product_name, product_size, product_category_id, product_qty_type
from farmers_market.product where product_size is null or TRIM(product_size)='';

-- group by
select market_date, customer_id,
sum(quantity) as items_purchased,
count(distinct product_id) as different_items_purchased
from farmers_market.customer_purchases 
group by market_date, customer_id
order by market_date, customer_id;

-- what's the total purchase by a customer on a single day
select market_date, customer_id,
sum(quantity * cost_to_customer_per_qty) as total_spent
from farmers_market.customer_purchases
group by customer_id, market_date
order by market_date, customer_id;

-- joining tables and group by
select c.customer_id, c.customer_first_name, c.customer_last_name,
v.vendor_id, v.vendor_name,
sum(cp.quantity * cp.cost_to_customer_per_qty)  as total_spent
from ((farmers_market.customer as c
left join farmers_market.customer_purchases as cp
on c.customer_id = cp.customer_id
)
left join farmers_market.vendor as v
on cp.vendor_id = v.vendor_id
)
where c.customer_id = 3
group by c.customer_id, c.customer_first_name, c.customer_last_name,
v.vendor_id, v.vendor_name
order by c.customer_id, v.vendor_id;

-- converting columns before group by 
select market_date, customer_id,
sum(case when product_qty_type='lbs' then quantity else 0 end) as qty_lbs_purchased,
sum(case when product_qty_type='unit' then quantity else 0 end) as qty_unit_purchased,
sum(case when product_qty_type not in('unit', 'lbs') then quantity else 0 end) as qty_other_purchased
from farmers_market.customer_purchases as cp
inner join farmers_market.product as p
on cp.product_id = p.product_id
group by market_date, customer_id
order by market_date, customer_id;

-- Window function
SELECT
vendor_id,
market_date,
product_id,
original_price,
ROW_NUMBER() OVER (PARTITION BY vendor_id ORDER BY original_price DESC) AS
price_rank
FROM farmers_market.vendor_inventory ORDER BY vendor_id, original_price DESC;

-- same query as above but instead of showing all the prices by vendor_id
-- we are showing only the costliest price
select * from 
(select vendor_id, market_date, product_id, original_price,
row_number() over (partition by vendor_id order by original_price desc) as price_rank
from farmers_market.vendor_inventory
order by vendor_id, original_price) as x
where x.price_rank = 1;




-- Subquery with joins, outputs the customers who bought a product when it rained
SELECT 
    cp.market_date,
    CONCAT(c.customer_first_name,
            ' ',
            c.customer_last_name) AS customer_name,
    p.product_name,
    p.product_size,
    p.product_qty_type,
    cp.quantity
FROM
    ((farmers_market.customer AS c
    LEFT JOIN farmers_market.customer_purchases AS cp ON c.customer_id = cp.customer_id)
    LEFT JOIN farmers_market.product AS p ON cp.product_id = p.product_id)
WHERE
    cp.market_date IN (SELECT 
            m.market_date
        FROM
            farmers_market.market_date_info AS m
        WHERE
            m.market_rain_flag = 1);

-- Subquery with joins, outputs the customers who bought a product when it rained
SELECT 
    cp.market_date,
    cp.transaction_time,
    CONCAT(c.customer_first_name,
            ' ',
            c.customer_last_name) AS customer_name,
    p.product_name,
    cp.quantity,
    cp.cost_to_customer_per_qty,
    md.market_rain_flag
FROM
    (((farmers_market.customer AS c
    LEFT JOIN farmers_market.customer_purchases AS cp ON c.customer_id = cp.customer_id)
    LEFT JOIN farmers_market.product AS p ON cp.product_id = p.product_id)
    LEFT JOIN farmers_market.market_date_info AS md ON cp.market_date = md.market_date)
WHERE
    md.market_rain_flag = 1
;

-- Case Statements
SELECT 
    market_date,
    market_day,
    market_rain_flag,
    CASE
        WHEN LOWER(market_day) IN ('saturday' , 'sunday') THEN 1
        ELSE 0
    END AS is_weekend
FROM
    farmers_market.market_date_info;
-- creating a flag to select all prices above 50
SELECT 
    market_date,
    customer_id,
    ROUND(quantity * cost_to_customer_per_qty, 2) AS price,
    CASE
        WHEN quantity * cost_to_customer_per_qty > 50 THEN 1
        ELSE 0
    END AS price_over_50
FROM
    farmers_market.customer_purchases;	

-- Building datasets for analytical reporting
select cp.market_date, md.market_day, md.market_week, md.market_year,
 cp.vendor_id, v.vendor_name, v.vendor_type,
round(sum(cost_to_customer_per_qty*quantity),2) as sales
from farmers_market.customer_purchases as cp
left join farmers_market.vendor as v
on cp.vendor_id = v.vendor_id
left join farmers_market.market_date_info as md
on cp.market_date = md.market_date
group by cp.vendor_id, cp.market_date 
order by cp.vendor_id, cp.market_date;

-- storing the result of the query so that the results can be used later on
with sales_by_day_vendor as 
(
select cp.market_date, md.market_day, md.market_week, md.market_year,
 cp.vendor_id, v.vendor_name, v.vendor_type,
round(sum(cost_to_customer_per_qty*quantity),2) as sales
from farmers_market.customer_purchases as cp
left join farmers_market.vendor as v
on cp.vendor_id = v.vendor_id
left join farmers_market.market_date_info as md
on cp.market_date = md.market_date
group by cp.vendor_id, cp.market_date 
order by cp.vendor_id, cp.market_date
),
trial_table as 
(select * from farmers_market.customers
)

select market_year, market_week,
sum(sales) as weekly_sales
from sales_by_day_vendor
group by market_year, market_week;

-- create a view of the same query above and store in the schema
create view farmers_market.vw_sales_by_day_vendor as 
(
select cp.market_date, md.market_day, md.market_week, md.market_year,
 cp.vendor_id, v.vendor_name, v.vendor_type,
round(sum(cost_to_customer_per_qty*quantity),2) as sales
from farmers_market.customer_purchases as cp
left join farmers_market.vendor as v
on cp.vendor_id = v.vendor_id
left join farmers_market.market_date_info as md
on cp.market_date = md.market_date
group by cp.vendor_id, cp.market_date 
order by cp.vendor_id, cp.market_date
);




































-- information schema of tables
select table_name from information_schema.tables;
select column_name from information_schema.columns where table_name= 'customer';
select column_name from information_schema.columns where table_name= 'customer_purchases';
select column_name from information_schema.columns where table_name= 'product';
select column_name from information_schema.columns where table_name= 'market_date_info';






-- Join
-- Left Join product table and product_category table on product_category_id
select p.product_id, p.product_name, p.product_category_id as product_prod_cat_id,
pc.product_category_id as category_prod_cat_id, pc.product_category_name
from farmers_market.product as p 
left join farmers_market.product_category as pc 
on p.product_category_id = pc.product_category_id
order by pc.product_category_name, p.product_name;
-- inner join
select c.* from farmers_market.customer as c
left join farmers_market.customer_purchases as cp
on c.customer_id = cp.customer_id 
where cp.customer_id is not null;
-- right join
select * from farmers_market.customer as c
right join farmers_market.customer_purchases as cp
on c.customer_id = cp.customer_id ;
-- left join with market date == NULL and not on '2019-03-02'
SELECT c.*, cp.market_date
FROM farmers_market.customer AS c
LEFT JOIN farmers_market.customer_purchases AS cp
ON c.customer_id = cp.customer_id
WHERE (cp.market_date <> '2019-03-02' OR cp.market_date IS NULL);
-- just want the list of customer names without any duplicates
SELECT distinct c.*
FROM farmers_market.customer AS c
LEFT JOIN farmers_market.customer_purchases AS cp
ON c.customer_id = cp.customer_id
WHERE (cp.market_date <> '2019-03-02' OR cp.market_date IS NULL);
/*
selecting all the booths from vendor_booth_assignments and vendor
first left join booth and vendor_booth_assignments and then to this result
left join vendor with the vendor id
*/
select b.booth_number,
b.booth_type,vba.market_date,
v.vendor_id,
v.vendor_name,
v.vendor_type 
from (
(farmers_market.booth as b
left join farmers_market.vendor_booth_assignments as vba 
on b.booth_number = vba.booth_number)
left join farmers_market.vendor as v on v.vendor_id = vba.vendor_id
)
order by b.booth_number, vba.market_date;

































/* showing the table names, type and the database engine of 
 all available tables in the schema
 */
select table_name, table_type, engine from information_schema.tables;
-- showing all the column names for a particular table
select column_name from information_schema.columns where table_name = "product";


















/* showcasing multiline comments
bla 
bla
bla
*/