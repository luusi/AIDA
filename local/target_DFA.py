from logaut import ltl2dfa
# Python imports, put at the top for simplicity
from pylogics.parsers import parse_ltl
from pythomata import SimpleDFA

from aida.declare_utils import build_declare_assumption, exactly_once, alt_precedence, absence_2, alt_succession, \
    not_coexistence
from aida.dfa_target import from_symbolic_automaton_to_declare_automaton

# all the atomic actions for the task
BUILD_RETRIEVE_STATOR = "build_retrieve_stator"
BUILD_RETRIEVE_ROTOR = "build_retrieve_rotor"
BUILD_RETRIEVE_INVERTER = "build_retrieve_inverter"
ASSEMBLE_MOTOR = "assemble_motor"
PAINTING = "painting"
RUNNING_IN = "running_in"
ELECTRIC_TEST = "electric_test"
STATIC_TEST = "static_test"

ALL_SYMBOLS = {
    BUILD_RETRIEVE_STATOR,
    BUILD_RETRIEVE_ROTOR,
    BUILD_RETRIEVE_INVERTER,
    ASSEMBLE_MOTOR,
    PAINTING,
    RUNNING_IN,
    ELECTRIC_TEST,
    STATIC_TEST,
}

def target_dfa() -> SimpleDFA:

    constraints = [
        exactly_once(BUILD_RETRIEVE_STATOR),
        exactly_once(BUILD_RETRIEVE_ROTOR),
        exactly_once(BUILD_RETRIEVE_INVERTER),
        exactly_once(RUNNING_IN),
        exactly_once(ASSEMBLE_MOTOR),
        absence_2(ELECTRIC_TEST),
        absence_2(PAINTING),
        absence_2(STATIC_TEST),
        alt_succession(BUILD_RETRIEVE_STATOR, ASSEMBLE_MOTOR),
        alt_succession(BUILD_RETRIEVE_ROTOR, ASSEMBLE_MOTOR),
        alt_succession(BUILD_RETRIEVE_INVERTER, ASSEMBLE_MOTOR),
        alt_succession(ASSEMBLE_MOTOR, RUNNING_IN),
        alt_precedence(ASSEMBLE_MOTOR, PAINTING),
        alt_precedence(ASSEMBLE_MOTOR, ELECTRIC_TEST),
        alt_precedence(ASSEMBLE_MOTOR, STATIC_TEST),
        not_coexistence(ELECTRIC_TEST, STATIC_TEST),
        build_declare_assumption(ALL_SYMBOLS),
    ]

    formula_str = " & ".join(map(lambda s: f"({s})", constraints))
    formula = parse_ltl(formula_str)
    automaton = ltl2dfa(formula, backend="lydia")
    declare_automaton = from_symbolic_automaton_to_declare_automaton(automaton, ALL_SYMBOLS)
    return declare_automaton
    #print(declare_automaton)
    #print("Number of states: ", len(declare_automaton.states))


if __name__ == '__main__':
    target_dfa()