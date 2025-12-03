def list_ordered_list(input_list, list_title):
    print(list_title)
    for i, item in enumerate(input_list, start=1):
        print(f"{i}. {item}")
    return input_list


def container_to_string(container, index):
    image_tags = container.image.tags
    image = image_tags[0] if image_tags else "N/A"
    return f"{index + 1}. ID: {container.short_id} - {container.name}: {image} ({container.status})"
