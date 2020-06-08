CREATE TABLE `kloans_loan` (
  `Loan_Id` CHAR(36),
  `Financial_Institution_Id` bigint,
  `Loan_Product_Id` CHAR(36),
  `Loan_Status` CHAR(25),
  `Original_Principal` DECIMAL(19,2),
  `Interest_Rate` DECIMAL(19,8),
  `Term_Length_In_Periods` INTEGER,
  `Origination_Date` DATE,
  `First_Payment_Date` DATE,
  `Maturity_Date` DATE,
  `Installment_Amount` DECIMAL(19,2),
  `Has_AutoPay` BIT,
  `AutoPay_Amount` DECIMAL(19,2),
  `Available_TakeBack_Balance` DECIMAL(19,2),
  `Current_Principal_Balance` DECIMAL(19,2),
  `Next_Due_Date` DATE,
  `Paid_Off_Date` DATE,
  `Charged_Off_Date` DATE,
  `Charged_Off_Amount` DECIMAL(19,2),
  `Delinquent_Days` INTEGER,
  `Delinquent_Amount` DECIMAL(19,2),
  `Payment_Frequency` VARCHAR(25),
  `Is_Fi_Employee_Loan` BIT,
  `Loan_Origination_Record_Id` VARCHAR(50),
  `Kloans_Internal_Account_Number` CHAR(11),
  `Branch` VARCHAR(50),
  `Loan_Officer` VARCHAR(50),
  PRIMARY KEY (`Loan_Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE `kloans_loan_applicant` (
  `Loan_Applicant_Id` CHAR(36),
  `Loan_Id` CHAR(36),
  `Consumer_Id` CHAR(36),
  `Applicant_type` VARCHAR(50),
  `Birth_Date` DATE
  `First_Name` VARCHAR(100),
  `Middle_name` VARCHAR(100),
  `Last_Name` VARCHAR(100),
  `Tax_Id` VARCHAR(10),
  `Email_Address` VARCHAR(255),
  `Home_Phone` VARCHAR(100),
  `Mobile_Phone` VARCHAR(100),
  `Work_Phone` VARCHAR(100),
  `Core_Customer_Id` VARCHAR(50),
  `Credit_Score` Integer,
 PRIMARY KEY (`Loan_Applicant_Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE `kloans_loan_applicant_address` (
  `Loan_Applicant_Address_Id` CHAR(36),
  `Loan_Applicant_Id` CHAR(36),
  `Loan_Applicant_Address_Type` VARCHAR(50),
  `Address_Line-1` VARCHAR(100),
  `Address_Line_2` VARCHAR(100),
  `City` VARCHAR(100),
  `State` VARCHAR(100),
  `Postal_Code` VARCHAR(100),
   PRIMARY KEY (`Loan_Applicant_Address_Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE `kloans_loan_product` (
  `Loan_Product_Id` BIGINT,
  `Loan_Type` VARCHAR(50),
  `Asset_Structure` VARCHAR(50),
  `Product_Code` VARCHAR(50),
  `Description` VARCHAR(50),
  `Is_Active` BIT,
 PRIMARY KEY (`Loan_Product_Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
