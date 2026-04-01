def process_image(image):
    # dummy integration logic

    objects = ["person", "car"]
    text = "sample text"
    caption = "A person with a car"

    return {
        "objects": objects,
        "extracted_text": text,
        "description": caption
    }


# test run
if __name__ == "__main__":
    result = process_image("image.jpg")
    print(result)