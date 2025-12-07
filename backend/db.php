<?php
require_once __DIR__ . '/config.php';

function get_db_connection() {
    static $conn = null;
    if ($conn === null) {
        $conn = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME, (int)DB_PORT);
        if ($conn->connect_errno) {
            http_response_code(500);
            echo json_encode(['error' => 'Database connection failed']);
            exit;
        }
        // set charset
        $conn->set_charset('utf8mb4');
    }
    return $conn;
}

function json_response($data) {
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode($data);
}

?>
