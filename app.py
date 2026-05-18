from flask import Flask, render_template, request, redirect

app = Flask(__name__)

pacientes = []
empresas = []
agendamentos = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/pacientes", methods=["GET", "POST"])
def cadastrar_paciente():
    if request.method == "POST":
        nome = request.form["nome"]
        cpf = request.form["cpf"]
        telefone = request.form["telefone"]

        pacientes.append({
            "nome": nome,
            "cpf": cpf,
            "telefone": telefone
        })

        return redirect("/pacientes")

    return render_template("pacientes.html", pacientes=pacientes)

@app.route("/empresas", methods=["GET", "POST"])
def cadastrar_empresa():
    if request.method == "POST":
        nome = request.form["nome"]
        cnpj = request.form["cnpj"]

        empresas.append({
            "nome": nome,
            "cnpj": cnpj
        })

        return redirect("/empresas")

    return render_template("empresas.html", empresas=empresas)

@app.route("/agendamento", methods=["GET", "POST"])
def agendamento():
    if request.method == "POST":
        paciente = request.form["paciente"]
        empresa = request.form["empresa"]
        data = request.form["data"]
        horario = request.form["horario"]
        exame = request.form["exame"]

        agendamentos.append({
            "paciente": paciente,
            "empresa": empresa,
            "data": data,
            "horario": horario,
            "exame": exame
        })

        return redirect("/agendamento")

    return render_template(
        "agendamento.html",
        pacientes=pacientes,
        empresas=empresas,
        agendamentos=agendamentos
    )

@app.route("/aso")
def aso():
    return render_template("aso.html", agendamentos=agendamentos)

if __name__ == "__main__":
    app.run(debug=True)