"""Module for image processing function"""
import time
import os
from fastapi import HTTPException

from src.services.file_service import file_path


def calculate_expected_images(prompt_list, lora_list, art_list, stack_loras):
    """Calculate the expected number of images to be generated."""
    expected_count = 0
    prompt_count = len(prompt_list)

    if stack_loras:
        # When stacked, generate one image per prompt for each group
        if lora_list:
            # For stacked loras, use the batch size from the first lora
            expected_count += prompt_count * int(lora_list[0].get("batchSize", 1))
        if art_list:
            # For stacked arts, use the batch size from the first art style
            expected_count += prompt_count * int(art_list[0].get("batchSize", 1))
    else:
        # When not stacked, generate images for each style individually
        for l in lora_list:
            expected_count += prompt_count * int(l.get("batchSize", 1))
        for a in art_list:
            expected_count += prompt_count * int(a.get("batchSize", 1))

    return expected_count


def wait_for_images(expected_count, check_interval=110):
    """Wait for the expected number of images to be generated."""
    start_time = time.time()
    last_count = 0
    last_check_time = start_time

    print(f"Waiting for {expected_count} images to be generated...")

    while True:
        try:
            image_files = [
                f for f in os.listdir(file_path) if f.lower().endswith((".png"))
            ]
            current_count = len(image_files)
            current_time = time.time()
            elapsed_minutes = (current_time - start_time) / 60
            if (
                current_count > last_count
                or (current_time - last_check_time) >= check_interval
            ):
                print(
                    f"Progress after {elapsed_minutes:.1f} minutes: {current_count}/{expected_count} images generated"
                )
                last_count = current_count
                last_check_time = current_time

            if current_count >= expected_count:
                total_minutes = (time.time() - start_time) / 60
                print(
                    f"All {expected_count} images have been generated successfully in {total_minutes:.1f} minutes!"
                )
                return True

            time.sleep(check_interval)

        except Exception as e:
            print(f"Error while waiting for images: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e)) from e
