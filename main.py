global session
import os
import urllib.parse

import gspread
import requests
import stripe
from dhooks import Embed, Webhook
from dotenv import load_dotenv
from flask import (
    Flask,
    abort,
    flash,
    json,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from nanoid import generate
from oauth2client.service_account import ServiceAccountCredentials
from requests_oauthlib import OAuth2Session

from hidden_vars_for_public_repo import OAUTH2_CLIENT_ID, OAUTH2_CLIENT_SECRET, BOT_TOKEN, GUILD_ID, STRIPE_API_KEY, STRIPE_PRICE # hidden file to import sensitive keys
# THE GSHEETS API KEY.JSON FILE IS ALSO HIDDEN BECAUSE IT CONTAINS SENSITIVE INFO

load_dotenv(".env")

# Discord setup
print(OAUTH2_CLIENT_ID)
print(OAUTH2_CLIENT_SECRET)
print(BOT_TOKEN)

# IDs
print(GUILD_ID)

# URLS
OAUTH2_REDIRECT_URL = lambda: url_for("callback", _external=True, _scheme="https")
API_BASE_URL = "https://discordapp.com/api"
AUTHORIZATION_BASE_URL = API_BASE_URL + "/oauth2/authorize"
TOKEN_URL = API_BASE_URL + "/oauth2/token"

# Stripe setup
stripe.api_key = STRIPE_API_KEY

STRIPE_PRICE = STRIPE_PRICE

# For dev environment
if os.getenv("DEV"):
    OAUTH2_CLIENT_ID = os.getenv("OAUTH2_CLIENT_ID", "")
    OAUTH2_CLIENT_SECRET = os.getenv("OAUTH2_CLIENT_SECRET", "")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    stripe.api_key = os.getenv("STRIPE_API_KEY", "")
    STRIP_PRICE = os.getenv("STRIPE_PRICE", "")

# Flask setup
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config.update(dict(PREFERRED_URL_SCHEME="https"))

# Google Sheets setup
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    "gsheets_api_key.json", scope
)
gc = gspread.authorize(credentials)

@app.route("/")
def redirect_to_login():
    """Redirects to the signup page."""
    return redirect("/signup")

@app.route("/signup", methods=["GET", "POST"])
@app.route("/signup/<int:step>", methods=["GET", "POST"])
def signup(step=0):
    """
    Handles the signup process in multiple steps.
    Input: Step number as an integer.
    Output: HTML content for the corresponding step.
    """
    match step:
        case 0:
            return login()
        case 1:
            return form()
        case 2:
            return account_2fa_process()

    abort(404)

def login():
    """Handles the login step of the signup process."""
    if request.method == "POST":
        return redirect("/signup/1")

    return render_template("login.html")

def form():
    """Handles the form input step of the signup process."""
    if request.method == "POST":
        session["form_data"] = {key: request.form.get(key) for key in request.form}

        if session["form_data"]["coupon_option"] == "yes":
            return redirect("/coupon")

        return redirect("/signup/2")

    return render_template("form.html")

def account_2fa_process():
    """
    Processes the 2FA setup and handles Google Sheets and Stripe integration.
    """
    if request.method == "POST":
        session["form_data"] = session["form_data"] | request.form

        # Adding info to g sheets
        wks = gc.open("Atomic Freebie Accounts From Site").sheet1
        form_data = session["form_data"]
        discord_server = form_data.get("discord_server")
        account_email = form_data.get("account_email")
        account_password = form_data.get("account_password")
        account_2fa_code = form_data.get("2FA_16_digit_code")
        coupon_code = form_data.get("coupon_code")
        discord_user = session["user"]
        email_password = f"{account_email}:{account_password}"
        guilds = session["guilds"]
        wks.append_row(
            [
                discord_server,
                email_password,
                account_2fa_code,
                json.dumps(discord_user),
                json.dumps(guilds),
            ]
        )

        # Sending to stripe checkout link if no coupon code
        try:

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price": STRIPE_PRICE,
                        "quantity": 1,
                    },
                ],
                mode="subscription",
                customer_email=session["form_data"].get("account_email"),
                success_url=url_for("confirmation", _external=True)
                + "?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=url_for("signup", step=2, _external=True),
                discounts=[{"coupon": coupon_code}] if coupon_code else [],
            )
        except Exception as e:
            return {"message": str(e)}

        return redirect(checkout_session.url, code=303)

    return render_template("2fa_process.html")

@app.route("/coupon", methods=["GET", "POST"])
def coupon():
    """
    Handles coupon validation and application during the signup process.
    """
    if request.method == "POST":
        promotion_code = request.form.get("coupon_code")

        if not promotion_code:
            return {"message": "Coupon code is required."}, 422

        promos = stripe.PromotionCode.list(code=promotion_code)

        if len(promos.data) < 1:
            return {"valid": False, "message": "Invalid coupon code. Please try again."}

        promo = promos.data[0]
        coupon_code = promo.coupon.id
        session["form_data"]["coupon_code"] = coupon_code
        session["form_data"] = session["form_data"]

        return {
            "valid": True,
            "message": "Coupon code has been applied!",
            "redirect": "/signup/2",
        }

    return render_template("coupon_code_input.html")

@app.route("/callback", methods=["GET"])
def callback():
    """
    Handles the OAuth2 callback for Discord authentication.
    """
    session["oauth2_state"] = generate()
    code = request.args.get("code")

    auth = OAuth2Session(
        OAUTH2_CLIENT_ID,
        redirect_uri=OAUTH2_REDIRECT_URL(),
        scope=["identify", "guilds.join", "messages.read", "guilds"],
    )
    token = auth.fetch_token(
        TOKEN_URL,
        code=code,
        client_id=OAUTH2_CLIENT_ID,
        client_secret=OAUTH2_CLIENT_SECRET,
        authorization_response=request.url,
    )

    data = auth.get("https://discord.com/api/users/@me").json()
    guilds = [
        x["id"] for x in auth.get("https://discord.com/api/users/@me/guilds").json()
    ]

    session["user"] = data
    session["guilds"] = guilds
    session["oauth2_token"] = token
    return redirect("/signup/1")

@app.route("/signup/discord")
def discord_signup():
    """
    Generates the Discord signup URL and redirects to it for OAuth2 authentication.
    """
    # generate this in the discord console
    redirect_url = urllib.parse.quote(
        OAUTH2_REDIRECT_URL(),
        safe="",
        encoding=None,
        errors=None,
    )

    return redirect(
        f"https://discord.com/oauth2/authorize?client_id={OAUTH2_CLIENT_ID}&response_type=code&redirect_uri={redirect_url}&scope=identify+guilds.join+messages.read+guilds"
    )

@app.route("/confirmation", methods=["GET"])
def confirmation():
    """
    Handles the confirmation of payment and sends notifications through Discord webhooks.
    """
    session_id = request.args.get("session_id")

    if not session_id:
        abort(422)

    checkout_session = stripe.checkout.Session.retrieve(session_id)

    if checkout_session.payment_status == "paid":
        # Send the webhook
        webhook_url = "https://discord.com/api/webhooks/1134271058040602635/ZfWkacyP_m96WG5R5jhCIp7O_ZTxzjoAy0vRCxonho1Zv91hH0shTJrfpsds1OlIe3LV"
        hook = Webhook(
            webhook_url,
            avatar_url="https://media.discordapp.net/attachments/874197963105271878/1007554190463221780/unknown.png?width=552&height=552",
        )
        embed = Embed(title="New Freebie Signup", color=0x464198)

        for key, value in session["form_data"].items():
            if "tos" not in key and key != "form_id":
                embed.add_field(
                    name=(key.replace("_", " ").title()),
                    value=f"`{value}`",
                    inline=False,
                )

        form = session["form_data"]

        embed.add_field(
            name="Account Info",
            value=f"{form['account_email']}:{form['account_password']};INPUT_PROXY;{form['2FA_16_digit_code']}",
        )

        hook.send(
            "<@517937449939238943>", embed=embed, username="Freebie Account Manager"
        )

        # add user to server
        user_id = session["user"]["id"]

        # open a dm channel from the bot to user
        # the access token for the user is required for this step, and as such requires user authentication
        join_resp = requests.put(
            f"https://discord.com/api/guilds/{GUILD_ID}/members/{user_id}",
            headers={"Authorization": "Bot " + BOT_TOKEN},
            json={"access_token": session["oauth2_token"]["access_token"]},
        )

        # send dm to user
        channel_resp = requests.post(
            f"https://discord.com/api/users/@me/channels",
            headers={"Authorization": "Bot " + BOT_TOKEN},
            json={"recipient_id": user_id},
        )
        dm_id = channel_resp.json()["id"]

        message = "Thanks for signing up for Freebie ACO. If you have any further questions, you can get in contact with our team by opening a support ticket in our Discord server - https://discord.gg/Engt3HHJmh."

        channel_resp = requests.post(
            f"https://discord.com/api/channels/{dm_id}/messages",
            headers={"Authorization": "Bot " + BOT_TOKEN},
            json={"content": message},
        )

    return render_template("confirmation.html")


if __name__ == "__main__":
    app.run(debug=True)
