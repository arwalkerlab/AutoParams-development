from flask import Flask, flash, request, redirect, url_for, render_template, session, send_from_directory
from werkzeug.utils import secure_filename
from glob import glob as G
import os
import subprocess as S
import uuid
import parmed

### Import all my default settings
from .defaults import *

def random_job_identifier():
    id = uuid.uuid4()
    return id.hex

def RefreshDB():
    global DATABASE_MOLS_SEEN
    DATABASE_MOLS_SEEN = []
    os.chdir(DATABASE_DIR)
    with open(TEMPLATES_DIR+"__db_dataset.html","w") as f:
        for file_loc in G("*/"):
            f.write(DataBaseEntry(file_loc))
    os.chdir(MAIN_DIR)

def DataBaseEntry(location):
    global DATABASE_MOLS_SEEN
    html_code = """<fieldset style="border-width:2px; border-style:solid; border-color:#78E2A0; padding: 1em;">"""
    if G(location+"*.smi"):
        smiles = open(G(location+'*.smi')[0]).read().strip()
        html_code+=f"<legend>{smiles}</legend>\n"
    else:
        return ""
    if smiles in DATABASE_MOLS_SEEN:
        return ""
    DATABASE_MOLS_SEEN.append(smiles)
    if G(location+"*.png"):
        chemdraw = G(location+"*.png")[0]
        html_code+=f"<img src='database/{chemdraw}' width=\"300\">\n"
    if G(location+"settings.txt"):
        html_code += "<a href=\"{{ url_for('db_download', filename="
        html_code +=G(location+"settings.txt")[0]
        html_code +=")}}\">AutoParams Settings File</a><br>\n"
    if G(location+"*.frcmod"):
        html_code += "<a href=\"{{ url_for('db_download', filename="
        html_code +=G(location+"*.frcmod")[0]
        html_code +=")}}\">FRCMOD File</a><br>\n"
    if G(location+"*.mol2"):
        html_code += "<a href=\"{{ url_for('db_download', filename="
        html_code +=G(location+"*.mol2")[0]
        html_code +=")}}\">MOL2 File</a><br>\n"
    if G(location+"tleap.in"):
        html_code += "<a href=\"{{ url_for('db_download', filename="
        html_code +=G(location+"tleap.in")[0]
        html_code +=")}}\">tleap Input File</a><br>\n"
    if G(location+"*.prmtop"):
        html_code += "<a href=\"{{ url_for('db_download', filename="
        html_code +=G(location+"*.prmtop")[0]
        html_code +=")}}\">PRMTOP File</a><br>\n"
    if G(location+"*.inpcrd"):
        html_code += "<a href=\"{{ url_for('db_download', filename="
        html_code +=G(location+"*.inpcrd")[0]
        html_code +=")}}\">INPCRD File</a><br>\n"
    html_code+="</fieldset>\n"
    return html_code

def CheckSMILESinDB(SMILES):
    if not G(SMILES_DB):
        S.call(f"touch {SMILES_DB}",shell=True)
    lines = open(SMILES_DB,"r").read().split("\n")
    if SMILES in lines:
        return True
    return False