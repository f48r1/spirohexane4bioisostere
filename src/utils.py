def xyzToMol(xyz, charge=0):
    from rdkit import Chem
    from rdkit.Chem import rdDetermineBonds
    
    # NOTE Sometimes it fail to determine Bonds
    try:
        conn_mol = Chem.Mol(xyz)
        rdDetermineBonds.DetermineBonds(conn_mol, charge=charge)
    # NOTE so we opt for hueckel solution
    except:
        conn_mol = Chem.Mol(xyz)
        rdDetermineBonds.DetermineConnectivity(conn_mol, useHueckel=True, charge=charge)

    return conn_mol

def drawMol(mol,legend='',highlightAtoms=[], remove_background = False, bw_color = False):
    from rdkit.Chem import Draw
    # d2d = Draw.MolDraw2DCairo(-1,-1)
    d2d = Draw.MolDraw2DSVG(-1,-1)
    dopts = d2d.drawOptions()

    if bw_color:
        dopts.useBWAtomPalette()

    dopts.continuousHighlight = True
    dopts.circleAtoms = False
    dopts.atomHighlightsAreCircles=False
    dopts.highlightRadius=0.1

    d2d.DrawMolecule(mol,legend=legend, highlightAtoms=highlightAtoms)
    d2d.FinishDrawing()
    # bio = BytesIO(d2d.GetDrawingText())
    svg = d2d.GetDrawingText()

    # return Image.open(bio)
    
    svg = svg.replace('svg:','')

    if not remove_background:
        return svg
    
    import re
    svg = re.sub(r'(?m)^<rect.*\n', '', svg)

    return svg