SELECT user_id,
       SUM(spent_in_gbp) AS total_spent_gbp
FROM   (SELECT t.user_id,
               ( t.amount * COALESCE((SELECT rate
                                      FROM   exchange_rates AS e
                                      WHERE  e.ts <= t.ts
                                             AND e.from_currency = t.currency
                                             AND e.to_currency = 'GBP'
                                      ORDER  BY e.ts DESC
                                      LIMIT  1), 1) ) AS spent_in_gbp
        FROM   transactions AS t) AS transactions_in_gbp
GROUP  BY transactions_in_gbp.user_id
ORDER  BY transactions_in_gbp.user_id ASC;  
