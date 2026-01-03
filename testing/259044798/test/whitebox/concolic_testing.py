from __future__ import annotations

import unittest
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Tuple, Set

import z3


@dataclass
class PathPredicate:
    expr: z3.BoolRef
    taken: bool


class ConcolicContext:
    def __init__(self) -> None:
        self.symbols: Dict[str, Any] = {}
        self.predicates: List[PathPredicate] = []

    def branch(self, concrete_cond: bool, symbolic_cond: z3.BoolRef) -> bool:
        self.predicates.append(PathPredicate(symbolic_cond, concrete_cond))
        return concrete_cond


class ConcolicExplorer:
    def __init__(self, max_iters: int = 30) -> None:
        self.max_iters = max_iters

    @staticmethod
    def _prefix_constraints(preds: List[PathPredicate], upto: int) -> List[z3.BoolRef]:
        cs: List[z3.BoolRef] = []
        for p in preds[:upto]:
            cs.append(p.expr if p.taken else z3.Not(p.expr))
        return cs

    @staticmethod
    def _flip_constraint(p: PathPredicate) -> z3.BoolRef:
        return z3.Not(p.expr) if p.taken else p.expr

    def explore(
        self,
        run_once: Callable[[Dict[str, Any]], Tuple[ConcolicContext, Any]],
        initial_inputs: Dict[str, Any],
        make_symbols: Callable[[ConcolicContext], None],
        add_domain_constraints: Callable[[ConcolicContext, z3.Solver], None],
        model_to_inputs: Callable[[ConcolicContext, z3.ModelRef], Dict[str, Any]],
    ) -> List[Tuple[Dict[str, Any], Any, ConcolicContext]]:
        results: List[Tuple[Dict[str, Any], Any, ConcolicContext]] = []
        seen: Set[Tuple[Tuple[str, str], ...]] = set()
        current_inputs = dict(initial_inputs)

        for _ in range(self.max_iters):
            ctx, result = run_once(current_inputs)
            results.append((current_inputs, result, ctx))

            progressed = False
            for i in range(len(ctx.predicates) - 1, -1, -1):
                solver = z3.Solver()

                sym_ctx = ConcolicContext()
                make_symbols(sym_ctx)
                add_domain_constraints(sym_ctx, solver)

                solver.add(self._prefix_constraints(ctx.predicates, i))
                solver.add(self._flip_constraint(ctx.predicates[i]))

                if solver.check() == z3.sat:
                    m = solver.model()
                    next_inputs = model_to_inputs(sym_ctx, m)
                    sig = tuple(sorted((k, repr(v)) for k, v in next_inputs.items()))
                    if sig in seen:
                        continue
                    seen.add(sig)
                    current_inputs = next_inputs
                    progressed = True
                    break

            if not progressed:
                break

        return results



def take_fill_in_the_blanks_quiz_core(name, questions, answers, responses, ctx: ConcolicContext):
    sym_name_is_none = ctx.symbols["name_is_none"]
    sym_q_len = ctx.symbols["q_len"]
    sym_a_len = ctx.symbols["a_len"]
    sym_r0_is_skip = ctx.symbols["r0_is_skip"]
    sym_r0_is_correct = ctx.symbols["r0_is_correct"]

    mismatch = (len(questions) != len(answers))
    if ctx.branch(mismatch, sym_q_len != sym_a_len):
        return {"error": "questions/answers length mismatch"}

    name_missing = (name is None)
    ctx.branch(name_missing, sym_name_is_none)

    empty_q = (len(questions) == 0)
    if ctx.branch(empty_q, sym_q_len == 0):
        return {"score": 0, "asked": 0, "skipped": 0}

    r0 = responses[0] if responses else ""
    is_skip = (r0.strip().lower() == "skip")
    ctx.branch(is_skip, sym_r0_is_skip)

    expected0 = answers[0] if answers else ""
    is_correct = (r0.strip().lower() == expected0.strip().lower())
    ctx.branch(is_correct, sym_r0_is_correct)

    score = 1 if (not is_skip and is_correct) else 0
    skipped = 1 if is_skip else 0
    return {"score": score, "asked": 1, "skipped": skipped}



def make_symbols(ctx: ConcolicContext):
    ctx.symbols["name_is_none"] = z3.Bool("name_is_none")
    ctx.symbols["q_len"] = z3.Int("q_len")
    ctx.symbols["a_len"] = z3.Int("a_len")
    ctx.symbols["r0_is_skip"] = z3.Bool("r0_is_skip")
    ctx.symbols["r0_is_correct"] = z3.Bool("r0_is_correct")


def add_domain_constraints(ctx: ConcolicContext, s: z3.Solver):
    q_len = ctx.symbols["q_len"]
    a_len = ctx.symbols["a_len"]
    s.add(q_len >= 0, q_len <= 3)
    s.add(a_len >= 0, a_len <= 3)


def model_to_inputs(ctx: ConcolicContext, m: z3.ModelRef):
    name_is_none = z3.is_true(m.eval(ctx.symbols["name_is_none"], model_completion=True))
    q_len = m.eval(ctx.symbols["q_len"], model_completion=True).as_long()
    a_len = m.eval(ctx.symbols["a_len"], model_completion=True).as_long()

    questions = [f"Q{i} ____" for i in range(q_len)]
    answers = [f"a{i}" for i in range(a_len)]
    name = None if name_is_none else "Alice"

    r0_is_skip = z3.is_true(m.eval(ctx.symbols["r0_is_skip"], model_completion=True))
    r0_is_correct = z3.is_true(m.eval(ctx.symbols["r0_is_correct"], model_completion=True))

    if q_len == 0:
        responses = []
    else:
        if r0_is_skip:
            responses = ["skip"]
        elif r0_is_correct and a_len > 0:
            responses = [answers[0]]
        else:
            responses = ["wrong"]

    return {"name": name, "questions": questions, "answers": answers, "responses": responses}


def run_once_fill(inputs):
    ctx = ConcolicContext()
    make_symbols(ctx)
    res = take_fill_in_the_blanks_quiz_core(
        inputs["name"], inputs["questions"], inputs["answers"], inputs["responses"], ctx
    )
    return ctx, res



def constraints_for_key(ctx: ConcolicContext, key: str):
    name_is_none = ctx.symbols["name_is_none"]
    q_len = ctx.symbols["q_len"]
    a_len = ctx.symbols["a_len"]
    r0_is_skip = ctx.symbols["r0_is_skip"]
    r0_is_correct = ctx.symbols["r0_is_correct"]

    if key == "1.1.1.1":
        return [z3.Not(name_is_none), q_len > 0, a_len == q_len, z3.Not(r0_is_skip), r0_is_correct]
    if key == "1.1.1.2":
        return [z3.Not(name_is_none), q_len > 0, a_len == q_len, z3.Or(r0_is_skip, z3.Not(r0_is_correct))]
    if key == "1.1.2.1":
        return [z3.Not(name_is_none), q_len == 0, a_len == 0]
    if key == "1.1.2.2":
        return [z3.Not(name_is_none), q_len == 0, a_len == 0]
    if key == "1.2.1.1":
        return [name_is_none, q_len > 0, a_len == q_len, z3.Not(r0_is_skip), r0_is_correct]
    if key == "1.2.1.2":
        return [name_is_none, q_len > 0, a_len == q_len, z3.Or(r0_is_skip, z3.Not(r0_is_correct))]
    if key == "1.2.2.1":
        return [name_is_none, q_len == 0, a_len == 0]
    if key == "1.2.2.2":
        return [name_is_none, q_len == 0, a_len == 0]
    if key == "<error>":
        return [q_len != a_len]

    raise ValueError(f"Unknown key: {key}")


def solve_for_key(key: str):
    ctx = ConcolicContext()
    make_symbols(ctx)
    s = z3.Solver()
    add_domain_constraints(ctx, s)
    s.add(constraints_for_key(ctx, key))
    if s.check() != z3.sat:
        raise AssertionError(f"UNSAT for key {key}")
    return model_to_inputs(ctx, s.model())



class TestConcolic(unittest.TestCase):
    def test_all_keys(self):
        keys = [
            "<error>",
            "1.1.1.1", "1.1.1.2",
            "1.1.2.1", "1.1.2.2",
            "1.2.1.1", "1.2.1.2",
            "1.2.2.1", "1.2.2.2",
        ]

        for k in keys:
            inp = solve_for_key(k)
            _, res = run_once_fill(inp)
            if k == "<error>":
                self.assertIn("error", res)
            else:
                
                if len(inp["questions"]) == len(inp["answers"]):
                    self.assertNotIn("error", res)

    def test_explorer_runs(self):
        explorer = ConcolicExplorer(max_iters=10)
        initial = {"name": "Alice", "questions": ["Q0 ____"], "answers": ["a0"], "responses": ["a0"]}

        runs = explorer.explore(
            run_once=run_once_fill,
            initial_inputs=initial,
            make_symbols=make_symbols,
            add_domain_constraints=add_domain_constraints,
            model_to_inputs=model_to_inputs,
        )
        self.assertGreaterEqual(len(runs), 1)

if __name__ == "__main__":
    import unittest
    unittest.main(verbosity=2)
