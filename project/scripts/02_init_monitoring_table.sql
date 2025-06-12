USE sales_company;

DROP TABLE IF EXISTS product_monitoring;
CREATE TABLE product_monitoring (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ProductID INT,
    ProductName VARCHAR(255),
    TotalSold INT,
    ThresholdDate DATETIME DEFAULT CURRENT_TIMESTAMP
);