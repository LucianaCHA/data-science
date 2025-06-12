DELIMITER $$
CREATE TRIGGER trigger_product_threshold_200k
AFTER INSERT ON sales
FOR EACH ROW
BEGIN
    DECLARE total_sales INT;

    SELECT SUM(Quantity)
    INTO total_sales
    FROM sales
    WHERE ProductID = NEW.ProductID;

    IF total_sales > 200000 THEN
        IF NOT EXISTS (
            SELECT 1 FROM product_monitoring
            WHERE ProductID = NEW.ProductID
        ) THEN
            INSERT INTO product_monitoring (
                ProductID,
                productName,
                TotalSold
            )
            SELECT 
                ProductID,
                ProductName,
                total_sales
            FROM products
            WHERE ProductID = NEW.ProductID;
        END IF;
    END IF;

END$$

DELIMITER ;