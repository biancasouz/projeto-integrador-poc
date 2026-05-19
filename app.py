from flask import Flask, render_template, request, redirect, url_for, abort
import uuid
import sqlite3

app = Flask(__name__)

DB = "database.db"


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS pacientes (
                id TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                cpf TEXT UNIQUE NOT NULL,
                telefone TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS empresas (
                id TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                cnpj TEXT UNIQUE NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS agendamentos (
                id TEXT PRIMARY KEY,
                paciente TEXT NOT NULL,
                empresa TEXT NOT NULL,
                data TEXT NOT NULL,
                horario TEXT NOT NULL,
                exame TEXT NOT NULL
            )
        """)
        conn.commit()


init_db()


@app.route("/")
def index():
    return render_template("index.html")


# ── Pacientes ────────────────────────────────────────────────────────────────


@app.route("/pacientes", methods=["GET", "POST"])
def cadastrar_paciente():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        cpf = request.form.get("cpf", "").strip()
        telefone = request.form.get("telefone", "").strip()

        if not nome or not cpf:
            abort(400, "Nome e CPF são obrigatórios")

        with get_db() as conn:
            try:
                conn.execute(
                    "INSERT INTO pacientes (id, nome, cpf, telefone) VALUES (?, ?, ?, ?)",
                    (str(uuid.uuid4()), nome, cpf, telefone),
                )
                conn.commit()
            except sqlite3.IntegrityError:
                abort(400, "CPF já cadastrado")

        return redirect(url_for("cadastrar_paciente"))

    with get_db() as conn:
        pacientes = conn.execute("SELECT * FROM pacientes").fetchall()

    return render_template("pacientes.html", pacientes=pacientes)


@app.route("/pacientes/deletar/<cpf>", methods=["POST"])
def deletar_paciente(cpf):
    with get_db() as conn:
        conn.execute("DELETE FROM pacientes WHERE cpf = ?", (cpf,))
        conn.commit()
    return redirect(url_for("cadastrar_paciente"))


# ── Empresas ─────────────────────────────────────────────────────────────────


@app.route("/empresas", methods=["GET", "POST"])
def cadastrar_empresa():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        cnpj = request.form.get("cnpj", "").strip()

        if not nome or not cnpj:
            abort(400, "Nome e CNPJ são obrigatórios")

        with get_db() as conn:
            try:
                conn.execute(
                    "INSERT INTO empresas (id, nome, cnpj) VALUES (?, ?, ?)",
                    (str(uuid.uuid4()), nome, cnpj),
                )
                conn.commit()
            except sqlite3.IntegrityError:
                abort(400, "CNPJ já cadastrado")

        return redirect(url_for("cadastrar_empresa"))

    with get_db() as conn:
        empresas = conn.execute("SELECT * FROM empresas").fetchall()

    return render_template("empresas.html", empresas=empresas)


@app.route("/empresas/deletar/<cnpj>", methods=["POST"])
def deletar_empresa(cnpj):
    with get_db() as conn:
        conn.execute("DELETE FROM empresas WHERE cnpj = ?", (cnpj,))
        conn.commit()
    return redirect(url_for("cadastrar_empresa"))


# ── Agendamentos ──────────────────────────────────────────────────────────────


@app.route("/agendamento", methods=["GET", "POST"])
def agendamento():
    if request.method == "POST":
        paciente = request.form.get("paciente", "").strip()
        empresa = request.form.get("empresa", "").strip()
        data = request.form.get("data", "").strip()
        horario = request.form.get("horario", "").strip()
        exame = request.form.get("exame", "").strip()

        if not paciente or not empresa or not data or not horario or not exame:
            abort(400, "Todos os campos são obrigatórios")

        with get_db() as conn:
            conn.execute(
                "INSERT INTO agendamentos (id, paciente, empresa, data, horario, exame) VALUES (?, ?, ?, ?, ?, ?)",
                (str(uuid.uuid4()), paciente, empresa, data, horario, exame),
            )
            conn.commit()

        return redirect(url_for("agendamento"))

    with get_db() as conn:
        pacientes = conn.execute("SELECT * FROM pacientes").fetchall()
        empresas = conn.execute("SELECT * FROM empresas").fetchall()
        agendamentos = conn.execute("SELECT * FROM agendamentos").fetchall()

    return render_template(
        "agendamento.html",
        pacientes=pacientes,
        empresas=empresas,
        agendamentos=agendamentos,
    )


@app.route("/agendamento/deletar/<id>", methods=["POST"])
def deletar_agendamento(id):
    with get_db() as conn:
        conn.execute("DELETE FROM agendamentos WHERE id = ?", (id,))
        conn.commit()
    return redirect(url_for("agendamento"))


# ── ASO ───────────────────────────────────────────────────────────────────────


@app.route("/aso")
def aso():
    with get_db() as conn:
        agendamentos = conn.execute("SELECT * FROM agendamentos").fetchall()
    return render_template("aso.html", agendamentos=agendamentos)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
