from concurrent.futures import ThreadPoolExecutor


def execute(fn, values):
    counter = 0
    with ThreadPoolExecutor(max_workers=30) as executor:
        for output in executor.map(fn, values):
            counter += 1
            print(f"{'{:6d}'.format(counter)}/{len(values)} | {output}")
