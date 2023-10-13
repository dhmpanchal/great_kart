-- TABLE
CREATE TABLE "admin_honeypot_loginattempt" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "username" varchar(255) NULL, "session_key" varchar(50) NULL, "user_agent" text NULL, "timestamp" datetime NOT NULL, "path" text NULL, "ip_address" char(39) NULL);
CREATE TABLE "auth_group" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(150) NOT NULL UNIQUE);
CREATE TABLE "auth_group_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "auth_permission" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "codename" varchar(100) NOT NULL, "name" varchar(255) NOT NULL);
CREATE TABLE "django_admin_log" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "action_time" datetime NOT NULL, "object_id" text NULL, "object_repr" varchar(200) NOT NULL, "change_message" text NOT NULL, "content_type_id" integer NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" integer NOT NULL REFERENCES "tbl_accounts" ("id") DEFERRABLE INITIALLY DEFERRED, "action_flag" smallint unsigned NOT NULL CHECK ("action_flag" >= 0));
CREATE TABLE "django_content_type" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app_label" varchar(100) NOT NULL, "model" varchar(100) NOT NULL);
CREATE TABLE "django_migrations" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app" varchar(255) NOT NULL, "name" varchar(255) NOT NULL, "applied" datetime NOT NULL);
CREATE TABLE "django_session" ("session_key" varchar(40) NOT NULL PRIMARY KEY, "session_data" text NOT NULL, "expire_date" datetime NOT NULL);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE "tbl_accounts" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "password" varchar(128) NOT NULL, "first_name" varchar(50) NOT NULL, "last_name" varchar(50) NOT NULL, "username" varchar(50) NOT NULL UNIQUE, "email" varchar(100) NOT NULL UNIQUE, "phone" varchar(50) NOT NULL, "date_joined" datetime NOT NULL, "last_login" datetime NOT NULL, "is_admin" bool NOT NULL, "is_staff" bool NOT NULL, "is_superadmin" bool NOT NULL, "is_active" bool NOT NULL);
CREATE TABLE "tbl_cart" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "cart_id" varchar(250) NOT NULL, "date_added" date NOT NULL);
CREATE TABLE "tbl_categories" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "category_name" varchar(50) NOT NULL UNIQUE, "slug" varchar(100) NOT NULL UNIQUE, "description" text NOT NULL, "cat_image" varchar(100) NOT NULL);
CREATE TABLE "tbl_item_in_cart" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "quantity" integer NOT NULL, "cart_id" integer NULL REFERENCES "tbl_cart" ("id") DEFERRABLE INITIALLY DEFERRED, "product_id" integer NOT NULL REFERENCES "tbl_products" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" integer NULL REFERENCES "tbl_accounts" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "tbl_item_in_cart_variations" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "itemincart_id" integer NOT NULL REFERENCES "tbl_item_in_cart" ("id") DEFERRABLE INITIALLY DEFERRED, "productvariation_id" integer NOT NULL REFERENCES "tbl_product_variation" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "tbl_orders" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "order_number" varchar(255) NULL, "first_name" varchar(255) NULL, "last_name" varchar(255) NULL, "phone" varchar(255) NULL, "email" varchar(255) NULL, "address_line1" varchar(255) NULL, "address_line2" varchar(255) NULL, "city" varchar(255) NULL, "state" varchar(255) NULL, "country" varchar(255) NULL, "zip_code" varchar(255) NULL, "order_note" varchar(255) NULL, "order_total" real NOT NULL, "tax" real NOT NULL, "ip" varchar(255) NULL, "is_ordered" bool NOT NULL, "payment_id" integer NULL REFERENCES "tbl_payments" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" integer NULL REFERENCES "tbl_accounts" ("id") DEFERRABLE INITIALLY DEFERRED, "status" varchar(255) NOT NULL);
CREATE TABLE "tbl_order_line" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "quantity" integer NOT NULL, "product_price" real NOT NULL, "ordered" bool NOT NULL, "order_id" integer NOT NULL REFERENCES "tbl_orders" ("id") DEFERRABLE INITIALLY DEFERRED, "payment_id" integer NULL REFERENCES "tbl_payments" ("id") DEFERRABLE INITIALLY DEFERRED, "product_id" integer NULL REFERENCES "tbl_products" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" integer NULL REFERENCES "tbl_accounts" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "tbl_order_line_variation" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "orderline_id" integer NOT NULL REFERENCES "tbl_order_line" ("id") DEFERRABLE INITIALLY DEFERRED, "productvariation_id" integer NOT NULL REFERENCES "tbl_product_variation" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "tbl_payments" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "payment_id" varchar(255) NULL, "payment_method" varchar(255) NULL, "amount_paid" varchar(255) NULL, "status" varchar(255) NULL, "user_id" integer NOT NULL REFERENCES "tbl_accounts" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "tbl_products" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "product_name" varchar(200) NOT NULL UNIQUE, "slug" varchar(200) NOT NULL UNIQUE, "description" text NOT NULL, "price" integer NOT NULL, "images" varchar(100) NOT NULL, "stock" integer NOT NULL, "is_available" bool NOT NULL, "category_id" integer NOT NULL REFERENCES "tbl_categories" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "tbl_product_gallery" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "image" varchar(255) NOT NULL, "product_id" integer NOT NULL REFERENCES "tbl_products" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "tbl_product_variation" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "variation_category" varchar(255) NOT NULL, "variation_value" varchar(255) NOT NULL, "product_id" integer NOT NULL REFERENCES "tbl_products" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "tbl_review_rating" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "subject" varchar(100) NOT NULL, "review" text NOT NULL, "rating" real NOT NULL, "ip" varchar(20) NOT NULL, "status" bool NOT NULL, "product_id" integer NOT NULL REFERENCES "tbl_products" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" integer NOT NULL REFERENCES "tbl_accounts" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "tbl_user_profile" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "address_line_1" varchar(100) NOT NULL, "address_line_2" varchar(100) NOT NULL, "profile_picture" varchar(100) NOT NULL, "city" varchar(20) NOT NULL, "state" varchar(20) NOT NULL, "country" varchar(20) NOT NULL, "zip_code" varchar(255) NULL, "user_id" integer NOT NULL UNIQUE REFERENCES "tbl_accounts" ("id") DEFERRABLE INITIALLY DEFERRED);
 
-- INDEX
CREATE INDEX "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" ("group_id");
CREATE UNIQUE INDEX "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" ("group_id", "permission_id");
CREATE INDEX "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" ("permission_id");
CREATE INDEX "auth_permission_content_type_id_2f476e4b" ON "auth_permission" ("content_type_id");
CREATE UNIQUE INDEX "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" ("content_type_id", "codename");
CREATE INDEX "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" ("content_type_id");
CREATE INDEX "django_admin_log_user_id_c564eba6" ON "django_admin_log" ("user_id");
CREATE UNIQUE INDEX "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" ("app_label", "model");
CREATE INDEX "django_session_expire_date_a5c62663" ON "django_session" ("expire_date");
CREATE INDEX "tbl_item_in_cart_cart_id_70b3ddc0" ON "tbl_item_in_cart" ("cart_id");
CREATE INDEX "tbl_item_in_cart_product_id_4a4656d4" ON "tbl_item_in_cart" ("product_id");
CREATE INDEX "tbl_item_in_cart_user_id_e6a8dd4e" ON "tbl_item_in_cart" ("user_id");
CREATE INDEX "tbl_item_in_cart_variations_itemincart_id_54301ec6" ON "tbl_item_in_cart_variations" ("itemincart_id");
CREATE UNIQUE INDEX "tbl_item_in_cart_variations_itemincart_id_productvariation_id_b660852c_uniq" ON "tbl_item_in_cart_variations" ("itemincart_id", "productvariation_id");
CREATE INDEX "tbl_item_in_cart_variations_productvariation_id_ecbdab8a" ON "tbl_item_in_cart_variations" ("productvariation_id");
CREATE INDEX "tbl_order_line_order_id_e1abbf30" ON "tbl_order_line" ("order_id");
CREATE INDEX "tbl_order_line_payment_id_0b6251f2" ON "tbl_order_line" ("payment_id");
CREATE INDEX "tbl_order_line_product_id_9235a5b9" ON "tbl_order_line" ("product_id");
CREATE INDEX "tbl_order_line_user_id_6649cdce" ON "tbl_order_line" ("user_id");
CREATE INDEX "tbl_order_line_variation_orderline_id_c8e27324" ON "tbl_order_line_variation" ("orderline_id");
CREATE UNIQUE INDEX "tbl_order_line_variation_orderline_id_productvariation_id_9353f6d6_uniq" ON "tbl_order_line_variation" ("orderline_id", "productvariation_id");
CREATE INDEX "tbl_order_line_variation_productvariation_id_97de09cd" ON "tbl_order_line_variation" ("productvariation_id");
CREATE INDEX "tbl_orders_payment_id_0c442fd7" ON "tbl_orders" ("payment_id");
CREATE INDEX "tbl_orders_user_id_0deb6338" ON "tbl_orders" ("user_id");
CREATE INDEX "tbl_payments_user_id_a821aa7b" ON "tbl_payments" ("user_id");
CREATE INDEX "tbl_product_gallery_product_id_36f0ea52" ON "tbl_product_gallery" ("product_id");
CREATE INDEX "tbl_product_variation_product_id_5cbc8f50" ON "tbl_product_variation" ("product_id");
CREATE INDEX "tbl_products_category_id_ae7e83fd" ON "tbl_products" ("category_id");
CREATE INDEX "tbl_review_rating_product_id_9cdf1bf1" ON "tbl_review_rating" ("product_id");
CREATE INDEX "tbl_review_rating_user_id_46a07ec3" ON "tbl_review_rating" ("user_id");
 
-- TRIGGER
 
-- VIEW
 
