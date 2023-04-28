import argparse
import asyncio
from typing import List

from mdp_dp_rl.processes.det_policy import DetPolicy
from aida.lmdp import LMDP

from aida.constants import GAMMAS
from aida.lvi import lexicographic_value_iteration
from local.targetDFA_simulator import TargetSimulatorDFA

from local.target_DFA import target_dfa
from local.IndustrialAPI.client_wrapper import ClientWrapper
from local.IndustrialAPI.data import ServiceInstance
from local.IndustrialAPI.helpers import setup_logger
from aida.lmdp import compute_composition_lmdp

logger = setup_logger("orchestrator")

parser = argparse.ArgumentParser("main")
parser.add_argument("--host", type=str, default="localhost", help="IP address of the HTTP IoT service.")
parser.add_argument("--port", type=int, default=8080, help="IP address of the HTTP IoT service.")


async def main(host: str, port: int) -> None:
    client = ClientWrapper(host, port)

    # check health
    response = await client.get_health()
    assert response.status_code == 200

    # get all services
    services: List[ServiceInstance] = await client.get_services()
    services = sorted(services, key=lambda x: x.service_id)
    logger.info(f"Got {len(services)} available services")

    # start main loop
    old_policy = None
    dfa_target = target_dfa()
    target_simulator = TargetSimulatorDFA(dfa_target)
    system_state = [service.service_spec.initial_state for service in services]
    iteration = 0
    while True:

        lmdp: LMDP = compute_composition_lmdp(dfa_target, [service.current_service_spec for service in services], GAMMAS)
        # set tolerance to stop value iteration earlier for faster convergence
        result_vf, actions = lexicographic_value_iteration(lmdp, tol=1e-5)
        orchestrator_policy = DetPolicy({s: list(opt_actions_from_s)[0] for s, opt_actions_from_s in actions.items()})

        # detect when policy changes
        if old_policy is None:
            old_policy = orchestrator_policy
        if old_policy.policy_data != orchestrator_policy.policy_data:
            logger.info(f"Optimal Policy has changed!\nold_policy = {old_policy}\nnew_policy={orchestrator_policy}")
        old_policy = orchestrator_policy

        # waiting for target action
        logger.info("Waiting for messages from target...")
        current_target_state = target_simulator.current_state

        logger.info(f"Iteration: {iteration}")
        current_state = (tuple(system_state), current_target_state)
        logger.info(f"Current state: {current_state}")

        orchestrator_choice = orchestrator_policy.get_action_for_state(current_state)
        if orchestrator_choice == "undefined":
            logger.error(f"Execution failed: composition failed in system state {system_state}")
            break
        # send_action_to_service
        target_action, service_index = orchestrator_choice
        logger.info(f"Chosen service: {service_index}, chosen action: {target_action}")
        service_id = services[service_index].service_id
        logger.info(f"Sending message to thing: {service_id}, {target_action}")
        await client.execute_service_action(service_id, target_action)
        logger.info(f"Action has been executed")
        new_service_instance = await client.get_service(service_id)
        if services[service_index].transition_function != new_service_instance.transition_function:
            logger.info(f"Transition function for service {new_service_instance.service_id} has changed! Old: {services[service_index].transition_function}, New: {new_service_instance.transition_function}")
        services[service_index] = new_service_instance
        system_state[service_index] = new_service_instance.current_state

        if target_action in dfa_target.alphabet:
            target_simulator.update_state(target_action)

        if target_simulator.current_state in dfa_target.accepting_states:
           target_simulator.reset()

        logger.info(f"Next service state: {new_service_instance.current_state}")
        old_transition_function = services[service_index].transition_function
        if old_transition_function != new_service_instance.transition_function:
            logger.info(f"Transition function has changed!\nOld: {old_transition_function}\nNew: {new_service_instance.transition_function}")

        logger.info("Sleeping one second...")
        await asyncio.sleep(1.0)
        iteration += 1


if __name__ == "__main__":
    arguments = parser.parse_args()
    result = asyncio.get_event_loop().run_until_complete(main(arguments.host, arguments.port))
