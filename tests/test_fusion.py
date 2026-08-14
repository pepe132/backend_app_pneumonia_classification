import pytest

from app.modules.evaluations.fusion import fuse_results


@pytest.mark.parametrize("severity", ["Bajo", "Medio", "Alto"])
def test_without_radiograph_preserves_tabular_severity(severity):
    result = fuse_results(severity)

    assert result["final_severity"] == severity
    assert result["radiographic_support"] == "not_available"
    assert result["concordance"] == "not_applicable"
    assert result["basis"] == "tabular_only"


def test_low_confidence_is_indeterminate():
    result = fuse_results("Medio", "pneumonia_viral", 0.527403, 0.60)

    assert result["final_severity"] == "Medio"
    assert result["radiographic_support"] == "indeterminate"
    assert result["concordance"] == "indeterminate"


@pytest.mark.parametrize("image_class", ["pneumonia_bacterial", "pneumonia_viral"])
def test_pneumonia_with_sufficient_confidence_supports_clinical_result(image_class):
    result = fuse_results("Medio", image_class, 0.85)

    assert result["final_severity"] == "Medio"
    assert result["radiographic_support"] == "supports_pneumonia"
    assert result["concordance"] == "concordant"


def test_normal_image_never_reduces_severity():
    result = fuse_results("Alto", "normal", 0.95)

    assert result["final_severity"] == "Alto"
    assert result["radiographic_support"] == "does_not_support_pneumonia"
    assert result["concordance"] == "discordant"


def test_covid_requires_review():
    result = fuse_results("Bajo", "covid_19", 0.90)

    assert result["final_severity"] == "Bajo"
    assert result["radiographic_support"] == "review_required"


def test_unknown_image_class_is_rejected():
    with pytest.raises(ValueError, match="Clase radiográfica no soportada"):
        fuse_results("Medio", "unknown", 0.99)
