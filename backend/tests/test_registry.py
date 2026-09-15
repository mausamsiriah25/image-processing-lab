from app.processors.registry import REGISTRY, all_ids


def test_registry_has_eleven_practicals():
    assert len(REGISTRY) == 11


def test_registry_ids_match_expected():
    expected = {
        "practical-01", "practical-02", "practical-03", "practical-04",
        "practical-05", "practical-06", "practical-07", "practical-08",
        "practical-09", "postlab-02", "postlab-03",
    }
    assert set(all_ids()) == expected


def test_practical09_is_multi_image():
    assert REGISTRY["practical-09"].multi_image is True
    assert REGISTRY["practical-09"].image_roles == ("template", "target")


def test_practical01_does_not_require_image():
    assert REGISTRY["practical-01"].requires_image is False
