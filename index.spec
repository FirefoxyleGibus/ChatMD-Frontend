block_cipher = None
a = Analysis(['index.py'],
         pathex=[''],
         binaries=None,
         datas=None,
         hiddenimports=[],
         hookspath=None,
         runtime_hooks=None,
         excludes=None,
         cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(pyz)
app = BUNDLE(exe,
         name='myscript.app',
         icon=None,
         bundle_identifier=None)