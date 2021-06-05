import multiprocessing as mp
from io import TextIOWrapper
from typing import Iterator

from enigma_simulator.enigma import Enigma


def read_gen(file: TextIOWrapper, chunk_size: int = 250) -> Iterator[str]:
    buffer = str()
    size = 0

    for line in file:
        size += len(line)
        buffer += line

        while size > chunk_size:
            size -= chunk_size
            res = buffer[0:chunk_size]
            buffer = buffer[chunk_size:]

            yield res

    yield buffer


def process_str(message: str) -> str:
    enigma = Enigma(["I", "II", "III"], [0, 0, 0], "B", "SF CG HD", [0, 0, 0])
    start_position, encrypted_key, encrypted = enigma.encrypt_transmission(message)
    return f"{start_position} {encrypted_key}\n{encrypted}\n" + "-" * 80 + "\n"


def main():
    with mp.Pool(processes=mp.cpu_count()) as pool:
        with open("large_text.txt", "r") as f:
            results = [pool.apply_async(process_str, (s,)) for s in read_gen(f, 250)]

        text = "".join(res.get() for res in results)

        with open("text_out2.txt", "w+") as g:
            g.write(text)


if __name__ == "__main__":
    main()
