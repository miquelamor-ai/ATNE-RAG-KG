<?php
/**
 * lanet_bridge.php — Pont d'autenticació ATNE ↔ lanet
 *
 * Desplegar a un servidor FJE (ex: apps.net.fje.edu/atne/lanet_bridge.php)
 * que tingui accés a connexio.net.php i NETSecure.
 *
 * Dos modes:
 *  GET  ?back=<url>   → flux redirect per al frontend
 *  POST (JSON)        → validació API per al backend Python
 */

define("DIR_LIB_DB", '/site/wwwroot/lib/BD/');

// Orígens ATNE permesos (afegir el domini prod quan estigui llest)
const ALLOWED_ORIGINS = [
    'https://atne-1050342211642.europe-west1.run.app',
    'https://net5.net.fje.edu',
    'https://apiserveis5.net.fje.edu',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
];

header('Content-Type: application/json; charset=utf-8');

// ── Mode POST: validació de token per al backend Python ──────────────────────
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $body  = json_decode(file_get_contents('php://input'), true);
    $token = trim($body['token'] ?? '');
    if (!$token) {
        http_response_code(400);
        die(json_encode(['ok' => false, 'error' => 'Token buit']));
    }
    $sessio = _validaToken($token);
    if (!$sessio) {
        http_response_code(401);
        die(json_encode(['ok' => false, 'error' => 'Token invàlid o expirat']));
    }
    die(json_encode(['ok' => true, 'login' => $sessio->login]));
}

// ── Mode GET: flux redirect per al frontend ──────────────────────────────────
$back = trim($_GET['back'] ?? '');
if (!$back) {
    http_response_code(400);
    die(json_encode(['ok' => false, 'error' => 'Paràmetre back obligatori']));
}

// Valida que back sigui un origen ATNE permès
$parsedBack = parse_url($back);
$backOrigin = ($parsedBack['scheme'] ?? '') . '://' . ($parsedBack['host'] ?? '');
if (isset($parsedBack['port'])) $backOrigin .= ':' . $parsedBack['port'];
if (!in_array($backOrigin, ALLOWED_ORIGINS, true)) {
    http_response_code(403);
    die(json_encode(['ok' => false, 'error' => 'Origen no autoritzat']));
}

$token = trim($_COOKIE['tokenNet'] ?? '');
if (!$token) {
    $selfUrl = 'https://' . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI'];
    header('Location: https://www.fje.edu/login?redirect=' . urlencode($selfUrl));
    exit;
}

$sessio = _validaToken($token);
if (!$sessio) {
    $selfUrl = 'https://' . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI'];
    header('Location: https://www.fje.edu/login?redirect=' . urlencode($selfUrl));
    exit;
}

// Redirigeix de tornada a ATNE amb token i login a la URL
$sep      = strpos($back, '?') !== false ? '&' : '?';
$location = $back . $sep
    . 'atne_token=' . urlencode($token)
    . '&atne_login=' . urlencode($sessio->login);
header('Location: ' . $location);
exit;

// ── Funció shared de validació (idèntica a NETSecure.php original) ────────────
function _validaToken(string $token) {
    include DIR_LIB_DB . 'connexio.net.php';
    try {
        $conn = new PDO("sqlsrv:server=$server;Database=$database", $user, $pwd, $options ?? []);
        $sql = $conn->prepare('SET ANSI_WARNINGS ON');
        $sql->execute();
        $sql = $conn->prepare('SET ANSI_NULLS ON');
        $sql->execute();
        $sql = $conn->prepare("NET2.[dbo].[ValidaToken] :token");
        $sql->execute(['token' => $token]);
        $row = $sql->fetch(PDO::FETCH_OBJ);
    } catch (PDOException $e) {
        error_log('[ATNE bridge] Error validaToken: ' . $e->getMessage());
        return false;
    }
    return (!empty($row->token) && $row->token == $token) ? $row : false;
}
