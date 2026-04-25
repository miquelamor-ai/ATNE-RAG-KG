<?php
header('Content-Type: application/json; charset=utf-8');

// CORS per entorn local
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    header('Access-Control-Allow-Origin: *');
    header('Access-Control-Allow-Methods: POST, OPTIONS');
    header('Access-Control-Allow-Headers: Content-Type');
    exit(0);
}

// Auth FJE (només en producció, skip en local si no existeix)
$netsecure = __DIR__ . '/../../../lib/NETSecure/NETSecure.php';
if (file_exists($netsecure)) {
    include $netsecure;
}

// Carrega .env si no estem en entorn FJE
$env_path = __DIR__ . '/../../.env';
if (file_exists($env_path)) {
    foreach (file($env_path, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) as $line) {
        if ($line !== '' && $line[0] !== '#' && str_contains($line, '=')) {
            [$k, $v] = explode('=', $line, 2);
            putenv(trim($k) . '=' . trim($v));
        }
    }
}

$api_key = getenv('OPENAI_API_KEY');
if (!$api_key) {
    http_response_code(500);
    echo json_encode(['error' => 'OPENAI_API_KEY no configurada'], JSON_UNESCAPED_UNICODE);
    exit;
}

require_once __DIR__ . '/../includes/prompt.php';

$data        = json_decode(file_get_contents('php://input'), true) ?? [];
$text        = trim($data['text']        ?? '');
$nivell      = $data['nivell']      ?? 'B1';
$perfils     = $data['perfils']     ?? [];
$complements = $data['complements'] ?? [];
$model       = $data['model']       ?? 'gpt-4o';
$l1          = trim($data['l1']     ?? '');

$allowed_models = ['o1-mini', 'gpt-4.1', 'gpt-4o', 'gpt-4o-mini', 'gpt-4.1-mini'];
if (!in_array($model, $allowed_models)) {
    $model = 'gpt-4o';
}

if ($text === '') {
    http_response_code(400);
    echo json_encode(['error' => 'El text és buit.'], JSON_UNESCAPED_UNICODE);
    exit;
}

$system_prompt = build_system_prompt($nivell, $perfils, $complements, $l1);

$payload = [
    'model'      => $model,
    'messages'   => [
        ['role' => 'system', 'content' => $system_prompt],
        ['role' => 'user',   'content' => $text],
    ],
    'max_tokens' => 4000,
];

// o1-mini no admet el paràmetre temperature
if (!str_starts_with($model, 'o1')) {
    $payload['temperature'] = 0.7;
}

$ch = curl_init('https://api.openai.com/v1/chat/completions');
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_POST           => true,
    CURLOPT_POSTFIELDS     => json_encode($payload),
    CURLOPT_HTTPHEADER     => [
        'Content-Type: application/json',
        'Authorization: Bearer ' . $api_key,
    ],
    CURLOPT_TIMEOUT        => 120,
]);

$response  = curl_exec($ch);
$http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$curl_err  = curl_error($ch);
curl_close($ch);

if ($curl_err) {
    http_response_code(500);
    echo json_encode(['error' => 'Error de xarxa: ' . $curl_err], JSON_UNESCAPED_UNICODE);
    exit;
}

if ($http_code !== 200) {
    $detail = json_decode($response, true)['error']['message'] ?? "codi $http_code";
    http_response_code($http_code);
    echo json_encode(['error' => "Error API OpenAI: $detail"], JSON_UNESCAPED_UNICODE);
    exit;
}

$result  = json_decode($response, true);
$adapted = $result['choices'][0]['message']['content'] ?? '';

echo json_encode(['adapted' => $adapted], JSON_UNESCAPED_UNICODE);
