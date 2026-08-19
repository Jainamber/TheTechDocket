"""
Vendored Tabler Icons (outline set), embedded as SVG path data.

Tabler Icons — Copyright (c) 2020-2026 Paweł Kuna. MIT License.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions: the above copyright
notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.

Source: https://tabler.io/icons (outline style, 24x24 grid, stroke-based).
"""

from markupsafe import Markup

ICONS: dict[str, list[str]] = {
    'alert-triangle': [
        'M12 9v4',
        'M10.363 3.591l-8.106 13.534a1.914 1.914 0 0 0 1.636 2.871h16.214a1.914 1.914 0 0 0 1.636 -2.87l-8.106 -13.536a1.914 1.914 0 0 0 -3.274 0',
        'M12 16h.01',
    ],
    'atom-2': [
        'M9 12a3 3 0 1 0 6 0a3 3 0 1 0 -6 0',
        'M12 21l0 .01',
        'M3 9l0 .01',
        'M21 9l0 .01',
        'M8 20.1a9 9 0 0 1 -5 -7.1',
        'M16 20.1a9 9 0 0 0 5 -7.1',
        'M6.2 5a9 9 0 0 1 11.4 0',
    ],
    'bolt': [
        'M13 3l0 7l6 0l-8 11l0 -7l-6 0l8 -11',
    ],
    'brain': [
        'M15.5 13a3.5 3.5 0 0 0 -3.5 3.5v1a3.5 3.5 0 0 0 7 0v-1.8',
        'M8.5 13a3.5 3.5 0 0 1 3.5 3.5v1a3.5 3.5 0 0 1 -7 0v-1.8',
        'M17.5 16a3.5 3.5 0 0 0 0 -7h-.5',
        'M19 9.3v-2.8a3.5 3.5 0 0 0 -7 0',
        'M6.5 16a3.5 3.5 0 0 1 0 -7h.5',
        'M5 9.3v-2.8a3.5 3.5 0 0 1 7 0v10',
    ],
    'briefcase': [
        'M3 9a2 2 0 0 1 2 -2h14a2 2 0 0 1 2 2v9a2 2 0 0 1 -2 2h-14a2 2 0 0 1 -2 -2l0 -9',
        'M8 7v-2a2 2 0 0 1 2 -2h4a2 2 0 0 1 2 2v2',
        'M12 12l0 .01',
        'M3 13a20 20 0 0 0 18 0',
    ],
    'bug': [
        'M9 9v-1a3 3 0 0 1 6 0v1',
        'M8 9h8a6 6 0 0 1 1 3v3a5 5 0 0 1 -10 0v-3a6 6 0 0 1 1 -3',
        'M3 13l4 0',
        'M17 13l4 0',
        'M12 20l0 -6',
        'M4 19l3.35 -2',
        'M20 19l-3.35 -2',
        'M4 7l3.75 2.4',
        'M20 7l-3.75 2.4',
    ],
    'building': [
        'M3 21l18 0',
        'M9 8l1 0',
        'M9 12l1 0',
        'M9 16l1 0',
        'M14 8l1 0',
        'M14 12l1 0',
        'M14 16l1 0',
        'M5 21v-16a2 2 0 0 1 2 -2h10a2 2 0 0 1 2 2v16',
    ],
    'building-factory-2': [
        'M3 21h18',
        'M5 21v-12l5 4v-4l5 4h4',
        'M19 21v-8l-1.436 -9.574a.5 .5 0 0 0 -.495 -.426h-1.145a.5 .5 0 0 0 -.494 .418l-1.43 8.582',
        'M9 17h1',
        'M14 17h1',
    ],
    'bulb': [
        'M3 12h1m8 -9v1m8 8h1m-15.4 -6.4l.7 .7m12.1 -.7l-.7 .7',
        'M9 16a5 5 0 1 1 6 0a3.5 3.5 0 0 0 -1 3a2 2 0 0 1 -4 0a3.5 3.5 0 0 0 -1 -3',
        'M9.7 17l4.6 0',
    ],
    'calendar': [
        'M4 7a2 2 0 0 1 2 -2h12a2 2 0 0 1 2 2v12a2 2 0 0 1 -2 2h-12a2 2 0 0 1 -2 -2v-12',
        'M16 3v4',
        'M8 3v4',
        'M4 11h16',
        'M11 15h1',
        'M12 15v3',
    ],
    'chart-bar': [
        'M3 13a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v6a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1l0 -6',
        'M15 9a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v10a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1l0 -10',
        'M9 5a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v14a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1l0 -14',
        'M4 20h14',
    ],
    'chart-line': [
        'M4 19l16 0',
        'M4 15l4 -6l4 2l4 -5l4 4',
    ],
    'cloud': [
        'M6.657 18c-2.572 0 -4.657 -2.007 -4.657 -4.483c0 -2.475 2.085 -4.482 4.657 -4.482c.393 -1.762 1.794 -3.2 3.675 -3.773c1.88 -.572 3.956 -.193 5.444 1c1.488 1.19 2.162 3.007 1.77 4.769h.99c1.913 0 3.464 1.56 3.464 3.486c0 1.927 -1.551 3.487 -3.465 3.487h-11.878',
    ],
    'coins': [
        'M9 14c0 1.657 2.686 3 6 3s6 -1.343 6 -3s-2.686 -3 -6 -3s-6 1.343 -6 3',
        'M9 14v4c0 1.656 2.686 3 6 3s6 -1.344 6 -3v-4',
        'M3 6c0 1.072 1.144 2.062 3 2.598s4.144 .536 6 0c1.856 -.536 3 -1.526 3 -2.598c0 -1.072 -1.144 -2.062 -3 -2.598s-4.144 -.536 -6 0c-1.856 .536 -3 1.526 -3 2.598',
        'M3 6v10c0 .888 .772 1.45 2 2',
        'M3 11c0 .888 .772 1.45 2 2',
    ],
    'cpu': [
        'M5 6a1 1 0 0 1 1 -1h12a1 1 0 0 1 1 1v12a1 1 0 0 1 -1 1h-12a1 1 0 0 1 -1 -1l0 -12',
        'M9 9h6v6h-6l0 -6',
        'M3 10h2',
        'M3 14h2',
        'M10 3v2',
        'M14 3v2',
        'M21 10h-2',
        'M21 14h-2',
        'M14 21v-2',
        'M10 21v-2',
    ],
    'currency-rupee': [
        'M18 5h-11h3a4 4 0 0 1 0 8h-3l6 6',
        'M7 9l11 0',
    ],
    'database': [
        'M4 6a8 3 0 1 0 16 0a8 3 0 1 0 -16 0',
        'M4 6v6a8 3 0 0 0 16 0v-6',
        'M4 12v6a8 3 0 0 0 16 0v-6',
    ],
    'device-mobile': [
        'M6 5a2 2 0 0 1 2 -2h8a2 2 0 0 1 2 2v14a2 2 0 0 1 -2 2h-8a2 2 0 0 1 -2 -2v-14',
        'M11 4h2',
        'M12 17v.01',
    ],
    'device-speaker': [
        'M5 5a2 2 0 0 1 2 -2h10a2 2 0 0 1 2 2v14a2 2 0 0 1 -2 2h-10a2 2 0 0 1 -2 -2l0 -14',
        'M9 14a3 3 0 1 0 6 0a3 3 0 1 0 -6 0',
        'M12 7l0 .01',
    ],
    'discount': [
        'M9 15l6 -6',
        'M9 9.5a.5 .5 0 1 0 1 0a.5 .5 0 1 0 -1 0',
        'M14 14.5a.5 .5 0 1 0 1 0a.5 .5 0 1 0 -1 0',
        'M3 12a9 9 0 1 0 18 0a9 9 0 1 0 -18 0',
    ],
    'eye-off': [
        'M10.585 10.587a2 2 0 0 0 2.829 2.828',
        'M16.681 16.673a8.717 8.717 0 0 1 -4.681 1.327c-3.6 0 -6.6 -2 -9 -6c1.272 -2.12 2.712 -3.678 4.32 -4.674m2.86 -1.146a9.055 9.055 0 0 1 1.82 -.18c3.6 0 6.6 2 9 6c-.666 1.11 -1.379 2.067 -2.138 2.87',
        'M3 3l18 18',
    ],
    'file-alert': [
        'M14 3v4a1 1 0 0 0 1 1h4',
        'M17 21h-10a2 2 0 0 1 -2 -2v-14a2 2 0 0 1 2 -2h7l5 5v11a2 2 0 0 1 -2 2',
        'M12 17l.01 0',
        'M12 11l0 3',
    ],
    'file-text': [
        'M14 3v4a1 1 0 0 0 1 1h4',
        'M17 21h-10a2 2 0 0 1 -2 -2v-14a2 2 0 0 1 2 -2h7l5 5v11a2 2 0 0 1 -2 2',
        'M9 9l1 0',
        'M9 13l6 0',
        'M9 17l6 0',
    ],
    'fingerprint': [
        'M18.9 7a8 8 0 0 1 1.1 5v1a6 6 0 0 0 .8 3',
        'M8 11a4 4 0 0 1 8 0v1a10 10 0 0 0 2 6',
        'M12 11v2a14 14 0 0 0 2.5 8',
        'M8 15a18 18 0 0 0 1.8 6',
        'M4.9 19a22 22 0 0 1 -.9 -7v-1a8 8 0 0 1 12 -6.95',
    ],
    'flame': [
        'M12 10.941c2.333 -3.308 .167 -7.823 -1 -8.941c0 3.395 -2.235 5.299 -3.667 6.706c-1.43 1.408 -2.333 3.294 -2.333 5.588c0 3.704 3.134 6.706 7 6.706c3.866 0 7 -3.002 7 -6.706c0 -1.712 -1.232 -4.403 -2.333 -5.588c-2.084 3.353 -3.257 3.353 -4.667 2.235',
    ],
    'gauge': [
        'M3 12a9 9 0 1 0 18 0a9 9 0 1 0 -18 0',
        'M11 12a1 1 0 1 0 2 0a1 1 0 1 0 -2 0',
        'M13.41 10.59l2.59 -2.59',
        'M7 12a5 5 0 0 1 5 -5',
    ],
    'gavel': [
        'M13 10l7.383 7.418c.823 .82 .823 2.148 0 2.967a2.11 2.11 0 0 1 -2.976 0l-7.407 -7.385',
        'M6 9l4 4',
        'M13 10l-4 -4',
        'M3 21h7',
        'M6.793 15.793l-3.586 -3.586a1 1 0 0 1 0 -1.414l2.293 -2.293l.5 .5l3 -3l-.5 -.5l2.293 -2.293a1 1 0 0 1 1.414 0l3.586 3.586a1 1 0 0 1 0 1.414l-2.293 2.293l-.5 -.5l-3 3l.5 .5l-2.293 2.293a1 1 0 0 1 -1.414 0',
    ],
    'hierarchy-2': [
        'M10 3h4v4h-4l0 -4',
        'M3 17h4v4h-4l0 -4',
        'M17 17h4v4h-4l0 -4',
        'M7 17l5 -4l5 4',
        'M12 7l0 6',
    ],
    'id': [
        'M3 7a3 3 0 0 1 3 -3h12a3 3 0 0 1 3 3v10a3 3 0 0 1 -3 3h-12a3 3 0 0 1 -3 -3l0 -10',
        'M7 10a2 2 0 1 0 4 0a2 2 0 1 0 -4 0',
        'M15 8l2 0',
        'M15 12l2 0',
        'M7 16l10 0',
    ],
    'key': [
        'M16.555 3.843l3.602 3.602a2.877 2.877 0 0 1 0 4.069l-2.643 2.643a2.877 2.877 0 0 1 -4.069 0l-.301 -.301l-6.558 6.558a2 2 0 0 1 -1.239 .578l-.175 .008h-1.172a1 1 0 0 1 -.993 -.883l-.007 -.117v-1.172a2 2 0 0 1 .467 -1.284l.119 -.13l.414 -.414h2v-2h2v-2l2.144 -2.144l-.301 -.301a2.877 2.877 0 0 1 0 -4.069l2.643 -2.643a2.877 2.877 0 0 1 4.069 0',
        'M15 9h.01',
    ],
    'list-details': [
        'M13 5h8',
        'M13 9h5',
        'M13 15h8',
        'M13 19h5',
        'M3 5a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1l0 -4',
        'M3 15a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1l0 -4',
    ],
    'lock-open': [
        'M5 13a2 2 0 0 1 2 -2h10a2 2 0 0 1 2 2v6a2 2 0 0 1 -2 2h-10a2 2 0 0 1 -2 -2l0 -6',
        'M11 16a1 1 0 1 0 2 0a1 1 0 1 0 -2 0',
        'M8 11v-5a4 4 0 0 1 8 0',
    ],
    'message-chatbot': [
        'M18 4a3 3 0 0 1 3 3v8a3 3 0 0 1 -3 3h-5l-5 3v-3h-2a3 3 0 0 1 -3 -3v-8a3 3 0 0 1 3 -3h12',
        'M9.5 9h.01',
        'M14.5 9h.01',
        'M9.5 13a3.5 3.5 0 0 0 5 0',
    ],
    'microphone': [
        'M9 5a3 3 0 0 1 3 -3a3 3 0 0 1 3 3v5a3 3 0 0 1 -3 3a3 3 0 0 1 -3 -3l0 -5',
        'M5 10a7 7 0 0 0 14 0',
        'M8 21l8 0',
        'M12 17l0 4',
    ],
    'network': [
        'M6 9a6 6 0 1 0 12 0a6 6 0 0 0 -12 0',
        'M12 3c1.333 .333 2 2.333 2 6s-.667 5.667 -2 6',
        'M12 3c-1.333 .333 -2 2.333 -2 6s.667 5.667 2 6',
        'M6 9h12',
        'M3 20h7',
        'M14 20h7',
        'M10 20a2 2 0 1 0 4 0a2 2 0 0 0 -4 0',
        'M12 15v3',
    ],
    'news': [
        'M16 6h3a1 1 0 0 1 1 1v11a2 2 0 0 1 -4 0v-13a1 1 0 0 0 -1 -1h-10a1 1 0 0 0 -1 1v12a3 3 0 0 0 3 3h11',
        'M8 8l4 0',
        'M8 12l4 0',
        'M8 16l4 0',
    ],
    'phone-call': [
        'M5 4h4l2 5l-2.5 1.5a11 11 0 0 0 5 5l1.5 -2.5l5 2v4a2 2 0 0 1 -2 2a16 16 0 0 1 -15 -15a2 2 0 0 1 2 -2',
        'M15 7a2 2 0 0 1 2 2',
        'M15 3a6 6 0 0 1 6 6',
    ],
    'photo-search': [
        'M15 8h.01',
        'M11.5 21h-5.5a3 3 0 0 1 -3 -3v-12a3 3 0 0 1 3 -3h12a3 3 0 0 1 3 3v5.5',
        'M15 18a3 3 0 1 0 6 0a3 3 0 1 0 -6 0',
        'M20.2 20.2l1.8 1.8',
        'M3 16l5 -5c.928 -.893 2.072 -.893 3 0l2 2',
    ],
    'plug': [
        'M9.785 6l8.215 8.215l-2.054 2.054a5.81 5.81 0 1 1 -8.215 -8.215l2.054 -2.054',
        'M4 20l3.5 -3.5',
        'M15 4l-3.5 3.5',
        'M20 9l-3.5 3.5',
    ],
    'receipt': [
        'M5 21v-16a2 2 0 0 1 2 -2h10a2 2 0 0 1 2 2v16l-3 -2l-2 2l-2 -2l-2 2l-2 -2l-3 2m4 -14h6m-6 4h6m-2 4h2',
    ],
    'robot': [
        'M6 6a2 2 0 0 1 2 -2h8a2 2 0 0 1 2 2v4a2 2 0 0 1 -2 2h-8a2 2 0 0 1 -2 -2l0 -4',
        'M12 2v2',
        'M9 12v9',
        'M15 12v9',
        'M5 16l4 -2',
        'M15 14l4 2',
        'M9 18h6',
        'M10 8v.01',
        'M14 8v.01',
    ],
    'rocket': [
        'M4 13a8 8 0 0 1 7 7a6 6 0 0 0 3 -5a9 9 0 0 0 6 -8a3 3 0 0 0 -3 -3a9 9 0 0 0 -8 6a6 6 0 0 0 -5 3',
        'M7 14a6 6 0 0 0 -3 6a6 6 0 0 0 6 -3',
        'M14 9a1 1 0 1 0 2 0a1 1 0 1 0 -2 0',
    ],
    'scale': [
        'M7 20l10 0',
        'M6 6l6 -1l6 1',
        'M12 3l0 17',
        'M9 12l-3 -6l-3 6a3 3 0 0 0 6 0',
        'M21 12l-3 -6l-3 6a3 3 0 0 0 6 0',
    ],
    'scissors': [
        'M3 7a3 3 0 1 0 6 0a3 3 0 1 0 -6 0',
        'M3 17a3 3 0 1 0 6 0a3 3 0 1 0 -6 0',
        'M8.6 8.6l10.4 10.4',
        'M8.6 15.4l10.4 -10.4',
    ],
    'search': [
        'M3 10a7 7 0 1 0 14 0a7 7 0 1 0 -14 0',
        'M21 21l-6 -6',
    ],
    'server-2': [
        'M3 7a3 3 0 0 1 3 -3h12a3 3 0 0 1 3 3v2a3 3 0 0 1 -3 3h-12a3 3 0 0 1 -3 -3v-2',
        'M3 15a3 3 0 0 1 3 -3h12a3 3 0 0 1 3 3v2a3 3 0 0 1 -3 3h-12a3 3 0 0 1 -3 -3l0 -2',
        'M7 8l0 .01',
        'M7 16l0 .01',
        'M11 8h6',
        'M11 16h6',
    ],
    'shield-lock': [
        'M12 3a12 12 0 0 0 8.5 3a12 12 0 0 1 -8.5 15a12 12 0 0 1 -8.5 -15a12 12 0 0 0 8.5 -3',
        'M11 11a1 1 0 1 0 2 0a1 1 0 1 0 -2 0',
        'M12 12l0 2.5',
    ],
    'shield-off': [
        'M17.67 17.667a12 12 0 0 1 -5.67 3.333a12 12 0 0 1 -8.5 -15c.794 .036 1.583 -.006 2.357 -.124m3.128 -.926a11.997 11.997 0 0 0 3.015 -1.95a12 12 0 0 0 8.5 3a12 12 0 0 1 -1.116 9.376',
        'M3 3l18 18',
    ],
    'sparkles': [
        'M16 18a2 2 0 0 1 2 2a2 2 0 0 1 2 -2a2 2 0 0 1 -2 -2a2 2 0 0 1 -2 2m0 -12a2 2 0 0 1 2 2a2 2 0 0 1 2 -2a2 2 0 0 1 -2 -2a2 2 0 0 1 -2 2m-7 12a6 6 0 0 1 6 -6a6 6 0 0 1 -6 -6a6 6 0 0 1 -6 6a6 6 0 0 1 6 6',
    ],
    'tag': [
        'M6.5 7.5a1 1 0 1 0 2 0a1 1 0 1 0 -2 0',
        'M3 6v5.172a2 2 0 0 0 .586 1.414l7.71 7.71a2.41 2.41 0 0 0 3.408 0l5.592 -5.592a2.41 2.41 0 0 0 0 -3.408l-7.71 -7.71a2 2 0 0 0 -1.414 -.586h-5.172a3 3 0 0 0 -3 3',
    ],
    'tornado': [
        'M21 4l-18 0',
        'M13 16l-6 0',
        'M11 20l4 0',
        'M6 8l14 0',
        'M4 12l12 0',
    ],
    'trending-up': [
        'M3 17l6 -6l4 4l8 -8',
        'M14 7l7 0l0 7',
    ],
    'user-shield': [
        'M6 21v-2a4 4 0 0 1 4 -4h2',
        'M22 16c0 4 -2.5 6 -3.5 6s-3.5 -2 -3.5 -6c1 0 2.5 -.5 3.5 -1.5c1 1 2.5 1.5 3.5 1.5',
        'M8 7a4 4 0 1 0 8 0a4 4 0 0 0 -8 0',
    ],
    'users': [
        'M5 7a4 4 0 1 0 8 0a4 4 0 1 0 -8 0',
        'M3 21v-2a4 4 0 0 1 4 -4h4a4 4 0 0 1 4 4v2',
        'M16 3.13a4 4 0 0 1 0 7.75',
        'M21 21v-2a4 4 0 0 0 -3 -3.85',
    ],
    'world': [
        'M3 12a9 9 0 1 0 18 0a9 9 0 0 0 -18 0',
        'M3.6 9h16.8',
        'M3.6 15h16.8',
        'M11.5 3a17 17 0 0 0 0 18',
        'M12.5 3a17 17 0 0 1 0 18',
    ],
}

ICON_NAMES = sorted(ICONS)

MOTIF_TO_ICON = {
    'waveform': 'phone-call',
    'shield': 'shield-lock',
    'scales': 'scale',
    'chip': 'cpu',
    'phone': 'device-mobile',
    'pages': 'file-text',
    'cloud': 'server-2',
    'price': 'coins',
    'magnify': 'bulb',
    'chat': 'message-chatbot',
    'neural': 'sparkles',
    'globe': 'world',
    'ticker': 'news',
}

_HUB_DEFAULT = {
    'ai-models': 'sparkles',
    'ai-tools': 'message-chatbot',
    'big-tech': 'world',
    'hardware': 'cpu',
    'policy': 'scale',
    'explainers': 'bulb',
    'docket': 'news',
}


def resolve_icon(name: str | None, motif: str | None = None, hub: str | None = None) -> str:
    """Resolve an icon name, falling back through motif and hub defaults to "sparkles"."""
    if name and name in ICONS:
        return name
    if motif and MOTIF_TO_ICON.get(motif) in ICONS:
        return MOTIF_TO_ICON[motif]
    return _HUB_DEFAULT.get(hub, "sparkles")


def svg_icon(name: str, cls: str = "ico", stroke: float = 1.75) -> str:
    """Render an icon as a compact inline <svg> string (Markup, unescaped for Jinja)."""
    resolved = name if name in ICONS else resolve_icon(None)
    paths = ICONS[resolved]
    path_tags = "".join(f'<path d="{d}"/>' for d in paths)
    svg = (
        f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        f'stroke-width="{stroke}" stroke-linecap="round" stroke-linejoin="round" '
        f'aria-hidden="true" focusable="false">{path_tags}</svg>'
    )
    return Markup(svg)
