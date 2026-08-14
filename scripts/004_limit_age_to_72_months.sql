SET XACT_ABORT ON;

BEGIN TRANSACTION;

IF EXISTS (SELECT 1 FROM dbo.Patients WHERE age_months < 0 OR age_months > 72)
    THROW 50004, 'Existen pacientes fuera del rango de 0 a 72 meses.', 1;

IF EXISTS (SELECT 1 FROM dbo.Evaluations WHERE edad_meses < 0 OR edad_meses > 72)
    THROW 50005, 'Existen evaluaciones fuera del rango de 0 a 72 meses.', 1;

IF EXISTS (
    SELECT 1 FROM sys.check_constraints
    WHERE name = 'CK_Patients_age_months_range'
      AND parent_object_id = OBJECT_ID('dbo.Patients')
)
    ALTER TABLE dbo.Patients DROP CONSTRAINT CK_Patients_age_months_range;

ALTER TABLE dbo.Patients WITH CHECK
ADD CONSTRAINT CK_Patients_age_months_range
    CHECK (age_months >= 0 AND age_months <= 72);

IF EXISTS (
    SELECT 1 FROM sys.check_constraints
    WHERE name = 'CK_Evaluations_edad_meses_range'
      AND parent_object_id = OBJECT_ID('dbo.Evaluations')
)
    ALTER TABLE dbo.Evaluations DROP CONSTRAINT CK_Evaluations_edad_meses_range;

ALTER TABLE dbo.Evaluations WITH CHECK
ADD CONSTRAINT CK_Evaluations_edad_meses_range
    CHECK (edad_meses >= 0 AND edad_meses <= 72);

COMMIT TRANSACTION;
