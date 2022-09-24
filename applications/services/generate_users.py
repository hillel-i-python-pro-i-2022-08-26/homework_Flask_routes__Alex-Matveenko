from applications.services.faker_service import fake


# Name_generator__start
def name_generate() -> str:
    name = fake.name().split()[0]
    email = f"{str(name.split()[0]).lower()}_example@mail.com"
    return f"{name}: {email}"

# Name_generator__stop
