import sqlite3

connection = sqlite3.connect("risk_management.db", check_same_thread=False)
cursor = connection.cursor()


def create_tables():
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS risks (
            user_name TEXT NOT NULL,
            email TEXT NOT NULL,
            user_prompt TEXT NOT NULL,
            ai_response TEXT,
            user_risk TEXT,
            user_risk_prob INT,
            ai_risk TEXT,
            ai_risk_prob INT,
            relevance_risk TEXT,
            relevance_risk_prob INT
        )
    """
    )
    connection.commit()


def select_all():
    rows = cursor.execute("SELECT * FROM risks").fetchall()
    print(rows)


def insert_data(
    user_name,
    email,
    user_prompt,
    ai_response=None,
    user_risk=None,
    user_risk_prob=None,
    ai_risk=None,
    ai_risk_prob=None,
    relevance_risk=None,
    relevance_risk_prob=None,
):
    cursor.execute(
        """
        INSERT INTO risks (user_name, email, user_prompt, ai_response, user_risk, user_risk_prob, ai_risk, ai_risk_prob, relevance_risk, relevance_risk_prob)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            user_name,
            email,
            user_prompt,
            ai_response,
            user_risk,
            user_risk_prob,
            ai_risk,
            ai_risk_prob,
            relevance_risk,
            relevance_risk_prob,
        ),
    )
    connection.commit()


def delete_data():
    cursor.execute("DELETE FROM risks")


if __name__ == "__main__":
    create_tables()
    select_all()
