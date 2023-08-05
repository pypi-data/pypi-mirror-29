import os
import json

from delphi.core import *
from delphi.utils import ltake, lfilter, compose, lmap, lzip, repeat
from delphi import app

from typing import List, Optional, Dict
import numpy as np
from delphi.state import State

from flask import render_template, request, redirect
from flask.cli import FlaskGroup

from functools import partial
from glob import glob
from pandas import Series
from itertools import cycle

from indra.statements import Influence
from indra.sources import eidos
from indra.assemblers import CAGAssembler 


import matplotlib as mpl

mpl.rcParams.update({
    "font.family": "serif", # use serif/main font for text elements
    "text.usetex": True,    # use inline math for ticks
    "font.serif": 'Palatino',
    "figure.figsize": [4,3],
})
mpl.use('Agg')

from matplotlib import pyplot as plt
import seaborn as sns
plt.style.use('ggplot')

state = State()

@app.route('/')
def show_index():
    """ Show the index page. """
    return render_template('index.html', 
                           text = "Input text to be processed here",
                           state = state)


@app.route("/processText")
def process_text():
    """ Process the input text. """

    # Clean up old data.
    for filename in glob('static/*.png')+glob('*.json'):
        os.remove(filename)

    state.inputText = request.args.get('textToProcess', '')
    eidos.process_text(state.inputText)
    return redirect('/setupExperiment')


@app.route("/setupExperiment")
def setupExperiment():
    """ Set up the experiment, get initial values of parameters. """
    state.statements = eidos.process_json_file('eidos_output.json').statements
    cag_assembler = CAGAssembler(state.statements)
    state.CAG = cag_assembler.make_model()
    state.elementsJSON = cag_assembler.export_to_cytoscapejs()
    with open('elements.json', 'w') as f:
        f.write(json.dumps(state.elementsJSON, indent=2))

    # Create keys for factors and their time derivatives
    
    state.factors = lmap(lambda n: n['data']['id'],
            filter(lambda n: n['data']['simulable'], state.elementsJSON['nodes']))
    state.escapedFactorNames = lmap(lambda n: n.replace(' ', '_'), state.factors)
    state.s_index = flatMap(lambda n: (n, f'∂{n}/∂t'), state.factors)

    # Set defaults
    state.sigmas = dict(lzip(state.factors, ltake(len(state.factors), repeat(1.0))))
    state.s0 = dict(lzip(state.s_index, ltake(len(state.s_index), cycle([100,0]))))

    state.elementsJSONforJinja = json.dumps(state.elementsJSON)
    return render_template("index.html", state = state)

@app.route("/runExperiment", methods=["POST"])
def make_histograms():
    """ Make histograms """
    initialValues=dict(lzip(state.s_index,request.form.getlist('initialValue')))
    sigmas = dict(lzip(state.factors, request.form.getlist('sigma')))

    for f in state.factors:
        state.sigmas[f]=float(sigmas[f])

    for k in state.s_index:
        state.s0[k]=float(initialValues[k])

    state.n_steps   = int(request.form.get('nsteps'))
    state.n_samples = int(request.form.get('nsamples'))
    state.Δt = float(request.form.get('Δt'))
    sampled_sequences = sample_sequences(state.statements,
            Series(state.s0, index = state.s0.keys()),
            n_steps = state.n_steps, n_samples = state.n_samples)

    fig, axes = plt.subplots()

    for i in range(len(state.factors)):
        for j in range(state.n_steps):
            axes.clear()
            compose(partial(sns.distplot, ax=axes), np.random.normal, np.array)(
                    lfilter(lambda v: abs(v) < 200,
                            map(lambda s: s[j][::2][i], sampled_sequences)))
            axes.set_xlim(0, 200)
            plt.tight_layout()
            fig.savefig(f'static/{state.escapedFactorNames[i]}_{j}.png', dpi=150)

    for n in state.elementsJSON['nodes']:
        n['data']['backgroundImage'] =  f'static/{n["data"]["id"]}_0.png'

    state.elementsJSONforJinja = json.dumps(state.elementsJSON)
    state.histos_built = True

    return render_template('index.html', state = state)

