/*Create table*/
CREATE TABLE tbl_Userpass (
    User_Id bigint PRIMARY KEY IDENTITY (1, 1),
    Username NVARCHAR (50) NOT NULL,
    Password NVARCHAR (50) NOT NULL
);

CREATE TABLE tbl_Grid (
    Grid_Id bigint PRIMARY KEY IDENTITY (1, 1),
	Grid_Name VARCHAR(255) NOT NULL,
    Crop VARCHAR(255) NOT NULL,
);

CREATE TABLE tbl_History (
    History_Id bigint PRIMARY KEY IDENTITY (1, 1),
    User_Id VARCHAR(255) NOT NULL,
    Grid_Id VARCHAR(255) NOT NULL,
	Record_Time DATETIME NOT NULL,
	Midpoint NVARCHAR(MAX) NOT NULL
);

INSERT INTO tbl_Userpass (Username,Password)
VALUES ('test', 'test');

/*Display*/
SELECT TOP (5) [User_Id]
      ,[Username]
      ,[Password]
  FROM [FYP].[dbo].[tbl_Userpass]

/*Delete*/
DELETE FROM tbl_Userpass WHERE User_Id='2' or Username='11111111';
