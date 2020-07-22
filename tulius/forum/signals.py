from django import dispatch


# analyze data and prepare to jsonify
thread_prepare_room = dispatch.Signal(
    providing_args=["room", "threads"])
thread_prepare_threads = dispatch.Signal(providing_args=["threads"])

# prepare data to json
thread_room_to_json = dispatch.Signal(
    providing_args=["thread", "response"])

before_create_thread = dispatch.Signal(providing_args=["thread", "data"])
after_create_thread = dispatch.Signal(
    providing_args=["thread", "data", "preview"])

update_thread = dispatch.Signal(providing_args=["thread", "data", "preview"])
