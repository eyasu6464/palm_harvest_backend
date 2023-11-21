CREATE TABLE Branch(
    branchid INT PRIMARY KEY,
    branchname VARCHAR(50),
    city VARCHAR(50),
    address_longitude VARCHAR(50),
    address_latitude VARCHAR(50),
);
CREATE TABLE User (
    userid INT PRIMARY KEY,
    branchid INT,
    user_type VARCHAR(50),
    address VARCHAR(50),
    status VARCHAR(50),
    FOREIGN KEY (branchid) REFERENCES (Branch)
);
CREATE TABLE Image(
    imageid INT PRIMARY KEY,
    harvester INT,
    image_created TIMESTAMP,
    image_uploaded TIMESTAMP,
    FOREIGN KEY (harvester) REFERENCES User(userid)

);
CREATE TABLE PalmDetail(
    palmid INT PRIMARY KEY,
    quality VARCHAR(50),
    imageid INT,
    real varchar(50),
    predicted boolean,
    x1_coordinate varchar(50),
    y1_coordinate varchar(50),
    x2_coordinate varchar(50),
    y2_coordinate varchar(50),
    palm_image_uploaded TIMESTAMP,
    FOREIGN KEY (palmid) REFERENCES Image(imageid)
);