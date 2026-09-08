SET XACT_ABORT ON;

BEGIN TRANSACTION;

IF COL_LENGTH('dbo.Patients', 'age_months') IS NULL
   AND COL_LENGTH('dbo.Patients', 'age') IS NOT NULL
BEGIN
    EXEC sp_rename 'dbo.Patients.age', 'age_months', 'COLUMN';
END;

IF COL_LENGTH('dbo.Patients', 'age_months') IS NULL
BEGIN
    THROW 50001, 'No existe la columna dbo.Patients.age_months.', 1;
END;

DECLARE @invalid_age_count int;

EXEC sp_executesql
    N'SELECT @count = COUNT(*)
      FROM dbo.Patients
      WHERE age_months < 0 OR age_months > 216;',
    N'@count int OUTPUT',
    @count = @invalid_age_count OUTPUT;

IF @invalid_age_count > 0
    THROW 50002, 'Existen edades fuera del rango de 0 a 216 meses.', 1;

IF NOT EXISTS (
    SELECT 1
    FROM sys.check_constraints
    WHERE name = 'CK_Patients_age_months_range'
      AND parent_object_id = OBJECT_ID('dbo.Patients')
)
BEGIN
    EXEC sp_executesql N'
        ALTER TABLE dbo.Patients WITH CHECK
        ADD CONSTRAINT CK_Patients_age_months_range
            CHECK (age_months >= 0 AND age_months <= 216);';
END;

COMMIT TRANSACTION;
