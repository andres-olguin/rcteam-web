<?php
// Formulario de contacto de RC Team Chile. Envía la consulta por correo al
// destinatario configurado. Sin base de datos: el mensaje queda solo en el correo.
declare(strict_types=1);

const DESTINO = 'contacto@rcteam.cl';
const REMITENTE = 'contacto@rcteam.cl';
const SITIO = 'https://rcteam.cl/';

header('X-Content-Type-Options: nosniff');
header('Referrer-Policy: same-origin');

function pagina(string $titulo, string $mensaje, bool $ok): void {
    $color = $ok ? '#0b3b66' : '#8a1c1c';
    echo '<!doctype html><html lang="es"><head><meta charset="utf-8">'
        . '<meta name="viewport" content="width=device-width,initial-scale=1">'
        . '<meta name="robots" content="noindex,nofollow"><title>' . htmlspecialchars($titulo) . ' | RC Team</title>'
        . '<style>body{font-family:system-ui,sans-serif;background:#f4f7fb;color:#111;margin:0;'
        . 'display:grid;place-items:center;min-height:100vh;padding:24px}main{max-width:520px;background:#fff;'
        . 'padding:32px;border-top:4px solid ' . $color . '}h1{color:' . $color . ';font-size:1.5rem;margin:0 0 12px}'
        . 'a{color:' . $color . '}</style></head><body><main><h1>' . htmlspecialchars($titulo) . '</h1><p>'
        . $mensaje . '</p><p><a href="' . SITIO . '">Volver a RC Team</a></p></main></body></html>';
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    pagina('Método no permitido', 'Usa el formulario de la página de contacto.', false);
}

// Campo trampa: los robots suelen completarlo; los humanos no lo ven.
if (trim((string)($_POST['sitio_web'] ?? '')) !== '') {
    pagina('Gracias', 'Recibimos tu consulta.', true);
}

// Quita saltos de línea para impedir inyección de cabeceras de correo.
function limpia(string $valor, int $max): string {
    $valor = trim(str_replace(["\r", "\n", "\0"], ' ', $valor));
    return mb_substr($valor, 0, $max);
}

$nombre   = limpia((string)($_POST['nombre'] ?? ''), 120);
$correo   = limpia((string)($_POST['email'] ?? ''), 160);
$telefono = limpia((string)($_POST['telefono'] ?? ''), 40);
$proyecto = limpia((string)($_POST['proyecto'] ?? ''), 160);
$mensaje  = trim(str_replace("\0", '', (string)($_POST['mensaje'] ?? '')));
$mensaje  = mb_substr($mensaje, 0, 5000);

if ($nombre === '' || $mensaje === '' || filter_var($correo, FILTER_VALIDATE_EMAIL) === false) {
    http_response_code(400);
    pagina('Revisa el formulario', 'Falta tu nombre, un correo válido o el mensaje. Vuelve atrás e inténtalo de nuevo.', false);
}

$asunto = mb_encode_mimeheader('Consulta web RC Team - ' . $nombre, 'UTF-8', 'B');
$cuerpo = "Nombre: $nombre\nCorreo: $correo"
    . ($telefono !== '' ? "\nTeléfono: $telefono" : '')
    . ($proyecto !== '' ? "\nProyecto: $proyecto" : '')
    . "\n\nMensaje:\n$mensaje\n\n--\nEnviado desde el formulario de rcteam.cl";

$cabeceras = [
    'From: RC Team Web <' . REMITENTE . '>',
    'Reply-To: ' . $correo,
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: 8bit',
];

if (!mail(DESTINO, $asunto, $cuerpo, implode("\r\n", $cabeceras))) {
    http_response_code(500);
    pagina('No pudimos enviar tu consulta', 'Intenta de nuevo en unos minutos o escríbenos a <a href="mailto:' . DESTINO . '">' . DESTINO . '</a>.', false);
}

pagina('Gracias', 'Recibimos tu consulta. Te responderemos al correo que nos dejaste.', true);
