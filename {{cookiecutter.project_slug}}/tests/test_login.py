from dash import Dash
from dash.testing.composite import DashComposite


def test_correct_login(dash_duo: DashComposite, app: Dash) -> None:
    """
    Ensure that the user is logged in
    """
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#loginSubmit", timeout=5)
    dash_duo.find_element("#exampleInputEmail").send_keys("john@doe.com")
    dash_duo.find_element("#exampleInputPassword").send_keys("changethis")
    dash_duo.find_element("#loginSubmit").click()

    dash_duo.wait_for_element("#content", timeout=5)


def test_wrong_login(dash_duo: DashComposite, app: Dash) -> None:
    """
    Ensure that validation message is shown when an invalid email
    and password in submitted
    """
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#loginSubmit", timeout=5)
    dash_duo.find_element("#loginSubmit").click()

    dash_duo.wait_for_text_to_equal(
        "#exampleInputEmailValidation", "Couldn't validate credentials", timeout=5
    )
    dash_duo.wait_for_text_to_equal(
        "#exampleInputPasswordValidation", "Couldn't validate credentials", timeout=5
    )
