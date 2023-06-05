from pets.models import PetBreeds


def verify_breed_is_allowed(breed):
    allowed_breeds = PetBreeds.get_pet_breeds()
    if breed not in allowed_breeds:
        raise ValueError(f"Invalid breed.")
