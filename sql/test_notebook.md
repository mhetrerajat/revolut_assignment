<!-- -->
>     -- TASK DESCRIPTION
>     -- Given the transactions table and table containing exchange rates:
>     
>     -- 1. Write down a query that gives us a breakdown of spend in GBP by each user.
>     -- Use the exchange rate with largest timestamp less or equal then transaction timestamp.
>     
>     -- explain analyze
>     
>     drop table if exists exchange_rates;
>     create table exchange_rates(
>     ts timestamp without time zone,
>     from_currency varchar(3),
>     to_currency varchar(3),
>     rate numeric
>     );
>     
>     truncate table exchange_rates;
>     insert into exchange_rates
>     values
>     ('2018-04-01 00:00:00', 'USD', 'GBP', '0.71'),
>     ('2018-04-01 00:00:05', 'USD', 'GBP', '0.82'),
>     ('2018-04-01 00:01:00', 'USD', 'GBP', '0.92'),
>     ('2018-04-01 01:02:00', 'USD', 'GBP', '0.62'),
>     
>     ('2018-04-01 02:00:00', 'USD', 'GBP', '0.71'),
>     ('2018-04-01 03:00:05', 'USD', 'GBP', '0.82'),
>     ('2018-04-01 04:01:00', 'USD', 'GBP', '0.92'),
>     ('2018-04-01 04:22:00', 'USD', 'GBP', '0.62'),
>     
>     ('2018-04-01 00:00:00', 'EUR', 'GBP', '1.71'),
>     ('2018-04-01 01:00:05', 'EUR', 'GBP', '1.82'),
>     ('2018-04-01 01:01:00', 'EUR', 'GBP', '1.92'),
>     ('2018-04-01 01:02:00', 'EUR', 'GBP', '1.62'),
>     
>     ('2018-04-01 02:00:00', 'EUR', 'GBP', '1.71'),
>     ('2018-04-01 03:00:05', 'EUR', 'GBP', '1.82'),
>     ('2018-04-01 04:01:00', 'EUR', 'GBP', '1.92'),
>     ('2018-04-01 05:22:00', 'EUR', 'GBP', '1.62'),
>     
>     ('2018-04-01 05:22:00', 'EUR', 'HUF', '0.062')
>     ;
>     
>     
>     -- Transactions
>     
>     drop table if exists transactions;
>     create table transactions (
>     ts timestamp without time zone,
>     user_id int,
>     currency varchar(3),
>     amount numeric
>     );
>     
>     truncate table transactions;
>     insert into transactions
>     values
>     ('2018-04-01 00:00:00', 1, 'EUR', 2.45),
>     ('2018-04-01 01:00:00', 1, 'EUR', 8.45),
>     ('2018-04-01 01:30:00', 1, 'USD', 3.5),
>     ('2018-04-01 20:00:00', 1, 'EUR', 2.45),
>     
>     ('2018-04-01 00:30:00', 2, 'USD', 2.45),
>     ('2018-04-01 01:20:00', 2, 'USD', 0.45),
>     ('2018-04-01 01:40:00', 2, 'USD', 33.5),
>     ('2018-04-01 18:00:00', 2, 'EUR', 12.45),
>     
>     ('2018-04-01 18:01:00', 3, 'GBP', 2),
>     
>     ('2018-04-01 00:01:00', 4, 'USD', 2),
>     ('2018-04-01 00:01:00', 4, 'GBP', 2)
>     ;
>     

> 
> <pre>
> ✓
> 
> ✓
> 
> ✓
> 
17 rows affected
> 
> ✓
> 
> ✓
> 
> ✓
> 
11 rows affected
> </pre>

<!-- -->
>     SELECT * from transactions order by transactions.user_id asc;
> 
> <pre>
> ts                  | user_id | currency | amount
> :------------------ | ------: | :------- | -----:
> 2018-04-01 00:00:00 |       1 | EUR      |   2.45
> 2018-04-01 01:00:00 |       1 | EUR      |   8.45
> 2018-04-01 01:30:00 |       1 | USD      |    3.5
> 2018-04-01 20:00:00 |       1 | EUR      |   2.45
> 2018-04-01 00:30:00 |       2 | USD      |   2.45
> 2018-04-01 01:20:00 |       2 | USD      |   0.45
> 2018-04-01 01:40:00 |       2 | USD      |   33.5
> 2018-04-01 18:00:00 |       2 | EUR      |  12.45
> 2018-04-01 18:01:00 |       3 | GBP      |      2
> 2018-04-01 00:01:00 |       4 | USD      |      2
> 2018-04-01 00:01:00 |       4 | GBP      |      2
> </pre>

<!-- -->
>     SELECT * from exchange_rates;
> 
> <pre>
> ts                  | from_currency | to_currency |  rate
> :------------------ | :------------ | :---------- | ----:
> 2018-04-01 00:00:00 | USD           | GBP         |  0.71
> 2018-04-01 00:00:05 | USD           | GBP         |  0.82
> 2018-04-01 00:01:00 | USD           | GBP         |  0.92
> 2018-04-01 01:02:00 | USD           | GBP         |  0.62
> 2018-04-01 02:00:00 | USD           | GBP         |  0.71
> 2018-04-01 03:00:05 | USD           | GBP         |  0.82
> 2018-04-01 04:01:00 | USD           | GBP         |  0.92
> 2018-04-01 04:22:00 | USD           | GBP         |  0.62
> 2018-04-01 00:00:00 | EUR           | GBP         |  1.71
> 2018-04-01 01:00:05 | EUR           | GBP         |  1.82
> 2018-04-01 01:01:00 | EUR           | GBP         |  1.92
> 2018-04-01 01:02:00 | EUR           | GBP         |  1.62
> 2018-04-01 02:00:00 | EUR           | GBP         |  1.71
> 2018-04-01 03:00:05 | EUR           | GBP         |  1.82
> 2018-04-01 04:01:00 | EUR           | GBP         |  1.92
> 2018-04-01 05:22:00 | EUR           | GBP         |  1.62
> 2018-04-01 05:22:00 | EUR           | HUF         | 0.062
> </pre>

<!-- -->
>     -- Find conversion rates for each transaction
>     SELECT *,
>            COALESCE(
>                       (SELECT rate
>                        FROM exchange_rates AS e
>                        WHERE e.ts <= t.ts
>                          AND e.from_currency = t.currency
>                          AND e.to_currency = 'GBP'
>                        ORDER BY e.ts DESC
>                        LIMIT 1), 1) AS conversion_rate
>     FROM transactions AS t;
> 
> <pre>
> ts                  | user_id | currency | amount | conversion_rate
> :------------------ | ------: | :------- | -----: | --------------:
> 2018-04-01 00:00:00 |       1 | EUR      |   2.45 |            1.71
> 2018-04-01 01:00:00 |       1 | EUR      |   8.45 |            1.71
> 2018-04-01 01:30:00 |       1 | USD      |    3.5 |            0.62
> 2018-04-01 20:00:00 |       1 | EUR      |   2.45 |            1.62
> 2018-04-01 00:30:00 |       2 | USD      |   2.45 |            0.92
> 2018-04-01 01:20:00 |       2 | USD      |   0.45 |            0.62
> 2018-04-01 01:40:00 |       2 | USD      |   33.5 |            0.62
> 2018-04-01 18:00:00 |       2 | EUR      |  12.45 |            1.62
> 2018-04-01 18:01:00 |       3 | GBP      |      2 |               1
> 2018-04-01 00:01:00 |       4 | USD      |      2 |            0.92
> 2018-04-01 00:01:00 |       4 | GBP      |      2 |               1
> </pre>

<!-- -->
>     -- Spent by each user in GBP
>     SELECT t.user_id, (t.amount * COALESCE((select rate from exchange_rates as e 
>                     where e.ts <= t.ts 
>                     and e.from_currency = t.currency 
>                     and e.to_currency = 'GBP'
>                     order by e.ts desc 
>                     limit 1), 1))
>          as spent_in_gbp FROM transactions as t
> 
> <pre>
> user_id | spent_in_gbp
> ------: | -----------:
>       1 |       4.1895
>       1 |      14.4495
>       1 |        2.170
>       1 |       3.9690
>       2 |       2.2540
>       2 |       0.2790
>       2 |       20.770
>       2 |      20.1690
>       3 |            2
>       4 |         1.84
>       4 |            2
> </pre>

<!-- -->
>     -- Total spent in gbp for each user
>     -- Actual solution for task
>     SELECT user_id,
>            SUM(spent_in_gbp) AS total_spent_gbp
>     FROM   (SELECT t.user_id,
>                    ( t.amount * COALESCE((SELECT rate
>                                           FROM   exchange_rates AS e
>                                           WHERE  e.ts <= t.ts
>                                                  AND e.from_currency = t.currency
>                                                  AND e.to_currency = 'GBP'
>                                           ORDER  BY e.ts DESC
>                                           LIMIT  1), 1) ) AS spent_in_gbp
>             FROM   transactions AS t) AS transactions_in_gbp
>     GROUP  BY transactions_in_gbp.user_id
>     ORDER  BY transactions_in_gbp.user_id ASC;  
> 
> <pre>
> user_id | total_spent_gbp
> ------: | --------------:
>       1 |         24.7780
>       2 |         43.4720
>       3 |               2
>       4 |            3.84
> </pre>

*db<>fiddle [here](https://dbfiddle.uk/?rdbms=postgres_9.6&fiddle=71a3cf754595827bc2a3d080ce1f05cc)*