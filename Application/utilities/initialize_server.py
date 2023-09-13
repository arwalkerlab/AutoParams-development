from utilities.utilities import *

def InitializeApp(app):
    app.config['SECRET_KEY'] = "01123581321_Dockerized"
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['DATABASE_FOLDER'] = DATABASE_DIR
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    main_start_dir = os.getcwd()
    MAIN_UPLOAD_FOLDER = os.path.join(main_start_dir,"uploads/")
    ### Any other QM packages should have similar functions included here as they get added in.
    USE_TERACHEM=IsTeraChemAvailable()
    RefreshDB()

def IsTeraChemAvailable():
    proc = S.Popen("which terachem",shell=True,stdout=S.PIPE,stderr=S.PIPE)
    out,err = proc.communicate()
    output = out.decode('utf-8')
    if output == '':
        return False
    return True