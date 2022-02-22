-- create tables
CREATE TABLE furniture.USER(
    id int auto_increment NOT NULL PRIMARY KEY,
    name VARCHAR(60) UNIQUE NOT NULL,
    email VARCHAR(60) UNIQUE NOT NULL,
    password VARCHAR(64) NOT NULL,
    admin_flag BOOLEAN default 0 NULL
);

CREATE TABLE furniture.CONDITION(
    id int auto_increment NOT NULL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE furniture.CATEGORY(
    id int auto_increment NOT NULL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);


CREATE TABLE furniture.PRODUCT(
    id int auto_increment NOT NULL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    price DECIMAL(20, 2) NOT NULL,
    condition_id int DEFAULT NULL,
    category_id int DEFAULT NULL,
    description VARCHAR(255),
    image_name VARCHAR(50) DEFAULT NULL,
    owner int NOT NULL,

    FOREIGN KEY (owner) 
        REFERENCES furniture.USER(id)
        ON DELETE CASCADE,

    FOREIGN KEY (condition_id)
        REFERENCES furniture.CONDITION(id)
        ON DELETE SET NULL,

    FOREIGN KEY (category_id)
        REFERENCES furniture.CATEGORY(id)
        ON DELETE SET NULL
);


-- INSER DATA
INSERT INTO furniture.USER (id, name, email, password, admin_flag) VALUES (1, 'admin', 'admin@gmail.com', 'ffe4a55050bebf76d64ca21e16357ac3347dcf8c6a52d93924aa5c0397b6626e', 1); 
INSERT INTO furniture.USER (id, name, email, password, admin_flag) VALUES (2, 'Mary p.', 'mary@gmail.com', '7c848d701c8114d9c5b7ad28b29e0ef0a6a03e052cf1771eac7b05a602f55d9d', 0); 
INSERT INTO furniture.USER (id, name, email, password, admin_flag) VALUES (3, 'Simão dinis', 'simaod@homail.com', 'bfe735eaad58272c4d7fb5b922ae78d278ee93d7663d0c9e4cb87b7572aadb01', 0); 


-- conditions
INSERT INTO furniture.CONDITION (id, name) VALUES (1, 'Mint');
INSERT INTO furniture.CONDITION (id, name) VALUES (2, 'Used');
INSERT INTO furniture.CONDITION (id, name) VALUES (3, 'Wrecked');


-- categories
INSERT INTO furniture.CATEGORY(id, name) VALUES(1, 'Bar furniture');
INSERT INTO furniture.CATEGORY(id, name) VALUES(2, 'Bedroom');
INSERT INTO furniture.CATEGORY(id, name) VALUES(3, 'Bookcases & Home offices');
INSERT INTO furniture.CATEGORY(id, name) VALUES(4, 'Kitchen & cupboards');
INSERT INTO furniture.CATEGORY(id, name) VALUES(5, 'Livingroom');
INSERT INTO furniture.CATEGORY(id, name) VALUES(6, 'Chairs');


-- products
INSERT INTO furniture.PRODUCT (name, price, condition_id, category_id, description, image_name, owner) VALUES ('NORDVIKEN', 995.0, 1, 1, 'Bar table, 140x80 cm', 'image_1.png', 1);
INSERT INTO furniture.PRODUCT (name, price, condition_id, category_id, description, image_name, owner) VALUES ('NORDVIKEN / NORDVIKEN', 2095.0, 1, 1,'Bar table and 4 bar stools', 'image_2.png', 1);
INSERT INTO furniture.PRODUCT (name, price, condition_id, category_id, description, image_name, owner) VALUES ('NORBERG', 225.0, 1, 1, 'Wall-mounted drop-leaf table, 74x60 cm', 'image_3.png', 1);
INSERT INTO furniture.PRODUCT (name, price, condition_id, category_id, description, image_name, owner) VALUES ('INGOLF', 345.0, 1, 1, 'Bar stool with backrest, 63 cm', 'image_4.png', 1);
INSERT INTO furniture.PRODUCT (name, price, condition_id, category_id, description, image_name, owner) VALUES ('FRANKLIN', 129.0, 1, 1, 'Bar stool with backrest, foldable, 63 cm', 'image_5.png', 1);
INSERT INTO furniture.PRODUCT (name, price, condition_id, category_id, description, image_name, owner) VALUES ('MINNEN', 395.0, 1, 2, 'Bed frame with slatted bed base, 80x200 cm', 'image_6.png', 1);
INSERT INTO furniture.PRODUCT (name, price, condition_id, category_id, description, image_name, owner) VALUES ('BRIMNES', 895.0, 1, 2, 'Bed frame w storage and headboard, 90x200 cm', 'image_7.png', 1);
INSERT INTO furniture.PRODUCT (name, price, condition_id, category_id, description, image_name, owner) VALUES ('SMÃ…GÃ–RA', 595.0, 1, 2, 'Cot, 60x120 cm', 'image_8.png', 1);
INSERT INTO furniture.PRODUCT (name, price, condition_id, category_id, description, image_name, owner) VALUES ('SLÃ„KT', 540.0, 1, 2, 'Bed frame with slatted bed base, 80x200 cm', 'image_9.png', 1);
INSERT INTO furniture.PRODUCT (name, price, condition_id, category_id, description, image_name, owner) VALUES ('LEIRVIK', 1195.0, 1, 2, 'Bed frame, 180x200 cm', 'image_10.png', 1);
INSERT INTO furniture.PRODUCT (name, price, condition_id, category_id, description, image_name, owner) VALUES ('JONAXEL', 135.0, 1, 3, 'Frame with mesh baskets, 25x51x70 cm', 'image_11.png', 1);
INSERT INTO furniture.PRODUCT (name, price, condition_id, category_id, description, image_name, owner) VALUES ('KOLBJÃ–RN', 345.0, 1, 3, 'Cabinet in/outdoor, 80x81 cm', 'image_12.png', 1);
INSERT INTO furniture.PRODUCT (name, price, condition_id, category_id, description, image_name, owner) VALUES ('GERSBY', 95.0, 2, 3, 'Bookcase, 60x180 cm', 'image_13.png', 1);
INSERT INTO furniture.PRODUCT (name, price, condition_id, category_id, description, image_name, owner) VALUES ('KALLAX', 115.0, 1, 3, 'Shelving unit, 77x77 cm', 'image_14.png', 1);
INSERT INTO furniture.PRODUCT (name, price, condition_id, category_id, description, image_name, owner) VALUES ('LACK', 199.0, 1, 3, 'Wall shelf unit, 30x190 cm', 'image_15.png', 1);
INSERT INTO furniture.PRODUCT (name, price, condition_id, category_id, description, image_name, owner) VALUES ('IVAR', 295.0, 3, 4, 'Cabinet, 80x30x83 cm', 'image_16.png', 1);
INSERT INTO furniture.PRODUCT (name, price, condition_id, category_id, description, image_name, owner) VALUES ('SYVDE', 595.0, 3, 4, 'Cabinet with glass doors, 100x123 cm', 'image_17.png', 1);
INSERT INTO furniture.PRODUCT (name, price, condition_id, category_id, description, image_name, owner) VALUES ('EKET', 377.0, 3, 4, 'Cabinet combination with feet, 70x25x107 cm', 'image_18.png', 1);
INSERT INTO furniture.PRODUCT (name, price, condition_id, category_id, description, image_name, owner) VALUES ('LIXHULT', 175.0, 3, 4, 'Cabinet, 60x35 cm', 'image_19.png', 1);
INSERT INTO furniture.PRODUCT (name, price, condition_id, category_id, description, image_name, owner) VALUES ('BILLY / OXBERG', 195.0, 3, 4, 'Bookcase with door, 40x30x106 cm', 'image_20.png', 2);
INSERT INTO furniture.PRODUCT (name, price, condition_id, category_id, description, image_name, owner) VALUES ('NORRÃ…KER', 295.0, 3, 5, 'Bench, 103 cm', 'image_21.png', 2);
INSERT INTO furniture.PRODUCT (name, price, condition_id, category_id, description, image_name, owner) VALUES ('NORRÃ…KER', 145.0, 3, 5, 'Stool, 45 cm', 'image_22.png', 2);
INSERT INTO furniture.PRODUCT (name, price, condition_id, category_id, description, image_name, owner) VALUES ('NORRÃ…KER', 596.0, 3, 5, 'Table, 125x74 cm', 'image_23.png', 2);
INSERT INTO furniture.PRODUCT (name, price, condition_id, category_id, description, image_name, owner) VALUES ('STENSELE', 450.0, 3, 5, 'Table, 70x70 cm', 'image_24.png', 2);
INSERT INTO furniture.PRODUCT (name, price, condition_id, category_id, description, image_name, owner) VALUES ('NORRÃ…KER', 395.0, 2, 5, 'Table, 74x74 cm', 'image_25.png', 2);
INSERT INTO furniture.PRODUCT (name, price, condition_id, category_id, description, image_name, owner) VALUES ('MALINDA', 25.0, 2, 6, 'Chair cushion, 40/35x38x7 cm', 'image_26.png', 2);
INSERT INTO furniture.PRODUCT (name, price, condition_id, category_id, description, image_name, owner) VALUES ('BINGSTA', 595.0, 2, 6, 'Armchair', 'image_27.png', 2);
INSERT INTO furniture.PRODUCT (name, price, condition_id, category_id, description, image_name, owner) VALUES ('PELLO', 195.0, 2, 6, 'Armchair', 'image_28.png', 2);
INSERT INTO furniture.PRODUCT (name, price, condition_id, category_id, description, image_name, owner) VALUES ('FANBYN', 295.0, 2, 6, 'Chair with armrests', 'image_29.png', 2);
INSERT INTO furniture.PRODUCT (name, price, condition_id, category_id, description, image_name, owner) VALUES ('MARIUS', 25.0, 2, 6, 'Stool', 'image_30.png', 2);
