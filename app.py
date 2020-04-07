# Dependencies
import os
import sqlalchemy
import json
import decimal
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    make_response,
    session,
    abort,
    redirect,
    url_for,
    flash,
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import pymysql
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    BooleanField,
    TextField,
    PasswordField,
    SelectField,
    DateField,
    DecimalField,
    SubmitField,
)
from wtforms.validators import InputRequired, Length, NumberRange, EqualTo
import datetime as dt
from decimal import Decimal
from Query_Visual import createJson, creatUserPersonalJson, creatplotdata
import json
import plotly
import plotly.graph_objects as go

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

# Set the secret key value
app.secret_key = "1a2b3c4d5e"

# Enter your database connection details below
# app.config['MYSQL_HOST'] = '127.0.0.1'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'password'
# app.config['MYSQL_DB'] = 'usda'

# Intialize MySQL
# mysql = MySQL(app)

#################################################
# Set up the database
#################################################
HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = "root"
PASSWORD = "uv9y9g5t"
DIALECT = "mysql"
DRIVER = "pymysql"
DATABASE = "usda"

# Connect to DB in DB Server
db_connection_string = (
    f"{DIALECT}+{DRIVER}://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}"
)

# FOLLOWING CODE IS FOR HEROKU######
##################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = (
    os.environ.get("JAWSDB_URL", "") or db_connection_string
)
db = SQLAlchemy(app)


class Meal_record(db.Model):
    __tablename__ = "meal_record"

    meal_item_code = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    type = db.Column(db.String(50))
    meal_date = db.Column(db.Date)
    meal_desc = db.Column(db.String(256))
    amount = db.Column(db.Float)

    def __repr__(self):
        return "<Meal_record %r>" % (self.name)


class User_account(db.Model):
    __tablename__ = "user_account"

    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(50))
    confirm_password = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    gender = db.Column(db.String(50))
    date_of_birth = db.Column(db.Date)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    physical_activity_level = db.Column(db.String(50))

    def __repr__(self):
        return "<User_account %r>" % (self.name)

class Nutrition(db.Model):
    __tablename__ = "nutrition"

    NDB_No = db.Column(db.Integer, primary_key=True, autoincrement=False)
    Shrt_Desc = db.Column(db.Text)
    Water = db.Column(db.Float)
    Energy = db.Column(db.Integer)
    Protein = db.Column(db.Float)
    Lipid_Total = db.Column(db.Float)
    Carbohydrate = db.Column(db.Float)
    Fiber = db.Column(db.Float)
    Sugar_Total = db.Column(db.Float)
    Calcium = db.Column(db.Integer)
    Iron = db.Column(db.Float)
    Magnesium = db.Column(db.Float)
    Phosphorus = db.Column(db.Integer)
    Potassium = db.Column(db.Integer)
    Sodium = db.Column(db.Integer)
    Zinc = db.Column(db.Float)
    Copper = db.Column(db.Float)
    Manganese = db.Column(db.Float)
    Selenium = db.Column(db.Float)
    Vitamin_C = db.Column(db.Float)
    Thiamin = db.Column(db.Float)
    Riboflavin = db.Column(db.Float)
    Niacin = db.Column(db.Float)
    Panto_Acid = db.Column(db.Float)
    Vitamin_B6 = db.Column(db.Float)
    Folate_Total = db.Column(db.Float)
    Folic_Acid = db.Column(db.Float)
    Food_Folate_mcg = db.Column(db.Float)
    Folate_DFE_mcg = db.Column(db.Float)
    Choline_Tot_mg = db.Column(db.Float)
    Vitamin_B12 = db.Column(db.Float)
    Vit_A_IU = db.Column(db.Integer)
    Vitamin_A = db.Column(db.Float)
    Retinol = db.Column(db.Float)
    Alpha_Carot_mcg = db.Column(db.Float)
    Beta_Carot_mcg = db.Column(db.Float)
    Beta_Crypt_mcg = db.Column(db.Float)
    Lycopene_mcg = db.Column(db.Float)
    Lut_Zea_mcg = db.Column(db.Float)
    Vitamin_E = db.Column(db.Float)
    Vitamin_D = db.Column(db.Float)
    Vit_D_IU = db.Column(db.Float)
    Vitamin_K = db.Column(db.Float)
    FA_Sat_g = db.Column(db.Float)
    FA_Mono_g = db.Column(db.Float)
    FA_Poly_g = db.Column(db.Float)
    Cholestrol = db.Column(db.Integer)
    Weight_grams = db.Column(db.Float)
    Weight_desc = db.Column(db.Text)
    GmWt_2 = db.Column(db.Float)
    GmWt_Desc2 = db.Column(db.Text)
    Refuse_Pct = db.Column(db.Integer)
    def __repr__(self):
        return "<Nutrition %r>" % (self.name)


@app.before_first_request
def setup():
    db.create_all()


# ABOVE CODE IS FOR HEROKU######
###################################################

# Commented when using a different method for Heroku
# engine = create_engine(db_connection_string)
# inspector = inspect(engine)
# table_names = inspector.get_table_names()
# print("Table names are: ", table_names)
# Set up the base class
# Base = automap_base()
# Base.prepare(db.engine, reflect=True)
# # print(Base.classes.values)
# # Table names
# User_account = Base.classes.user_account
# Meal_record = Base.classes.meal_record
# Nutrition = Base.classes.nutrition
# Create the database session
# session_db = Session(bind=engine)
# print("session_db is: ", session_db)
# Comment code above for heroku deployment

#############################################################################################
# Route #1("/")
# Home Page
#############################################################################################
@app.route("/index.html")
@app.route("/")
def main():
    session["page"] = " "
    # Check if the user is already logged in
    # If user is logged in then re-route to dashborad page
    if checkLoggedIn() == True:
        session["page"] = "dashboard"
        return redirect("/dashboard")
    # else route to home page
    session["page"] = " "
    return render_template("index.html")


#############################################################################################
# Route #2(/login)
# Design a query for the existing user to login
#############################################################################################


@app.route("/login", methods=["GET", "POST"])
def login():
    # Output message if something goes wrong...
    msg = ""
    print("Start of stuff")
    # Check if "username" and "password" POST requests exist (user submitted form)
    if (
        request.method == "POST"
    ):  # and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        request_username = request.form["username"]
        request_password = request.form["password"]
        # Check if account exists using MySQL
        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute('SELECT * FROM user_accounts WHERE username = %s AND password = %s', (username, password))
        if request_username and request_password:
            # Fetch one record and return result
            print(
                "request_username: "
                + request_username
                + " | request_password: "
                + request_password
            )
            account = loginsys(request_username, request_password)
            # If account exists in accounts table in out database
            if account:
                # Create session data, we can access this data in other routes
                session["loggedin"] = True
                session["username"] = account[3]
                # Redirect to home page
                session["page"] = "dashboard"
                return redirect("/dashboard")
            else:
                # Account doesnt exist or username/password incorrect
                msg = "Incorrect username/password!"
    session["page"] = " "
    return render_template("index.html", msg=msg)


def loginsys(username, password):
    print("Username: " + username + " Password: " + password)
    user_ls = (
        db.session.query(
            User_account.first_name,
            User_account.last_name,
            User_account.gender,
            User_account.username,
        )
        .filter(User_account.username == username)
        .filter(User_account.password == password)
        .first()
    )
    print("user_ls: " + str(user_ls))
    return user_ls


##############################################################################################
# Route #3(/register)
# Design a query for the register a new user
#############################################################################################


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=4, max=20)]
    )
    password = PasswordField("Password", validators=[InputRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    first_name = StringField(
        "First Name", validators=[InputRequired(), Length(min=2, max=50)]
    )
    last_name = StringField(
        "Last Name", validators=[InputRequired(), Length(min=2, max=50)]
    )
    gender = SelectField("Gender", choices=[("male", "Male"), ("female", "Female")])
    date_of_birth = DateField("Bate of Birth (YYYY-MM-DD)", format="%Y-%m-%d")
    height = DecimalField(
        "Height (Inches)",
        places=2,
        rounding=None,
        validators=[InputRequired(), NumberRange(min=0, max=500, message="Blah")],
    )
    weight = DecimalField(
        "Weight (Pounds)",
        places=2,
        rounding=None,
        validators=[InputRequired(), NumberRange(min=0, max=2000, message="Blah")],
    )
    physical_activity_level = SelectField(
        "Physical Activity Level",
        choices=[
            ("sedentary", "Sedentary"),
            ("lightly active", "Lightly Active"),
            ("moderately active", "Moderately Active"),
            ("very active", "Very Active"),
            ("extra active", "Extra Active"),
        ],
    )
    submit = SubmitField("Get Started")


@app.route("/register", methods=["GET", "POST"])
def register():

    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", "success")

        new_user = User_account(
            username=form.username.data,
            password=form.password.data,
            confirm_password=form.confirm_password.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            gender=form.gender.data,
            date_of_birth=form.date_of_birth.data,
            height=form.height.data,
            weight=form.weight.data,
            physical_activity_level=form.physical_activity_level.data,
        )
        db.session.add(new_user)
        db.session.commit()

        return redirect("/dashboard")
    return render_template("New_user.html", form=form)


##############################################################################################
# Route #4(/home)
# This will be the home page, only accessible for loggedin users
#############################################################################################


class AddMeal(FlaskForm):
    inputdate = DateField("inputdate", format="%Y-%m-%d")
    meal_category = StringField("meal_category", validators=[InputRequired()])
    food_desc = StringField("food_desc", validators=[InputRequired()])
    servings_count = DecimalField(
        "servings_count",
        places=2,
        rounding=None,
        validators=[InputRequired(), NumberRange(min=0, max=20)],
    )
    foodNameId = DecimalField("foodNameId")
    submit = SubmitField("Add")


# Code to display daily statistics on dashboard
# daily_goal_list = [1800, 130, 25, 2200, 25, 25.2]


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if checkLoggedIn() == False:
        return redirect("/login")

    session["page"] = "dashboard"

    # Code to display daily statistics on dashboard - part 1

    daily_goal_list = [1800, 130, 25, 2200, 25, 25.2]
    form = AddMeal(request.form)
    if form.validate_on_submit():
        # flash(f'Meal Added for {form.meal_category.data}!', 'successfully')

        new_meal = Meal_record(
            username=session["username"],
            meal_date=form.inputdate.data,
            type=form.meal_category.data,
            meal_desc=form.food_desc.data,
            amount=form.servings_count.data,
            meal_item_code=form.foodNameId.data,
        )
        db.session.add(new_meal)
        db.session.commit()

        print("Adding meal")
        return redirect("/dashboard")

    # Code to display daily statistics on dashboard - part 2
    # display_stats
    cmd = (
        db.session.query(
            func.round(
                func.coalesce(func.sum((Nutrition.Energy / 100)
                            * (Meal_record.amount)
                            * (Nutrition.Weight_grams)), 0), 2
            ).label("cal"),
            func.round(
                func.coalesce(
                    func.sum((Nutrition.Carbohydrate/100) 
                    * (Meal_record.amount)
                    * (Nutrition.Weight_grams)), 0
                ),
                2,
            ).label("carbs"),
            func.round(
                func.coalesce(
                    func.sum((Nutrition.Lipid_Total/100) 
                    * (Meal_record.amount)
                    * (Nutrition.Weight_grams)), 0
                ),
                2,
            ).label("fats"),
            func.round(
                func.coalesce(func.sum((Nutrition.Sodium/100) 
                * (Meal_record.amount)
                 * (Nutrition.Weight_grams)), 0), 2
            ).label("sodium"),
            func.round(
                func.coalesce(
                    func.sum((Nutrition.Sugar_Total/100) 
                    * (Meal_record.amount)
                     * (Nutrition.Weight_grams)), 0
                ),
                2,
            ).label("sugar"),
            func.round(
                func.coalesce(func.sum((Nutrition.Fiber/100) 
                * (Meal_record.amount)
                * (Nutrition.Weight_grams)), 0), 2
            ).label("fiber"),
            func.count().label("cnt"),
        )
        .filter(Meal_record.username == session["username"])
        .filter(Meal_record.meal_item_code == Nutrition.NDB_No)
        .filter(Meal_record.meal_date == dt.date.today())
    )
    daily_stats = cmd.first()

    results = [0.0, 0, 0, 0, 0, 0]

    if daily_stats.cnt != 0:
        results = [
            float(daily_stats.cal),
            float(daily_stats.carbs),
            float(daily_stats.fats),
            float(daily_stats.sodium),
            float(daily_stats.sugar),
            float(daily_stats.fiber),
        ]
    #      cmd = session_db.query(func.round(func.sum(Nutrition.Energy),0).label('cal'),\
    #                                 func.round(func.sum(Nutrition.Carbohydrate),2).label('carbs'),\
    #                                 func.round(func.sum(Nutrition.Lipid_Total),0).label('fats'),\
    #                                 func.round(func.sum(Nutrition.Sodium), 2).label('sodium'),\
    #                                 func.round(func.sum(Nutrition.Sugar_Total),2).label('sugar'),\
    #                                 func.round(func.sum(Nutrition.Fiber),2).label('fiber'),\
    #                                 func.count().label('cnt')).\
    #                                 filter(Meal_record.username == session['username']).\
    #                                 filter(Meal_record.meal_item_code == Nutrition.NDB_No).\
    #                                 filter(Meal_record.meal_date == dt.date.today())
    #     daily_stats = cmd.first()

    #     results = [0,0,0,0,0,0]

    #     if(daily_stats.cnt!=0):
    #         results = [daily_stats.cal, daily_stats.carbs, daily_stats.fats, daily_stats.sodium, daily_stats.sugar, daily_stats.fiber]
    # >>>>>>> master
    print("daily stats are: ", daily_stats)
    print("daily stats cnt: ", daily_stats.cnt)

    # Code to display last 5 entries on dashboard
    # <<<<<<< display_stats
    top5_entries = (
        db.session.query(Meal_record)
        .filter(Meal_record.username == session["username"])
        .order_by(Meal_record.meal_date.desc())
        .limit(5)
    )

    # print("Meal desc for the entry on dashbord are: ", top5_entries[4].meal_desc)
    # top5_entries_l = [top5_entries[i] for i in range(6)]
    # print(top5_entries_l[0].meal_date)
    return render_template(
        "dashboard.html",
        form=form,
        results=results,
        daily_goal_list=daily_goal_list,
        top5_entries=top5_entries,
        daily_stats=daily_stats,
    )


@app.route("/intake")
def food_tracker():
    if checkLoggedIn() == False:
        return redirect("/login")

    session["page"] = "intake"
    # Code to display last 100 entries on food_diary
    top100_entries = (
        db.session.query(Meal_record)
        .filter(Meal_record.username == session["username"])
        .order_by(Meal_record.meal_date.desc())
        .limit(100)
    )

    return render_template("food_history.html", top100_entries=top100_entries)


@app.route("/analysis", methods=['GET'])
def analysis():
    if checkLoggedIn() == False:
        return redirect("/login")
    session["page"] = "analysis"
    
    # plot_type = request.args.get("selectnutrients")
    plot_type = "All"
    desired_date = request.args.get("date")

    if request.method == 'GET' and desired_date:
       
        cmd = (
            db.session.query(
                func.round(
                    func.coalesce(
                        func.sum(
                            (Nutrition.Energy / 100)
                            * (Meal_record.amount)
                            * (Nutrition.Weight_grams)
                        ),
                        0,
                    ),
                    2,
                ).label("cal"),
                func.round(
                    func.coalesce(
                        func.sum(
                            (Nutrition.Water / 100)
                            * (Meal_record.amount)
                            * (Nutrition.Weight_grams)
                        ),
                        0,
                    ),
                    2,
                ).label("water"),
                func.round(
                    func.coalesce(
                        func.sum(
                            (Nutrition.Carbohydrate / 100)
                            * (Meal_record.amount)
                            * (Nutrition.Weight_grams)
                        ),
                        0,
                    ),
                    2,
                ).label("carbs"),
                func.round(
                    func.coalesce(
                        func.sum(
                            (Nutrition.Fiber / 100)
                            * (Meal_record.amount)
                            * (Nutrition.Weight_grams)
                        ),
                        0,
                    ),
                    2,
                ).label("fiber"),
                func.round(
                    func.coalesce(
                        func.sum(
                            (Nutrition.Protein / 100)
                            * (Meal_record.amount)
                            * (Nutrition.Weight_grams)
                        ),
                        0,
                    ),
                    2,
                ).label("protein"),
                func.round(
                    func.coalesce(
                        func.sum(
                            (Nutrition.Calcium / 100)
                            * (Meal_record.amount)
                            * (Nutrition.Weight_grams)
                        ),
                        0,
                    ),
                    2,
                ).label("calcium"),
                func.round(
                    func.coalesce(
                        func.sum(
                            (Nutrition.Copper / 100)
                            * (Meal_record.amount)
                            * (Nutrition.Weight_grams)
                        ),
                        0,
                    ),
                    2,
                ).label("copper"),
                func.round(
                    func.coalesce(
                        func.sum(
                            (Nutrition.Iron / 100)
                            * (Meal_record.amount)
                            * (Nutrition.Weight_grams)
                        ),
                        0,
                    ),
                    2,
                ).label("iron"),
                func.round(
                    func.coalesce(
                        func.sum(
                            (Nutrition.Magnesium / 100)
                            * (Meal_record.amount)
                            * (Nutrition.Weight_grams)
                        ),
                        0,
                    ),
                    2,
                ).label("magnesium"),
                func.round(
                    func.coalesce(
                        func.sum(
                            (Nutrition.Manganese / 100)
                            * (Meal_record.amount)
                            * (Nutrition.Weight_grams)
                        ),
                        0,
                    ),
                    2,
                ).label("manganese"),
                func.round(
                    func.coalesce(
                        func.sum(
                            (Nutrition.Phosphorus / 100)
                            * (Meal_record.amount)
                            * (Nutrition.Weight_grams)
                        ),
                        0,
                    ),
                    2,
                ).label("phosphorus"),
                func.round(
                    func.coalesce(
                        func.sum(
                            (Nutrition.Selenium / 100)
                            * (Meal_record.amount)
                            * (Nutrition.Weight_grams)
                        ),
                        0,
                    ),
                    2,
                ).label("selenium"),
                func.round(
                    func.coalesce(
                        func.sum(
                            (Nutrition.Zinc / 100)
                            * (Meal_record.amount)
                            * (Nutrition.Weight_grams)
                        ),
                        0,
                    ),
                    2,
                ).label("zinc"),
                func.round(
                    func.coalesce(
                        func.sum(
                            (Nutrition.Potassium / 100)
                            * (Meal_record.amount)
                            * (Nutrition.Weight_grams)
                        ),
                        0,
                    ),
                    2,
                ).label("potassium"),
                func.round(
                    func.coalesce(
                        func.sum(
                            (Nutrition.Sodium / 100)
                            * (Meal_record.amount)
                            * (Nutrition.Weight_grams)
                        ),
                        0,
                    ),
                    2,
                ).label("sodium"),
                func.round(
                    func.coalesce(
                        func.sum(
                            (Nutrition.Vitamin_A / 100)
                            * (Meal_record.amount)
                            * (Nutrition.Weight_grams)
                        ),
                        0,
                    ),
                    2,
                ).label("vitamin_A"),
                func.round(
                    func.coalesce(
                        func.sum(
                            (Nutrition.Vitamin_C / 100)
                            * (Meal_record.amount)
                            * (Nutrition.Weight_grams)
                        ),
                        0,
                    ),
                    2,
                ).label("vitamin_C"),
                func.round(
                    func.coalesce(
                        func.sum(
                            (Nutrition.Vitamin_D / 100)
                            * (Meal_record.amount)
                            * (Nutrition.Weight_grams)
                        ),
                        0,
                    ),
                    2,
                ).label("vitamin_D"),
                func.round(
                    func.coalesce(
                        func.sum(
                            (Nutrition.Vitamin_E / 100)
                            * (Meal_record.amount)
                            * (Nutrition.Weight_grams)
                        ),
                        0,
                    ),
                    2,
                ).label("vitamin_E"),
                func.round(
                    func.coalesce(
                        func.sum(
                            (Nutrition.Vitamin_K / 100)
                            * (Meal_record.amount)
                            * (Nutrition.Weight_grams)
                        ),
                        0,
                    ),
                    2,
                ).label("vitamin_K"),
                func.round(
                    func.coalesce(
                        func.sum(
                            (Nutrition.Thiamin / 100)
                            * (Meal_record.amount)
                            * (Nutrition.Weight_grams)
                        ),
                        0,
                    ),
                    2,
                ).label("thiamin"),
                func.round(
                    func.coalesce(
                        func.sum(
                            (Nutrition.Riboflavin / 100)
                            * (Meal_record.amount)
                            * (Nutrition.Weight_grams)
                        ),
                        0,
                    ),
                    2,
                ).label("riboflavin"),
                func.round(
                    func.coalesce(
                        func.sum(
                            (Nutrition.Niacin / 100)
                            * (Meal_record.amount)
                            * (Nutrition.Weight_grams)
                        ),
                        0,
                    ),
                    2,
                ).label("niacin"),
                func.round(
                    func.coalesce(
                        func.sum(
                            (Nutrition.Vitamin_B6 / 100)
                            * (Meal_record.amount)
                            * (Nutrition.Weight_grams)
                        ),
                        0,
                    ),
                    2,
                ).label("vitamin_B6"),
                func.round(
                    func.coalesce(
                        func.sum(
                            (Nutrition.Folate_Total / 100)
                            * (Meal_record.amount)
                            * (Nutrition.Weight_grams)
                        ),
                        0,
                    ),
                    2,
                ).label("folate"),
                func.round(
                    func.coalesce(
                        func.sum(
                            (Nutrition.Vitamin_B12 / 100)
                            * (Meal_record.amount)
                            * (Nutrition.Weight_grams)
                        ),
                        0,
                    ),
                    2,
                ).label("vitamin_B12"),
                func.round(
                    func.coalesce(
                        func.sum(
                            (Nutrition.Panto_Acid / 100)
                            * (Meal_record.amount)
                            * (Nutrition.Weight_grams)
                        ),
                        0,
                    ),
                    2,
                ).label("panto_acid_VB5"),
                func.round(
                    func.coalesce(
                        func.sum(
                            (Nutrition.Choline_Tot_mg / 100)
                            * (Meal_record.amount)
                            * (Nutrition.Weight_grams)
                        ),
                        0,
                    ),
                    2,
                ).label("choline"),
                func.round(
                    func.coalesce(
                        func.sum(
                            (Nutrition.Lipid_Total / 100)
                            * (Meal_record.amount)
                            * (Nutrition.Weight_grams)
                        ),
                        0,
                    ),
                    2,
                ).label("fats"),
            )
            .join(Meal_record, Nutrition.NDB_No == Meal_record.meal_item_code)
            .filter(Meal_record.username == session["username"])
            .filter(Meal_record.meal_date == desired_date)
        )

        daily_stats = cmd.first()

        userdata_nutrition_data = createJson(daily_stats)
        cmd1 = (
            db.session.query(
                User_account.height.label("height"),
                User_account.weight.label("weight"),
                User_account.physical_activity_level.label("phy"),
                User_account.gender.label("gender"),
                User_account.date_of_birth.label("dob"),
            )
            .join(Meal_record, User_account.username == Meal_record.username)
            .filter(User_account.username == session["username"])
        )
        user_info = cmd1.first()
        user_personal_data = creatUserPersonalJson(user_info)
        print(user_personal_data)

        user_info = {
            "userdata_nutrition_data": userdata_nutrition_data,
            "user_personal_data": user_personal_data,
            "plot_type": plot_type,
        }
        graphJSON = creatplotdata(user_info)
        ids = ["plot1", "plot2","plot3"]
                
        return render_template("Daily_vizualization.html", ids=ids, graphJSON=graphJSON)  
    return render_template("Daily_vizualization.html")


def checkLoggedIn():
    if "loggedin" in session:
        if session["loggedin"] == True:
            return True
    return False


@app.route("/nutrition", methods=["GET"])
def nutrition():
    if checkLoggedIn() == False:
        return redirect("/login")
    session["page"] = "nutrition"

    ndbNo = request.args.get("ndbNo")

    if ndbNo:
        nutriData = (
            db.session.query(Nutrition).filter(Nutrition.NDB_No == ndbNo).first()
        )
        return render_template("nutrition.html", nutriData=nutriData)

    return render_template("nutrition.html")


# @app.route('/register')
# def register():
#     session['page']='register'
#     return render_template("New_user.html")


@app.route("/intake")
def intake():
    if checkLoggedIn() == False:
        return redirect("/login")
    session["page"] = "intake"
    return render_template("intake.html")


@app.route("/logout")
def logout():
    if checkLoggedIn() == False:
        session["page"] = " "
        return render_template("login.html", msg="Already logged out!")
    else:
        session["loggedin"] = False
        messages = "loggedout"
        session["messages"] = messages
        session["page"] = " "
        return redirect("/")


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


@app.route("/nutriquicksearch", methods=["GET"])
def nutriquicksearch():
    searchkey = request.args.get("term")
    if not searchkey:
        return '{  "data": [] } '
    resultSet = (
        db.session.query(
            Nutrition.NDB_No,
            Nutrition.Shrt_Desc,
            Nutrition.Weight_desc,
            Nutrition.Weight_grams,
        )
        .filter(Nutrition.Shrt_Desc.ilike("%" + searchkey + "%"))
        .all()
    )
    return json.dumps(resultSet, cls=DecimalEncoder)


if __name__ == "__main__":
    app.run(debug=True)
    # app.run()
