import unittest

from pythogic.ltlf.semantics.FiniteTrace import FiniteTrace
from pythogic.ltlf.LTLf import LTLf
from pythogic.base.Formula import AtomicFormula, Next, Until, Eventually, Always, Not, And, TrueFormula, FalseFormula, \
    Or, LDLfLast
from pythogic.base.Alphabet import Alphabet
from pythogic.base.Symbol import Symbol



class TestLTLf(unittest.TestCase):
    """Tests for `pythogic.ltlf` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        # Symbols
        self.a_sym = Symbol("a")
        self.b_sym = Symbol("b")
        self.c_sym = Symbol("c")

        # Propositions
        self.a = AtomicFormula(self.a_sym)
        self.b = AtomicFormula(self.b_sym)
        self.c = AtomicFormula(self.c_sym)

        # Formulas
        self.not_a = Not(self.a)
        self.a_and_b = And(self.a,self.b)
        self.next_a = Next(self.a)
        self.a_until_c = Until(self.a, self.c)
        self.b_until_a = Until(self.b, self.a)

        # Derived Formulas
        self.true = TrueFormula()
        self.false = FalseFormula()
        self.last = LDLfLast()
        self.a_or_b = Or(self.a, self.b)
        self.eventually_c = Eventually(self.c)
        self.eventually_a = Eventually(self.a)
        self.always_a = Always(self.a)
        self.always_b = Always(self.b)

        self.alphabet = Alphabet({self.a_sym, self.b_sym, self.c_sym})
        # Traces
        self.ltlf = LTLf(self.alphabet)
        self.trace_1_list = [
            {self.a_sym, self.b_sym},
            {self.a_sym, self.c_sym},
            {self.a_sym, self.b_sym},
            {self.a_sym, self.c_sym},
            {self.b_sym, self.c_sym},
        ]
        self.trace_1 = FiniteTrace(self.trace_1_list, self.alphabet)

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_str(self):

        self.assertEqual(str(self.a), "a")
        self.assertEqual(str(self.not_a), "~(a)")
        self.assertEqual(str(self.a_and_b), "(a & b)")
        self.assertEqual(str(self.next_a), "○(a)")
        self.assertEqual(str(self.a_until_c), "(a U c)")
        self.assertEqual(str(self.true), "⊤")
        self.assertEqual(str(self.false), "⊥")
        self.assertEqual(str(self.last), "Last")
        self.assertEqual(str(self.a_or_b), "(a | b)")
        self.assertEqual(str(self.eventually_c), "◇(c)")
        self.assertEqual(str(self.always_a), "□(a)")

        self.assertEqual(str(self.trace_1), "Trace (length=5)"
                                                 "\n\t0: {a, b}"
                                                 "\n\t1: {a, c}"
                                                 "\n\t2: {a, b}"
                                                 "\n\t3: {a, c}"
                                                 "\n\t4: {b, c}"
                         )

    def test_truth(self):
        self.assertFalse(self.ltlf.truth(self.not_a, self.trace_1, 0))
        self.assertTrue(self.ltlf.truth (self.not_a, self.trace_1, 4))
        self.assertTrue(self.ltlf.truth (self.a_and_b, self.trace_1, 0))
        self.assertFalse(self.ltlf.truth(self.a_and_b, self.trace_1, 1))
        self.assertTrue(self.ltlf.truth (self.next_a, self.trace_1, 0))
        self.assertFalse(self.ltlf.truth(self.next_a, self.trace_1, 3))
        self.assertFalse(self.ltlf.truth(self.next_a, self.trace_1, 4))
        self.assertTrue(self.ltlf.truth (self.a_until_c, self.trace_1, 0))
        self.assertFalse(self.ltlf.truth(self.b_until_a, self.trace_1, 4))
        self.assertTrue(self.ltlf.truth (self.a_until_c, self.trace_1, 4))
         # j = 4, no k => reduces to check if c is in state j
        self.assertTrue( self.ltlf.truth(self.true, self.trace_1, 0))
        self.assertFalse(self.ltlf.truth(self.false, self.trace_1, 0))
        self.assertTrue(self.ltlf.truth (self.a_or_b, self.trace_1, 1))
        self.assertTrue(self.ltlf.truth (self.eventually_c, self.trace_1, 0))
        self.assertFalse(self.ltlf.truth(self.eventually_a, self.trace_1, 4))
        self.assertTrue(self.ltlf.truth (self.always_b, self.trace_1, 4))
        self.assertFalse(self.ltlf.truth(self.always_b, self.trace_1, 3))
        self.assertFalse(self.ltlf.truth(self.always_a, self.trace_1, 0))



