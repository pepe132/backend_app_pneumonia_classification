IF COL_LENGTH('dbo.Evaluations', 'final_severity') IS NULL
    ALTER TABLE dbo.Evaluations ADD final_severity VARCHAR(20) NULL;
GO

IF COL_LENGTH('dbo.Evaluations', 'radiographic_support') IS NULL
    ALTER TABLE dbo.Evaluations ADD radiographic_support VARCHAR(40) NULL;
GO

IF COL_LENGTH('dbo.Evaluations', 'concordance') IS NULL
    ALTER TABLE dbo.Evaluations ADD concordance VARCHAR(30) NULL;
GO

IF COL_LENGTH('dbo.Evaluations', 'fusion_basis') IS NULL
    ALTER TABLE dbo.Evaluations ADD fusion_basis VARCHAR(40) NULL;
GO

IF COL_LENGTH('dbo.Evaluations', 'fusion_explanation') IS NULL
    ALTER TABLE dbo.Evaluations ADD fusion_explanation VARCHAR(500) NULL;
GO

IF COL_LENGTH('dbo.Evaluations', 'recommendation_code') IS NULL
    ALTER TABLE dbo.Evaluations ADD recommendation_code VARCHAR(50) NULL;
GO

IF COL_LENGTH('dbo.Evaluations', 'fusion_version') IS NULL
    ALTER TABLE dbo.Evaluations ADD fusion_version VARCHAR(30) NULL;
GO

IF OBJECT_ID('dbo.Radiographs', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.Radiographs (
        radiograph_id VARCHAR(40) NOT NULL,
        evaluation_id VARCHAR(40) NOT NULL,
        uploaded_by VARCHAR(40) NOT NULL,
        file_path VARCHAR(500) NOT NULL,
        original_filename VARCHAR(255) NOT NULL,
        content_type VARCHAR(100) NOT NULL,
        file_size INT NOT NULL,
        image_class VARCHAR(40) NOT NULL,
        confidence FLOAT NOT NULL,
        prob_covid FLOAT NOT NULL,
        prob_normal FLOAT NOT NULL,
        prob_bacterial FLOAT NOT NULL,
        prob_viral FLOAT NOT NULL,
        model_version VARCHAR(100) NOT NULL,
        created_at DATETIMEOFFSET NOT NULL
            CONSTRAINT DF_Radiographs_created_at DEFAULT SYSDATETIMEOFFSET(),
        CONSTRAINT PK_Radiographs PRIMARY KEY (radiograph_id),
        CONSTRAINT UQ_Radiographs_evaluation_id UNIQUE (evaluation_id),
        CONSTRAINT FK_Radiographs_Evaluations
            FOREIGN KEY (evaluation_id)
            REFERENCES dbo.Evaluations(evaluation_id),
        CONSTRAINT FK_Radiographs_Users
            FOREIGN KEY (uploaded_by)
            REFERENCES dbo.Users(user_id)
    );
END;
GO

UPDATE dbo.Evaluations
SET
    final_severity = COALESCE(final_severity, severity_tabular),
    radiographic_support = COALESCE(radiographic_support, 'not_available'),
    concordance = COALESCE(concordance, 'not_applicable'),
    fusion_basis = COALESCE(fusion_basis, 'tabular_only'),
    fusion_explanation = COALESCE(
        fusion_explanation,
        'Severidad estimada únicamente con datos clínicos; no se incluyó una radiografía.'
    ),
    recommendation_code = COALESCE(
        recommendation_code,
        CASE LOWER(severity_tabular)
            WHEN 'bajo' THEN 'severity_bajo'
            WHEN 'medio' THEN 'severity_medio'
            WHEN 'alto' THEN 'severity_alto'
            ELSE NULL
        END
    ),
    fusion_version = COALESCE(fusion_version, 'rules-v1.0')
WHERE severity_tabular IS NOT NULL;
GO
