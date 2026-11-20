"""Builder 1 implements the student's policy here."""
from models import Elevator, Request, Decision
from rules import eligible_ids

def choose_elevator(elevators: tuple[Elevator, Elevator], request: Request) -> Decision:
    """Choose one eligible elevator according to POLICY.md; never mutate inputs."""
    eligible = set(eligible_ids(elevators, request))
    if not eligible:
        return Decision(
            None,
            "No eligible elevator under the shared capacity and route rules; policy defers the request (WAIT).",
        )

    candidates = [elevator for elevator in elevators if elevator.id in eligible]

    def tie_key(elevator: Elevator) -> tuple[int, str]:
        return (0 if elevator.id == "A" else 1, elevator.id)

    scheduled = [
        elevator for elevator in candidates if request.floor in elevator.stops
    ]
    if scheduled:
        selected = min(scheduled, key=tie_key)
        return Decision(
            selected.id,
            f"Rule 1: elevator {selected.id} is already scheduled to stop at "
            f"floor {request.floor}; tie-breaker favors A when needed.",
        )

    light_moving = [
        elevator
        for elevator in candidates
        if elevator.direction != "idle" and elevator.load_kg <= 260
    ]
    if light_moving:
        selected = min(light_moving, key=tie_key)
        return Decision(
            selected.id,
            f"Rule 2: elevator {selected.id} is moving and has load "
            f"{selected.load_kg} kg (at or below the inclusive 260 kg limit); "
            "tie-breaker favors A when needed.",
        )

    selected = min(
        candidates,
        key=lambda elevator: (
            abs(elevator.floor - request.floor),
            *tie_key(elevator),
        ),
    )
    return Decision(
        selected.id,
        f"Rule 3: elevator {selected.id} is the nearest eligible car at "
        f"{abs(selected.floor - request.floor)} floor(s) away; tie-breaker "
        "favors A when needed.",
    )
