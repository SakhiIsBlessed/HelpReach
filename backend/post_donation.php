<?php
require_once __DIR__ . '/db.php';
// Accept POST: title, description, quantity, pickup_info
if ($_SERVER['REQUEST_METHOD'] !== 'POST') { http_response_code(405); exit; }

session_start();
if (empty($_SESSION['user_id'])) { http_response_code(401); json_response(['error'=>'Unauthorized']); exit; }

$title = trim($_POST['title'] ?? '');
$description = trim($_POST['description'] ?? '');
$quantity = trim($_POST['quantity'] ?? '');
$pickup = trim($_POST['pickup_info'] ?? '');

if (!$title) { http_response_code(400); json_response(['error'=>'Missing title']); exit; }

$db = get_db_connection();
$stmt = $db->prepare('INSERT INTO donations (title,description,quantity,pickup_info,donor_id) VALUES (?,?,?,?,?)');
$stmt->bind_param('ssssi', $title, $description, $quantity, $pickup, $_SESSION['user_id']);
if ($stmt->execute()) { json_response(['ok'=>true,'donation_id'=>$db->insert_id]); }
else { http_response_code(500); json_response(['error'=>'DB']); }
$stmt->close();

?>
