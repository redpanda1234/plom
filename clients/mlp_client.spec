# -*- mode: python -*-

block_cipher = None

a = Analysis(['mlp_client.py'],
             # pathex=['/Users/andrew/Projects/MLP/clients'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

for icon in ['cross', 'delete', 'line', 'move', 'pan', 'pen', 'rectangle', 'redo', 'text', 'tick', 'undo', 'zoom', 'comment', 'comment_up', 'comment_down']:
  a.datas += [('{}.svg'.format(icon), 'icons/{}.svg'.format(icon), 'DATA')]

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='mlp_client',
          debug=False,
          strip=False,
          onefile=True,
          upx=True,
          runtime_tmpdir=None,
          console=True )
