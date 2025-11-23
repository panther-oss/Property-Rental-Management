
DROP DATABASE IF EXISTS propertyrental;
CREATE DATABASE propertyrental;
USE propertyrental;



-- Create owner table
CREATE TABLE owner (
    Owner_ID INT NOT NULL AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Phone VARCHAR(15),
    Email VARCHAR(100) UNIQUE,
    Bank_Account VARCHAR(20),
    PRIMARY KEY (Owner_ID)
);

-- Create property table
CREATE TABLE property (
    Property_ID INT NOT NULL AUTO_INCREMENT,
    Address VARCHAR(255),
    Size_Sqft INT,
    Property_Type VARCHAR(50),
    Booking_Status VARCHAR(20),
    Property_Cost FLOAT,
    City VARCHAR(50),
    Furnished TINYINT(1),
    Owner_ID INT,
    PRIMARY KEY (Property_ID),
    FOREIGN KEY (Owner_ID) REFERENCES owner(Owner_ID) ON DELETE CASCADE
);

-- Create tenant table
CREATE TABLE tenant (
    Tenant_ID INT NOT NULL AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Phone VARCHAR(15),
    Email VARCHAR(100) UNIQUE,
    Income FLOAT,
    PRIMARY KEY (Tenant_ID)
);

-- Create lease table
CREATE TABLE lease (
    Lease_ID INT NOT NULL AUTO_INCREMENT,
    Start_Date DATE,
    End_Date DATE,
    Monthly_Rent FLOAT,
    Security_Deposit FLOAT,
    Property_ID INT,
    Tenant_ID INT,
    PRIMARY KEY (Lease_ID),
    FOREIGN KEY (Property_ID) REFERENCES property(Property_ID) ON DELETE CASCADE,
    FOREIGN KEY (Tenant_ID) REFERENCES tenant(Tenant_ID) ON DELETE CASCADE
);

-- Create payment table
CREATE TABLE payment (
    Payment_ID INT NOT NULL AUTO_INCREMENT,
    Payment_Date DATE,
    Amount FLOAT,
    Mode_of_Payment VARCHAR(50),
    Status VARCHAR(20),
    Lease_ID INT,
    PRIMARY KEY (Payment_ID),
    FOREIGN KEY (Lease_ID) REFERENCES lease(Lease_ID) ON DELETE CASCADE
);

-- Create maintenance table
CREATE TABLE maintenance (
    Maintenance_ID INT NOT NULL AUTO_INCREMENT,
    Maintenance_Date DATE,
    Maintenance_Type VARCHAR(100),
    Cost FLOAT,
    Status VARCHAR(20) DEFAULT 'Pending',
    Property_ID INT,
    PRIMARY KEY (Maintenance_ID),
    FOREIGN KEY (Property_ID) REFERENCES property(Property_ID) ON DELETE CASCADE
);

-- Create complaint table
CREATE TABLE complaint (
    Complaint_ID INT NOT NULL AUTO_INCREMENT,
    Complaint_Date DATE,
    Status VARCHAR(50) NOT NULL DEFAULT 'Under Review',
    Tenant_ID INT,
    Property_ID INT,
    PRIMARY KEY (Complaint_ID),
    FOREIGN KEY (Tenant_ID) REFERENCES tenant(Tenant_ID) ON DELETE CASCADE,
    FOREIGN KEY (Property_ID) REFERENCES property(Property_ID) ON DELETE CASCADE
);

-- Create complaint_log table
CREATE TABLE complaint_log (
    Log_ID INT NOT NULL AUTO_INCREMENT,
    Complaint_ID INT,
    Logged_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Action VARCHAR(50),
    PRIMARY KEY (Log_ID),
    FOREIGN KEY (Complaint_ID) REFERENCES complaint(Complaint_ID) ON DELETE CASCADE
);

-- Create tenant_lease junction table
CREATE TABLE tenant_lease (
    Tenant_ID INT NOT NULL,
    Lease_ID INT NOT NULL,
    PRIMARY KEY (Tenant_ID, Lease_ID),
    FOREIGN KEY (Tenant_ID) REFERENCES tenant(Tenant_ID) ON DELETE CASCADE,
    FOREIGN KEY (Lease_ID) REFERENCES lease(Lease_ID) ON DELETE CASCADE
);


-- Insert Owners
INSERT INTO owner (Name, Phone, Email, Bank_Account) VALUES
('John Smith', '1234567890', 'john.smith@example.com', '1234567890123456'),
('Sarah Johnson', '2345678901', 'sarah.j@example.com', '2345678901234567'),
('Michael Brown', '3456789012', 'michael.b@example.com', '3456789012345678'),
('Emily Davis', '4567890123', 'emily.d@example.com', '4567890123456789'),
('Robert Wilson', '5678901234', 'robert.w@example.com', '5678901234567890');

-- Insert Properties
INSERT INTO property (Address, Size_Sqft, Property_Type, Booking_Status, Property_Cost, City, Furnished, Owner_ID) VALUES
('123 Main St, Apt 4B', 1200, 'Apartment', 'Available', 250000, 'New York', 1, 1),
('456 Oak Avenue', 2500, 'House', 'Available', 450000, 'Los Angeles', 0, 1),
('789 Pine Road, Unit 12', 900, 'Apartment', 'Available', 180000, 'Chicago', 1, 2),
('321 Elm Street', 3000, 'House', 'Available', 550000, 'Houston', 1, 2),
('654 Maple Drive', 1500, 'Condo', 'Available', 320000, 'Phoenix', 1, 3),
('987 Cedar Lane', 2200, 'House', 'Available', 480000, 'Philadelphia', 0, 3),
('147 Birch Court', 1100, 'Apartment', 'Available', 220000, 'San Antonio', 1, 4),
('258 Willow Way', 1800, 'Condo', 'Available', 380000, 'San Diego', 1, 4),
('369 Spruce St', 2800, 'House', 'Available', 520000, 'Dallas', 0, 5),
('741 Ash Boulevard', 1300, 'Apartment', 'Available', 270000, 'San Jose', 1, 5);

-- Insert Tenants
INSERT INTO tenant (Name, Phone, Email, Income) VALUES
('Alice Johnson', '1112223333', 'alice.j@email.com', 75000),
('Bob Williams', '2223334444', 'bob.w@email.com', 62000),
('Carol Martinez', '3334445555', 'carol.m@email.com', 58000),
('David Anderson', '4445556666', 'david.a@email.com', 82000),
('Emma Thomas', '5556667777', 'emma.t@email.com', 71000),
('Frank Garcia', '6667778888', 'frank.g@email.com', 65000),
('Grace Lee', '7778889999', 'grace.l@email.com', 78000),
('Henry Rodriguez', '8889990000', 'henry.r@email.com', 69000);

-- Insert Leases
INSERT INTO lease (Start_Date, End_Date, Monthly_Rent, Security_Deposit, Property_ID, Tenant_ID) VALUES
('2025-01-01', '2025-12-31', 2000, 4000, 1, 1),
('2025-02-01', '2026-01-31', 2500, 5000, 2, 2),
('2025-01-15', '2025-12-15', 1500, 3000, 3, 3),
('2025-03-01', '2026-02-28', 2800, 5600, 4, 4),
('2025-01-10', '2025-12-10', 2200, 4400, 5, 5);

-- Insert Payments
INSERT INTO payment (Payment_Date, Amount, Mode_of_Payment, Status, Lease_ID) VALUES
('2025-01-05', 2000, 'Bank Transfer', 'Completed', 1),
('2025-02-05', 2000, 'Credit Card', 'Completed', 1),
('2025-02-05', 2500, 'Bank Transfer', 'Completed', 2),
('2025-01-20', 1500, 'Check', 'Completed', 3),
('2025-03-05', 2800, 'Bank Transfer', 'Pending', 4),
('2025-01-15', 2200, 'Cash', 'Completed', 5);

-- Insert Maintenance Records
INSERT INTO maintenance (Maintenance_Date, Maintenance_Type, Cost, Status, Property_ID) VALUES
('2025-01-10', 'Plumbing Repair', 500, 'Completed', 1),
('2025-02-15', 'HVAC Service', 800, 'In Progress', 2),
('2025-01-20', 'Electrical Work', 650, 'Pending', 3),
('2025-03-01', 'Roof Repair', 1200, 'Pending', 4),
('2025-01-25', 'Painting', 900, 'Completed', 5);

-- Insert Complaints
INSERT INTO complaint (Complaint_Date, Status, Tenant_ID, Property_ID) VALUES
('2025-01-15', 'Resolved', 1, 1),
('2025-02-10', 'Under Review', 2, 2),
('2025-01-22', 'In Progress', 3, 3),
('2025-03-05', 'Under Review', 4, 4);

-- Insert Complaint Logs
INSERT INTO complaint_log (Complaint_ID, Action) VALUES
(1, 'Complaint registered'),
(1, 'Maintenance scheduled'),
(1, 'Issue resolved'),
(2, 'Complaint registered'),
(3, 'Complaint registered'),
(3, 'Investigation started');

-- Insert Tenant-Lease relationships
INSERT INTO tenant_lease (Tenant_ID, Lease_ID) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);



-- Trigger 1: Update property booking status after lease creation
DELIMITER //
CREATE TRIGGER update_booking_status_after_lease
AFTER INSERT ON lease
FOR EACH ROW
BEGIN
    UPDATE property
    SET Booking_Status = 'Rented'
    WHERE Property_ID = NEW.Property_ID;
END //
DELIMITER ;

-- Trigger 2: Update property status when maintenance is in progress
DELIMITER //
CREATE TRIGGER update_property_after_maintenance
AFTER INSERT ON maintenance
FOR EACH ROW
BEGIN
    IF NEW.Status = 'In Progress' THEN
        UPDATE property
        SET Booking_Status = 'Under Maintenance'
        WHERE Property_ID = NEW.Property_ID;
    END IF;
END //
DELIMITER ;

-- Trigger 3: Validate payment amount matches monthly rent
DELIMITER //
CREATE TRIGGER validate_payment_amount
BEFORE INSERT ON payment
FOR EACH ROW
BEGIN
    DECLARE rent_amount FLOAT;
    SELECT Monthly_Rent INTO rent_amount FROM lease WHERE Lease_ID = NEW.Lease_ID;
    IF NEW.Amount <> rent_amount THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Payment amount does not match monthly rent';
    END IF;
END //
DELIMITER ;



-- Trigger 4: Prevent deletion of property if it has active leases
DELIMITER //
CREATE TRIGGER prevent_property_delete_with_active_lease
BEFORE DELETE ON property
FOR EACH ROW
BEGIN
    DECLARE active_leases INT;
    SELECT COUNT(*) INTO active_leases
    FROM lease
    WHERE Property_ID = OLD.Property_ID
    AND CURDATE() BETWEEN Start_Date AND End_Date;
    
    IF active_leases > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cannot delete property with active leases';
    END IF;
END //
DELIMITER ;

-- Trigger 5: Validate lease dates
DELIMITER //
CREATE TRIGGER validate_lease_dates
BEFORE INSERT ON lease
FOR EACH ROW
BEGIN
    IF NEW.Start_Date >= NEW.End_Date THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Start date must be before end date';
    END IF;
END //
DELIMITER ;




-- Procedure 1: Get Property Revenue Report
DELIMITER //
CREATE PROCEDURE GetPropertyRevenue(IN property_id INT)
BEGIN
    SELECT 
        p.Property_ID,
        p.Address,
        p.Property_Type,
        o.Name as Owner_Name,
        COUNT(DISTINCT l.Lease_ID) as Total_Leases,
        SUM(pay.Amount) as Total_Revenue,
        AVG(l.Monthly_Rent) as Average_Rent,
        MAX(pay.Payment_Date) as Last_Payment_Date
    FROM property p
    LEFT JOIN owner o ON p.Owner_ID = o.Owner_ID
    LEFT JOIN lease l ON p.Property_ID = l.Property_ID
    LEFT JOIN payment pay ON l.Lease_ID = pay.Lease_ID
    WHERE p.Property_ID = property_id
    GROUP BY p.Property_ID, p.Address, p.Property_Type, o.Name;
END //
DELIMITER ;

-- Procedure 2: Get Tenant Payment History
DELIMITER //
CREATE PROCEDURE GetTenantPaymentHistory(IN tenant_id INT)
BEGIN
    SELECT 
        t.Tenant_ID,
        t.Name as Tenant_Name,
        t.Email,
        p.Address as Property_Address,
        l.Start_Date,
        l.End_Date,
        l.Monthly_Rent,
        pay.Payment_ID,
        pay.Payment_Date,
        pay.Amount,
        pay.Mode_of_Payment,
        pay.Status
    FROM tenant t
    LEFT JOIN lease l ON t.Tenant_ID = l.Tenant_ID
    LEFT JOIN property p ON l.Property_ID = p.Property_ID
    LEFT JOIN payment pay ON l.Lease_ID = pay.Lease_ID
    WHERE t.Tenant_ID = tenant_id
    ORDER BY pay.Payment_Date DESC;
END //
DELIMITER ;

-- Procedure 3: Get Monthly Rent Report
DELIMITER //
CREATE PROCEDURE GetMonthlyRentReport(IN report_month INT, IN report_year INT)
BEGIN
    SELECT 
        p.Property_ID,
        p.Address,
        t.Name as Tenant_Name,
        l.Monthly_Rent as Expected_Amount,
        COALESCE(SUM(pay.Amount), 0) as Received_Amount,
        (l.Monthly_Rent - COALESCE(SUM(pay.Amount), 0)) as Balance,
        CASE 
            WHEN COALESCE(SUM(pay.Amount), 0) >= l.Monthly_Rent THEN 'Paid'
            WHEN COALESCE(SUM(pay.Amount), 0) > 0 THEN 'Partial'
            ELSE 'Unpaid'
        END as Payment_Status
    FROM property p
    INNER JOIN lease l ON p.Property_ID = l.Property_ID
    INNER JOIN tenant t ON l.Tenant_ID = t.Tenant_ID
    LEFT JOIN payment pay ON l.Lease_ID = pay.Lease_ID 
        AND MONTH(pay.Payment_Date) = report_month 
        AND YEAR(pay.Payment_Date) = report_year
    WHERE l.Start_Date <= LAST_DAY(STR_TO_DATE(CONCAT(report_year, '-', report_month, '-01'), '%Y-%m-%d'))
        AND (l.End_Date IS NULL OR l.End_Date >= STR_TO_DATE(CONCAT(report_year, '-', report_month, '-01'), '%Y-%m-%d'))
    GROUP BY p.Property_ID, p.Address, t.Name, l.Monthly_Rent;
END //
DELIMITER ;



-- Procedure 4: Get Overdue Payments
DELIMITER //
CREATE PROCEDURE GetOverduePayments()
BEGIN
    SELECT 
        pay.Payment_ID,
        pay.Payment_Date,
        pay.Amount,
        t.Name as Tenant_Name,
        t.Phone as Tenant_Phone,
        p.Address as Property_Address,
        DATEDIFF(CURDATE(), pay.Payment_Date) as Days_Overdue
    FROM payment pay
    INNER JOIN lease l ON pay.Lease_ID = l.Lease_ID
    INNER JOIN tenant t ON l.Tenant_ID = t.Tenant_ID
    INNER JOIN property p ON l.Property_ID = p.Property_ID
    WHERE pay.Status = 'Pending'
    AND pay.Payment_Date < CURDATE()
    ORDER BY Days_Overdue DESC;
END //
DELIMITER ;


-- Procedure 5: Get All Pending Payments with Total
DELIMITER //
CREATE PROCEDURE GetAllPendingPayments()
BEGIN
    SELECT 
        pay.Payment_ID,
        pay.Payment_Date,
        pay.Amount,
        pay.Mode_of_Payment,
        pay.Status,
        pay.Lease_ID,
        t.Name as Tenant_Name,
        p.Address as Property_Address,
        NULL as Total_Pending_Amount
    FROM payment pay
    LEFT JOIN lease l ON pay.Lease_ID = l.Lease_ID
    LEFT JOIN tenant t ON l.Tenant_ID = t.Tenant_ID
    LEFT JOIN property p ON l.Property_ID = p.Property_ID
    WHERE pay.Status = 'Pending'
    
    UNION ALL
    
    SELECT 
        NULL, NULL, NULL, 'TOTAL', NULL, NULL, NULL, NULL,
        SUM(Amount) as Total_Pending_Amount
    FROM payment 
    WHERE Status = 'Pending';
END //
DELIMITER ;

============================

-- Function 1: Calculate Total Rent for Lease Period
DELIMITER //
CREATE FUNCTION CalculateTotalRent(lease_id INT)
RETURNS DECIMAL(10,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE total_rent DECIMAL(10,2);
    DECLARE monthly_rent DECIMAL(10,2);
    DECLARE months_count INT;
    DECLARE start_dt DATE;
    DECLARE end_dt DATE;
    
    SELECT Monthly_Rent, Start_Date, End_Date 
    INTO monthly_rent, start_dt, end_dt
    FROM lease 
    WHERE Lease_ID = lease_id;
    
    SET months_count = TIMESTAMPDIFF(MONTH, start_dt, end_dt);
    SET total_rent = monthly_rent * months_count;
    
    RETURN total_rent;
END //
DELIMITER ;

-- Function 2: Check if Tenant has Pending Payments
DELIMITER //
CREATE FUNCTION HasPendingPayments(tenant_id INT)
RETURNS BOOLEAN
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE pending_count INT;
    
    SELECT COUNT(*) INTO pending_count
    FROM payment pay
    INNER JOIN lease l ON pay.Lease_ID = l.Lease_ID
    WHERE l.Tenant_ID = tenant_id 
        AND pay.Status = 'Pending';
    
    RETURN pending_count > 0;
END //
DELIMITER ;

-- Function 3: Get Property Occupancy Rate for Owner
DELIMITER //
CREATE FUNCTION GetPropertyOccupancyRate(owner_id INT)
RETURNS DECIMAL(5,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE total_properties INT;
    DECLARE rented_properties INT;
    DECLARE occupancy_rate DECIMAL(5,2);
    
    SELECT COUNT(*) INTO total_properties
    FROM property
    WHERE Owner_ID = owner_id;
    
    SELECT COUNT(*) INTO rented_properties
    FROM property
    WHERE Owner_ID = owner_id 
        AND Booking_Status = 'Rented';
    
    IF total_properties > 0 THEN
        SET occupancy_rate = (rented_properties / total_properties) * 100;
    ELSE
        SET occupancy_rate = 0;
    END IF;
    
    RETURN occupancy_rate;
END //
DELIMITER ;

-- Function 4: Get Tenant Outstanding Balance
DELIMITER //
CREATE FUNCTION GetTenantOutstandingBalance(tenant_id INT)
RETURNS DECIMAL(10,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE total_expected DECIMAL(10,2);
    DECLARE total_paid DECIMAL(10,2);
    DECLARE outstanding DECIMAL(10,2);
    
    SELECT SUM(l.Monthly_Rent * TIMESTAMPDIFF(MONTH, l.Start_Date, IFNULL(l.End_Date, CURDATE())))
    INTO total_expected
    FROM lease l
    WHERE l.Tenant_ID = tenant_id;
    
    SELECT COALESCE(SUM(pay.Amount), 0)
    INTO total_paid
    FROM payment pay
    INNER JOIN lease l ON pay.Lease_ID = l.Lease_ID
    WHERE l.Tenant_ID = tenant_id 
        AND pay.Status = 'Completed';
    
    SET outstanding = COALESCE(total_expected, 0) - COALESCE(total_paid, 0);
    
    RETURN outstanding;
END //
DELIMITER ;

-- Function 5: Get Average Maintenance Cost by Property Type
DELIMITER //
CREATE FUNCTION GetAvgMaintenanceCostByType(property_type VARCHAR(50))
RETURNS DECIMAL(10,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE avg_cost DECIMAL(10,2);
    
    SELECT AVG(m.Cost) INTO avg_cost
    FROM maintenance m
    INNER JOIN property p ON m.Property_ID = p.Property_ID
    WHERE p.Property_Type = property_type;
    
    RETURN COALESCE(avg_cost, 0);
END //
DELIMITER ;

-- Function 6: Check if Property is Available
DELIMITER //
CREATE FUNCTION IsPropertyAvailable(property_id INT)
RETURNS BOOLEAN
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE booking_status VARCHAR(20);
    DECLARE is_available BOOLEAN;
    
    SELECT Booking_Status INTO booking_status
    FROM property
    WHERE Property_ID = property_id;
    
    SET is_available = (booking_status = 'Available');
    
    RETURN is_available;
END //
DELIMITER ;

