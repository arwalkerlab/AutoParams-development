import subprocess as S
import os
from glob import glob as G
from ..defaults import BIN_DIR
def GetRESPCharges(pdbfile,charge,mult,jobfolder,level_of_theory="b3lyp",basis_set="6-31gss"):
    ## This version uses Psi4/PsiRESP with a custom script included alongside
    ## the main Flask Application to properly run PsiRESP externally.
    resp_charges = []
    S.call(f"{BIN_DIR}PsiRESPJob -p {pdbfile} -c {charge} -m {mult} -d {jobfolder}",shell=True)
    currdir = os.getcwd()
    if not G(jobfolder+"single_point/"):
        return False
    os.chdir(jobfolder+"/single_point/")
    S.call("sh run_single_point.sh",shell=True)
    os.chdir(currdir)
    S.call(f"{BIN_DIR}PsiRESPJob -p {pdbfile} -c {charge} -m {mult} -d {jobfolder}",shell=True)
    if not G("resp.out"):
        return False
    for line in open("resp.out","r").readlines():
        resp_charges.append(line.strip())
    return resp_charges