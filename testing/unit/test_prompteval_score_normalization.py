from tools.prompteval import __main__ as pe


def test_normalize_score_to_pct_never_negative():
    # 0 from a model should be treated as worst-case, not negative percent
    assert pe._normalize_score_to_pct(0) == 0.0
    assert pe._normalize_score_to_pct(-5) == 0.0


def test_normalize_score_to_pct_rubric_bounds():
    # Rubric 1..10 maps to 0..100
    assert pe._normalize_score_to_pct(1) == 0.0
    assert pe._normalize_score_to_pct(10) == 100.0


def test_normalize_score_to_pct_accepts_fraction_and_percent():
    # Sometimes models emit fractions or already-normalized percent values
    assert pe._normalize_score_to_pct(0.5) == 50.0
    assert pe._normalize_score_to_pct(75) == 75.0
    assert pe._normalize_score_to_pct(150) == 100.0
