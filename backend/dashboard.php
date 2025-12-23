<?php
session_start();
if(!isset($_SESSION['uid'])){
    header("Location: login.php");
}
echo "Welcome to Helpreach Dashboard";
?>
<br><a href="logout.php">Logout</a>
