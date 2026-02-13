import requests
import streamlit as st
import time


def trigger_dbt_build():
    owner = st.secrets["GITHUB_OWNER"]
    repo = st.secrets["GITHUB_REPO"]
    workflow = st.secrets["GITHUB_WORKFLOW_FILE"]
    token = st.secrets["GITHUB_TOKEN"]
    ref = st.secrets.get("GITHUB_REF", "main")

    dispatch_url = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow}/dispatches"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }

    # Dispara
    r = requests.post(dispatch_url, headers=headers, json={"ref": ref})
    if r.status_code not in (200, 201, 202, 204):
        raise RuntimeError(r.text)

    # Espera 3 segundos para o run aparecer
    time.sleep(3)

    # Busca o run mais recente
    runs_url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs"
    runs = requests.get(runs_url, headers=headers).json()

    latest_run = runs["workflow_runs"][0]
    return latest_run["id"]


def wait_for_run(run_id, timeout=180):
    owner = st.secrets["GITHUB_OWNER"]
    repo = st.secrets["GITHUB_REPO"]
    token = st.secrets["GITHUB_TOKEN"]

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }

    run_url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs/{run_id}"

    start = time.time()

    while time.time() - start < timeout:
        r = requests.get(run_url, headers=headers).json()
        status = r["status"]
        conclusion = r.get("conclusion")

        if status == "completed":
            return conclusion == "success"

        time.sleep(5)

    return False
