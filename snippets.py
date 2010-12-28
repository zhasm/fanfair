from os.path import dirname as dirname
from os.path import join as pathjoin

def alert(msg):
    '''return javascript alert window with givin message'''
    return '''<script type="text/javascript" charset="utf-8">
    alert("%s");
</script>''' % msg

def getPath(sufix=""):
    '''get absolute path of the current dir'''
    path = dirname(__file__)
    try:
        index=path.index("..")
        if index!=-1:
            path=path[:index]
    except:
        pass
    return pathjoin(path, sufix).replace('\\','/')


