from flask import Flask, render_template, redirect, request, flash
#from flask_wtf import Form
from wtforms import Form, StringField, SelectField
from pricer import price_searcher
import requests
from forms import ProductSearchForm
import pandas as pd
import sqlalchemy

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Search')
def Search():
    arg1 = request.args['arg1']
    table_name = arg1.replace(' ', '')
    mydict = price_searcher(arg1)
    #print(mydict)
    strings = []
    df = pd.DataFrame(columns = ['product', 'description', 'image', 'site'])
    for key in mydict:
        string1 = f"{key} is selling the {arg1} {mydict[key][1]} for ${mydict[key][0]}"
        dict2 = {}
        dict2['product'] = arg1
        dict2['description'] = string1
        dict2['image'] = mydict[key][2]
        dict2['site'] = key
        strings.append(dict2)
        df = df.append(dict2, ignore_index = True)

    df = df.reset_index()
    df = df.rename(columns = {'index':'id'})

    rds_connection_string = "postgres:eagles@localhost:5432/ETL_Project_DB"
    engine = sqlalchemy.create_engine(f'postgresql://{rds_connection_string}')

    df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
    try:
        if not engine.dialect.has_table(engine, table_name):
            with engine.connect() as con:
                con.execute(f"ALTER TABLE {table_name} ADD PRIMARY KEY (id);")
    except sqlalchemy.exc.ProgrammingError as e:
        print('The table already exists')
    except sqlalchemy.exc.IntegrityError:
        print('The table already exists')

    return render_template('Search.html', results = strings, name = arg1)

if __name__ == '__main__':
    app.run(debug=True)






    #print('step 2')
    #print(item.form['text'])
    #print(item.form)
    #print(item)
    # results = price_searcher(form.product_name.data)
    # if len(results) > 0:
    #     print('step 3')
    #     return  render_template('search.html', results=results)
    # else:
    #     print('step 4')
    #     print('No results found!')
    #     return redirect('/')


    # form = ProductSearchForm()
    # if form.validate_on_submit():
    #     #flash('Valid Search Accepted')
    #     results = price_searcher(form.product_name.data)
    #     return render_template('Search.html', form = form, results = results)
    # else:
    #     return render_template('index.html')




# @app.route('/', methods=['GET', 'POST'])
#     def index():
#         if request.method == "POST":
#             dictionary = price_searcher(request)
#             return search_results(dictionary)
#
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     search = MusicSearchForm(request.form)
#     if request.method == 'POST':
#         return search_results(search)
#     return render_template('index.html', form=search)
#
# @app.route('/results')
# def search_results(dictionary):
#
#
# @app.route('/results')
# def search_results(search):
#     results = []
#     search_string = search.data['search']
#     if search.data['search'] == '':
#         qry = db_session.query(Album)
#         results = qry.all()
#     if not results:
#         flash('No results found!')
#         return redirect('/')
#     else:
#         # display results
#         return render_template('results.html', results=results)
