import formulario
import sys


def test_connection():
    # used when running the frozen executable with a special flag
    try:
        from db import conectar
        conn = conectar()
        print("Connection OK", conn.is_connected())
        conn.close()
    except Exception as e:
        print("Connection failed", repr(e))
        sys.exit(1)

if __name__ == "__main__" and "--test" in sys.argv:
    test_connection()
    sys.exit(0)
