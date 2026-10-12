import unittest

from scripts.agreement_probe import EXAMPLE, normalized_signals, report


class AgreementProbeTests(unittest.TestCase):
    def test_example_reproduces_documented_illustration(self):
        got = report(EXAMPLE)
        self.assertEqual(got["engine_count"], 7)
        self.assertEqual(got["agreement_score"], 28.6)
        self.assertEqual(got["direction"], "MILDLY BULLISH")
        self.assertEqual(got["non_neutral_fraction_pct"], 85.7)
        self.assertEqual(
            got["leave_one_engine_out"]["elliott"]["direction_without_engine"],
            "BULLISH",
        )

    def test_all_neutral_has_zero_non_neutral_fraction(self):
        got = report({"a": "NEUTRAL", "b": "NEUTRAL"})
        self.assertEqual(got["agreement_score"], 0)
        self.assertEqual(got["direction"], "NEUTRAL")
        self.assertEqual(got["non_neutral_fraction_pct"], 0)

    def test_saved_prediction_shape_and_nested_labels_supported(self):
        out = report({"engine_signals": {"a": "BEARISH", "b": "NEUTRAL"}})
        self.assertEqual(out["agreement_score"], -50)
        nested = normalized_signals({"signals": {"a": {"signal": "BULLISH"}}})
        self.assertEqual(nested["a"]["signal"], "BULLISH")

    def test_invalid_input_fails_instead_of_counting_as_neutral(self):
        for raw in ({}, {"x": "SELL"}, {"x": None}, [], {"x": {"signal": "bullish"}}):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                report(raw)


if __name__ == "__main__":
    unittest.main()
