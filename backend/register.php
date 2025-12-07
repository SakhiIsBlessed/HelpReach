<?php
require_once __DIR__ . '/db.php';
// Expect POST: name, email, password
if ($_SERVER['REQUEST_METHOD'] !== 'POST') { http_response_code(405); exit; }

$name = trim($_POST['name'] ?? '');
$email = trim($_POST['email'] ?? '');
$password = $_POST['password'] ?? '';

if (!$name || !$email || !$password) {
    http_response_code(400);
    json_response(['error' => 'Missing fields']);
    exit;
}

// basic validation
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(400);
    json_response(['error' => 'Invalid email']);
    exit;
}

$db = get_db_connection();

// check existing
$stmt = $db->prepare('SELECT id FROM users WHERE email = ?');
$stmt->bind_param('s', $email);
$stmt->execute();
$stmt->store_result();
if ($stmt->num_rows > 0) {
    http_response_code(409);
    json_response(['error' => 'Email already registered']);
    exit;
}
$stmt->close();

$password_hash = password_hash($password, PASSWORD_DEFAULT);
$stmt = $db->prepare('INSERT INTO users (name,email,password_hash) VALUES (?,?,?)');
$stmt->bind_param('sss', $name, $email, $password_hash);
if ($stmt->execute()) {
    session_start();
    $_SESSION['user_id'] = $db->insert_id;
    json_response(['ok' => true, 'user_id' => $db->insert_id]);
} else {
    http_response_code(500);
    json_response(['error' => 'DB error']);
}
$stmt->close();

?>
