**Odoo Client App Project Setup**

**Prerequisites**

Python 3.x
PostgreSQL
Odoo 16/17
Git


**Installation Steps**

**1. Clone the repository**

cd OdooProject

**2. Install Dependencies**
Make sure to have Odoo dependencies installed. You can use the following command to install the necessary Python packages:
pip install -r requirements.txt

**3. Set up PostgreSQL**

Consider the below ; 

Install PostgreSQL and create a database:
sudo -u postgres psql
CREATE DATABASE odoo_db;
CREATE USER odoo_user WITH PASSWORD 'yourpassword';
ALTER ROLE odoo_user SET client_encoding TO 'utf8';
ALTER ROLE odoo_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE odoo_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE odoo_db TO odoo_user;

**4. Configure Odoo**
Create the Odoo configuration file (odoo.conf) in the root directory:
db_host = localhost
db_port = 5432
db_user = odoo_user
db_password = yourpassword
addons_path = addons
data_dir = /var/lib/odoo
logfile = /var/log/odoo/odoo.log

**5. Run Odoo**
odoo-bin --config=odoo.conf
