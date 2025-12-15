<?php
include "db_connect.php";

if(isset($_POST['register'])){
    $name = $_POST['name'];
    $email = $_POST['email'];
    $pass = password_hash($_POST['password'], PASSWORD_DEFAULT);
    $role = "user";

    $q = "INSERT INTO users(name,email,password,role) VALUES('$name','$email','$pass','$role')";
    mysqli_query($conn, $q);
    echo "Registration Successful";
}
?>

<form method="post">
    <input type="text" name="name" placeholder="Name" required><br><br>
    <input type="email" name="email" placeholder="Email" required><br><br>
    <input type="password" name="password" placeholder="Password" required><br><br>
    <button name="register">Register</button>
</form>
