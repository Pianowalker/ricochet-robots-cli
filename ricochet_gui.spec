# -*- mode: python ; coding: utf-8 -*-
# Spec file para empaquetar SOLO la versión GUI de Ricochet Robots.
# Genera un único .exe standalone sin consola.

a = Analysis(
    ['run_gui.py'],
    pathex=['src'],
    binaries=[],
    datas=[],
    hiddenimports=[
        'ricochet',
        'ricochet.domain',
        'ricochet.domain.game',
        'ricochet.domain.models',
        'ricochet.domain.maps',
        'ricochet.domain.quadrant',
        'ricochet.domain.sessions',
        'ricochet.domain.sessions.single_player_session',
        'ricochet.domain.sessions.practice_session',
        'ricochet.gui',
        'ricochet.gui.main',
        'ricochet.gui.game_window',
        'ricochet.gui.renderer',
        'ricochet.gui.input_handler',
        'ricochet.gui.animation',
        'ricochet.gui.sounds',
        'ricochet.gui.ui',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=['ricochet.cli'],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ricochet-gui',
    debug=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,       # Sin ventana de consola
)
