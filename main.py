from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
chave_api = os.getenv("OPENAI_API_KEY")

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
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run()