import pandas as pd
from flask import Flask, request, render_template
import joblib

MODELS_PATH = "models/"
ETR_MODEL_PATH = MODELS_PATH + "exp_a_etr_model.pkl"
XGBC_MODEL_PATH = MODELS_PATH + "exp_b_xgbc_model.pkl"
models = {
    "etr": ETR_MODEL_PATH,
    "xgbc": XGBC_MODEL_PATH
}
data = {
    'features_dict': {
        "idade": {
            "label": "Idade", 
            "type": "number"},
        "dt_internacao": {
            "label": "Data de internação",
            "type": "datetime-local"
            },
        "n_coletas_creatinina": {
            "label": "Número de coletas de creatinina (atual)",
            "type": "number"
            },
        "valor_creatinina": {
            "label": "Valor da creatinina (atual)", 
            "type": "number"
            },
        "dt_creatinina": {
            "label": "Data da coleta da creatinina",
            "type": "datetime-local"
            },
        "valor_controle_Frequência Cardíaca": {
            "label": "Valor do controle da frequência cardíaca (atual)",
            "type": "number"
            },
        "dt_controle_Frequência Cardíaca": {
            "label": "Data do controle da frequência cardíaca",
              "type": "datetime-local"
              },
        "valor_controle_Frequência Respiratória": {
            "label": "Valor do controle da frequência respiratória (atual)",
            "type": "number"
            },
        "dt_controle_Frequência Respiratória": {"label": "Diferença entre a data do controle da frequência respiratória", "type": "datetime-local"},
        "valor_controle_Pressão Arterial Diastólica": {"label": "Valor do controle da pressão arterial diastólica (atual)", "type": "number"},
        "dt_controle_Pressão Arterial Diastólica": {"label": "Diferença entre a data do controle da pressão arterial diastólica", "type": "datetime-local"},
        "valor_controle_Pressão Arterial Sistólica": {"label": "Valor do controle da pressão arterial sistólica (atual)", "type": "number"},
        "dt_controle_Pressão Arterial Sistólica": {"label": "Diferença entre a data do controle da pressão arterial sistólica", "type": "datetime-local"},
        "valor_controle_Temperatura  Axilar": {"label": "Valor do controle da temperatura axilar (atual)", "type": "number"},
        "dt_controle_Temperatura  Axilar": {"label": "Diferença entre a data do controle da temperatura axilar", "type": "datetime-local"},
        "variacao_valor_creatinina_1": {"label": "Variação do valor da creatinina (1)", "type": "number"},
        "diff_entre_dt_creatinina_1": {"label": "Diferença entre a data de coleta da creatinina (1) e a data de internação", "type": "datetime-local"},
        "variacao_valor_controle_1_Frequência Cardíaca": {"label": "Variação do valor do controle da frequência cardíaca (1)", "type": "number"},
        "diff_entre_dt_controle_1_Frequência Cardíaca": {"label": "Diferença entre a data do controle da frequência cardíaca (1) e a data de internação", "type": "datetime-local"},
        "variacao_valor_controle_1_Frequência Respiratória": {"label": "Variação do valor do controle da frequência respiratória (1)", "type": "number"},
        "diff_entre_dt_controle_1_Frequência Respiratória": {"label": "Diferença entre a data do controle da frequência respiratória (1) e a data de internação", "type": "datetime-local"},
        "variacao_valor_controle_1_Pressão Arterial Diastólica": {"label": "Variação do valor do controle da pressão arterial diastólica (1)", "type": "number"},
        "diff_entre_dt_controle_1_Pressão Arterial Diastólica": {"label": "Diferença entre a data do controle da pressão arterial diastólica (1) e a data de internação", "type": "datetime-local"},
        "variacao_valor_controle_1_Pressão Arterial Sistólica": {"label": "Variação do valor do controle da pressão arterial sistólica (1)", "type": "number"},
        "diff_entre_dt_controle_1_Pressão Arterial Sistólica": {"label": "Diferença entre a data do controle da pressão arterial sistólica (1) e a data de internação", "type": "datetime-local"},
        "variacao_valor_controle_1_Temperatura  Axilar": {"label": "Variação do valor do controle da temperatura axilar (1)", "type": "number"},
        "diff_entre_dt_controle_1_Temperatura  Axilar": {"label": "Diferença entre a data do controle da temperatura axilar (1) e a data de internação", "type": "datetime-local"},
        "variacao_valor_creatinina_2": {"label": "Variação do valor da creatinina (2)", "type": "number"},
        "diff_entre_dt_creatinina_2": {"label": "Diferença entre a data de coleta da creatinina (2) e a data de internação", "type": "datetime-local"},
        "variacao_valor_controle_2_Frequência Cardíaca": {"label": "Variação do valor do controle da frequência cardíaca (2)", "type": "number"},
        "diff_entre_dt_controle_2_Frequência Cardíaca": {"label": "Diferença entre a data do controle da frequência cardíaca (2) e a data de internação", "type": "datetime-local"},
        "variacao_valor_controle_2_Frequência Respiratória": {"label": "Variação do valor do controle da frequência respiratória (2)", "type": "number"},
        "diff_entre_dt_controle_2_Frequência Respiratória": {"label": "Diferença entre a data do controle da frequência respiratória (2) e a data de internação", "type": "datetime-local"},
        "variacao_valor_controle_2_Pressão Arterial Diastólica": {"label": "Variação do valor do controle da pressão arterial diastólica (2)", "type": "number"},
        "diff_entre_dt_controle_2_Pressão Arterial Diastólica": {"label": "Diferença entre a data do controle da pressão arterial diastólica (2) e a data de internação", "type": "datetime-local"},
        "variacao_valor_controle_2_Pressão Arterial Sistólica": {"label": "Variação do valor do controle da pressão arterial sistólica (2)", "type": "number"},
        "diff_entre_dt_controle_2_Pressão Arterial Sistólica": {"label": "Diferença entre a data do controle da pressão arterial sistólica (2) e a data de internação", "type": "datetime-local"},
        "variacao_valor_controle_2_Temperatura  Axilar": {"label": "Variação do valor do controle da temperatura axilar (2)", "type": "number"},
        "diff_entre_dt_controle_2_Temperatura  Axilar": {"label": "Diferença entre a data do controle da temperatura axilar (2) e a data de internação", "type": "datetime-local"}
    },
    'radio_buttons': {
        "Modelo A:": "etr",
        "Modelo B:": "xgbc"
    }
}

app = Flask(__name__)

@app.route('/')
def home():
    global data
    return render_template('index.html', data=data)

@app.route('/resultado', methods=['GET'])
def predict(
    model_type: str,
):
    global models

    if model_type not in models:
        return "Model not found", 404
    else:
        model_path = models[model_type]
    
    preprocessed_data = preprocess_data(request.form)
    prediction = make_prediction(model_path, preprocessed_data)
    if model_type == 'etr':
        prediction = ira_heuristic(prediction, preprocessed_data)

    data = {}

    return render_template('index.html', ira=True, show_result=True, data=data)

if __name__ == "__main__":
    app.run(debug=True)

def preprocess_data(input_data):
    print(input_data)
    return pd.DataFrame(input_data, index=[0])

def ira_heuristic(input_data, inference_data):
    pass

def make_prediction(model_path, input_data):
    model = joblib.load(model_path)
    # preprocess the data
    input_data = preprocess_data(input_data)
    # make a prediction
    prediction = model.predict(input_data)
    return prediction

