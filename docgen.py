import pandas as pd

def load_file(file):
    if file.type == "text/plain":
        return file.read().decode("utf-8")
    elif file.type == "text/csv":
        return pd.read_csv(file)
    elif file.type in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]:
        return pd.read_excel(file)
    else:
        return None

def generate_ml_doc(data):
    if isinstance(data, str):
        return f"### ML Documentation\n\n{data}"
    elif isinstance(data, pd.DataFrame):
        desc = data.describe().to_string()
        cols = ", ".join(data.columns)
        return f"### ML Documentation\n\nData Summary:\n{desc}\n\nColumns:\n{cols}"
    else:
        return "Unsupported data format for ML Documentation."

def generate_sar_repo(data):
    if isinstance(data, str):
        return f"### SAR Repository\n\nContent:\n{data}"
    elif isinstance(data, pd.DataFrame):
        sample = data.head(3).to_string()
        return f"### SAR Repository\n\nSample Data:\n{sample}"
    else:
        return "Unsupported data format for SAR Repository."
