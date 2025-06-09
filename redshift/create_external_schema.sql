create external schema smartcity_ext
from data catalog
database 'smartcity_db'
iam_role 'arn:aws:iam::<your-account-id>:role/<your-glue-redshift-role>'
create external database if not exists;
