from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
chave_api = os.getenv("OPENAI_API_KEY")
if not chave_api:
    logger.error("Chave da API OpenAI não encontrada no arquivo .env!")
    raise ValueError("A chave da API OpenAI não foi encontrada no arquivo .env!")

modelo = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

template_mensagem = ChatPromptTemplate.from_messages([
    ("system", "Traduza o texto a seguir para {idioma}"),
    ("user", "{texto}")
])

chain = template_mensagem | modelo | parser

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/traduzir", methods=["POST"])
def traduzir():
    texto = request.form.get("texto")
    idioma = request.form.get("idioma")
    
    if not texto or not idioma:
        return jsonify({"erro": "Por favor, forneça o texto e o idioma."}), 400
    
    try:
        output = chain.invoke({"texto": texto, "idioma": idioma})
        return jsonify({"traducao": output})

    except ValueError as e:
        logger.error(f"Erro de valor: {e}")
        return jsonify({"erro": "Erro de valor! Verifique se os parâmetros estão corretos."}), 400

    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        return jsonify({"erro": "Houve um erro ao processar sua solicitação. Tente novamente mais tarde."}), 500

if __name__ == "__main__":
    app.run()