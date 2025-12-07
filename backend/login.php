<?php
require_once __DIR__ . '/db.php';
// Expect POST: email, password
if ($_SERVER['REQUEST_METHOD'] !== 'POST') { http_response_code(405); exit; }

$email = trim($_POST['email'] ?? '');
$password = $_POST['password'] ?? '';
if (!$email || !$password) { http_response_code(400); json_response(['error'=>'Missing']); exit; }

$db = get_db_connection();
$stmt = $db->prepare('SELECT id,password_hash FROM users WHERE email = ?');
$stmt->bind_param('s', $email);
$stmt->execute();
$stmt->bind_result($id, $hash);
if ($stmt->fetch()) {
    if (password_verify($password, $hash)) {
        session_start();
        $_SESSION['user_id'] = $id;
        json_response(['ok'=>true,'user_id'=>$id]);
    } else { http_response_code(401); json_response(['error'=>'Invalid']); }
} else { http_response_code(401); json_response(['error'=>'Invalid']); }
$stmt->close();

?>
