# TESTS DESCRIPTION
# python main.py --help
#
# TESTS WITHOUT BLOCKCHAIN
#
# python main.py --help
 python main.py --type authentication --authentication-url http://127.0.0.1:5002 --jwt-secret 8f9a7c2e4d1b6a5f3c9d8e7f0a2b4c6d1e3f5a7b9c0d2e4f6a8b0c2d4e6f8a0 --roles-field roles --owner-role owner --customer-role customer --courier-role courier
# python main.py --type level0 --with-authentication --authentication-url http://127.0.0.1:5002 --owner-url http://127.0.0.1:5003 --customer-url http://127.0.0.1:5004
# python main.py --type level1 --with-authentication --authentication-url http://127.0.0.1:5002 --owner-url http://127.0.0.1:5003 --customer-url http://127.0.0.1:5004
# python main.py --type level2 --with-authentication --authentication-url http://127.0.0.1:5002 --customer-url http://127.0.0.1:5004 --courier-url http://127.0.0.1:5005 --owner-url http://127.0.0.1:5003
# python main.py --type level3 --with-authentication --authentication-url http://127.0.0.1:5002 --owner-url http://127.0.0.1:5003 --customer-url http://127.0.0.1:5004 --courier-url http://127.0.0.1:5005
 python main.py --type all --authentication-url http://127.0.0.1:5002 --jwt-secret 8f9a7c2e4d1b6a5f3c9d8e7f0a2b4c6d1e3f5a7b9c0d2e4f6a8b0c2d4e6f8a0 --roles-field roles --owner-role owner --customer-role customer --courier-role courier --with-authentication --owner-url http://127.0.0.1:5003 --customer-url http://127.0.0.1:5004 --courier-url http://127.0.0.1:5005
#
# TESTS WITH BLOCKCHAIN
#
# python main.py --type level1 --with-authentication --authentication-url http://127.0.0.1:5000 --jwt-secret JWT_SECRET_DEV_KEY --roles-field roles --owner-url http://127.0.0.1:5001 --customer-url http://127.0.0.1:5002 --with-blockchain --provider-url http://127.0.0.1:8545 --owner-private-key 0xb64be88dd6b89facf295f4fd0dda082efcbe95a2bb4478f5ee582b7efe88cf60
# python main.py --type level2 --with-authentication --authentication-url http://127.0.0.1:5000 --jwt-secret JWT_SECRET_DEV_KEY --roles-field roles --owner-url http://127.0.0.1:5001 --customer-url http://127.0.0.1:5002 --courier-url http://127.0.0.1:5003 --with-blockchain --provider-url http://127.0.0.1:8545 --owner-private-key 0xb64be88dd6b89facf295f4fd0dda082efcbe95a2bb4478f5ee582b7efe88cf60
# python main.py --type level3 --with-authentication --authentication-url http://127.0.0.1:5000 --jwt-secret JWT_SECRET_DEV_KEY --roles-field roles --owner-url http://127.0.0.1:5001 --customer-url http://127.0.0.1:5002 --courier-url http://127.0.0.1:5003 --with-blockchain --provider-url http://127.0.0.1:8545 --owner-private-key 0xb64be88dd6b89facf295f4fd0dda082efcbe95a2bb4478f5ee582b7efe88cf60
 python main.py --type all --authentication-url http://127.0.0.1:5002 --jwt-secret 8f9a7c2e4d1b6a5f3c9d8e7f0a2b4c6d1e3f5a7b9c0d2e4f6a8b0c2d4e6f8a0 --roles-field roles  --owner-role owner --customer-role customer --courier-role courier --with-authentication --owner-url http://127.0.0.1:5003 --customer-url http://127.0.0.1:5004 --courier-url http://127.0.0.1:5005 --with-blockchain --provider-url http://127.0.0.1:8545 --owner-private-key 0xb64be88dd6b89facf295f4fd0dda082efcbe95a2bb4478f5ee582b7efe88cf60

#(.venv) PS C:\Users\tijan\OneDrive\Desktop\iep_projekat_predaja\Tests> python -c "import ssl, certifi; print('using:', ssl.create_default_context().get_ca_certs() is not None, certifi.where())"

#STORE CLEAN UP
#----------------------------------------
#DELETE FROM order_products;
#DELETE FROM product_categories;
#DELETE FROM orders;
#DELETE FROM products;
#DELETE FROM categories;
#
#ALTER TABLE orders     AUTO_INCREMENT = 1;
#ALTER TABLE products   AUTO_INCREMENT = 1;
#ALTER TABLE categories AUTO_INCREMENT = 1;
#-- (and children too if you want)
#ALTER TABLE order_products    AUTO_INCREMENT = 1;
#ALTER TABLE product_categories AUTO_INCREMENT = 1;

#CERTIFICATE USER ENV VARIABLES
#----------------------------------------
#SSL_CERT_FILE
#C:\Users\tijan\OneDrive\Desktop\iep_projekat_predaja\.venv\Lib\site-packages\certifi\cacert.pem