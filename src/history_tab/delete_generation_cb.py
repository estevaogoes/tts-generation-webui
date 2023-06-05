import shutil


def delete_generation_cb(refresh):
    def delete_generation(directory: str):
        shutil.rmtree(directory)

        return refresh()

    return delete_generation