use fyp_transaction_data;
describe fyp_transaction_data.cleaned_transactions;
ALTER TABLE cleaned_transactions
ADD PRIMARY KEY (product_id);
DROP TABLE cleaned_transactions;

select * from cleaned_transactions where product_id=23521259265;

select count(*) from cleaned_transactions;
select * from cleaned_transactions;


