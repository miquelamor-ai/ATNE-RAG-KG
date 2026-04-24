<?php
/**
 * lanet_bridge.php — Pont d'autenticació ATNE ↔ lanet
 *
 * Dos modes:
 *  GET  ?back=<url>   → flux redirect per al frontend
 *  POST (JSON)        → validació API per al backend Python
 */

define("DIR_LIB_DB", __DIR__ . '/../BD/');

const ALLOWED_ORIGINS = [
    'https://atne-1050342211642.europe-west1.run.app',
    'https://net5.net.fje.edu',
    'https://apiserveis5.net.fje.edu',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
];

// ── Mode POST: validació per al backend Python ────────────────────────────────
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    header('Content-Type: application/json; charset=utf-8');
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

// ── Mode GET: flux redirect per al frontend ───────────────────────────────────
$back = trim($_GET['back'] ?? '');
if (!$back) {
    header('Content-Type: application/json; charset=utf-8');
    http_response_code(400);
    die(json_encode(['ok' => false, 'error' => 'Paràmetre back obligatori']));
}

$parsedBack = parse_url($back);
$backOrigin = ($parsedBack['scheme'] ?? '') . '://' . ($parsedBack['host'] ?? '');
if (isset($parsedBack['port'])) $backOrigin .= ':' . $parsedBack['port'];
if (!in_array($backOrigin, ALLOWED_ORIGINS, true)) {
    header('Content-Type: application/json; charset=utf-8');
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

$sep      = strpos($back, '?') !== false ? '&' : '?';
$location = $back . $sep
    . 'atne_token=' . urlencode($token)
    . '&atne_login=' . urlencode($sessio->login);
header('Location: ' . $location);
exit;

// ── Validació (còpia exacta de NETSecure.php) ─────────────────────────────────
function _validaToken(string $token) {
    include DIR_LIB_DB . 'connexio.net.php';
    try {
        // LoginTimeout=5 evita que es quedi penjat si MSSQL no és accessible
        $dsn  = "sqlsrv:server=$server;Database=$database;LoginTimeout=5";
        $conn = new PDO($dsn, $user, $pwd, $options ?? []);
        $sql  = $conn->prepare('SET ANSI_WARNINGS ON');
        $sql->execute();
        $sql = $conn->prepare('SET ANSI_NULLS ON');
        $sql->execute();
        $sql = $conn->prepare("NET2.[dbo].[ValidaToken] :token");
        $sql->execute(['token' => $token]);
        $row = $sql->fetch(PDO::FETCH_OBJ);
    } catch (\Throwable $e) {
        error_log('[ATNE bridge] Error validaToken: ' . $e->getMessage());
        return false;
    }
    return (!empty($row->token) && $row->token == $token) ? $row : false;
}
