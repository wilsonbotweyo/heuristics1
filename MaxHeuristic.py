import pddl.state
from pddl.heuristic import Heuristic

class MaxHeuristic(Heuristic):
    def are_goals_satisfied(self, initial_state, positive_goals, negative_goals):
        return (pddl.state.applicable(initial_state, positive_goals, negative_goals))

    def can_apply_action_to_state(self, state, action):
        return pddl.state.applicable(state, action.positive_preconditions, action.negative_preconditions)

    def get_state_with_applied_action(self, state, action):
        return pddl.state.apply(state, action.add_effects, action.del_effects)

    def h(self, actions, initial_state, positive_goals, negative_goals, debug=False):

        if (self.are_goals_satisfied(initial_state, positive_goals, negative_goals)):
            return 0
        # Funtion similar to graphplan's algorithm, adds list of states till there is a possibility of solving all the goals
        all_state_predicates = set(initial_state)
        steps_taken = 0
        negative_goals = set(negative_goals)

        # adding all results till goal is achieved.

        while (steps_taken < 10000): # if combinations of actions are greater than 99999 then bail.
            if (self.are_goals_satisfied(all_state_predicates, positive_goals, negative_goals)):
                return steps_taken 
            steps_taken += 1
            # creating a new state with possible states from current ones
            next_state_predicates = set(all_state_predicates)
            for action in actions:
                # Skip action when it cant be executed
                if (not action.positive_preconditions.issubset(all_state_predicates)):
                    continue

                # add all new effects to the list if they not exist
                for predicate in action.add_effects:
                    next_state_predicates.add(predicate)
                for predicate in action.del_effects:
                    #  remove the negative goals til they empty or satisfy the initial state, due to them being different from positive ones
                    negative_goals.discard(predicate)

            # change the old set of state parts with  new one
            del all_state_predicates
            all_state_predicates = next_state_predicates
        return float("inf")


if __name__ == '__main__':
    from pddl.pddl_parser import PDDL_Parser
    from pddl.action import Action
    from pddl.state import applicable, apply
    import sys

    dwr = "examples/dwr/dwr.pddl"
    pb1_dwr = "examples/dwr/pb1.pddl"
    pb2_dwr = "examples/dwr/pb2.pddl"

    tsp = "examples/tsp/tsp.pddl"
    pb1_tsp = "examples/tsp/pb1.pddl"

    dinner = "examples/dinner/dinner.pddl"
    pb1_dinner = "examples/dinner/pb1.pddl"
    
    dompteur = "examples/dompteur/dompteur.pddl"
    pb1_dompteur = "examples/dompteur/pb1.pddl"

    def parse_domain_problem(domain, problem):
        parser = PDDL_Parser()
        parser.parse_domain(domain)
        parser.parse_problem(problem)
        actions = []
        for action in parser.actions:
            for act in action.groundify(parser.objects):
                actions.append(act)
        return parser, actions

    def test_heuristic(domain, problem, h, expected):
        parser, actions = parse_domain_problem(domain, problem)
        #try:
        v = h.h(actions, parser.state, parser.positive_goals, parser.negative_goals, True)
        if (v == expected):
            print(" -> Success: "+str(v)+" == "+str(expected)+" at domain \""+str(domain)+"\"")
        else:
            print(" -> Error: "+str(v)+" != "+str(expected)+" at domain \""+str(domain)+"\"")

    h = MaxHeuristic()
    test_heuristic(dwr, pb1_dwr, h, 6)
    test_heuristic(dwr, pb2_dwr, h, 0)
    test_heuristic(tsp, pb1_tsp, h, 2)
    test_heuristic(dinner, pb1_dinner, h, 1)
    test_heuristic(dompteur, pb1_dompteur, h, 1)
