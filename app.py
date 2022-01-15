from flask import Flask, request, render_template
from singleasset_helper import get_asset_data


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        collection_slug = request.form.get("collection_name")
        token_id = request.form.get("token_id")
        try:
            data = get_asset_data(collection_slug, token_id)
        except Exception:
            data = get_asset_data('boredapeyachtclub', 1234)
            data['id'] = "ERROR!!!"
            print("Error")
    else:
        data = get_asset_data('boredapeyachtclub', 1234)
    return render_template('index.html', data=data)


@app.route("/about", methods=["GET", "POST"])
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run()
