<?php
function conectar() {
    $conn = new mysqli('localhost', 'root', '', 'QLOCUR'); 
    if ($conn->connect_error) {
        die("Conexión fallida: " . $conn->connect_error);
    }
    return $conn;
}
?>
