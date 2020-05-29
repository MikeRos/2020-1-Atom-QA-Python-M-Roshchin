# User initially added to DB
ADMIN_USERNAME = 'ADMIN_USER'
ADMIN_PASSWORD = 'ADMIN'
ADMIN_VK_ID = 'vk_6897345'
# Some data prepared to test api validation
invalid_reg_data = [
    # username, password, email
    ["u", "p", "email"],
    ["1", "2", "@"]
]

# Some data prepared to test ui registration validation
# Can define different combination on reg data and error hints
invalid_reg_parametrization = [
    # username, email, password, password_confirmation, hint_message for this case
    ["s", "email@mail.com", "some_pass",  "some_pass", "Incorrect username length"],  # Too short name case
    ["s"*100, "email@mail.com", "some_pass",  "some_pass", "Incorrect username length"],  # Too long name case
    ["some_name", "e", "some_pass",  "some_pass", "Incorrect email length"],  # Too short email case
    ["some_name", "e"*100, "some_pass",  "some_pass", "Incorrect email length"],  # Too long email case
    ["some_name", "e"*10, "some_pass",  "some_pass", "Invalid email address"],  # Invalid email case
    ["some_name", "email@mail.com", "some_pass"*30,  "some_pass"*30, "Incorrect password length"],  # Too long password case
    ["some_name", "email@mail.com", "some_pass",  "some_passs", "Passwords must match"],  # Password not match case
    ["some_name", "email@mail.com", "some_pass",  "", "Passwords must match"],  # Password not confirmed case
    ["s", "s", "p", "p_c", "Multi error hint"]  # TODO not sure if message should be like this
    # TODO can add more complex cases with multiple errors
]
