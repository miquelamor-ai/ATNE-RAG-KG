<?php
/**
 * lanet_debug.php — DIAGNÒSTIC temporal. Esborrar un cop resolt el problema.
 * Pujar a apiserveis5.net.fje.edu/atne/lanet_debug.php i obrir al navegador.
 */
header('Content-Type: text/plain; charset=utf-8');

define("DIR_LIB_DB", __DIR__ . '/../BD/');

echo "=== ATNE Bridge Debug ===\n\n";

// 1. Cookie
$token = trim($_COOKIE['tokenNet'] ?? '');
echo "1. Cookie tokenNet: " . ($token ? "TROBAT (" . substr($token, 0, 10) . "...)" : "NO TROBAT") . "\n";
if (!$token) { echo "   → El problema és que el cookie no arriba.\n"; die(); }

// 2. connexio.net.php
$connFile = DIR_LIB_DB . 'connexio.net.php';
echo "2. connexio.net.php: " . (file_exists($connFile) ? "EXISTEIX" : "NO EXISTEIX a $connFile") . "\n";
if (!file_exists($connFile)) { echo "   → El path és incorrecte.\n"; die(); }

include $connFile;
echo "   server=$server  database=$database  user=$user\n";

// 3. Driver PDO sqlsrv
echo "3. Driver pdo_sqlsrv: " . (in_array('sqlsrv', PDO::getAvailableDrivers()) ? "DISPONIBLE" : "NO DISPONIBLE") . "\n";
echo "   Drivers disponibles: " . implode(', ', PDO::getAvailableDrivers()) . "\n";

// 4. Connexió MSSQL
echo "4. Connexió MSSQL... ";
try {
    $dsn  = "sqlsrv:server=$server;Database=$database;LoginTimeout=5";
    $conn = new PDO($dsn, $user, $pwd, $options ?? []);
    echo "OK\n";
} catch (\Throwable $e) {
    echo "ERROR: " . $e->getMessage() . "\n";
    die();
}

// 5. Stored procedure
echo "5. NET2.[dbo].[ValidaToken]... ";
try {
    $sql = $conn->prepare('SET ANSI_WARNINGS ON'); $sql->execute();
    $sql = $conn->prepare('SET ANSI_NULLS ON');    $sql->execute();
    $sql = $conn->prepare("NET2.[dbo].[ValidaToken] :token");
    $sql->execute(['token' => $token]);
    $row = $sql->fetch(PDO::FETCH_OBJ);
    if ($row) {
        echo "OK\n";
        echo "   token retornat: " . substr($row->token ?? '', 0, 10) . "...\n";
        echo "   login: " . ($row->login ?? '(buit)') . "\n";
        $match = (!empty($row->token) && $row->token == $token);
        echo "   token coincideix: " . ($match ? "SÍ → VALIDACIÓ OK" : "NO → token no coincideix") . "\n";
    } else {
        echo "Cap resultat — token no trobat a la BD\n";
    }
} catch (\Throwable $e) {
    echo "ERROR: " . $e->getMessage() . "\n";
}
