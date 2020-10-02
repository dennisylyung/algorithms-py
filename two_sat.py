import unittest
from typing import Any, Sequence, Tuple, Dict, Union

from graph_search import DirectedGraph


class Literal:
    """
    A variable reference or its negation
    """

    def __init__(self, sign: bool, variable: Union[str, int]):
        """
        Declare a literal.
        :param sign: True for positive literal, False for negative literal.
        :param variable: The reference for the variable.
        """
        self.variable = variable
        self.sign = sign

    @classmethod
    def from_str(cls, expression: str):
        """
        Construct a literal from a text expression (e.g. a => xa, -2 => -x2).
        if the variable reference can be cast to integer, it will be saved as one.
        Otherwise, variable references are saved as strings.
        :param expression: the text expression
        :return: a Literal instance.
        :raises ValueError: if an invalid expressions is provided
        """
        if not expression:
            raise ValueError('empty expression.')
        if expression[0] == '-':
            value_expression = expression[1:]
            sign = False
        elif expression[0] == '+':
            value_expression = expression[1:]
            sign = True
        else:
            value_expression = expression
            sign = True
        try:
            return cls(sign, int(value_expression))
        except ValueError:
            return cls(sign, value_expression)

    def to_tuple(self) -> Tuple[bool, Union[str, int]]:
        """
        return the sign and the variable reference as a tuple
        :return: sign, variable reference
        """
        return self.sign, self.variable

    def evaluate(self, assignment: Dict[Union[str, int], bool]) -> bool:
        """
        evaluate the literal with a variable dictionary.
        :param assignment: the variable dictionary with the variable reference as key, and the boolean value as value.
        :return: boolean evaluation of the literal
        """
        try:
            if self.sign:
                return assignment[self.variable]
            else:
                return not assignment[self.variable]
        except KeyError:
            raise ValueError(f'Missing variable {self.variable} in assignment')

    def __repr__(self):
        sign = '' if self.sign else '¬'
        value = f'𝑥{self.variable}'
        return sign + value

    def __neg__(self):
        return self.__class__(not self.sign, self.variable)

    def __hash__(self):
        return hash((self.sign, self.variable))

    def __eq__(self, other):
        return self.sign == other.sign and self.variable == other.variable

    def __ne__(self, other):
        return self != other


class Clause:

    def __init__(self, l1: Literal, l2: Literal):
        """
        Construct a 2-literals disjunction clause
        :param l1: the first Literal
        :param l2: the second Literal
        """
        self.l1 = l1
        self.l2 = l2

    @classmethod
    def from_str(cls, expression: str, sep=' '):
        """
        Construct a clause from a text expression (e.g. "1 -2").
        if the variable references can be cast to integers, they will be cast so.
        Otherwise, variable references are saved as strings.
        :param expression: a text expression (e.g. "1 -2"),
        which is the literal references separated by the delimiter `sep`.
        :param sep: the delimiter of the literals
        :return: a Clause instance
        """
        l1, l2 = tuple(expression.split(sep, 2))
        return cls(Literal.from_str(l1), Literal.from_str(l2))

    def literals(self) -> Tuple[Literal, Literal]:
        """
        get the literals as a tuple
        :return: (Literal 1, Literal 2)
        """
        return self.l1, self.l2

    def evaluate(self, assignment: Dict[Any, bool]) -> bool:
        """
        evaluate the clause with a variable dictionary.
        :param assignment: the variable dictionary with the variable reference as key, and the boolean value as value.
        :return: boolean evaluation of the clause
        """
        return self.l1.evaluate(assignment) or self.l2.evaluate(assignment)

    def __repr__(self):
        return f'({self.l1} ⋁ {self.l2})'


class TwoSat:
    """
    A 2-satisfiability (2-SAT) problem instance
    """

    def __init__(self, clauses: Sequence[Clause]):
        """
        Initialize a 2-satisfiability problem instance with a list of clauses.
        :param clauses: The clauses of the problem
        """
        self.clauses = clauses
        self.implication_graph = self.build_implication_graph(clauses)

    @classmethod
    def from_str(cls, expressions: Sequence[str], sep=' '):
        """
        Construct a 2-satisfiability problem instance from text expressions if clauses (e.g. "1 -2").
        if the variable references can be cast to integer, they will be cast so.
        Otherwise, variable references are saved as strings.
        :param expressions: a sequence of text expressions (e.g. "1 -2"),
        which is the literal references separated by the delimiter `sep`.
        :param sep: the delimiter of the literals
        :return: a TwoSat instance
        """
        return TwoSat([Clause.from_str(expr, sep) for expr in expressions])

    @staticmethod
    def build_implication_graph(clauses: Sequence[Clause]) -> DirectedGraph:
        """
        Build the implication graph of a sequence of clauses
        :param clauses: the sequence of clauses
        :return: a DirectedGraph instance of the implication graph
        """
        vertices = set()
        edges = set()
        for clause in clauses:
            # add the implication edge of each clause
            l1, l2 = clause.literals()
            vertices.add(l1)
            vertices.add(-l1)
            vertices.add(l2)
            vertices.add(-l2)
            edges.add((-l1, l2, 1))
            edges.add((-l2, l1, 1))
        return DirectedGraph.index_edges(list(vertices), list(edges))

    def solve(self) -> Dict[Union[str, int], bool]:
        """
        Try to solve the 2-SAT problem using the strongly-connected-components (SCC) algorithm.
        It runs in linear time.
        :return: variable assignments in a dictionary
        :raises UnsatisfiableError: if the 2-SAT problem is not satisfiable
        """
        # find the SCCs using the Kosaraju's algorithm
        sccs = self.implication_graph.find_scc('stack')
        assignment = {}
        for scc in sccs:
            constraints = {}
            for literal in scc:
                sign, variable = literal.to_tuple()
                # check if the SCC contains both the positive and negative literals of the same variable
                # which means that the problem is not satisfiable
                if variable in constraints and constraints[variable] != sign:
                    raise self.UnsatisfiableError(self)  # the problem is not satisfiable
                else:
                    constraints[variable] = sign
                # Since Kosaraju's algorithm naturally sort the SCCs in topological order,
                # the solution can be found simply be assigning a value when a variable is first seen
                # True if the positive literal is seen first (has higher lower topological order)
                # False if the negative literal is seen first
                if variable not in assignment:
                    assignment[variable] = sign
        return assignment

    def evaluate(self, assignment: Dict[Any, bool]):
        return all([clause.evaluate(assignment) for clause in self.clauses])

    def __repr__(self):
        if len(self.clauses) <= 5:
            return '(' + ' ∧ '.join([str(clause) for clause in self.clauses]) + ')'
        else:
            return '(' + ' ∧ '.join([str(clause) for clause in self.clauses[:5]]) + ' ∧ ...)'

    class UnsatisfiableError(Exception):

        def __init__(self, problem):
            super().__init__(f'2-sat problem {problem} is not satisfiable')


class TestTwoSat(unittest.TestCase):

    def test_evaluate(self):
        problem = TwoSat.from_str(['1 2', '2 -1', '-1 -2'])
        valid_assignment = {1: False, 2: True}
        invalid_assignment = {1: True, 2: False}
        self.assertTrue(problem.evaluate(valid_assignment))
        self.assertFalse(problem.evaluate(invalid_assignment))

    def test_satisfiable(self):
        problem = TwoSat.from_str(['1 2', '2 -1', '-1 -2'])
        assignment = problem.solve()
        self.assertTrue(problem.evaluate(assignment))
        print(f'2-sat problem {problem} is satisfiable')

    def test_unsatisfiable(self):
        problem = TwoSat.from_str(['1 2', '2 -1', '1 -2', '-1 -2'])
        with self.assertRaises(TwoSat.UnsatisfiableError) as cm:
            problem.solve()
        print(cm.exception)


if __name__ == '__main__':
    unittest.main(exit=False)

    for file in ['data/2sat1.txt', 'data/2sat2.txt', 'data/2sat3.txt', 'data/2sat4.txt', 'data/2sat5.txt',
                 'data/2sat6.txt']:
        with open(file, mode='r') as f:
            data = f.readlines()

        problem = TwoSat.from_str(data[1:])
        assert len(problem.clauses) == int(data[0])
        try:
            assignment = problem.solve()
            assert problem.evaluate(assignment)
            print(f'solution found for {file}: 2-sat problem {problem} is satisfiable')
        except TwoSat.UnsatisfiableError as e:
            print(f'no solution for {file}: {e}')
