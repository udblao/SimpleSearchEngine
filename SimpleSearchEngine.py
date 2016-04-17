from flask import Flask, request, render_template
from BooleanSearch import BooleanSearch
from BuildTheFilesWeNeed import BuildTheFilesWeNeed
from VectorSpaceSearch import VectorSpaceSearch
from BasicSearch import BasicSearch
import json
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    contents = {}
    paths = {}
    ids = []
    index = 'please input'
    if request.method == 'POST':
        index = request.form['index']
        value = request.form['search']
        print(index)
        if index:
            print(value)
            if value == 'BasicSearch':
                ids = basic.search(index)
            elif value == 'VectorSpaceSearch':
                ids = vector.search(index)
            elif value == 'BooleanSearch':
                ids = boolean.search(index)
            else:
                index = 'SOME WRONG HAPPEN!!!'
            if ids:
                for id in ids:
                    paths.setdefault(id, boolean.get_document_path_by_id(id))
                    contents.setdefault(id, boolean.get_content_by_path(paths[id]))
    return render_template('index.html', ids=ids, contents=contents ,paths=paths, index=index)


if __name__ == '__main__':
    buildfiles = BuildTheFilesWeNeed()
    buildfiles.build_term_frequency_file()
    buildfiles.build_tfidvector_file()

    basic = BasicSearch()
    basic.basci_serach()

    vector = VectorSpaceSearch()
    vector.vector_space_search()

    boolean = BooleanSearch()
    boolean.boolean_search()

    app.run(debug=True)
