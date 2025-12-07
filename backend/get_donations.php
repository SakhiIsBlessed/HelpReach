<?php
require_once __DIR__ . '/db.php';
// GET: returns latest donations as JSON
$db = get_db_connection();
$res = $db->query('SELECT d.*, u.name as donor_name FROM donations d JOIN users u ON u.id = d.donor_id ORDER BY d.created_at DESC LIMIT 200');
$out = [];
while ($row = $res->fetch_assoc()) {
    $out[] = $row;
}
json_response(['ok'=>true,'donations'=>$out]);

?>
