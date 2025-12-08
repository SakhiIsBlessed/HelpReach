<?php
// Simple DB test script — visit in browser to verify connection
require_once __DIR__ . '/db.php';
try {
    $db = get_db_connection();
    $res = $db->query('SELECT VERSION() as v');
    $ver = $res->fetch_assoc()['v'] ?? 'unknown';
    header('Content-Type: application/json');
    echo json_encode(['ok'=>true,'mysql_version'=>$ver]);
} catch (Exception $e) {
    http_response_code(500);
    header('Content-Type: application/json');
    echo json_encode(['ok'=>false,'error'=>$e->getMessage()]);
}

?>
