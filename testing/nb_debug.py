"""
Precursor to CI: Quick notebook run and eye-balling the HTML output
"""
import nbformat
from nbconvert import HTMLExporter

from nbclient import NotebookClient

import os
import pandas as pd
import numpy as np
import opendp.smartnoise.core as sn

def try_sn():
    # establish data information
    #data_path = 'https://raw.githubusercontent.com/opendp/smartnoise-samples/86-requirements-fix/analysis/data/PUMS_california_demographics_1000/data.csv'
    data_path = os.path.join('.', 'data', 'PUMS_california_demographics_1000', 'data.csv')
    data_path = os.path.abspath(data_path)
    print('data_path', data_path)
    var_names = ["age", "sex", "educ", "race", "income", "married", "pid"]
    D = pd.read_csv(data_path)['age']
    D_mean_age = np.mean(D)
    print('D_mean_age', D_mean_age)

    # establish extra information for this simulation
    age_lower_bound = 0.
    age_upper_bound = 100.
    D_tilde = np.clip(D, age_lower_bound, age_upper_bound)
    D_tilde_mean_age = np.mean(D_tilde)
    data_size = 1000

    df = pd.read_csv(data_path)
    df_as_array = [list(row) for row in df.itertuples()]
    #df.values.tolist()
    print('D.values', df_as_array)

    n_sims = 2
    releases = []
    with sn.Analysis(dynamic=True) as analysis:
        data = sn.Dataset(path=data_path, column_names = var_names)
        #data = sn.Dataset(value=df_as_array, column_names=var_names)
        D = sn.to_float(data['age'])
        # preprocess data (resize is a no-op because we have the correct data size)
        D_tilde = sn.resize(sn.clamp(data=D, lower=0., upper=100.), number_rows=data_size)

        for index in range(n_sims):
        # get DP mean of age
            releases.append(sn.dp_mean(
                data=sn.impute(D_tilde),
                privacy_usage={'epsilon': 1}))

    accuracy = releases[0].get_accuracy(0.05)

    analysis.release()
    dp_values = [release.value for release in releases]
    print('Accuracy interval (with accuracy value {0}) contains the true mean on D_tilde with probability {1}'.format(
        round(accuracy, 4),
        np.mean([(D_tilde_mean_age >= val - accuracy) & (D_tilde_mean_age <= val + accuracy) for val in dp_values])))


def run_nb_test(nb_filename, output_fname):
    """test run"""
    print(f'(1) Run notebook: {nb_filename}')
    ye_notebook = nbformat.read(nb_filename, as_version=4)


    client = NotebookClient(ye_notebook,
                    timeout=600,
                    kernel_name='python3',
                    resources={'metadata': {'path': '.'}}
                    )

    client.execute()

    if not os.path.isdir('test_output'):
        os.makedirs('test_output')

    output_file = f'test_output/{output_fname}'
    nbformat.write(ye_notebook, output_file)
    print(f'(2) file written: {output_file}')

    ye_notebook2 = nbformat.read(output_file, as_version=4)
    # 2. Instantiate the exporter. We use the `classic` template for now; we'll get into more details
    # later about how to customize the exporter further.
    html_exporter = HTMLExporter()
    html_exporter.template_name = 'classic'

    # 3. Process the notebook we loaded earlier
    (body, resources) = html_exporter.from_notebook_node(ye_notebook)

    html_filename = f'{output_file}.html'
    open(html_filename, 'w').write(body)
    print(f'file written: {html_filename}')



def run_analysis_notebooks():
    os.chdir('../analysis')

    inputs = [
              #('accuracy_pitfalls.ipynb', 'out_accuracy_pitfalls.ipynb'),
              #('basic_data_analysis.ipynb', 'out_basic_data_analysis.ipynb'),
              #('covariance.ipynb', 'out_covariance.ipynb'),
              #('histograms.ipynb', 'out_histograms.ipynb'),
              #('unknown_dataset_size.ipynb', 'out_unknown_dataset_size.ipynb'),
              #('utility_laplace_mean.ipynb', 'out_utility_laplace_mean.ipynb'),
              #('tutorial_mental_health_in_tech_survey.ipynb', 'out_tutorial_mental_health_in_tech_survey.ipynb'),
              ('../attacks/simple_attack.ipynb', 'out_simple_attack.ipynb'),
            ]

    for input_nb, output_nb in inputs:
        run_nb_test(input_nb, output_nb)


def run_attack_notebooks():
    os.chdir('../attacks')

    inputs = [
              ('simple_attack.ipynb', 'out_simple_attack.ipynb'),
            ]

    for input_nb, output_nb in inputs:
        run_nb_test(input_nb, output_nb)

def run_reconstruction_notebooks():
    os.chdir('../attacks/reconstruction')

    inputs = [
              ('reconstruction.ipynb', 'out_reconstruction.ipynb'),
            ]

    for input_nb, output_nb in inputs:
        run_nb_test(input_nb, output_nb)

if __name__ == '__main__':
    #try_sn()
    run_analysis_notebooks()
    # run_attack_notebooks()
    # run_reconstruction_notebooks()