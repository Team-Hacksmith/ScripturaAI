def id_generator(start=1):
    current_id = start
    while True:
        yield current_id
        current_id += 1
