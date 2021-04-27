from enigma_simulator.components import get_reflector
from enigma_simulator.components import get_rotor
from enigma_simulator.components import Plugboard
from enigma_simulator.utils import char_to_vec
from enigma_simulator.utils import vec_to_char


class Enigma:
    def __init__(
        self,
        rotor_names: list[str],
        rotor_positions: list[int],
        ring_settings: list[int],
        reflector_type: str,
        plugboard_connections: str,
    ) -> None:
        self.left_rotor, self.middle_rotor, self.right_rotor = tuple(
            get_rotor(*i) for i in zip(rotor_names, rotor_positions, ring_settings)
        )
        self.reflector = get_reflector(reflector_type)
        self.plugboard = Plugboard(plugboard_connections)

    def encrypt(self, message: str) -> str:
        encrypted = ""
        for char in list(message):
            self.rotate()

            vec = char_to_vec(char)
            vec = self.plugboard.forward(vec)
            vec = self.right_rotor.forward(vec)
            vec = self.middle_rotor.forward(vec)
            vec = self.left_rotor.forward(vec)
            vec = self.reflector.forward(vec)
            vec = self.left_rotor.backward(vec)
            vec = self.middle_rotor.backward(vec)
            vec = self.right_rotor.backward(vec)
            vec = self.plugboard.forward(vec)
            char = vec_to_char(vec)

            encrypted += char

        return encrypted

    def rotate(self) -> None:
        if self.middle_rotor.at_notch:
            self.middle_rotor.turnover()
            self.left_rotor.turnover()
        elif self.right_rotor.at_notch:
            self.middle_rotor.turnover()

        self.right_rotor.turnover()
