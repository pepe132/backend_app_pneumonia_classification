SET XACT_ABORT ON;

BEGIN TRANSACTION;

IF EXISTS (SELECT 1 FROM dbo.Evaluations)
   AND (
       COL_LENGTH('dbo.Evaluations', 'edad_meses') IS NULL
       OR COL_LENGTH('dbo.Evaluations', 'peso_kg') IS NULL
       OR COL_LENGTH('dbo.Evaluations', 'vomita_todo') IS NULL
       OR COL_LENGTH('dbo.Evaluations', 'glasgow') IS NULL
       OR COL_LENGTH('dbo.Evaluations', 'dias_dificultad_respiratoria') IS NULL
       OR COL_LENGTH('dbo.Evaluations', 'dolor_toracico') IS NULL
   )
BEGIN
    THROW 50003, 'Evaluations contiene filas; se requiere definir un backfill antes de agregar campos obligatorios.', 1;
END;

IF COL_LENGTH('dbo.Evaluations', 'edad_meses') IS NULL
    ALTER TABLE dbo.Evaluations ADD edad_meses int NOT NULL;

IF COL_LENGTH('dbo.Evaluations', 'peso_kg') IS NULL
    ALTER TABLE dbo.Evaluations ADD peso_kg float NOT NULL;

IF COL_LENGTH('dbo.Evaluations', 'vomita_todo') IS NULL
    ALTER TABLE dbo.Evaluations ADD vomita_todo bit NOT NULL;

IF COL_LENGTH('dbo.Evaluations', 'glasgow') IS NULL
    ALTER TABLE dbo.Evaluations ADD glasgow int NOT NULL;

IF COL_LENGTH('dbo.Evaluations', 'dias_dificultad_respiratoria') IS NULL
    ALTER TABLE dbo.Evaluations ADD dias_dificultad_respiratoria int NOT NULL;

IF COL_LENGTH('dbo.Evaluations', 'dolor_toracico') IS NULL
    ALTER TABLE dbo.Evaluations ADD dolor_toracico bit NOT NULL;

IF NOT EXISTS (
    SELECT 1 FROM sys.check_constraints
    WHERE name = 'CK_Evaluations_edad_meses_range'
      AND parent_object_id = OBJECT_ID('dbo.Evaluations')
)
    EXEC sp_executesql N'
        ALTER TABLE dbo.Evaluations WITH CHECK
        ADD CONSTRAINT CK_Evaluations_edad_meses_range
            CHECK (edad_meses >= 0 AND edad_meses <= 216);';

IF NOT EXISTS (
    SELECT 1 FROM sys.check_constraints
    WHERE name = 'CK_Evaluations_peso_kg_range'
      AND parent_object_id = OBJECT_ID('dbo.Evaluations')
)
    EXEC sp_executesql N'
        ALTER TABLE dbo.Evaluations WITH CHECK
        ADD CONSTRAINT CK_Evaluations_peso_kg_range
            CHECK (peso_kg > 0 AND peso_kg <= 150);';

IF NOT EXISTS (
    SELECT 1 FROM sys.check_constraints
    WHERE name = 'CK_Evaluations_glasgow_range'
      AND parent_object_id = OBJECT_ID('dbo.Evaluations')
)
    EXEC sp_executesql N'
        ALTER TABLE dbo.Evaluations WITH CHECK
        ADD CONSTRAINT CK_Evaluations_glasgow_range
            CHECK (glasgow >= 3 AND glasgow <= 15);';

IF NOT EXISTS (
    SELECT 1 FROM sys.check_constraints
    WHERE name = 'CK_Evaluations_dias_dificultad_range'
      AND parent_object_id = OBJECT_ID('dbo.Evaluations')
)
    EXEC sp_executesql N'
        ALTER TABLE dbo.Evaluations WITH CHECK
        ADD CONSTRAINT CK_Evaluations_dias_dificultad_range
            CHECK (dias_dificultad_respiratoria >= 0 AND dias_dificultad_respiratoria <= 60);';

COMMIT TRANSACTION;
