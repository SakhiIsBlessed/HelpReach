<?php
session_start();
include "db_connect.php";

if(isset($_POST['login'])){
    $email = $_POST['email'];
    $pass = $_POST['password'];

    $q = "SELECT * FROM users WHERE email='$email'";
    $res = mysqli_query($conn, $q);
    $user = mysqli_fetch_assoc($res);

    if($user && password_verify($pass, $user['password'])){
        $_SESSION['uid'] = $user['id'];
        $_SESSION['role'] = $user['role'];
        header("Location: dashboard.php");
    } else {
        echo "Invalid Login";
    }
}
?>

<form method="post">
    <input type="email" name="email" placeholder="Email" required><br><br>
    <input type="password" name="password" placeholder="Password" required><br><br>
    <button name="login">Login</button>
</form>
